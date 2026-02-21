"""URL Shortener - FastAPI application."""
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, init_db
from app.auth import verify_api_key
from app.crud import create_short_url, get_by_short_code, increment_click, list_urls
from app.schemas import UrlCreate, UrlResponse, UrlStatsResponse
from app.models import ShortUrl

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")


def _is_expired(url: ShortUrl) -> bool:
    """Check if short URL has expired."""
    if url.expires_at is None:
        return False
    return datetime.now(timezone.utc) >= url.expires_at


def _to_response(url: ShortUrl) -> UrlResponse:
    """Convert ShortUrl model to UrlResponse schema."""
    return UrlResponse(
        short_code=url.short_code,
        long_url=url.long_url,
        full_short_url=f"{BASE_URL}/r/{url.short_code}",
        click_count=url.click_count,
        created_at=url.created_at,
    )


def _to_stats_response(url: ShortUrl) -> UrlStatsResponse:
    """Convert ShortUrl model to UrlStatsResponse schema."""
    return UrlStatsResponse(
        short_code=url.short_code,
        long_url=url.long_url,
        click_count=url.click_count,
        created_at=url.created_at,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    await init_db()
    yield


app = FastAPI(
    title="URL Shortener API",
    description="Create short URLs, redirect, and track click counts.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - links to API docs."""
    return {
        "message": "URL Shortener API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "create": "POST /urls",
        "redirect": "GET /r/{short_code}",
        "stats": "GET /urls/{short_code}/stats",
    }


@app.get("/health")
async def health():
    """Health check endpoint (no auth required)."""
    return {"status": "ok"}


@app.post("/urls", response_model=UrlResponse, status_code=status.HTTP_201_CREATED)
async def create_url(
    data: UrlCreate,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Create a short URL from a long URL. Returns existing if duplicate."""
    try:
        db_url = await create_short_url(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    return _to_response(db_url)


@app.get("/r/{short_code}")
async def redirect(
    short_code: str,
    db: AsyncSession = Depends(get_db),
):
    """Resolve short code and redirect to original URL. Public, increments click count."""
    url = await get_by_short_code(db, short_code)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")
    if _is_expired(url):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL has expired")
    await increment_click(db, short_code)
    return RedirectResponse(url=url.long_url, status_code=status.HTTP_302_FOUND)


@app.get("/urls/{short_code}/stats", response_model=UrlStatsResponse)
async def get_stats(
    short_code: str,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Get click count and metadata for a short URL."""
    url = await get_by_short_code(db, short_code)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")
    if _is_expired(url):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL has expired")
    return _to_stats_response(url)


@app.get("/urls", response_model=list[UrlResponse])
async def list_all_urls(
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """List all short URLs (for dashboard)."""
    urls = await list_urls(db)
    return [_to_response(u) for u in urls]
