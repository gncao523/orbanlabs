# URL Shortener - Planning Notes

## Overview

Build a URL Shortener application that:
- Takes long URLs and generates short codes
- Redirects users from short URL to original
- Tracks click counts per short link

## Requirements Checklist

### Backend (FastAPI + Python)
- [x] Endpoint to create short URL from long URL
- [x] Redirect endpoint (resolves short code → original URL)
- [x] Stats endpoint (click count for given short URL)
- [x] API key auth for creating URLs (redirects public)
- [x] SQLite persistence
- [x] Edge cases:
  - Duplicate URLs: return existing short URL if same long URL already shortened
  - Invalid URLs: validate format (http/https)
  - Expired or missing short codes: 404

### Frontend (Next.js + React)
- [x] Form to paste long URL and get short one
- [x] Dashboard showing created URLs and click counts
- [x] Loading and error states

### Testing
- [x] Meaningful backend tests

### Documentation
- [x] API documentation
- [x] Setup guide
- [x] AI usage log

## Design Decisions

### Short Code Generation
- Use `secrets.token_urlsafe(8)` truncated to 6 chars (alphanumeric, URL-safe)
- Collision handling: retry up to 5 times if duplicate short_code
- Alternative: use base62 encoding of auto-increment ID for deterministic uniqueness

### Duplicate URLs
- When creating a short URL, check if the exact long URL already exists
- If yes, return the existing short URL instead of creating a duplicate
- Keeps the system clean and allows idempotent behavior

### URL Validation
- Must start with `http://` or `https://`
- Pydantic validator enforces format

### Expiration
- Optional `expires_at` field (nullable)
- Redirect returns 404 if link expired
- Stats returns 404 for expired/missing

### Database Schema
- `short_urls` table: id, short_code (unique), long_url, click_count, created_at, expires_at

### API Structure
- `POST /urls` — create short URL (auth required)
- `GET /r/{short_code}` — redirect (public)
- `GET /urls/{short_code}/stats` — get click count (auth optional for listing; public stats per link could be debated—we'll require auth for stats to prevent enumeration)
- Actually: stats should be accessible so dashboard can show them. Require auth for stats too.
