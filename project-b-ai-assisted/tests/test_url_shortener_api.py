"""Tests for URL Shortener API endpoints."""
import os

os.environ["URLSHORTENER_API_KEY"] = "us_test_7f3a9b2c1e4d8f6a5b3c9d2e"

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.database import get_db
from conftest import override_get_db, TEST_API_KEY


@pytest.mark.asyncio
async def test_health(client):
    """Health endpoint does not require auth."""
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_short_url(client):
    """Create a short URL and verify response."""
    payload = {"long_url": "https://example.com/long/path"}
    r = await client.post("/urls", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["long_url"] == payload["long_url"]
    assert "short_code" in data
    assert len(data["short_code"]) >= 3
    assert data["click_count"] == 0
    assert "full_short_url" in data
    assert "/r/" in data["full_short_url"]


@pytest.mark.asyncio
async def test_create_without_api_key():
    """Creating a URL without API key returns 401."""
    from app.main import app
    from app.database import get_db

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test", follow_redirects=False
    ) as ac:
        r = await ac.post("/urls", json={"long_url": "https://example.com"})
    assert r.status_code == 401
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_invalid_url_rejected(client):
    """Invalid URL format returns 422."""
    r = await client.post("/urls", json={"long_url": "not-a-url"})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_redirect_increments_clicks(client):
    """Redirect resolves short code and increments click count."""
    cr = await client.post("/urls", json={"long_url": "https://example.com/target"})
    assert cr.status_code == 201
    short_code = cr.json()["short_code"]

    r = await client.get(f"/r/{short_code}")
    assert r.status_code == 302
    assert r.headers["location"] == "https://example.com/target"

    stats = await client.get(f"/urls/{short_code}/stats")
    assert stats.status_code == 200
    assert stats.json()["click_count"] == 1

    # Second redirect
    await client.get(f"/r/{short_code}")
    stats2 = await client.get(f"/urls/{short_code}/stats")
    assert stats2.json()["click_count"] == 2


@pytest.mark.asyncio
async def test_redirect_404_for_missing_code(client):
    """Redirect returns 404 for non-existent short code."""
    r = await client.get("/r/nonexistent")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_stats_404_for_missing_code(client):
    """Stats returns 404 for non-existent short code."""
    r = await client.get("/urls/nonexistent/stats")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_duplicate_url_returns_existing(client):
    """Same long URL returns existing short URL (no duplicate)."""
    url = "https://example.com/duplicate-test"
    r1 = await client.post("/urls", json={"long_url": url})
    r2 = await client.post("/urls", json={"long_url": url})
    assert r1.status_code == 201
    assert r2.status_code == 201
    assert r1.json()["short_code"] == r2.json()["short_code"]


@pytest.mark.asyncio
async def test_list_urls(client):
    """List URLs returns created short URLs."""
    await client.post("/urls", json={"long_url": "https://a.com"})
    await client.post("/urls", json={"long_url": "https://b.com"})
    r = await client.get("/urls")
    assert r.status_code == 200
    urls = r.json()
    assert len(urls) >= 2
    codes = [u["short_code"] for u in urls]
    assert len(set(codes)) == len(codes)
