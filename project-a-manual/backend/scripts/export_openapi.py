#!/usr/bin/env python3
"""Export OpenAPI schema to docs/openapi.json (run from project-a-manual root)."""
import json
import sys
from pathlib import Path

# Add backend to path so we can import app
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.main import app

if __name__ == "__main__":
    spec = app.openapi()
    out_path = backend_dir.parent / "docs" / "openapi.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
    print(f"Exported OpenAPI spec to {out_path}")
