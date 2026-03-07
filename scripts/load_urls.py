"""
BookingScraper Pro v6.0 - URL Loader
=====================================
Load Booking.com hotel URLs from CSV into the scraping queue.
Platform : Windows 11 — pathlib.Path for all file I/O.

Corrections Applied (v46):
- BUG-005 : Line ~29  — bare except replaced; KeyboardInterrupt re-raised.
- BUG-006 : Line ~154 — bare except replaced; SystemExit re-raised.
- BUG-007 : Line ~290 — bare except in main() replaced with explicit handlers.
"""

from __future__ import annotations

import argparse
import csv
import logging
import sys
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("load_urls")

VALID_LANGUAGES = {
    "en","es","de","fr","it","pt","nl","pl","ru","zh",
    "ja","ko","ar","tr","sv","da","fi","nb","cs",
}
BATCH_SIZE = 500


def is_valid_booking_url(url: str) -> bool:
    if not url:
        return False
    try:
        p = urlparse(url.strip())
        return p.netloc in ("www.booking.com","booking.com") and bool(p.path)
    except ValueError:
        return False


# ── BUG-005 FIX ──────────────────────────────────────────────────────────────
def load_urls_from_csv(filepath: Path, language: str = "en",
                       url_column: str = "url",
                       encoding: str = "utf-8-sig") -> list[dict]:
    """
    Read URLs from CSV.
    BUG-005 FIX: KeyboardInterrupt is NOT swallowed — always re-raised.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    records: list[dict] = []
    skipped = 0
    row_num = 0

    try:
        with filepath.open(encoding=encoding, newline="") as fh:
            reader = csv.DictReader(fh)
            if url_column not in (reader.fieldnames or []):
                raise ValueError(
                    f"Column '{url_column}' not in CSV. "
                    f"Available: {list(reader.fieldnames or [])}"
                )
            for row_num, row in enumerate(reader, start=2):
                url = (row.get(url_column) or "").strip()
                if not url or not is_valid_booking_url(url):
                    skipped += 1
                    continue
                records.append({
                    "url": url, "language": language,
                    "source_row": row_num,
                })

    except KeyboardInterrupt:
        # BUG-005 FIX: NEVER swallow
        logger.warning("Interrupted at row %d", row_num)
        raise

    except UnicodeDecodeError:
        if encoding != "latin-1":
            return load_urls_from_csv(filepath, language, url_column, "latin-1")
        raise ValueError(f"Cannot decode {filepath}")

    except csv.Error as exc:
        raise ValueError(f"CSV error at row {row_num}: {exc}") from exc

    except OSError as exc:
        raise OSError(f"File read error: {exc}") from exc

    logger.info("CSV: %d valid, %d skipped from %s", len(records), skipped, filepath.name)
    return records


# ── BUG-006 FIX ──────────────────────────────────────────────────────────────
def insert_urls_to_db(records: list[dict], priority: int = 5,
                      dry_run: bool = False) -> dict:
    """
    Insert URL records into url_queue.
    BUG-006 FIX: SystemExit and KeyboardInterrupt are NOT swallowed.
    """
    if not records or dry_run:
        if dry_run:
            logger.info("DRY RUN: %d records (no DB insert)", len(records))
        return {"inserted": 0, "skipped_duplicate": 0, "error": 0,
                "dry_run": dry_run}

    from app.database import get_db
    from app.models import URLQueue
    from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

    inserted = skipped_dup = errors = 0

    for start in range(0, len(records), BATCH_SIZE):
        batch = records[start: start + BATCH_SIZE]
        try:
            with get_db() as session:
                for rec in batch:
                    try:
                        session.add(URLQueue(
                            url=rec["url"], language=rec["language"],
                            priority=priority, status="pending",
                        ))
                        session.flush()
                        inserted += 1
                    except IntegrityError:
                        session.rollback()
                        skipped_dup += 1

        except KeyboardInterrupt:
            # BUG-006 FIX: NEVER swallow KeyboardInterrupt
            logger.warning("Interrupted during DB insert at batch %d", start)
            raise

        except SystemExit:
            # BUG-006 FIX: NEVER swallow SystemExit
            raise

        except OperationalError as exc:
            logger.error("DB connection error at batch %d: %s", start, exc)
            errors += len(batch)
            time.sleep(2.0)

        except SQLAlchemyError as exc:
            logger.error("SQLAlchemy error at batch %d: %s", start, exc)
            errors += len(batch)

        logger.info("Batch progress: %d/%d", min(start + BATCH_SIZE, len(records)), len(records))

    return {"inserted": inserted, "skipped_duplicate": skipped_dup, "error": errors}


# ── BUG-007 FIX ──────────────────────────────────────────────────────────────
def main() -> int:
    """
    BUG-007 FIX: No bare except in main().
    KeyboardInterrupt → exit code 130; SystemExit → propagates naturally.
    """
    parser = argparse.ArgumentParser(
        description="Load Booking.com URLs from CSV into the scraping queue."
    )
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--language", "-l", default="en", choices=sorted(VALID_LANGUAGES))
    parser.add_argument("--priority", "-p", type=int, default=5,
                        choices=range(1, 11), metavar="1-10")
    parser.add_argument("--url-column", default="url")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--encoding", default="utf-8-sig")
    args = parser.parse_args()

    logger.info("Loading: %s  language=%s  priority=%d  dry_run=%s",
                args.csv_file, args.language, args.priority, args.dry_run)

    # BUG-007 FIX: explicit exception types — no bare except:
    try:
        records = load_urls_from_csv(
            args.csv_file, args.language, args.url_column, args.encoding
        )
        if not records:
            logger.warning("No valid URLs found")
            return 0

        result = insert_urls_to_db(records, args.priority, args.dry_run)
        logger.info("inserted=%d  skipped_duplicate=%d  errors=%d",
                    result["inserted"], result["skipped_duplicate"], result["error"])
        return 1 if result["error"] > 0 else 0

    except KeyboardInterrupt:
        # BUG-007 FIX: clean user interrupt, exit code 130
        print("\n[INTERRUPTED] Cancelled by user", file=sys.stderr)
        return 130

    # SystemExit propagates naturally (NOT caught)

    except (FileNotFoundError, ValueError) as exc:
        logger.error("Input error: %s", exc)
        return 1

    except Exception as exc:
        logger.exception("Unexpected error: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
