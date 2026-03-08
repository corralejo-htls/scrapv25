"""
scraper_service.py — BookingScraper Pro v48
Fixes applied:
  BUG-104 / SCRAP-CON-003: Redis uses a shared connection pool, not per-call new conn.
  SCRAP-BUG-016          : max_workers validated at runtime, not just at config load.
  SCRAP-BUG-017          : Timeout configurable via settings, not hardcoded.
  SCRAP-COMP-003         : High-complexity methods decomposed into helpers.
  Platform               : Windows 11 / ThreadPoolExecutor (not ProcessPoolExecutor).
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeout
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import redis as redis_lib

from app.config import get_settings
from app.database import get_db
from app.extractor import HotelExtractor, detect_language
from app.models import Hotel, ScrapingLog, URLLanguageStatus, URLQueue
from app.scraper import CloudScraperEngine, SeleniumEngine, build_language_url

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Shared Redis connection pool — BUG-104 fix
# ---------------------------------------------------------------------------
_redis_pool: Optional[redis_lib.ConnectionPool] = None
_redis_pool_lock = threading.Lock()


def _get_redis_pool() -> Optional[redis_lib.ConnectionPool]:
    """Return (or create) the shared Redis connection pool."""
    global _redis_pool
    if _redis_pool is None:
        with _redis_pool_lock:
            if _redis_pool is None:  # double-checked locking
                try:
                    cfg = get_settings()
                    _redis_pool = redis_lib.ConnectionPool.from_url(
                        cfg.REDIS_URL,
                        max_connections=cfg.REDIS_MAX_CONNECTIONS,
                        decode_responses=True,
                        socket_connect_timeout=3,
                        socket_timeout=3,
                    )
                    logger.info("Redis connection pool created: max_connections=%d", cfg.REDIS_MAX_CONNECTIONS)
                except Exception as exc:
                    logger.warning("Could not create Redis pool: %s", exc)
    return _redis_pool


def _get_redis_client() -> Optional[redis_lib.Redis]:
    """Return a Redis client backed by the shared pool."""
    pool = _get_redis_pool()
    if pool:
        return redis_lib.Redis(connection_pool=pool)
    return None


# ---------------------------------------------------------------------------
# Distributed URL lock via Redis SET NX
# ---------------------------------------------------------------------------

def _try_claim_url(url_id: str) -> bool:
    """Attempt to claim a URL for processing via Redis SET NX."""
    try:
        r = _get_redis_client()
        if r:
            key = f"url_lock:{url_id}"
            cfg = get_settings()
            timeout = cfg.SCRAPER_REQUEST_TIMEOUT * cfg.MAX_RETRIES * 3
            return bool(r.set(key, "1", nx=True, ex=timeout))
    except Exception as exc:
        logger.debug("Redis claim failed for %s: %s — proceeding without distributed lock.", url_id, exc)
    return True  # Fallback: allow processing if Redis unavailable


def _release_url(url_id: str) -> None:
    """Release a URL lock from Redis."""
    try:
        r = _get_redis_client()
        if r:
            r.delete(f"url_lock:{url_id}")
    except Exception as exc:
        logger.debug("Redis release failed for %s: %s", url_id, exc)


# ---------------------------------------------------------------------------
# Stats (protected by lock)
# ---------------------------------------------------------------------------

class _Stats:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.processed = 0
        self.succeeded = 0
        self.failed = 0
        self.skipped = 0

    def record(self, *, succeeded: bool = False, failed: bool = False, skipped: bool = False) -> None:
        with self._lock:
            self.processed += 1
            if succeeded:
                self.succeeded += 1
            elif failed:
                self.failed += 1
            elif skipped:
                self.skipped += 1

    def to_dict(self) -> Dict[str, int]:
        with self._lock:
            return {
                "processed": self.processed,
                "succeeded": self.succeeded,
                "failed": self.failed,
                "skipped": self.skipped,
            }


# ---------------------------------------------------------------------------
# ScraperService
# ---------------------------------------------------------------------------

class ScraperService:
    """
    Orchestrates URL scraping with worker pool, VPN rotation, and DB persistence.
    Windows 11: uses ThreadPoolExecutor (not multiprocessing) for I/O-bound tasks.
    """

    def __init__(self) -> None:
        self._cfg = get_settings()
        self._cloud_engine = CloudScraperEngine()
        self._selenium_engine = SeleniumEngine()
        self._stats = _Stats()

    # ── Public API ────────────────────────────────────────────────────────────

    def dispatch_batch(
        self,
        url_ids: Optional[List[str]] = None,
        max_workers: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Dispatch a batch of scraping jobs.
        SCRAP-BUG-016: max_workers clamped to config maximum at runtime.
        """
        workers = self._resolve_workers(max_workers)
        urls = self._fetch_pending_urls(url_ids)

        if not urls:
            return {"status": "no_work", "queued": 0}

        logger.info("Dispatching batch: urls=%d workers=%d", len(urls), workers)

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(self._process_url, url_obj): url_obj
                for url_obj in urls
            }
            # SCRAP-BUG-017: configurable timeout per URL
            timeout = self._cfg.SCRAPER_REQUEST_TIMEOUT * self._cfg.MAX_RETRIES * 2

            for future in as_completed(futures, timeout=timeout):
                url_obj = futures[future]
                try:
                    future.result()
                except FuturesTimeout:
                    logger.error("URL %s timed out after %ds", url_obj.id, timeout)
                    self._mark_error(url_obj, "Processing timeout exceeded")
                    self._stats.record(failed=True)
                except Exception as exc:
                    logger.error("URL %s raised exception: [%s] %s", url_obj.id, type(exc).__name__, exc)
                    self._mark_error(url_obj, str(exc)[:2000])
                    self._stats.record(failed=True)

        result = self._stats.to_dict()
        result["status"] = "complete"
        return result

    # ── Private helpers ───────────────────────────────────────────────────────

    def _resolve_workers(self, requested: Optional[int]) -> int:
        """Clamp max_workers to config limit. SCRAP-BUG-016 fix."""
        max_allowed = self._cfg.SCRAPER_MAX_WORKERS
        if requested is None:
            return max_allowed
        clamped = min(max(1, requested), max_allowed)
        if clamped != requested:
            logger.warning(
                "Requested max_workers=%d exceeds limit=%d. Clamped to %d.",
                requested, max_allowed, clamped,
            )
        return clamped

    def _fetch_pending_urls(self, url_ids: Optional[List[str]]) -> List[URLQueue]:
        """Fetch pending URL records from the database."""
        with get_db() as session:
            q = session.query(URLQueue).filter(URLQueue.status == "pending")
            if url_ids:
                try:
                    uuids = [uuid.UUID(uid) for uid in url_ids]
                    q = q.filter(URLQueue.id.in_(uuids))
                except ValueError as exc:
                    logger.warning("Invalid UUID in url_ids: %s", exc)
            rows = q.order_by(URLQueue.priority.desc(), URLQueue.created_at).limit(200).all()
            # Detach from session before returning
            session.expunge_all()
            return rows

    def _process_url(self, url_obj: URLQueue) -> None:
        """Process a single URL through all enabled languages."""
        url_id_str = str(url_obj.id)

        if not _try_claim_url(url_id_str):
            logger.debug("URL %s already claimed, skipping.", url_id_str)
            self._stats.record(skipped=True)
            return

        try:
            self._mark_processing(url_obj)
            languages = self._cfg.ENABLED_LANGUAGES

            all_ok = True
            for lang in languages:
                ok = self._scrape_language(url_obj, lang)
                if not ok:
                    all_ok = False

            self._mark_done(url_obj, all_ok)
            self._stats.record(succeeded=True)

        except Exception as exc:
            logger.error("_process_url failed for %s: [%s] %s", url_id_str, type(exc).__name__, exc)
            self._mark_error(url_obj, str(exc)[:2000])
            self._stats.record(failed=True)
        finally:
            _release_url(url_id_str)

    def _scrape_language(self, url_obj: URLQueue, lang: str) -> bool:
        """Scrape one language variant of a hotel URL. Returns True on success."""
        lang_url = build_language_url(url_obj.base_url or url_obj.url, lang)
        start_ts = time.monotonic()

        html = self._cloud_engine.scrape(lang_url, retries=self._cfg.MAX_LANG_RETRIES)

        # Fallback to Selenium if CloudScraper fails
        if html is None:
            logger.info("CloudScraper failed for %s/%s — trying Selenium.", url_obj.id, lang)
            html = self._selenium_engine.scrape(lang_url)

        duration_ms = int((time.monotonic() - start_ts) * 1000)

        if html is None:
            self._log_scraping_event(url_obj, lang, "scrape_failed", "error", duration_ms)
            self._upsert_lang_status(url_obj, lang, "error", "All scraping engines failed")
            return False

        # Extract hotel data
        extractor = HotelExtractor(html, url=lang_url, language=lang)
        hotel_data = extractor.extract_all()

        # Persist hotel record
        try:
            self._upsert_hotel(url_obj, lang, hotel_data, duration_ms)
            self._log_scraping_event(url_obj, lang, "scrape_success", "done", duration_ms)
            self._upsert_lang_status(url_obj, lang, "done", None)
            return True
        except Exception as exc:
            logger.error("Hotel upsert failed for %s/%s: %s", url_obj.id, lang, exc)
            self._log_scraping_event(url_obj, lang, "upsert_failed", "error", duration_ms, str(exc))
            self._upsert_lang_status(url_obj, lang, "error", str(exc)[:2000])
            return False

    def _upsert_hotel(
        self,
        url_obj: URLQueue,
        lang: str,
        data: Dict[str, Any],
        duration_ms: int,
    ) -> None:
        with get_db() as session:
            existing = (
                session.query(Hotel)
                .filter_by(url_id=url_obj.id, language=lang)
                .first()
            )
            if existing:
                for k, v in data.items():
                    if hasattr(existing, k):
                        setattr(existing, k, v)
                existing.scrape_duration_s = duration_ms / 1000
                existing.version_id += 1
            else:
                hotel = Hotel(
                    url_id=url_obj.id,
                    language=lang,
                    scrape_duration_s=duration_ms / 1000,
                    scrape_engine="cloudscraper",
                    **{k: v for k, v in data.items() if hasattr(Hotel, k)},
                )
                session.add(hotel)

    def _upsert_lang_status(
        self,
        url_obj: URLQueue,
        lang: str,
        status: str,
        error: Optional[str],
    ) -> None:
        with get_db() as session:
            row = (
                session.query(URLLanguageStatus)
                .filter_by(url_id=url_obj.id, language=lang)
                .first()
            )
            if row:
                row.status = status
                row.last_error = error
                row.attempts += 1
            else:
                session.add(URLLanguageStatus(
                    url_id=url_obj.id,
                    language=lang,
                    status=status,
                    last_error=error,
                    attempts=1,
                ))

    def _log_scraping_event(
        self,
        url_obj: URLQueue,
        lang: str,
        event_type: str,
        status: str,
        duration_ms: int,
        error_msg: Optional[str] = None,
    ) -> None:
        try:
            with get_db() as session:
                session.add(ScrapingLog(
                    url_id=url_obj.id,
                    language=lang,
                    event_type=event_type,
                    status=status,
                    duration_ms=duration_ms,
                    error_message=(error_msg or "")[:2000] if error_msg else None,
                ))
        except Exception as exc:
            # Logging failure must not abort the scraping workflow
            logger.warning("Failed to write ScrapingLog: %s", exc)

    def _mark_processing(self, url_obj: URLQueue) -> None:
        with get_db() as session:
            row = session.get(URLQueue, url_obj.id)
            if row:
                row.status = "processing"

    def _mark_done(self, url_obj: URLQueue, all_ok: bool) -> None:
        with get_db() as session:
            row = session.get(URLQueue, url_obj.id)
            if row:
                row.status = "done" if all_ok else "error"
                row.scraped_at = datetime.now(timezone.utc)

    def _mark_error(self, url_obj: URLQueue, error: str) -> None:
        with get_db() as session:
            row = session.get(URLQueue, url_obj.id)
            if row:
                row.status = "error"
                row.retry_count += 1
                row.last_error = error[:2000]
                if row.retry_count >= row.max_retries:
                    row.status = "error"
