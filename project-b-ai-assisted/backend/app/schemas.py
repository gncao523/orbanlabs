"""Pydantic schemas for request/response validation."""
import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


def _validate_url(url: str) -> str:
    """Ensure URL starts with http:// or https://."""
    if not url or not url.strip():
        raise ValueError("URL is required")
    url = url.strip()
    if not re.match(r"^https?://", url, re.IGNORECASE):
        raise ValueError("URL must start with http:// or https://")
    return url


class UrlCreate(BaseModel):
    """Schema for creating a short URL."""
    long_url: str = Field(..., min_length=1, max_length=2048)
    custom_code: str | None = Field(None, min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_-]+$")

    @field_validator("long_url")
    @classmethod
    def validate_long_url(cls, v: str) -> str:
        return _validate_url(v)


class UrlResponse(BaseModel):
    """Schema for short URL response."""
    short_code: str
    long_url: str
    full_short_url: str
    click_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class UrlStatsResponse(BaseModel):
    """Schema for stats response."""
    short_code: str
    long_url: str
    click_count: int
    created_at: datetime

    class Config:
        from_attributes = True
