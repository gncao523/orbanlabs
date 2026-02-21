# URL Shortener - API Documentation

Base URL: `http://localhost:8000`

## Authentication

Protected endpoints require the `X-API-Key` header:

```
X-API-Key: your_api_key_here
```

Set via `URLSHORTENER_API_KEY` environment variable (default: `us_sample_7f3a9b2c1e4d8f6a5b3c9d2e` for development).

---

## Endpoints

### Create Short URL

**POST** `/urls`

Creates a short URL from a long URL. If the same long URL was already shortened, returns the existing short URL.

**Auth:** Required

**Request body:**
```json
{
  "long_url": "https://example.com/very/long/path",
  "custom_code": "optional-custom-code"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| long_url | string | Yes | Must start with `http://` or `https://` |
| custom_code | string | No | Optional custom short code (alphanumeric, 3–20 chars) |

**Response (201):**
```json
{
  "short_code": "aB3xYz",
  "long_url": "https://example.com/very/long/path",
  "full_short_url": "http://localhost:8000/r/aB3xYz",
  "click_count": 0,
  "created_at": "2025-02-21T12:00:00Z"
}
```

**Errors:**
- `401` — Missing API key
- `403` — Invalid API key
- `422` — Invalid URL format or custom_code (e.g. already taken)

---

### Redirect

**GET** `/r/{short_code}`

Resolves the short code and redirects (302) to the original URL. Increments click count. Public, no auth.

**Response:**
- `302` — Redirect to original URL
- `404` — Short code not found or expired

---

### Stats

**GET** `/urls/{short_code}/stats`

Returns click count and metadata for a short URL.

**Auth:** Required

**Response (200):**
```json
{
  "short_code": "aB3xYz",
  "long_url": "https://example.com/very/long/path",
  "click_count": 42,
  "created_at": "2025-02-21T12:00:00Z"
}
```

**Errors:**
- `401` / `403` — Auth failure
- `404` — Short code not found or expired

---

### List URLs

**GET** `/urls`

Returns all short URLs created (for dashboard). Requires auth.

**Response (200):**
```json
[
  {
    "short_code": "aB3xYz",
    "long_url": "https://example.com/very/long/path",
    "full_short_url": "http://localhost:8000/r/aB3xYz",
    "click_count": 42,
    "created_at": "2025-02-21T12:00:00Z"
  }
]
```

---

### Health Check

**GET** `/health`

No auth. Returns `{"status": "ok"}`.
