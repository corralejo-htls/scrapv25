"""
BookingScraper Pro v6.0 - Celery Tasks
=======================================
All async tasks executed by the Celery worker.
Platform : Windows 11 — --pool=threads required.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from celery import shared_task
from sqlalchemy import text

from app.celery_app import celery_app
from app.database import get_db
from app.models import URLQueue

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
@celery_app.task(bind=True, max_retries=3, default_retry_delay=60, name="app.tasks.scrape_url")
def scrape_url(self, url_id: str, language: str = "en") -> dict:
    """
    Scrape a single (url_id, language) pair.
    Retried automatically on transient failures.
    """
    from app.scraper_service import ScraperService
    try:
        service = ScraperService()
        return service.scrape_one_by_id(url_id=uuid.UUID(url_id), language=language)
    except Exception as exc:
        logger.exception("Task scrape_url failed: url_id=%s lang=%s", url_id, language)
        raise self.retry(exc=exc)


# ─────────────────────────────────────────────────────────────────────────────
@celery_app.task(name="app.tasks.scrape_batch")
def scrape_batch(url_ids: list[str], language: str = "en") -> dict:
    """Enqueue a batch of URLs as individual scrape tasks."""
    dispatched = 0
    for uid in url_ids:
        scrape_url.delay(uid, language)
        dispatched += 1
    return {"dispatched": dispatched, "language": language}


# ─────────────────────────────────────────────────────────────────────────────
@celery_app.task(name="app.tasks.reset_stale_processing_urls")
def reset_stale_processing_urls(stale_minutes: int = 30) -> dict:
    """
    Reset URLs that have been in 'processing' state too long
    (e.g., worker crashed mid-scrape).
    """
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=stale_minutes)
    reset_count = 0
    try:
        with get_db() as session:
            stale = (
                session.query(URLQueue)
                .filter(
                    URLQueue.status    == "processing",
                    URLQueue.claimed_at < cutoff,
                )
                .all()
            )
            for row in stale:
                row.status      = "pending"
                row.claimed_by  = None
                row.claimed_at  = None
                row.version_id += 1
                reset_count    += 1
        logger.info("Reset %d stale processing URLs (cutoff=%s)", reset_count, cutoff)
    except Exception as exc:
        logger.error("reset_stale_processing_urls failed: %s", exc)
    return {"reset": reset_count}


# ─────────────────────────────────────────────────────────────────────────────
@celery_app.task(name="app.tasks.ensure_log_partitions")
def ensure_log_partitions() -> dict:
    """
    Create next month's scraping_logs partition if it does not exist yet.
    Run daily via Celery Beat.
    """
    from datetime import date
    created = []
    try:
        with get_db() as session:
            for offset in range(1, 3):   # next 2 months
                part_date  = (date.today().replace(day=1) + timedelta(days=32 * offset)).replace(day=1)
                next_date  = (part_date + timedelta(days=32)).replace(day=1)
                part_name  = f"scraping_logs_{part_date.strftime('%Y_%m')}"
                exists = session.execute(
                    text("SELECT 1 FROM pg_tables WHERE tablename=:n AND schemaname='public'"),
                    {"n": part_name},
                ).fetchone()
                if not exists:
                    session.execute(text(
                        f"CREATE TABLE IF NOT EXISTS {part_name} "
                        f"PARTITION OF scraping_logs "
                        f"FOR VALUES FROM ('{part_date}') TO ('{next_date}')"
                    ))
                    created.append(part_name)
                    logger.info("Created log partition: %s", part_name)
    except Exception as exc:
        logger.error("ensure_log_partitions failed: %s", exc)
    return {"created": created}


# ─────────────────────────────────────────────────────────────────────────────
@celery_app.task(name="app.tasks.download_hotel_images")
def download_hotel_images(hotel_id: str, image_urls: list[str]) -> dict:
    """Download images for a hotel asynchronously."""
    from app.config import get_settings
    from app.image_downloader import ImageDownloader
    cfg = get_settings()
    dl  = ImageDownloader(
        output_dir=cfg.IMAGES_DIR,
        max_workers=cfg.IMAGES_MAX_WORKERS,
        per_image_timeout=cfg.IMAGES_TIMEOUT,
        max_size_mb=cfg.IMAGES_MAX_SIZE_MB,
    )
    result = dl.download_images(image_urls, hotel_id)
    return {
        "hotel_id"  : hotel_id,
        "total"     : result.total,
        "downloaded": result.downloaded,
        "errors"    : result.errors,
    }
