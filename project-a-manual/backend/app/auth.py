"""API key authentication."""
import os
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In production, use env var. Default for development.
VALID_API_KEY = os.getenv("NOTES_API_KEY", "dev-api-key-change-me")


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Verify the API key from the request header."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Provide X-API-Key header.",
        )
    if api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key.",
        )
    return api_key
