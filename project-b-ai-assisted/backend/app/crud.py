"""CRUD operations for short URLs."""
import secrets
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ShortUrl
from app.schemas import UrlCreate


def _generate_short_code() -> str:
    """Generate a URL-safe short code (6 chars)."""
    return secrets.token_urlsafe(8)[:6].replace("-", "x").replace("_", "y")


async def get_by_short_code(db: AsyncSession, short_code: str) -> Optional[ShortUrl]:
    """Get a short URL by its code."""
    result = await db.execute(
        select(ShortUrl).where(ShortUrl.short_code == short_code)
    )
    return result.scalar_one_or_none()


async def get_by_long_url(db: AsyncSession, long_url: str) -> Optional[ShortUrl]:
    """Get existing short URL for a long URL (for duplicate handling)."""
    result = await db.execute(
        select(ShortUrl).where(ShortUrl.long_url == long_url)
    )
    return result.scalar_one_or_none()


async def create_short_url(db: AsyncSession, data: UrlCreate) -> ShortUrl:
    """
    Create a short URL. If long_url already exists, return existing.
    Handles custom_code or generates random code with collision retry.
    """
    long_url = data.long_url.strip()

    # Duplicate check: same long URL → return existing
    existing = await get_by_long_url(db, long_url)
    if existing:
        return existing

    short_code = data.custom_code
    if short_code:
        short_code = short_code.strip()
        # Check custom code not taken
        taken = await get_by_short_code(db, short_code)
        if taken:
            raise ValueError(f"Short code '{short_code}' is already taken")
    else:
        for _ in range(5):
            short_code = _generate_short_code()
            if not await get_by_short_code(db, short_code):
                break
        else:
            raise ValueError("Could not generate unique short code")

    db_url = ShortUrl(short_code=short_code, long_url=long_url)
    db.add(db_url)
    await db.flush()
    await db.refresh(db_url)
    return db_url


async def increment_click(db: AsyncSession, short_code: str) -> Optional[ShortUrl]:
    """Increment click count and return the ShortUrl, or None if not found."""
    url = await get_by_short_code(db, short_code)
    if not url:
        return None
    url.click_count += 1
    await db.flush()
    await db.refresh(url)
    return url


async def list_urls(db: AsyncSession) -> list[ShortUrl]:
    """List all short URLs ordered by created_at desc."""
    result = await db.execute(
        select(ShortUrl).order_by(ShortUrl.created_at.desc())
    )
    return list(result.scalars().all())
