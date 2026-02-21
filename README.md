# OrbanLabs

Two full-stack apps. Same tech, different way of building them.

## Overview

| **project-a-manual** | Notes API | By hand, no AI |
| **project-b-ai-assisted** | URL Shortener | With Cursor / AI help |


## What they share

Backend: FastAPI, SQLAlchemy (async), SQLite  
Frontend: Next.js + React  
Auth: API key in the `X-API-Key` header  
CORS: localhost:3000  
Tests: pytest, in-memory SQLite

Same folder layout too:

```
project-{a,b}/
├── backend/          # FastAPI
│   ├── app/
│   │   ├── main.py   # routes, lifespan
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── auth.py
│   │   └── database.py
│   └── requirements.txt
├── frontend/         # Next.js
├── tests/
└── docs/
```

---

## Project A: Notes API

CRUD for notes. You can filter by tag or search by keyword in title/body.

Endpoints: `POST /notes`, `GET /notes`, `GET /notes/{id}`, `PUT /notes/{id}`, `DELETE /notes/{id}`

Built it myself from scratch — models, schemas, CRUD, routes. No AI.

---

## Project B: URL Shortener

Paste a long URL, get a short one. Redirect works, click counts too.

Endpoints: `POST /urls`, `GET /r/{short_code}` (public redirect), `GET /urls/{short_code}/stats`, `GET /urls` — the last two need the API key.

Built this one with Cursor. AI helped with backend, short-code generation, edge cases (duplicates, bad URLs, 404s), frontend, tests, and docs. More in `project-b-ai-assisted/docs/ai-usage-log.md`.

---

## How to run

**Backend**

```cmd, not "bash"

cd project-{a-manual|b-ai-assisted}/backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

```

API at `http://localhost:8000`, docs at `/docs`.

**Frontend**

```bash

cd project-{a-manual|b-ai-assisted}/frontend
npm install
npm run dev

```

App at `http://localhost:3000`.

**Tests**

```cmd

cd project-{a-manual|b-ai-assisted}
pip install -r tests/requirements-test.txt
pytest tests/ -v

```

---

## Docs

- **project-a-manual:** `docs/How to run my project.md`, `docs/API-Documentation-Guide.md`
- **project-b-ai-assisted:** `docs/setup.md`, `docs/api.md`, `docs/planning.md`, `docs/ai-usage-log.md`
