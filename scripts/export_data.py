"""
export_data.py — BookingScraper Pro v6.0.0 build 52
====================================================
Export hotel data to CSV or JSON.

Cambios v52:
  STRUCT-011 : h.city → h.address_city (campo renombrado en hotels).
  STRUCT-012 : h.country ELIMINADO — usar h.address_country.
  CLEANUP    : h.address eliminado — campo muerto desde STRUCT-004 (v50).

Usage:
    python scripts/export_data.py --format csv --output hotels_export.csv
    python scripts/export_data.py --format json --language es --output hotels_es.json
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import get_db
from app.models import Hotel


def export_hotels(
    output_path: Path,
    fmt: str = "csv",
    language: Optional[str] = None,
    limit: int = 10_000,
) -> int:
    with get_db() as session:
        q = session.query(Hotel)
        if language:
            q = q.filter(Hotel.language == language)
        rows = q.order_by(Hotel.created_at.desc()).limit(limit).all()

    records: List[Dict[str, Any]] = [
        {
            "id":               str(h.id),
            "url":              h.url,
            "language":         h.language,
            "hotel_name":       h.hotel_name,
            # STRUCT-011 (v52): renombrado desde 'city'
            "address_city":     h.address_city,
            # STRUCT-012 (v52): 'country' eliminado — usar 'address_country'
            "street_address":   h.street_address,
            "address_locality": h.address_locality,
            "address_country":  h.address_country,
            "postal_code":      h.postal_code,
            "star_rating":      h.star_rating,
            "review_score":     h.review_score,
            "review_count":     h.review_count,
            "scrape_engine":    h.scrape_engine,
            "created_at":       h.created_at.isoformat() if h.created_at else None,
        }
        for h in rows
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "json":
        output_path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    else:
        if not records:
            print("No records to export.")
            return 0
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)

    print(f"Exported {len(records)} records to {output_path}")
    return len(records)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Export hotel data to CSV or JSON")
    parser.add_argument("--format", choices=["csv", "json"], default="csv")
    parser.add_argument("--output", default="hotels_export.csv")
    parser.add_argument("--language", default=None, help="Filter by language code (e.g. es, en, it)")
    parser.add_argument("--limit", type=int, default=10_000)
    args = parser.parse_args()

    export_hotels(
        output_path=Path(args.output),
        fmt=args.format,
        language=args.language,
        limit=args.limit,
    )
