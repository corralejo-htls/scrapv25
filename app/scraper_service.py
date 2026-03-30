# =============================================================================
# app/scraper_service.py — BookingScraper Pro v6.0.0 Build 63-fix
# =============================================================================
# FIX: ImportError — model names corrected to match app/models.py
#
#   WRONG  (Build 63):  from app.models import Hotels, ScrapingLogs
#   CORRECT:            from app.models import Hotel, ScrapingLogs
#
#   Pattern confirmed from schema_v60_complete.sql (source of truth):
#     SQL table       → Python model class
#     hotels          → Hotel           (MODEL-002 comment: "HotelLegal.has_legal_content")
#     hotels_legal    → HotelLegal      (explicit: "MODEL-002: models.py — HotelLegal")
#     hotels_description → HotelDescription
#     hotels_policies    → HotelPolicies
#
#   The documentation incorrectly listed "Hotels" (plural).
#   The actual class follows standard SQLAlchemy singular convention.
#
# All other Build 63 logic (Selenium-only engine, BUG-LANG-001/002 fixes)
# is preserved unchanged.
# =============================================================================

from __future__ import annotations

import logging
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db

# ─── CORRECTED MODEL IMPORTS ──────────────────────────────────────────────────
# Build 63 had:  from app.models import URLQueue, URLLanguageStatus, Hotels, ScrapingLogs
# Correct names derived from schema_v60_complete.sql MODEL-002 annotation:
from app.models import URLQueue, URLLanguageStatus, Hotel, ScrapingLogs
# ─────────────────────────────────────────────────────────────────────────────

from app.scraper import SeleniumEngine, build_language_url
from app.extractor import BookingExtractor
from app.image_downloader import ImageDownloader

logger = logging.getLogger(__name__)


# =============================================================================
# HELPERS
# =============================================================================

def _build_language_list(cfg) -> list[str]:
    """
    Build ordered language list: English always first, remainder as configured.
    """
    raw: list[str] = [
        lang.strip().lower()
        for lang in getattr(cfg, "ENABLED_LANGUAGES", "en,es,de,it,fr,pt").split(",")
        if lang.strip()
    ]
    if "en" in raw:
        raw.remove("en")
    return ["en"] + raw


def _get_vpn_manager(cfg):
    """Return the appropriate VPN manager based on VPN_ENABLED config."""
    if not getattr(cfg, "VPN_ENABLED", False):
        from app.vpn_manager_windows import NullVPNManager
        return NullVPNManager()
    try:
        from app.vpn_manager_windows import NordVPNManager
        return NordVPNManager(cfg)
    except Exception as exc:
        logger.warning(
            "Could not initialise NordVPNManager: %s — using NullVPNManager", exc
        )
        from app.vpn_manager_windows import NullVPNManager
        return NullVPNManager()


# =============================================================================
# ScraperService
# =============================================================================

class ScraperService:
    """
    High-level orchestration for multi-language hotel scraping.

    Build 63: SeleniumEngine is the sole scraping engine.
    Build 63-fix: Model class names corrected (Hotel, not Hotels).
    """

    def __init__(self) -> None:
        self._cfg = get_settings()
        self._selenium_engine = SeleniumEngine()
        self._vpn = _get_vpn_manager(self._cfg)
        # BUG-EXTRACTOR-001 (Build 63-fix):
        #   BookingExtractor (alias of HotelExtractor) is NOT a stateless singleton.
        #   HotelExtractor.__init__ requires 'html' as a positional argument and
        #   parses the page at construction time.  It must be instantiated per
        #   language request inside _scrape_language(), not here.
        self._image_downloader = ImageDownloader()

    # ── Public interface ──────────────────────────────────────────────────────

    def dispatch_batch(self) -> dict:
        """
        Query URL queue for pending URLs and process them in parallel.
        """
        cfg = self._cfg
        max_workers: int = getattr(cfg, "SCRAPER_MAX_WORKERS", 2)

        with get_db() as session:
            pending = (
                session.query(URLQueue)
                .filter(URLQueue.status == "pending")
                .order_by(URLQueue.priority.desc(), URLQueue.created_at.asc())
                .limit(max_workers)
                .all()
            )

        if not pending:
            return {"status": "idle", "pending": 0}

        count = len(pending)
        logger.info("Dispatching %d URL(s) to %d worker(s)", count, max_workers)

        with get_db() as session:
            for url_obj in pending:
                url_obj.status = "processing"
                url_obj.updated_at = _now()
            session.commit()

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {
                pool.submit(self._process_url_safe, url_obj): url_obj
                for url_obj in pending
            }
            for future in as_completed(futures):
                url_obj = futures[future]
                try:
                    future.result()
                except Exception as exc:
                    logger.error(
                        "Unhandled error processing URL %s: %s",
                        url_obj.id, exc, exc_info=True,
                    )

        return {"status": "done", "processed": count}

    def _process_url_safe(self, url_obj: URLQueue) -> None:
        """Wrapper around _process_url() that catches all exceptions."""
        try:
            self._process_url(url_obj)
        except Exception as exc:
            logger.error(
                "Fatal error in _process_url for %s: %s",
                url_obj.id, exc, exc_info=True,
            )
            self._mark_url_error(url_obj, str(exc))

    # ── Per-URL orchestration ─────────────────────────────────────────────────

    def _process_url(self, url_obj: URLQueue) -> None:
        """
        Iterate over all configured languages for a single URL.

        Build 61: Inter-language delay + forced VPN on consecutive failures.
        Build 62: ip_known_blocked flag + reset_browser() after VPN rotation.
        Build 63: Selenium-only (CloudScraper removed).
        """
        cfg = self._cfg
        url_id: str = str(url_obj.id)
        languages: list[str] = _build_language_list(cfg)

        consecutive_failures: int = 0
        max_consec: int = getattr(cfg, "MAX_CONSECUTIVE_LANG_FAILURES", 1)
        ip_known_blocked: bool = False

        completed: list[str] = []
        failed: list[str] = []

        for i, lang in enumerate(languages):

            # ── BUG-LANG-001-FIX-A: Inter-language delay ──────────────────────
            if i > 0:
                base_delay: float = getattr(cfg, "LANG_SCRAPE_DELAY", 10.0)
                jitter: float = random.uniform(
                    0.0, getattr(cfg, "LANG_SCRAPE_JITTER", 5.0)
                )
                total_delay: float = base_delay + jitter
                logger.info(
                    "BUG-LANG-001-FIX: inter-language delay %.1fs "
                    "(base=%.1f jitter=%.1f) before %s/%s",
                    total_delay, base_delay, jitter, url_id, lang,
                )
                time.sleep(total_delay)

            # ── VPN rotation decision (BUG-LANG-001 + BUG-LANG-002) ───────────
            vpn_rotated: bool = False
            should_rotate_now: bool = (
                getattr(cfg, "VPN_ENABLED", False)
                and (ip_known_blocked or consecutive_failures >= max_consec)
            )

            if should_rotate_now:
                reason = (
                    "ip_known_blocked=True"
                    if ip_known_blocked
                    else f"{consecutive_failures} consecutive failures"
                )
                logger.warning(
                    "BUG-LANG-001-FIX: %s for URL %s — "
                    "forcing VPN rotation before %s",
                    reason, url_id, lang,
                )
                try:
                    rotated: bool = self._vpn.rotate(force=True)
                    if rotated:
                        logger.info(
                            "BUG-LANG-001-FIX: VPN rotated (forced) — "
                            "consecutive_failures reset. Continuing with %s/%s",
                            url_id, lang,
                        )
                        consecutive_failures = 0
                        ip_known_blocked = False
                        vpn_rotated = True
                    else:
                        logger.warning(
                            "BUG-LANG-001-FIX: VPN rotation returned False "
                            "for %s/%s", url_id, lang,
                        )
                except Exception as exc:
                    logger.error(
                        "Forced VPN rotation exception for %s/%s: %s",
                        url_id, lang, exc,
                    )

            # ── BUG-LANG-002-FIX: Browser restart after VPN rotation ──────────
            if vpn_rotated and getattr(cfg, "SELENIUM_RESTART_AFTER_VPN_ROTATE", True):
                reset_ok: bool = self._selenium_engine.reset_browser()
                log_fn = logger.info if reset_ok else logger.warning
                log_fn(
                    "BUG-LANG-002-FIX: Selenium browser reset %s after VPN "
                    "rotation for %s/%s",
                    "OK" if reset_ok else "FAILED",
                    url_id, lang,
                )

            # ── Scrape ────────────────────────────────────────────────────────
            ok: bool = self._scrape_language(url_obj, lang)

            if ok:
                completed.append(lang)
                consecutive_failures = 0
                ip_known_blocked = False
                logger.info("URL %s lang=%s: SUCCESS", url_id, lang)
            else:
                failed.append(lang)
                consecutive_failures += 1
                ip_known_blocked = True
                logger.warning("URL %s lang=%s: FAILED", url_id, lang)

        # ── Finalize URL ──────────────────────────────────────────────────────
        total = len(languages)
        success_count = len(completed)

        if success_count == total:
            logger.info(
                "URL %s: COMPLETE (%d/%d) langs=%s",
                url_id, success_count, total, completed,
            )
        elif success_count > 0:
            logger.warning(
                "URL %s: PARTIAL (%d/%d) completed=%s failed=%s",
                url_id, success_count, total, completed, failed,
            )
        else:
            logger.error("URL %s: ALL FAILED (%d/%d)", url_id, success_count, total)

        final_status = "done" if success_count == total else "error"
        self._finalize_url(url_obj, final_status, completed, failed)

    # ── Per-language scraping ─────────────────────────────────────────────────

    def _scrape_language(self, url_obj: URLQueue, lang: str) -> bool:
        """
        Scrape a single language for the given URL.
        Build 63: Selenium only — CloudScraper removed.
        """
        cfg = self._cfg
        url_id: str = str(url_obj.id)
        lang_url: str = build_language_url(
            url_obj.base_url or str(url_obj.url), lang
        )
        start_ts: float = time.monotonic()

        html: Optional[str] = self._selenium_engine.scrape(lang_url, lang)

        # Interval-based VPN rotation on Selenium failure
        if html is None and getattr(cfg, "VPN_ENABLED", False):
            if self._vpn.should_rotate():
                logger.info(
                    "VPN rotating (interval=%ds elapsed) after failure %s/%s",
                    getattr(cfg, "VPN_ROTATION_INTERVAL", 50), url_id, lang,
                )
                try:
                    rotated: bool = self._vpn.rotate()
                    if rotated:
                        logger.info(
                            "VPN rotated — retrying %s/%s with Selenium.", url_id, lang
                        )
                        if getattr(cfg, "SELENIUM_RESTART_AFTER_VPN_ROTATE", True):
                            self._selenium_engine.reset_browser()
                        html = self._selenium_engine.scrape(lang_url, lang)
                except Exception as exc:
                    logger.error("VPN rotation error for %s/%s: %s", url_id, lang, exc)

        duration_ms: int = int((time.monotonic() - start_ts) * 1_000)

        if html is None:
            self._upsert_lang_status(url_obj, lang, "error", "All scraping engines failed")
            self._log_scraping_event(
                url_obj, lang, "scrape_failed", "error",
                duration_ms, "All scraping engines failed",
            )
            return False

        try:
            # BUG-EXTRACTOR-001 (Build 63-fix):
            #   HotelExtractor is a per-page object: html + url + language are
            #   supplied at construction time and the page is parsed immediately.
            #   Correct API: BookingExtractor(html, url, lang).extract_all()
            #   Old call used self._extractor.extract(html, lang) — non-existent
            #   method on a pre-constructed singleton without html (two bugs).
            extractor = BookingExtractor(
                html=html,
                url=lang_url,
                language=lang,
            )
            extracted = extractor.extract_all()
        except Exception as exc:
            logger.error("Extraction failed for %s/%s: %s", url_id, lang, exc, exc_info=True)
            self._upsert_lang_status(url_obj, lang, "error", f"Extraction error: {exc}")
            return False

        if not extracted:
            logger.warning("Extractor returned empty result for %s/%s", url_id, lang)
            self._upsert_lang_status(url_obj, lang, "error", "Extractor returned empty result")
            return False

        try:
            hotel_id = self._persist_hotel_data(url_obj, lang, extracted, duration_ms)
        except Exception as exc:
            logger.error("Persistence failed for %s/%s: %s", url_id, lang, exc, exc_info=True)
            self._upsert_lang_status(url_obj, lang, "error", f"DB write error: {exc}")
            return False

        # Image download — English pass only (photos are language-independent)
        photos = extracted.get("photos", [])
        if photos and hotel_id and lang == "en":
            try:
                saved, total = self._image_downloader.download_photo_batch(hotel_id, photos)
                logger.info(
                    "download_photo_batch: %d/%d photo-files saved for hotel %s",
                    saved, total, hotel_id,
                )
            except Exception as exc:
                logger.warning("Image download failed for hotel %s: %s", hotel_id, exc)

        self._upsert_lang_status(url_obj, lang, "done", None)
        self._log_scraping_event(url_obj, lang, "scrape_success", "done", duration_ms, None)
        return True

    # ── Persistence helpers ───────────────────────────────────────────────────

    def _persist_hotel_data(
        self,
        url_obj: URLQueue,
        lang: str,
        data: dict,
        duration_ms: int,
    ) -> Optional[str]:
        """Upsert hotel data into all relevant tables. Returns hotel UUID."""
        with get_db() as session:
            hotel = self._upsert_hotel(session, url_obj, lang, data, duration_ms)
            hotel_id = str(hotel.id)
            self._upsert_hotel_description(session, url_obj, hotel, lang, data)
            self._upsert_hotel_policies(session, url_obj, hotel, lang, data)
            self._upsert_hotel_legal(session, url_obj, hotel, lang, data)
            session.commit()
            return hotel_id

    def _upsert_hotel(
        self,
        session: Session,
        url_obj: URLQueue,
        lang: str,
        data: dict,
        duration_ms: int,
    ) -> Hotel:
        """Insert or update the main Hotel row for this URL+language."""
        existing = (
            session.query(Hotel)
            .filter_by(url_id=url_obj.id, language=lang)
            .first()
        )
        now = _now()

        fields = {
            "url_id":            url_obj.id,
            "url":               build_language_url(str(url_obj.base_url or url_obj.url), lang),
            "language":          lang,
            "hotel_name":        data.get("hotel_name"),
            "hotel_id_booking":  data.get("hotel_id_booking"),
            "address_city":      data.get("address_city"),
            "latitude":          data.get("latitude"),
            "longitude":         data.get("longitude"),
            "star_rating":       data.get("star_rating"),
            "review_score":      data.get("review_score"),
            "review_count":      data.get("review_count"),
            "main_image_url":    data.get("main_image_url"),
            "short_description": data.get("short_description"),
            "rating_value":      data.get("rating_value"),
            "best_rating":       data.get("best_rating"),
            "street_address":    data.get("street_address"),
            "address_locality":  data.get("address_locality"),
            "address_country":   data.get("address_country"),
            "postal_code":       data.get("postal_code"),
            "room_types":        data.get("room_types"),
            "raw_data":          data.get("raw_data"),
            "scrape_duration_s": duration_ms / 1_000,
            "scrape_engine":     "selenium",   # Build 63: always selenium
            "updated_at":        now,
        }

        if existing:
            for k, v in fields.items():
                setattr(existing, k, v)
            return existing

        hotel = Hotel(**fields, created_at=now)
        session.add(hotel)
        session.flush()
        return hotel

    def _upsert_hotel_description(
        self,
        session: Session,
        url_obj: URLQueue,
        hotel: Hotel,
        lang: str,
        data: dict,
    ) -> None:
        """Upsert HotelDescription row."""
        from app.models import HotelDescription
        desc_text = data.get("description")
        existing = (
            session.query(HotelDescription)
            .filter_by(url_id=url_obj.id, language=lang)
            .first()
        )
        now = _now()
        if existing:
            existing.description = desc_text
            existing.updated_at = now
        else:
            session.add(
                HotelDescription(
                    hotel_id=hotel.id,
                    url_id=url_obj.id,
                    language=lang,
                    description=desc_text,
                    created_at=now,
                )
            )

    def _upsert_hotel_policies(
        self,
        session: Session,
        url_obj: URLQueue,
        hotel: Hotel,
        lang: str,
        data: dict,
    ) -> None:
        """Upsert HotelPolicies rows."""
        from app.models import HotelPolicies
        policies: list[dict] = data.get("policies", [])
        for policy in policies:
            policy_name = policy.get("policy_name") or policy.get("name")
            if not policy_name:
                continue
            existing = (
                session.query(HotelPolicies)
                .filter_by(hotel_id=hotel.id, language=lang, policy_name=policy_name)
                .first()
            )
            now = _now()
            if existing:
                existing.policy_details = policy.get("policy_details") or policy.get("details")
            else:
                session.add(
                    HotelPolicies(
                        hotel_id=hotel.id,
                        url_id=url_obj.id,
                        language=lang,
                        policy_name=policy_name,
                        policy_details=policy.get("policy_details") or policy.get("details"),
                        created_at=now,
                    )
                )

    def _upsert_hotel_legal(
        self,
        session: Session,
        url_obj: URLQueue,
        hotel: Hotel,
        lang: str,
        data: dict,
    ) -> None:
        """
        Upsert HotelLegal row.

        BUG-DB-002-FIX (v60): Always insert 1 row per hotel/language.
        has_legal_content=True if legal block was found, False if absent.
        """
        from app.models import HotelLegal
        legal_data = data.get("legal") or {}
        has_content = bool(legal_data)

        existing = (
            session.query(HotelLegal)
            .filter_by(hotel_id=hotel.id, language=lang)
            .first()
        )
        now = _now()
        if existing:
            existing.legal             = legal_data.get("legal")
            existing.legal_info        = legal_data.get("legal_info")
            existing.legal_details     = legal_data.get("legal_details")
            existing.has_legal_content = has_content
        else:
            session.add(
                HotelLegal(
                    hotel_id=hotel.id,
                    url_id=url_obj.id,
                    language=lang,
                    legal=legal_data.get("legal"),
                    legal_info=legal_data.get("legal_info"),
                    legal_details=legal_data.get("legal_details"),
                    has_legal_content=has_content,
                    created_at=now,
                )
            )

    # ── Status / logging helpers ──────────────────────────────────────────────

    def _upsert_lang_status(
        self,
        url_obj: URLQueue,
        lang: str,
        status: str,
        error: Optional[str],
    ) -> None:
        """Update URLLanguageStatus for this URL+language combination."""
        with get_db() as session:
            existing = (
                session.query(URLLanguageStatus)
                .filter_by(url_id=url_obj.id, language=lang)
                .first()
            )
            now = _now()
            if existing:
                existing.status     = status
                existing.last_error = (error[:2000] if error else None)
                existing.attempts   = (existing.attempts or 0) + 1
                existing.updated_at = now
            else:
                session.add(
                    URLLanguageStatus(
                        url_id=url_obj.id,
                        language=lang,
                        status=status,
                        last_error=(error[:2000] if error else None),
                        attempts=1,
                        created_at=now,
                        updated_at=now,
                    )
                )
            session.commit()

    def _log_scraping_event(
        self,
        url_obj: URLQueue,
        lang: str,
        event_type: str,
        status: str,
        duration_ms: int,
        error_message: Optional[str] = None,
    ) -> None:
        """Insert a ScrapingLogs record."""
        try:
            import uuid as _uuid
            with get_db() as session:
                session.add(
                    ScrapingLogs(
                        id=_uuid.uuid4(),
                        url_id=url_obj.id,
                        language=lang,
                        event_type=event_type,
                        status=status,
                        duration_ms=duration_ms,
                        error_message=(error_message[:2000] if error_message else None),
                        scraped_at=_now(),
                    )
                )
                session.commit()
        except Exception as exc:
            logger.warning("Failed to log scraping event: %s", exc)

    def _finalize_url(
        self,
        url_obj: URLQueue,
        status: str,
        completed: list[str],
        failed: list[str],
    ) -> None:
        """Write final status and language lists to url_queue."""
        with get_db() as session:
            db_obj = session.get(URLQueue, url_obj.id)
            if db_obj:
                db_obj.status              = status
                db_obj.languages_completed = ",".join(completed) if completed else ""
                db_obj.languages_failed    = ",".join(failed)    if failed    else ""
                db_obj.scraped_at          = _now()
                db_obj.updated_at          = _now()
                if failed:
                    db_obj.last_error = (
                        f"Incomplete: {len(completed)}/{len(completed)+len(failed)} "
                        f"languages. OK={completed} FAILED={failed}"
                    )[:2000]
                session.commit()

    def _mark_url_error(self, url_obj: URLQueue, error: str) -> None:
        """Mark a URL as errored due to a fatal exception."""
        with get_db() as session:
            db_obj = session.get(URLQueue, url_obj.id)
            if db_obj:
                db_obj.status     = "error"
                db_obj.last_error = error[:2000]
                db_obj.updated_at = _now()
                session.commit()

    def _count_successful_languages(self, session: Session, url_id) -> int:
        """Count distinct languages in the hotels table for this URL."""
        from sqlalchemy import func
        result = (
            session.query(func.count(Hotel.language.distinct()))
            .filter(Hotel.url_id == url_id)
            .scalar()
        )
        return result or 0


# =============================================================================
# UTILITIES
# =============================================================================

def _now():
    """Return current UTC datetime."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc)
