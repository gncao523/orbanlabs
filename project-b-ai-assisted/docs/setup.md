# URL Shortener - Setup Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

## Backend Setup

1. Create and activate a virtual environment:

   ```cmd
   cd project-b-ai-assisted/backend
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies:

   ```cmd
   pip install -r requirements.txt
   ```

3. (Optional) Configure environment. Copy `backend/.env.example` to `backend/.env`:

   ```cmd
   # API key for creating URLs and viewing stats (default shown)
   URLSHORTENER_API_KEY=us_sample_7f3a9b2c1e4d8f6a5b3c9d2e

   # Database (default: sqlite+aiosqlite:///./urlshortener.db)
   DATABASE_URL=sqlite+aiosqlite:///./urlshortener.db

   # Base URL for short links (default: http://localhost:8000)
   BASE_URL=http://localhost:8000
   ```

4. Run the backend:

   ```cmd
   uvicorn app.main:app --reload
   ```

   API: `http://localhost:8000`  
   Swagger: `http://localhost:8000/docs`  
   ReDoc: `http://localhost:8000/redoc`

## Frontend Setup

1. Install dependencies:

   ```bash
   cd project-b-ai-assisted/frontend
   npm install
   ```

2. Configure. Copy `frontend/.env.example` to `frontend/.env.local`:

   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_API_KEY=us_sample_7f3a9b2c1e4d8f6a5b3c9d2e
   ```

3. Run the frontend:

   ```bash
   npm run dev
   ```

   App: `http://localhost:3000`

## Running Tests

```bash
cd project-b-ai-assisted
pip install -r tests/requirements-test.txt
pytest tests/ -v
```

Ensure `backend` is on the Python path (pytest.ini sets this).
