"""Tests for Notes API endpoints."""
import os
import pytest
from httpx import AsyncClient

# Set test API key before importing app
os.environ["NOTES_API_KEY"] = "nb_sample_7f3a9b2c1e4d8f6a5b3c9d2e"


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    """Health endpoint does not require auth."""
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_note(client: AsyncClient):
    """Create a note and verify response."""
    payload = {
        "title": "Test Note",
        "body": "This is the body.",
        "tags": ["test", "sample"],
    }
    r = await client.post("/notes", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["tags"] == payload["tags"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_note_without_api_key():
    """Creating a note without API key returns 401."""
    # Client has API key in fixture - create one without it
    from app.main import app
    from app.database import get_db
    from conftest import override_get_db

    app.dependency_overrides[get_db] = override_get_db
    from httpx import ASGITransport, AsyncClient

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post("/notes", json={"title": "X", "body": "Y", "tags": []})
    assert r.status_code == 401
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_notes(client: AsyncClient):
    """List notes returns created notes."""
    await client.post(
        "/notes",
        json={"title": "Note 1", "body": "Body 1", "tags": ["a"]},
    )
    await client.post(
        "/notes",
        json={"title": "Note 2", "body": "Body 2", "tags": ["b"]},
    )
    r = await client.get("/notes")
    assert r.status_code == 200
    notes = r.json()
    assert len(notes) >= 2
    titles = [n["title"] for n in notes]
    assert "Note 1" in titles
    assert "Note 2" in titles


@pytest.mark.asyncio
async def test_filter_by_tag(client: AsyncClient):
    """Filter notes by tag."""
    await client.post(
        "/notes",
        json={"title": "Tagged", "body": "X", "tags": ["unique-tag-xyz"]},
    )
    r = await client.get("/notes", params={"tag": "unique-tag-xyz"})
    assert r.status_code == 200
    notes = r.json()
    assert len(notes) >= 1
    assert any(n["title"] == "Tagged" for n in notes)


@pytest.mark.asyncio
async def test_filter_by_keyword(client: AsyncClient):
    """Filter notes by keyword in title/body."""
    await client.post(
        "/notes",
        json={"title": "UniqueKeyword", "body": "Content", "tags": []},
    )
    r = await client.get("/notes", params={"keyword": "UniqueKeyword"})
    assert r.status_code == 200
    notes = r.json()
    assert len(notes) >= 1
    assert any(n["title"] == "UniqueKeyword" for n in notes)


@pytest.mark.asyncio
async def test_get_note_by_id(client: AsyncClient):
    """Get a single note by ID."""
    cr = await client.post(
        "/notes",
        json={"title": "Single", "body": "Body", "tags": []},
    )
    note_id = cr.json()["id"]
    r = await client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Single"


@pytest.mark.asyncio
async def test_get_note_404(client: AsyncClient):
    """Get non-existent note returns 404."""
    r = await client.get("/notes/99999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_update_note(client: AsyncClient):
    """Update a note."""
    cr = await client.post(
        "/notes",
        json={"title": "Original", "body": "Old", "tags": []},
    )
    note_id = cr.json()["id"]
    r = await client.put(
        f"/notes/{note_id}",
        json={"title": "Updated", "body": "New body"},
    )
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"
    assert r.json()["body"] == "New body"


@pytest.mark.asyncio
async def test_delete_note(client: AsyncClient):
    """Delete a note."""
    cr = await client.post(
        "/notes",
        json={"title": "To Delete", "body": "X", "tags": []},
    )
    note_id = cr.json()["id"]
    r = await client.delete(f"/notes/{note_id}")
    assert r.status_code == 204
    get_r = await client.get(f"/notes/{note_id}")
    assert get_r.status_code == 404


@pytest.mark.asyncio
async def test_create_note_validation(client: AsyncClient):
    """Invalid input returns 422."""
    r = await client.post("/notes", json={"title": "", "body": "X", "tags": []})
    assert r.status_code == 422
