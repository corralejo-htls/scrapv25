"""
BookingScraper Pro v6.0 - Data Export Script
============================================
Export scraped hotel data to CSV or Excel format.
Platform : Windows 11 — uses pathlib.Path for all file I/O.

Usage:
  python scripts/export_data.py --format csv --output C:/BookingScraper/exports/hotels.csv
  python scripts/export_data.py --format excel --language es --city Madrid
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s")
logger = logging.getLogger("export_data")


def export_hotels(
    output_path : Path,
    fmt         : str   = "csv",
    language    : Optional[str] = None,
    city        : Optional[str] = None,
    country     : Optional[str] = None,
    status      : Optional[str] = None,
    limit       : Optional[int] = None,
) -> int:
    """Export hotel data to CSV or Excel. Returns number of rows exported."""
    try:
        import pandas as pd
        from app.database import get_db
        from app.models import Hotel
    except ImportError as exc:
        logger.error("Import error: %s", exc)
        return 0

    rows: list[dict] = []
    try:
        with get_db() as session:
            q = session.query(Hotel)
            if language:
                q = q.filter(Hotel.language == language)
            if city:
                q = q.filter(Hotel.city.ilike(f"%{city}%"))
            if country:
                q = q.filter(Hotel.country.ilike(f"%{country}%"))
            if status:
                q = q.filter(Hotel.scrape_status == status)
            if limit:
                q = q.limit(limit)

            for h in q.all():
                rows.append({
                    "id"           : str(h.id),
                    "url"          : h.url or "",
                    "language"     : h.language,
                    "hotel_name"   : h.hotel_name or "",
                    "hotel_id_ext" : h.hotel_id_ext or "",
                    "star_rating"  : float(h.star_rating)  if h.star_rating  else "",
                    "review_score" : float(h.review_score) if h.review_score else "",
                    "review_count" : h.review_count or "",
                    "address"      : h.address or "",
                    "city"         : h.city or "",
                    "country"      : h.country or "",
                    "latitude"     : float(h.latitude)  if h.latitude  else "",
                    "longitude"    : float(h.longitude) if h.longitude else "",
                    "scrape_status": h.scrape_status,
                    "scrape_engine": h.scrape_engine or "",
                    "scraped_at"   : h.scraped_at.isoformat() if h.scraped_at else "",
                    "amenities"    : "|".join(h.amenities) if isinstance(h.amenities, list) else "",
                    "photo_count"  : len(h.photos) if isinstance(h.photos, list) else 0,
                })
    except Exception as exc:
        logger.error("Database query failed: %s", exc)
        return 0

    if not rows:
        logger.warning("No hotels found matching the criteria")
        return 0

    df = pd.DataFrame(rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if fmt == "csv":
            df.to_csv(output_path, index=False, encoding="utf-8-sig")  # utf-8-sig for Windows Excel
            logger.info("Exported %d hotels to CSV: %s", len(rows), output_path)
        elif fmt == "excel":
            df.to_excel(output_path, index=False, engine="openpyxl")
            logger.info("Exported %d hotels to Excel: %s", len(rows), output_path)
        else:
            logger.error("Unsupported format: %s", fmt)
            return 0
    except Exception as exc:
        logger.error("Write error: %s", exc)
        return 0

    return len(rows)


def main() -> int:
    from app.config import get_settings
    cfg = get_settings()

    parser = argparse.ArgumentParser(
        description="Export BookingScraper Pro hotel data to CSV or Excel."
    )
    parser.add_argument("--format",   choices=["csv", "excel"], default="csv")
    parser.add_argument("--output",   type=Path,
                        default=Path(cfg.EXPORT_DIR) / "hotels.csv")
    parser.add_argument("--language", default=None)
    parser.add_argument("--city",     default=None)
    parser.add_argument("--country",  default=None)
    parser.add_argument("--status",   choices=["done","error","partial","pending"], default=None)
    parser.add_argument("--limit",    type=int, default=None)
    args = parser.parse_args()

    count = export_hotels(
        output_path=args.output,
        fmt        =args.format,
        language   =args.language,
        city       =args.city,
        country    =args.country,
        status     =args.status,
        limit      =args.limit,
    )
    return 0 if count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
