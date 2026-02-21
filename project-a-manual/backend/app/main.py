"""Notes API - FastAPI application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, init_db
from app.auth import verify_api_key
from app.crud import create_note, get_note, get_notes, update_note, delete_note
from app.schemas import NoteCreate, NoteUpdate, NoteResponse
from app.models import Note


def _note_to_response(note: Note) -> NoteResponse:
    """Convert Note model to NoteResponse schema."""
    import json
    tags = json.loads(note.tags) if note.tags else []
    return NoteResponse(
        id=note.id,
        title=note.title,
        body=note.body,
        tags=tags,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    await init_db()
    yield
    # Cleanup if needed
    pass


app = FastAPI(
    title="Notes API",
    description="A simple CRUD API for text notes with search and tag filtering.",
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
        "message": "Notes API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "notes": "/notes",
    }


@app.get("/health")
async def health():
    """Health check endpoint (no auth required)."""
    return {"status": "ok"}


@app.post("/notes", response_model=NoteResponse)
async def create_note_endpoint(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Create a new note."""
    db_note = await create_note(db, note)
    return _note_to_response(db_note)


@app.get("/notes", response_model=list[NoteResponse])
async def list_notes(
    tag: str | None = Query(None, description="Filter by tag"),
    keyword: str | None = Query(None, description="Search in title and body"),
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """List notes with optional tag and keyword filters."""
    notes = await get_notes(db, tag=tag, keyword=keyword)
    return [_note_to_response(n) for n in notes]


@app.get("/notes/{note_id}", response_model=NoteResponse)
async def read_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Get a single note by ID."""
    note = await get_note(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )
    return _note_to_response(note)


@app.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note_endpoint(
    note_id: int,
    note_update: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Update a note."""
    db_note = await update_note(db, note_id, note_update)
    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )
    return _note_to_response(db_note)


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note_endpoint(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Delete a note."""
    deleted = await delete_note(db, note_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )
    return None
