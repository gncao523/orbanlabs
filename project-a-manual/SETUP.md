# Notes API - Setup Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

## Backend Setup

1. Create and activate a virtual environment:

   ```bash
   cd project-a-manual/backend
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set environment variables:

   ```bash
   # API key for authentication (default: dev-api-key-change-me)
   set NOTES_API_KEY=your-secret-api-key

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

2. (Optional) Configure API URL and key in `.env.local`:

   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_API_KEY=dev-api-key-change-me
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
