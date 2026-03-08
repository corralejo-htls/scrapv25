"""
load_urls.py — Load hotel URLs from a CSV file into url_queue.
Usage: python scripts/load_urls.py urls.csv
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import get_settings
from app.database import get_db
from app.models import URLQueue

# BUG-110: validate against settings (single source of truth)
_cfg = get_settings()
VALID_LANGUAGES = set(_cfg.ENABLED_LANGUAGES)

_BOOKING_URL_PREFIX = "https://www.booking.com/hotel/"


def _is_valid_url(url: str) -> bool:
    return bool(url) and url.startswith(_BOOKING_URL_PREFIX) and len(url) <= 2048


def load_csv(filepath: Path, max_mb: int = 10) -> int:
    file_size_mb = filepath.stat().st_size / (1024 * 1024)
    if file_size_mb > max_mb:
        print(f"ERROR: File {filepath} exceeds {max_mb}MB limit ({file_size_mb:.1f}MB).")
        return 0

    inserted = 0
    skipped = 0
    invalid = 0

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        urls = []
        for row in reader:
            url = (row.get("url") or row.get("URL") or "").strip()
            if _is_valid_url(url):
                urls.append(url)
            else:
                invalid += 1

    with get_db() as session:
        for url in urls:
            existing = session.query(URLQueue).filter_by(url=url).first()
            if existing:
                skipped += 1
            else:
                session.add(URLQueue(url=url, base_url=url))
                inserted += 1

    print(f"Loaded: inserted={inserted} skipped(dup)={skipped} invalid={invalid}")
    return inserted


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/load_urls.py <urls.csv>")
        sys.exit(1)
    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        sys.exit(1)
    load_csv(csv_path, max_mb=_cfg.CSV_MAX_FILE_MB)
