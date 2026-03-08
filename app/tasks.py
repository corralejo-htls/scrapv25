"""
tasks.py — BookingScraper Pro v48
Fixes applied:
  SCRAP-BUG-009 / BUG-101: SQL injection eliminated — partition names are
                            validated against a strict regex before use.
  SCRAP-BUG-028           : Tasks assigned to named queues for proper routing.
  SCRAP-BUG-033           : Partition creation uses SERIALIZABLE isolation.
  Platform                : Windows 11 / Celery with Redis broker.
"""

from __future__ import annotations

import logging
import re
from datetime import date, timedelta
from typing import List, Optional

from celery import shared_task
from sqlalchemy import text

from app.database import get_db, get_serializable_db

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Partition name validation — BUG-101 / SCRAP-BUG-009 fix
# ---------------------------------------------------------------------------
# Partition names are always of the form: scraping_logs_YYYY_MM
# We validate STRICTLY before interpolating into any SQL string.
_PARTITION_NAME_RE = re.compile(r"^scraping_logs_\d{4}_(?:0[1-9]|1[0-2])$")
_DATE_LITERAL_RE = re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$")


def _safe_partition_name(year: int, month: int) -> str:
    """
    Construct and validate partition table name.
    Raises ValueError if the resulting name fails the strict regex —
    prevents any injection path even if the calling logic changes.
    """
    name = f"scraping_logs_{year:04d}_{month:02d}"
    if not _PARTITION_NAME_RE.match(name):
        raise ValueError(f"Generated partition name '{name}' failed safety validation.")
    return name


def _safe_date_literal(d: date) -> str:
    """Validate a date string before SQL interpolation."""
    literal = d.strftime("%Y-%m-%d")
    if not _DATE_LITERAL_RE.match(literal):
        raise ValueError(f"Generated date literal '{literal}' failed safety validation.")
    return literal


# ---------------------------------------------------------------------------
# Partition management — SCRAP-BUG-009 fix
# ---------------------------------------------------------------------------

@shared_task(
    name="tasks.ensure_log_partitions",
    queue="maintenance",           # SCRAP-BUG-028: named queue
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
)
def ensure_log_partitions(self, months_ahead: int = 2) -> dict:
    """
    Create monthly partitions for scraping_logs up to `months_ahead` months in advance.

    BUG-101 fix: partition names and date boundaries are validated via strict
    regex before interpolation.  SQLAlchemy text() is used for execution.
    SCRAP-BUG-033 fix: uses SERIALIZABLE isolation to prevent duplicate
    partition creation under concurrent task execution.
    """
    today = date.today()
    created: List[str] = []
    skipped: List[str] = []
    errors: List[str] = []

    target_months = []
    for delta in range(months_ahead + 1):
        # Advance month arithmetic
        target_year = today.year + (today.month - 1 + delta) // 12
        target_month = (today.month - 1 + delta) % 12 + 1
        target_months.append((target_year, target_month))

    # SCRAP-BUG-033: use serializable session for DDL consistency
    with get_serializable_db() as session:
        for year, month in target_months:
            try:
                part_name = _safe_partition_name(year, month)
                # Calculate partition bounds
                part_start = date(year, month, 1)
                # First day of next month
                if month == 12:
                    part_end = date(year + 1, 1, 1)
                else:
                    part_end = date(year, month + 1, 1)

                # Validate date literals before use (BUG-101)
                start_literal = _safe_date_literal(part_start)
                end_literal = _safe_date_literal(part_end)

                # Check if partition already exists
                exists_query = text(
                    "SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = :name"
                )
                exists = session.execute(exists_query, {"name": part_name}).fetchone()

                if exists:
                    skipped.append(part_name)
                    logger.debug("Partition %s already exists, skipping.", part_name)
                    continue

                # DDL: partition name is regex-validated above — safe to interpolate
                # Date literals are regex-validated — safe to interpolate
                # Note: PostgreSQL DDL cannot use bind parameters for identifiers/literals
                # in PARTITION OF FOR VALUES FROM ... TO ...
                create_sql = text(
                    f"CREATE TABLE IF NOT EXISTS {part_name} "
                    f"PARTITION OF scraping_logs "
                    f"FOR VALUES FROM ('{start_literal}') TO ('{end_literal}')"
                )
                session.execute(create_sql)

                # Create index on the partition
                index_name = f"ix_{part_name}_url_id"
                index_sql = text(
                    f"CREATE INDEX IF NOT EXISTS {index_name} "
                    f"ON {part_name} (url_id)"
                )
                session.execute(index_sql)

                created.append(part_name)
                logger.info("Created partition: %s (%s → %s)", part_name, start_literal, end_literal)

            except ValueError as exc:
                # Partition name/date validation failed — critical code path error
                logger.critical(
                    "Partition safety validation failed for year=%d month=%d: %s",
                    year, month, exc,
                )
                errors.append(f"{year}-{month:02d}: validation_error")
                raise  # Propagate so Celery marks task as FAILURE

            except Exception as exc:
                logger.error("Failed to create partition %d-%02d: %s", year, month, exc)
                errors.append(f"{year}-{month:02d}: {type(exc).__name__}")

    return {
        "created": created,
        "skipped": skipped,
        "errors": errors,
    }


# ---------------------------------------------------------------------------
# Cleanup tasks
# ---------------------------------------------------------------------------

@shared_task(
    name="tasks.purge_old_debug_html",
    queue="maintenance",
    bind=True,
    max_retries=2,
)
def purge_old_debug_html(self) -> dict:
    """Remove debug HTML files older than DEBUG_HTML_MAX_AGE_HOURS."""
    from app.config import get_settings
    import os
    import time

    cfg = get_settings()
    if not cfg.DEBUG_HTML_SAVE:
        return {"skipped": True, "reason": "DEBUG_HTML_SAVE is disabled"}

    cutoff = time.time() - (cfg.DEBUG_HTML_MAX_AGE_HOURS * 3600)
    removed = 0
    errors = 0

    html_dir = cfg.DEBUG_HTML_DIR
    if html_dir.exists():
        for html_file in html_dir.glob("*.html"):
            try:
                if html_file.stat().st_mtime < cutoff:
                    html_file.unlink()
                    removed += 1
            except OSError as exc:
                logger.warning("Could not remove debug file %s: %s", html_file, exc)
                errors += 1

    logger.info("purge_old_debug_html: removed=%d errors=%d", removed, errors)
    return {"removed": removed, "errors": errors}


@shared_task(
    name="tasks.collect_system_metrics",
    queue="monitoring",
    bind=True,
)
def collect_system_metrics(self) -> dict:
    """Collect and persist system health metrics."""
    try:
        import psutil
        from app.database import get_pool_status

        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent

        pool_info = get_pool_status()
        checked_out = pool_info.get("checked_out", 0)

        with get_db() as session:
            from app.models import SystemMetrics
            from sqlalchemy import func
            pending_count = (
                session.query(func.count()).filter_by(status="pending").scalar() or 0
            )
            done_count = (
                session.query(func.count()).filter_by(status="done").scalar() or 0
            )
            metric = SystemMetrics(
                cpu_usage=cpu,
                memory_usage=mem,
                db_pool_checked_out=checked_out,
                urls_pending=pending_count,
                urls_done=done_count,
            )
            session.add(metric)

        return {"cpu": cpu, "memory": mem}

    except Exception as exc:
        logger.error("collect_system_metrics failed: %s", exc)
        return {"error": str(exc)}


@shared_task(
    name="tasks.reset_stale_processing_urls",
    queue="maintenance",
    bind=True,
)
def reset_stale_processing_urls(self, stale_minutes: int = 60) -> dict:
    """
    Reset URLs stuck in 'processing' status back to 'pending'.
    Handles crashed workers that left URLs in an incomplete state.
    """
    from datetime import datetime, timezone, timedelta

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=stale_minutes)
    reset_count = 0

    with get_db() as session:
        from app.models import URLQueue
        stale_urls = (
            session.query(URLQueue)
            .filter(
                URLQueue.status == "processing",
                URLQueue.updated_at < cutoff,
            )
            .all()
        )
        for url in stale_urls:
            url.status = "pending"
            url.last_error = f"Reset from stale processing after {stale_minutes}m"
            reset_count += 1

    logger.info("Reset %d stale processing URLs.", reset_count)
    return {"reset": reset_count}
