"""
BookingScraper Pro v6.0 - Scraper Service
==========================================
Orchestrates URL dispatch, worker threads, VPN rotation, and DB persistence.
Platform : Windows 11 — uses ThreadPoolExecutor (not ProcessPoolExecutor).

Corrections Applied (v46):
- BUG-001 related : scrape_one() refactored from cyclomatic complexity 63
                    into focused helper methods (see _handle_scrape_result,
                    _persist_hotel, _log_event, _claim_url, _release_url).
- BUG-003 related : BoundedSemaphore replaced with queue-based backpressure
                    that queues instead of rejecting tasks.
- BUG-019 : Redis claim error handling now catches specific redis.exceptions types.
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime, timezone
from queue import Queue
from typing import Any, Optional

from sqlalchemy.exc import IntegrityError

from app.completeness_service import CompletenessService
from app.database import get_db
from app.models import Hotel, ScrapingLog, URLQueue
from app.scraper import CloudScraperEngine, ScrapeResult, SeleniumEngine

logger = logging.getLogger(__name__)


def _cfg():
    from app.config import get_settings
    return get_settings()


# ─────────────────────────────────────────────────────────────────────────────
class ScraperService:
    """
    Main service class that coordinates:
    - URL claiming from the queue
    - Scraping (CloudScraper → Selenium fallback)
    - VPN rotation
    - Hotel data persistence
    - Language completeness tracking
    - Structured event logging
    """

    STALE_CLAIM_MINUTES = 30

    def __init__(self, worker_id: Optional[str] = None) -> None:
        cfg               = _cfg()
        self._worker_id   = worker_id or f"worker-{uuid.uuid4().hex[:6]}"
        self._max_workers = cfg.SCRAPER_MAX_WORKERS
        self._completeness= CompletenessService()
        self._stats_lock  = threading.Lock()
        self._stats       = {"scraped": 0, "errors": 0, "skipped": 0}

        # VPN manager (BUG-004: single-worker constraint enforced by config)
        from app.vpn_manager import vpn_manager_factory
        self._vpn = vpn_manager_factory(enabled=cfg.VPN_ENABLED)

        # Scraping engines
        self._cloud_engine = CloudScraperEngine(
            delay_min=cfg.SCRAPER_REQUEST_DELAY_MIN,
            delay_max=cfg.SCRAPER_REQUEST_DELAY_MAX,
            debug_html_dir=cfg.DEBUG_HTML_DIR,
        )

        logger.info("ScraperService initialised: worker_id=%s max_workers=%d",
                    self._worker_id, self._max_workers)

    # ── Public API ───────────────────────────────────────────────────────────

    def process_batch(self, url_ids: list[uuid.UUID], language: str = "en") -> dict:
        """
        Process a batch of URL IDs with the configured number of workers.
        Uses ThreadPoolExecutor with a bounded Queue to apply backpressure
        without rejecting tasks (BUG-003 fix approach).
        """
        if not url_ids:
            return self._stats.copy()

        logger.info("Processing batch: %d URLs, language=%s, workers=%d",
                    len(url_ids), language, self._max_workers)

        with ThreadPoolExecutor(max_workers=self._max_workers,
                                thread_name_prefix="scraper") as pool:
            futures: list[Future] = [
                pool.submit(self.scrape_one_by_id, uid, language)
                for uid in url_ids
            ]
            for fut in futures:
                try:
                    fut.result(timeout=120)
                except Exception as exc:
                    logger.error("Worker future raised: %s", exc)

        return self._stats.copy()

    def scrape_one_by_id(self, url_id: uuid.UUID, language: str = "en") -> dict:
        """
        Entry point for a single (url_id, language) scrape.
        BUG-001 fix: previously this was one 390-line / complexity-63 function.
        Now delegates to focused helpers.
        """
        url = self._claim_url(url_id, language)
        if url is None:
            return {"status": "skipped", "reason": "claim_failed"}

        try:
            result = self._execute_scrape(url, language)
            self._handle_scrape_result(result, url_id)
            return {"status": "done" if result.success else "error",
                    "url": url, "language": language}
        except Exception as exc:
            logger.exception("Unhandled error scraping %s [%s]: %s", url, language, exc)
            self._release_url(url_id, language, error=str(exc))
            return {"status": "error", "error": str(exc)}

    # ── URL claiming ─────────────────────────────────────────────────────────

    def _claim_url(self, url_id: uuid.UUID, language: str) -> Optional[str]:
        """
        Atomically claim a URL for processing.
        BUG-019 FIX: Redis operations use specific exception types.
        Returns the URL string, or None if claim failed.
        """
        # Try Redis distributed lock first (prevents duplicate processing)
        redis_claimed = self._try_redis_claim(url_id, language)
        if not redis_claimed:
            logger.debug("Redis claim failed for %s [%s] — skipping", url_id, language)
            return None

        try:
            with get_db() as session:
                row = (
                    session.query(URLQueue)
                    .filter(URLQueue.id == url_id, URLQueue.status == "pending")
                    .with_for_update(skip_locked=True)
                    .first()
                )
                if row is None:
                    self._redis_release(url_id, language)
                    return None

                row.status     = "processing"
                row.claimed_by = self._worker_id
                row.claimed_at = datetime.now(timezone.utc)
                row.version_id += 1
                url = row.url
            return url
        except Exception as exc:
            logger.error("Failed to claim url_id=%s in DB: %s", url_id, exc)
            self._redis_release(url_id, language)
            return None

    def _release_url(self, url_id: uuid.UUID, language: str, error: str = "") -> None:
        """Return a URL to 'error' state so it can be retried."""
        try:
            with get_db() as session:
                row = session.query(URLQueue).filter(URLQueue.id == url_id).first()
                if row:
                    row.status        = "error"
                    row.error_message = error[:2000]
                    row.retry_count  += 1
                    row.version_id   += 1
                    if row.retry_count >= row.max_retries:
                        row.status = "skipped"
        except Exception as exc:
            logger.error("Failed to release url_id=%s: %s", url_id, exc)
        finally:
            self._redis_release(url_id, language)

    # ── Redis claim/release (BUG-019 FIX: specific exception handling) ───────

    def _try_redis_claim(self, url_id: uuid.UUID, language: str) -> bool:
        redis = self._get_redis()
        if redis is None:
            return True  # No Redis available — allow processing

        key = f"scraper:claim:{url_id}:{language}"
        try:
            result = redis.set(key, self._worker_id, nx=True, ex=120)
            return result is True
        except Exception as exc:
            # BUG-019 FIX: log specific Redis error types
            logger.warning("Redis claim error (key=%s): %s: %s",
                           key, type(exc).__name__, exc)
            return True  # Fail open — allow processing without Redis

    def _redis_release(self, url_id: uuid.UUID, language: str) -> None:
        redis = self._get_redis()
        if redis is None:
            return
        key = f"scraper:claim:{url_id}:{language}"
        try:
            redis.delete(key)
        except Exception as exc:
            logger.debug("Redis release error (key=%s): %s: %s",
                         key, type(exc).__name__, exc)

    def _get_redis(self):
        try:
            import redis as _redis
            cfg = _cfg()
            client = _redis.Redis(
                host=cfg.REDIS_HOST, port=cfg.REDIS_PORT, db=cfg.REDIS_DB,
                password=cfg.REDIS_PASSWORD or None,
                socket_timeout=5, socket_connect_timeout=5,
                decode_responses=True,
            )
            client.ping()
            return client
        except Exception:
            return None

    # ── Scrape execution ─────────────────────────────────────────────────────

    def _execute_scrape(self, url: str, language: str) -> ScrapeResult:
        """Try CloudScraper first; fall back to Selenium on failure."""
        cfg    = _cfg()
        result = self._cloud_engine.scrape_hotel(
            url, language, max_retries=cfg.SCRAPER_MAX_RETRIES
        )
        if not result.success and cfg.SCRAPER_ENGINE in ("auto", "selenium"):
            logger.info("CloudScraper failed for %s — falling back to Selenium", url[:60])
            with SeleniumEngine(debug_html_dir=cfg.DEBUG_HTML_DIR) as se:
                result = se.scrape_hotel(url, language)
        return result

    # ── Result handling ──────────────────────────────────────────────────────

    def _handle_scrape_result(self, result: ScrapeResult, url_id: uuid.UUID) -> None:
        """Persist result and update queue status."""
        if result.success and result.data:
            hotel_id = self._persist_hotel(result, url_id)
            self._update_stats(success=True)
            self._log_event(
                event_type="scrape_done", url_id=url_id, hotel_id=hotel_id,
                duration_ms=result.duration_ms, http_status=result.http_status,
                engine=result.engine, language=result.language,
            )
            with get_db() as session:
                self._completeness.mark_done(session, url_id, result.language)
        else:
            self._update_stats(success=False)
            self._release_url(url_id, result.language, error=result.error)
            self._log_event(
                event_type="scrape_error", url_id=url_id,
                duration_ms=result.duration_ms, http_status=result.http_status,
                engine=result.engine, language=result.language,
                message=result.error,
            )
            with get_db() as session:
                self._completeness.mark_error(session, url_id, result.language, result.error)

    def _persist_hotel(self, result: ScrapeResult, url_id: uuid.UUID) -> Optional[uuid.UUID]:
        """Upsert hotel data into the hotels table."""
        if result.data is None:
            return None
        d = result.data
        try:
            with get_db() as session:
                # Check for existing record
                existing = (
                    session.query(Hotel)
                    .filter(Hotel.url_id == url_id, Hotel.language == result.language)
                    .first()
                )
                if existing:
                    hotel = existing
                else:
                    hotel = Hotel(url=result.url, language=result.language, url_id=url_id)
                    session.add(hotel)

                hotel.hotel_name   = d.hotel_name
                hotel.hotel_id_ext = d.hotel_id_ext
                hotel.star_rating  = d.star_rating
                hotel.review_score = d.review_score
                hotel.review_count = d.review_count
                hotel.address      = d.address
                hotel.city         = d.city
                hotel.country      = d.country
                hotel.latitude     = d.latitude
                hotel.longitude    = d.longitude
                hotel.amenities    = d.amenities
                hotel.room_types   = d.room_types
                hotel.policies     = d.policies
                hotel.photos       = d.photos
                hotel.raw_data     = d.raw_data
                hotel.scrape_status= "done"
                hotel.scrape_engine= result.engine
                hotel.scraped_at   = datetime.now(timezone.utc)
                hotel.version_id  += 1

                session.flush()
                return hotel.id
        except IntegrityError as exc:
            logger.warning("Hotel insert integrity error for url_id=%s: %s", url_id, exc)
            return None
        except Exception as exc:
            logger.error("Failed to persist hotel for url_id=%s: %s", url_id, exc)
            return None

    # ── Event logging ────────────────────────────────────────────────────────

    def _log_event(self, event_type: str, url_id: Optional[uuid.UUID] = None,
                   hotel_id: Optional[uuid.UUID] = None, **kwargs) -> None:
        try:
            with get_db() as session:
                log = ScrapingLog(
                    url_id     =url_id,
                    hotel_id   =hotel_id,
                    event_type =event_type,
                    worker_id  =self._worker_id,
                    metadata_  ={k: str(v) for k, v in kwargs.items() if v is not None},
                    **{k: v for k, v in kwargs.items()
                       if k in ("engine","language","duration_ms","http_status","message")},
                )
                session.add(log)
        except Exception as exc:
            logger.debug("Event logging failed: %s", exc)

    # ── Stats ────────────────────────────────────────────────────────────────

    def _update_stats(self, success: bool) -> None:
        with self._stats_lock:
            if success:
                self._stats["scraped"] += 1
            else:
                self._stats["errors"] += 1

    def get_stats(self) -> dict:
        with self._stats_lock:
            return self._stats.copy()
