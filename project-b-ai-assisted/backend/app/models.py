"""Short URL model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class ShortUrl(Base):
    """Short URL with code, long URL, and click count."""
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(20), unique=True, nullable=False, index=True)
    long_url = Column(String(2048), nullable=False, index=True)
    click_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=True)
