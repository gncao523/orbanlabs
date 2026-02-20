# Notes API - Planning Notes

## Understanding the Requirements

- **CRUD** for text notes (Create, Read, Update, Delete)
- **Note fields**: title, body, tags (list), created_at, updated_at
- **Search**: filter by tag OR keyword in title/body
- **Auth**: API key in header (X-API-Key)
- **Persistence**: SQLite
- **Validation**: Input validation and meaningful error responses
- **Frontend**: Next.js list, search/filter, create/edit form, error handling
- **Tests**: Meaningful backend tests
- **Docs**: OpenAPI/Swagger (auto-generated), setup guide

## Approach Chosen

### Backend (FastAPI)

- **ORM**: SQLAlchemy async with aiosqlite for SQLite
- **Models**: Single `notes` table; tags stored as JSON array string (SQLite has no native array type)
- **Auth**: FastAPI `APIKeyHeader` dependency; validate against env var `NOTES_API_KEY`
- **Search**: GET /notes with optional `tag` and `keyword` query params; tag uses JSON contains, keyword uses ILIKE on title/body

### Alternatives Considered

1. **Tags storage**: JSON string vs separate tags table. Chose JSON for simplicity; a tags table would scale better for many tags and complex queries.
2. **Sync vs async SQLAlchemy**: Chose async for consistency with FastAPI’s async style and future scalability.

### Tradeoffs

- JSON tags: Simple but limits complex tag queries; good enough for this scope.
- Single API key: No per-user isolation; suitable for a small/internal API.

## Architecture

```
backend/
  app/
    main.py       - FastAPI app, routes
    database.py   - SQLite + async session
    models.py     - Note model
    schemas.py    - Pydantic validation
    auth.py       - API key verification
    crud.py       - DB operations
frontend/
  app/            - Next.js App Router
  lib/api.ts      - API client
```
