# Notes API - Project Running Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

## Backend Setup

1. Create and activate a virtual environment:

   ```cmd
   cd project-a-manual/backend
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   ```

2. Install dependencies:

   ```cmd
   pip install -r requirements.txt
   ```

3. (Optional) Set environment variables. Copy `backend/.env.example` to `backend/.env` or set manually:

   ```bash
   # API key for authentication (default: nb_sample_7f3a9b2c1e4d8f6a5b3c9d2e)
   set NOTES_API_KEY=nb_sample_7f3a9b2c1e4d8f6a5b3c9d2e

   # Database URL (default: sqlite+aiosqlite:///./notes.db)
   set DATABASE_URL=sqlite+aiosqlite:///./notes.db
   ```

4. Run the backend:

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Frontend Setup

1. Install dependencies:

   ```bash
   cd project-a-manual/frontend
   npm install
   ```

2. (Optional) Configure API URL and key. Copy `frontend/.env.example` to `frontend/.env.local` or set manually:

   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_API_KEY=nb_sample_7f3a9b2c1e4d8f6a5b3c9d2e
   ```

3. Run the frontend:

   ```bash
   npm run dev
   ```

   The app will be at `http://localhost:3000`.

## Running Tests

```bash
cd project-a-manual
pip install -r tests/requirements-test.txt
pytest tests/ -v
```

Ensure you're in the project root or that `backend` is on the Python path when running pytest.
