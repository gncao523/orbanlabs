"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base note schema."""
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(...)
    tags: list[str] = Field(default_factory=list)


class NoteCreate(NoteBase):
    """Schema for creating a note."""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating a note (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    body: Optional[str] = None
    tags: Optional[list[str]] = None


class NoteResponse(NoteBase):
    """Schema for note response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
