"""CRUD operations for notes."""
import json
from datetime import datetime
from typing import Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Note
from app.schemas import NoteCreate, NoteUpdate


def _tags_to_json(tags: list[str]) -> str:
    """Serialize tags list to JSON string."""
    return json.dumps(tags)


def _json_to_tags(tags_str: str) -> list[str]:
    """Deserialize JSON string to tags list."""
    try:
        return json.loads(tags_str) if tags_str else []
    except json.JSONDecodeError:
        return []


async def create_note(db: AsyncSession, note: NoteCreate) -> Note:
    """Create a new note."""
    db_note = Note(
        title=note.title,
        body=note.body,
        tags=_tags_to_json(note.tags),
    )
    db.add(db_note)
    await db.flush()
    await db.refresh(db_note)
    return db_note


async def get_note(db: AsyncSession, note_id: int) -> Optional[Note]:
    """Get a note by ID."""
    result = await db.execute(select(Note).where(Note.id == note_id))
    return result.scalar_one_or_none()


async def get_notes(
    db: AsyncSession,
    tag: Optional[str] = None,
    keyword: Optional[str] = None,
) -> list[Note]:
    """Get notes with optional tag and keyword filters."""
    query = select(Note).order_by(Note.updated_at.desc())

    if tag:
        # Filter by tag (JSON array contains the tag)
        query = query.where(Note.tags.contains(f'"{tag}"'))

    if keyword:
        kw = f"%{keyword}%"
        query = query.where(
            or_(Note.title.ilike(kw), Note.body.ilike(kw))
        )

    result = await db.execute(query)
    return list(result.scalars().all())


async def update_note(db: AsyncSession, note_id: int, note_update: NoteUpdate) -> Optional[Note]:
    """Update a note."""
    db_note = await get_note(db, note_id)
    if not db_note:
        return None

    update_data = note_update.model_dump(exclude_unset=True)
    if "tags" in update_data:
        update_data["tags"] = _tags_to_json(update_data["tags"])

    for key, value in update_data.items():
        setattr(db_note, key, value)

    db_note.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(db_note)
    return db_note


async def delete_note(db: AsyncSession, note_id: int) -> bool:
    """Delete a note."""
    db_note = await get_note(db, note_id)
    if not db_note:
        return False
    await db.delete(db_note)
    await db.flush()
    return True
