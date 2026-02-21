# Project Running Guide for "project-a-manual"

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

## To run the backend

1. Create and activate a virtual environment:

   ```You should run cmd terminal not bash (windows system commands are)

   cd project-a-manual/backend
   python -m venv venv
   venv\Scripts\activate

   ```

2. Install dependencies:

   ```cmd

   pip install -r requirements.txt

   ```

3. Use this value as an example data

   NOTES_API_KEY=nb_sample_7f3a9b2c1e4d8f6a5b3c9d2e
   DATABASE_URL=sqlite+aiosqlite:///./notes.db
   
4. To start the backend:

   ``` open cmd and run this command:

      uvicorn app.main:app --reload

   ```


   The API will be available at `http://localhost:8000`.

   - You can see Swagger UI: http://localhost:8000/docs
   - You can see ReDoc: http://localhost:8000/redoc

## To run the frontend 

1. Install dependencies:

   ```open the terminal

   cd project-a-manual/frontend
   npm install

   ```

2. Use this value as for an example:

   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_API_KEY=nb_sample_7f3a9b2c1e4d8f6a5b3c9d2e
   ```

3. Run the frontend:

   ```bash

   npm run dev

   ```

   You can see website UI at `http://localhost:3000`.

## Running Tests

```You should run in cmd

cd project-a-manual
pip install -r tests/requirements-test.txt
pytest tests/ -v

```

