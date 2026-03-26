"""
scraper_service.py — BookingScraper Pro v6.0.0 build 58
========================================================
Cambios v58 — STRATEGY-E (Enhanced State with Conditional Commit):

  BUG-INTEGRITY-001: _process_url() corregido — all_ok=True hardcodeado reemplazado
                     por lógica condicional completa (Strategy E).
                     ANTES: self._mark_done(url_obj, all_ok=True)  ← siempre 'done'
                     AHORA: lógica de 3 casos según conteo real de idiomas en DB.
                     Ref: Strategy_E_Implementation_Guide_EN.md

  STRATEGY-E-001   : _count_successful_languages() nueva — fuente de verdad en DB.
                     COUNT(*) FROM hotels WHERE url_id = X.

  STRATEGY-E-002   : _mark_incomplete() nueva — marca URL como 'error' PRESERVANDO
                     los datos de idiomas exitosos. Habilita partial retry.

  STRATEGY-E-003   : _cleanup_empty_url() nueva — limpia datos solo en fallo total
                     (0 idiomas exitosos). Borra hotels + tablas relacionadas.

  STRATEGY-E-004   : languages_completed / languages_failed actualizados en
                     url_queue para diagnóstico rápido sin JOIN.

  MODEL-001        : URLQueue.languages_completed y languages_failed añadidos
                     (String(64), nullable, default='').

  SCHEMA-001       : url_queue.status CHECK constraint ampliado con 'incomplete'.
                     url_queue añade columnas languages_completed, languages_failed.

Cambios v55:

  BUG-LANG-001 : _process_url() corregido — 'en' siempre se procesa primero.
                 Si 'en' no está en ENABLED_LANGUAGES, se añade automáticamente.
                 El orden de procesamiento garantiza que 'en' es el primer idioma
                 sin importar la configuración del usuario en .env.

  BUG-IMG-UNPACK: _download_images() corregido — download_photo_batch() retorna
                  Dict[str, int], no tuple(int, int). La asignación ahora usa
                  sum(results.values()) para obtener el total descargado.

Cambios v53:

  STRUCT-013 : _upsert_fine_print() nueva — persiste el HTML sanitizado del
               bloque Fine Print en hotels_fine_print.
               Estrategia upsert (UniqueConstraint url_id+language).
               'fine_print' extraído de hotel_data via pop() antes del upsert principal.

  STRUCT-014 : _upsert_all_services() nueva — persiste todos los servicios
               en hotels_all_services. Delete-then-insert por (hotel_id, language).
               'all_services' extraído de hotel_data via pop() antes del upsert.

  STRUCT-015 : _upsert_faqs() nueva — persiste preguntas frecuentes en
               hotels_faqs. Delete-then-insert por (hotel_id, language).
               'faqs' extraído de hotel_data via pop() antes del upsert.
               BUG-FAQ-ANSWERS (v56): acepta List[Dict] con ask + answer.

  STRUCT-016 : _upsert_guest_reviews() nueva — persiste categorías de reseñas
               de huéspedes en hotels_guest_reviews.
               Delete-then-insert por (hotel_id, language).
               'guest_reviews' extraído de hotel_data via pop() antes del upsert.

  STRUCT-017 : _upsert_property_highlights() nueva — persiste el HTML sanitizado
               del bloque Property Highlights en hotels_property_highlights.
               Estrategia upsert (UniqueConstraint url_id+language).
               'property_highlights' extraído de hotel_data via pop() antes del upsert.

  FLOW-002   : _scrape_language() hace pop de 'fine_print', 'all_services',
               'faqs', 'guest_reviews' y 'property_highlights' de hotel_data
               ANTES del upsert de hotels, garantizando que estos campos nunca
               se escriben en la tabla hotels.

Cambios v51:

  STRUCT-005 : _upsert_amenities() nueva — persiste lista de amenidades en
               hotels_amenities (una fila por amenidad). Delete-then-insert por
               (hotel_id, language) para garantizar sincronización con el HTML actual.
               'amenities' extraído de hotel_data via pop() antes del upsert principal.

  STRUCT-006 : _upsert_policies() nueva — persiste lista de políticas en
               hotels_policies. Delete-then-insert por (hotel_id, language).
               'policies' extraído de hotel_data via pop() antes del upsert principal.

  STRUCT-007 : _upsert_legal() nueva — persiste información legal en hotels_legal
               con estrategia upsert (UniqueConstraint hotel_id+language).
               'legal' extraído de hotel_data via pop() antes del upsert principal.

  STRUCT-008 : _upsert_popular_services() nueva — persiste servicios populares
               en hotels_popular_services. Delete-then-insert por (hotel_id, language).
               'popular_services' extraído de hotel_data via pop() antes del upsert.

  FLOW-001   : scrape_url_for_language() hace pop de 'amenities', 'popular_services',
               'policies' y 'legal' de hotel_data ANTES del upsert de hotels,
               garantizando que estos campos nunca se escriben en la tabla hotels.

Fixes v50:
  STRUCT-001 : _upsert_description() — hotels_description.
  STRUCT-002 : photos eliminados de hotels.
  STRUCT-003 : review_count mapeado desde JSON-LD.

Platform: Windows 11 / ThreadPoolExecutor (not ProcessPoolExecutor).
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

from sqlalchemy import func
from app.config import get_settings
from app.database import get_db
from app.extractor import HotelExtractor, detect_language
from app.models import (
    Hotel, HotelAllService, HotelAmenity, HotelDescription, HotelFAQ,
    HotelFinePrint, HotelGuestReview, HotelLegal, HotelPolicy,
    HotelPopularService, HotelPropertyHighlights, ScrapingLog,
    URLLanguageStatus, URLQueue,
)
from app.scraper import CloudScraperEngine, SeleniumEngine, build_language_url
from app.vpn_manager_windows import get_vpn_manager

try:
    from app.image_downloader import ImageDownloader as _ImageDownloader
except ImportError:
    _ImageDownloader = None  # type: ignore[assignment,misc]

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level VPN manager (singleton — initialised once per worker process)
# ---------------------------------------------------------------------------
_vpn_manager = None
_vpn_manager_lock = threading.Lock()


def _get_vpn():
    """Return (or create) the module-level VPN manager."""
    global _vpn_manager
    if _vpn_manager is None:
        with _vpn_manager_lock:
            if _vpn_manager is None:
                _vpn_manager = get_vpn_manager()
    return _vpn_manager


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
            if _redis_pool is None:
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
    return True


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
        self._vpn = _get_vpn()
        logger.info(
            "ScraperService INIT | VPN_ENABLED=%s | HEADLESS_BROWSER=%s | "
            "workers=%d | languages=%s | vpn_interval=%ds | vpn_countries=%s",
            self._cfg.VPN_ENABLED,
            self._cfg.HEADLESS_BROWSER,
            self._cfg.SCRAPER_MAX_WORKERS,
            ",".join(self._cfg.ENABLED_LANGUAGES),
            self._cfg.VPN_ROTATION_INTERVAL,
            ",".join(self._cfg.VPN_COUNTRIES) if self._cfg.VPN_ENABLED else "N/A",
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def dispatch_batch(
        self,
        url_ids: Optional[List[str]] = None,
        max_workers: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Dispatch a batch of scraping jobs.
        SCRAP-BUG-016: max_workers clamped to config maximum at runtime.
        VPN-FIX-001:   connect VPN before batch; rotate on block detection.
        """
        workers = self._resolve_workers(max_workers)
        urls = self._fetch_pending_urls(url_ids)

        if not urls:
            return {"status": "no_work", "queued": 0}

        if self._cfg.VPN_ENABLED:
            try:
                connected = self._vpn.connect()
                if connected:
                    logger.info("VPN connected OK before batch start.")
                else:
                    logger.warning("VPN connect returned False — proceeding without VPN.")
            except Exception as vpn_exc:
                logger.warning("VPN connect error: %s — proceeding without VPN.", vpn_exc)

        logger.info("Dispatching batch: urls=%d workers=%d", len(urls), workers)

        try:
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {
                    executor.submit(self._process_url, url_obj): url_obj
                    for url_obj in urls
                }
                for future in as_completed(futures, timeout=None):
                    url_obj = futures[future]
                    try:
                        future.result()
                    except Exception as exc:
                        logger.error("URL %s raised exception: [%s] %s", url_obj.id, type(exc).__name__, exc)
                        self._mark_error(url_obj, str(exc)[:2000])
                        self._stats.record(failed=True)
        finally:
            try:
                self._selenium_engine.close()
                logger.info("Selenium browser closed after batch completion.")
            except Exception as close_exc:
                logger.warning("Selenium close error (non-critical): %s", close_exc)

        result = self._stats.to_dict()
        result["status"] = "complete"
        return result

    # ── Private helpers ───────────────────────────────────────────────────────

    def _resolve_workers(self, requested: Optional[int]) -> int:
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
        with get_db() as session:
            q = session.query(URLQueue).filter(URLQueue.status == "pending")
            if url_ids:
                try:
                    uuids = [uuid.UUID(uid) for uid in url_ids]
                    q = q.filter(URLQueue.id.in_(uuids))
                except ValueError as exc:
                    logger.warning("Invalid UUID in url_ids: %s", exc)
            rows = q.order_by(URLQueue.priority.desc(), URLQueue.created_at).limit(200).all()
            session.expunge_all()
            return rows

    def _process_url(self, url_obj: URLQueue) -> None:
        """
        Process a single URL through all enabled languages.

        STRATEGY E — Build 58: Enhanced State with Conditional Commit.
        BUG-INTEGRITY-001: all_ok=True hardcoded replaced with real validation.

        Decision tree (3 cases):
          Case 1: actual_count == expected  → mark 'done'        (full success)
          Case 2: actual_count > 0          → mark 'error'       (partial — data PRESERVED)
          Case 3: actual_count == 0         → cleanup + 'error'  (total failure)
        """
        url_id_str = str(url_obj.id)

        if not _try_claim_url(url_id_str):
            logger.debug("URL %s already claimed, skipping.", url_id_str)
            self._stats.record(skipped=True)
            return

        try:
            self._mark_processing(url_obj)

            # BUG-LANG-001 (v55): 'en' always first.
            languages = list(self._cfg.ENABLED_LANGUAGES)
            if 'en' in languages:
                languages.remove('en')
            languages.insert(0, 'en')

            expected_count = len(languages)
            lang_results: Dict[str, bool] = {}

            for lang in languages:
                try:
                    ok = self._scrape_language(url_obj, lang)
                    lang_results[lang] = ok
                    if ok:
                        logger.info("URL %s lang=%s: SUCCESS", url_id_str, lang)
                    else:
                        logger.warning("URL %s lang=%s: FAILED", url_id_str, lang)
                except Exception as lang_exc:
                    logger.error(
                        "URL %s lang=%s: EXCEPTION [%s] %s",
                        url_id_str, lang, type(lang_exc).__name__, lang_exc,
                    )
                    lang_results[lang] = False

            # Source of truth: count records committed to DB
            actual_count = self._count_successful_languages(url_obj.id)
            success_langs = [lg for lg, ok in lang_results.items() if ok]
            failed_langs  = [lg for lg, ok in lang_results.items() if not ok]

            if actual_count == expected_count:
                # ── Case 1: Complete success ─────────────────────────────────
                logger.info(
                    "URL %s: COMPLETE (%d/%d) langs=%s",
                    url_id_str, actual_count, expected_count, success_langs,
                )
                self._mark_done(url_obj, all_ok=True,
                                success_langs=success_langs, failed_langs=[])
                self._stats.record(succeeded=True)

            elif actual_count > 0:
                # ── Case 2: Partial success — PRESERVE data for partial retry ─
                error_msg = (
                    f"Incomplete: {actual_count}/{expected_count} languages. "
                    f"OK={success_langs} FAILED={failed_langs}"
                )
                logger.warning("URL %s: PARTIAL — %s", url_id_str, error_msg)
                self._mark_incomplete(url_obj, error_msg,
                                      success_langs=success_langs,
                                      failed_langs=failed_langs)
                self._stats.record(failed=True)

            else:
                # ── Case 3: Total failure — cleanup empty records ─────────────
                error_msg = f"All languages failed: {failed_langs}"
                logger.error("URL %s: TOTAL FAILURE — %s", url_id_str, error_msg)
                self._cleanup_empty_url(url_obj.id)
                self._mark_error(url_obj, error_msg)
                self._stats.record(failed=True)

        except Exception as exc:
            logger.error(
                "_process_url failed for %s: [%s] %s",
                url_id_str, type(exc).__name__, exc,
            )
            self._mark_error(url_obj, str(exc)[:2000])
            self._stats.record(failed=True)
        finally:
            _release_url(url_id_str)

    # ── Strategy E helpers ────────────────────────────────────────────────────

    def _count_successful_languages(self, url_id: uuid.UUID) -> int:
        """
        Count language records committed to the hotels table for this URL.
        STRATEGY-E-001: hotels table is the source of truth for success.

        Args:
            url_id: UUID of the url_queue row.
        Returns:
            int — number of distinct language rows in hotels (0..N).
        """
        try:
            with get_db() as session:
                count = (
                    session.query(func.count(Hotel.id))
                    .filter(Hotel.url_id == url_id)
                    .scalar()
                )
                return int(count or 0)
        except Exception as exc:
            logger.error(
                "_count_successful_languages failed for %s: [%s] %s",
                url_id, type(exc).__name__, exc,
            )
            return 0

    def _mark_incomplete(
        self,
        url_obj: URLQueue,
        error_msg: str,
        success_langs: Optional[List[str]] = None,
        failed_langs: Optional[List[str]] = None,
    ) -> None:
        """
        Mark URL as 'error' while PRESERVING partial scraping data.
        STRATEGY-E-002: data is NEVER deleted on partial failure.
        Updates languages_completed and languages_failed for fast diagnostics.

        Args:
            url_obj: URLQueue row to update.
            error_msg: Human-readable summary of what failed.
            success_langs: List of successfully scraped language codes.
            failed_langs: List of failed language codes.
        """
        try:
            with get_db() as session:
                row = session.get(URLQueue, url_obj.id)
                if row:
                    row.status = "error"
                    row.last_error = error_msg[:2000]
                    row.languages_completed = ",".join(success_langs or [])
                    row.languages_failed    = ",".join(failed_langs or [])
                    row.retry_count += 1
                    row.updated_at = datetime.now(timezone.utc)
                    # Keep scraped_at to indicate partial progress was made
                    if not row.scraped_at:
                        row.scraped_at = datetime.now(timezone.utc)
                    session.commit()
            logger.info(
                "URL %s marked incomplete — data PRESERVED. ok=%s fail=%s",
                url_obj.id, success_langs, failed_langs,
            )
        except Exception as exc:
            logger.error(
                "_mark_incomplete failed for %s: [%s] %s",
                url_obj.id, type(exc).__name__, exc,
            )

    def _cleanup_empty_url(self, url_id: uuid.UUID) -> None:
        """
        Delete all scraping artefacts for a URL that has ZERO successful languages.
        STRATEGY-E-003: called ONLY when actual_count == 0 (total failure).
        Safe to call — idempotent, uses DELETE WHERE.

        Args:
            url_id: UUID of the failed URL.
        """
        from app.models import (
            HotelDescription, HotelAmenity, HotelPolicy, HotelLegal,
            HotelPopularService, HotelFinePrint, HotelAllService,
            HotelFAQ, HotelGuestReview, HotelPropertyHighlights,
        )
        satellite_models = [
            HotelDescription, HotelAmenity, HotelPolicy, HotelLegal,
            HotelPopularService, HotelFinePrint, HotelAllService,
            HotelFAQ, HotelGuestReview, HotelPropertyHighlights,
        ]
        try:
            with get_db() as session:
                for model in satellite_models:
                    n = (
                        session.query(model)
                        .filter(model.url_id == url_id)
                        .delete(synchronize_session=False)
                    )
                    if n:
                        logger.debug("Cleanup %s: %d rows removed for url_id=%s",
                                     model.__tablename__, n, url_id)
                n_hotels = (
                    session.query(Hotel)
                    .filter(Hotel.url_id == url_id)
                    .delete(synchronize_session=False)
                )
                n_uls = (
                    session.query(URLLanguageStatus)
                    .filter(URLLanguageStatus.url_id == url_id)
                    .delete(synchronize_session=False)
                )
                session.commit()
            logger.info(
                "Cleanup complete for url_id=%s: hotels=%d uls=%d",
                url_id, n_hotels, n_uls,
            )
        except Exception as exc:
            logger.error(
                "_cleanup_empty_url failed for %s: [%s] %s",
                url_id, type(exc).__name__, exc,
            )

    def _scrape_language(self, url_obj: URLQueue, lang: str) -> bool:
        """
        Scrape one language variant of a hotel URL. Returns True on success.

        v50 changes:
          STRUCT-001: description extraída de hotel_data y guardada en
                      hotels_description via _upsert_description().
          STRUCT-002: hotel_data["photos"] ya NO se asigna. Las fotos se
                      gestionan exclusivamente por image_downloads.

        Photo download strategy (NEW-PHOTOS-001, v49):
          1. download_photo_batch() — hotelPhotos JS metadata (en only, preferred).
          2. download_batch()       — URL-only list fallback.

        VPN-FIX-001: rotación de VPN cuando todos los engines fallan.
        BUG-IMG-401: gallery_urls contienen URLs completas con k= auth params.
        """
        lang_url = build_language_url(url_obj.base_url or url_obj.url, lang)
        start_ts = time.monotonic()

        html = self._cloud_engine.scrape(lang_url, retries=self._cfg.MAX_LANG_RETRIES)

        if html is None:
            logger.info("CloudScraper failed for %s/%s — trying Selenium.", url_obj.id, lang)
            html = self._selenium_engine.scrape(lang_url, lang)

        # ── VPN: rotate on block detection and retry once ─────────────────────
        if html is None and self._cfg.VPN_ENABLED:
            try:
                if self._vpn.should_rotate():
                    logger.info(
                        "VPN rotating (interval=%ds elapsed) after failure %s/%s",
                        self._cfg.VPN_ROTATION_INTERVAL, url_obj.id, lang,
                    )
                    rotated = self._vpn.rotate()
                    if rotated:
                        logger.info("VPN rotated — retrying %s/%s with CloudScraper.", url_obj.id, lang)
                        html = self._cloud_engine.scrape(lang_url, retries=1)
                        if html is None:
                            logger.info("CloudScraper still blocked — retrying Selenium after VPN rotate.")
                            html = self._selenium_engine.scrape(lang_url, lang)
                    else:
                        logger.warning("VPN rotation failed for %s/%s", url_obj.id, lang)
                else:
                    elapsed = int(time.monotonic() - self._vpn._last_rotation) if hasattr(self._vpn, '_last_rotation') else 0
                    logger.debug("VPN rotate skipped — %ds elapsed of %ds interval",
                                 elapsed, self._cfg.VPN_ROTATION_INTERVAL)
            except Exception as vpn_exc:
                logger.warning("VPN rotate error for %s/%s: %s", url_obj.id, lang, vpn_exc)

        duration_ms = int((time.monotonic() - start_ts) * 1000)

        if html is None:
            self._log_scraping_event(url_obj, lang, "scrape_failed", "error", duration_ms)
            self._upsert_lang_status(url_obj, lang, "error", "All scraping engines failed")
            return False

        # Extract hotel data
        extractor = HotelExtractor(html, url=lang_url, language=lang)
        hotel_data = extractor.extract_all()

        # STRUCT-001: Separar description de hotel_data antes del upsert de hotels.
        description = hotel_data.pop("description", None)

        # STRUCT-005: Separar amenities — van a hotels_amenities, NO a hotels
        amenities: List[str] = hotel_data.pop("amenities", None) or []

        # STRUCT-008: Separar popular_services — van a hotels_popular_services
        popular_services: List[str] = hotel_data.pop("popular_services", None) or []

        # STRUCT-006: Separar policies — van a hotels_policies, NO a hotels
        policies: List[Dict[str, Any]] = hotel_data.pop("policies", None) or []

        # STRUCT-007: Separar legal — va a hotels_legal, NO a hotels
        legal: Optional[Dict[str, Any]] = hotel_data.pop("legal", None)

        # STRUCT-013 (v53): Separar fine_print — va a hotels_fine_print, NO a hotels
        fine_print: Optional[str] = hotel_data.pop("fine_print", None)

        # STRUCT-014 (v53): Separar all_services — van a hotels_all_services, NO a hotels
        all_services: List[str] = hotel_data.pop("all_services", None) or []

        # STRUCT-015 (v53): Separar faqs — van a hotels_faqs, NO a hotels
        faqs: List[str] = hotel_data.pop("faqs", None) or []

        # STRUCT-016 (v53): Separar guest_reviews — van a hotels_guest_reviews, NO a hotels
        guest_reviews: List[Dict[str, Any]] = hotel_data.pop("guest_reviews", None) or []

        # STRUCT-017 (v53): Separar property_highlights — va a hotels_property_highlights
        property_highlights: Optional[str] = hotel_data.pop("property_highlights", None)

        # ── Photo data collection (English only) ──────────────────────────────
        # Imágenes son language-independent — se recolectan una sola vez en 'en'.
        # STRUCT-002: hotel_data["photos"] ya NO se asigna — image_downloads es
        # la fuente única de verdad para fotos.
        gallery_photos: List[Dict] = []
        gallery_urls: List[str] = []

        if lang == "en":
            if hasattr(self._selenium_engine, "_last_gallery_photos"):
                gallery_photos = self._selenium_engine._last_gallery_photos or []

            if hasattr(self._selenium_engine, "_last_gallery_urls"):
                gallery_urls = self._selenium_engine._last_gallery_urls or []

            if gallery_photos:
                logger.info(
                    "Photos: %d rich photo records (hotelPhotos JS) for %s",
                    len(gallery_photos), url_obj.id,
                )
            elif gallery_urls:
                logger.info(
                    "Photos: %d URL-only records (DOM fallback) for %s",
                    len(gallery_urls), url_obj.id,
                )
            else:
                logger.debug("Photos: no gallery data collected for %s", url_obj.id)

            # STRUCT-002: NO asignar hotel_data["photos"] — eliminado.
            # La información de fotos se persiste solo en image_downloads/image_data.

        # Persist hotel record (sin description, sin photos, sin amenities, sin policies)
        try:
            self._upsert_hotel(url_obj, lang, hotel_data, duration_ms)

            # STRUCT-001: Persistir description en hotels_description
            if description:
                self._upsert_description(url_obj, lang, description)

            # STRUCT-005: Persistir amenidades normalizadas en hotels_amenities
            if amenities:
                self._upsert_amenities(url_obj, lang, amenities)

            # STRUCT-008: Persistir servicios populares en hotels_popular_services
            if popular_services:
                self._upsert_popular_services(url_obj, lang, popular_services)

            # STRUCT-006: Persistir políticas en hotels_policies
            if policies:
                self._upsert_policies(url_obj, lang, policies)

            # STRUCT-007: Persistir información legal en hotels_legal
            if legal:
                self._upsert_legal(url_obj, lang, legal)

            # STRUCT-013 (v53): Persistir Fine Print HTML en hotels_fine_print
            if fine_print:
                self._upsert_fine_print(url_obj, lang, fine_print)

            # STRUCT-014 (v53): Persistir todos los servicios en hotels_all_services
            if all_services:
                self._upsert_all_services(url_obj, lang, all_services)

            # STRUCT-015 (v53): Persistir FAQs en hotels_faqs
            if faqs:
                self._upsert_faqs(url_obj, lang, faqs)

            # STRUCT-016 (v53): Persistir reseñas de huéspedes en hotels_guest_reviews
            if guest_reviews:
                self._upsert_guest_reviews(url_obj, lang, guest_reviews)

            # STRUCT-017 (v53): Persistir Property Highlights HTML en hotels_property_highlights
            if property_highlights:
                self._upsert_property_highlights(url_obj, lang, property_highlights)

            self._log_scraping_event(url_obj, lang, "scrape_success", "done", duration_ms)
            self._upsert_lang_status(url_obj, lang, "done", None)

            # ── Image download (English only, after hotel row is committed) ───
            if lang == "en" and _ImageDownloader is not None:
                has_photos = bool(gallery_photos or gallery_urls)
                if has_photos:
                    self._download_images(url_obj, lang, gallery_photos, gallery_urls)

            return True

        except Exception as exc:
            logger.error("Hotel upsert failed for %s/%s: %s", url_obj.id, lang, exc)
            self._log_scraping_event(url_obj, lang, "upsert_failed", "error", duration_ms, str(exc))
            self._upsert_lang_status(url_obj, lang, "error", str(exc)[:2000])
            return False

    def _download_images(
        self,
        url_obj: URLQueue,
        lang: str,
        gallery_photos: List[Dict],
        gallery_urls: List[str],
    ) -> None:
        """
        Download hotel images using ImageDownloader.

        Strategy:
          - download_photo_batch() when gallery_photos (hotelPhotos JS metadata).
            Persists image_data rows + image_downloads with id_photo and category.
          - download_batch() when only gallery_urls (URL-only list fallback).
        """
        try:
            with get_db() as session:
                hotel = (
                    session.query(Hotel)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if not hotel:
                    logger.warning("Hotel not found for image download: %s/%s", url_obj.id, lang)
                    return
                hotel_uuid = hotel.id

            downloader = _ImageDownloader()

            if gallery_photos:
                try:
                    # BUG-IMG-UNPACK (v55): download_photo_batch() returns
                    # Dict[str, int] (id_photo → download_count), NOT a tuple.
                    # Previous code "downloaded, total = ..." caused ValueError.
                    results = downloader.download_photo_batch(
                        hotel_id=hotel_uuid,
                        photos=gallery_photos,
                    )
                    downloaded = sum(results.values()) if isinstance(results, dict) else 0
                    logger.info(
                        "ImageDownloader (photo_batch): %d/%d photos saved for hotel %s",
                        downloaded, len(gallery_photos), hotel_uuid,
                    )
                except AttributeError:
                    logger.warning(
                        "ImageDownloader.download_photo_batch not available — "
                        "extracting URLs from gallery_photos as fallback"
                    )
                    gallery_urls = gallery_urls or [
                        p.get("highres_url") or p.get("large_url") or p.get("thumb_url", "")
                        for p in gallery_photos
                        if p.get("highres_url") or p.get("large_url") or p.get("thumb_url")
                    ]

            if not gallery_photos and gallery_urls:
                results = downloader.download_batch(
                    hotel_id=hotel_uuid,
                    image_urls=gallery_urls,
                )
                downloaded = sum(1 for ok in results.values() if ok)
                logger.info(
                    "ImageDownloader (url_batch): %d/%d images saved for hotel %s",
                    downloaded, len(gallery_urls), hotel_uuid,
                )

        except Exception as img_exc:
            logger.warning("ImageDownloader failed for %s: %s", url_obj.id, img_exc)

    def _upsert_hotel(
        self,
        url_obj: URLQueue,
        lang: str,
        data: Dict[str, Any],
        duration_ms: int,
    ) -> None:
        """
        Persiste / actualiza el registro Hotel.

        STRUCT-001: 'description' ya fue extraído de data antes de llamar aquí.
        STRUCT-002: 'photos' ya no está en data.
        BUG-HOTEL-UPSERT: _EXPLICIT_KEYS evita TypeError por kwargs duplicados.
        """
        _EXPLICIT_KEYS = {
            "language", "url_id", "scrape_duration_s", "scrape_engine",
            "version_id", "created_at", "updated_at", "id",
            # STRUCT-001/002: nunca escribir estos campos en hotels
            "description", "photos",
            # STRUCT-005/006/007/008: gestionados en tablas independientes
            "amenities", "policies", "legal", "popular_services",
            # STRUCT-013/014/015/016/017 (v53): gestionados en tablas independientes
            "fine_print", "all_services", "faqs", "guest_reviews", "property_highlights",
        }
        with get_db() as session:
            existing = (
                session.query(Hotel)
                .filter_by(url_id=url_obj.id, language=lang)
                .first()
            )
            if existing:
                for k, v in data.items():
                    if hasattr(existing, k) and k not in _EXPLICIT_KEYS:
                        setattr(existing, k, v)
                existing.scrape_duration_s = duration_ms / 1000
                existing.version_id += 1
            else:
                hotel = Hotel(
                    url_id=url_obj.id,
                    language=lang,
                    scrape_duration_s=duration_ms / 1000,
                    scrape_engine="cloudscraper",
                    **{k: v for k, v in data.items()
                       if hasattr(Hotel, k) and k not in _EXPLICIT_KEYS},
                )
                session.add(hotel)

    def _upsert_description(
        self,
        url_obj: URLQueue,
        lang: str,
        description: str,
    ) -> None:
        """
        STRUCT-001: Persiste / actualiza descripción en hotels_description.

        Requiere que el Hotel ya exista (se llama después de _upsert_hotel).
        Usa (url_id, language) como clave de upsert — igual que hotels.
        """
        try:
            with get_db() as session:
                hotel = (
                    session.query(Hotel)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if not hotel:
                    logger.warning(
                        "Cannot upsert description — Hotel not found for url_id=%s lang=%s",
                        url_obj.id, lang,
                    )
                    return

                existing = (
                    session.query(HotelDescription)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if existing:
                    existing.description = description
                    existing.hotel_id = hotel.id   # mantener FK actualizada
                else:
                    session.add(HotelDescription(
                        hotel_id=hotel.id,
                        url_id=url_obj.id,
                        language=lang,
                        description=description,
                    ))
        except Exception as exc:
            logger.warning(
                "Failed to upsert HotelDescription for %s/%s: %s",
                url_obj.id, lang, exc,
            )

    # ── STRUCT-005 ─────────────────────────────────────────────────────────────

    def _upsert_amenities(
        self,
        url_obj: URLQueue,
        lang: str,
        amenities: List[str],
    ) -> None:
        """
        STRUCT-005: Persiste lista de amenidades en hotels_amenities.

        Estrategia: DELETE WHERE (hotel_id, language) + INSERT bulk.
        Esto garantiza sincronización exacta con el HTML actual en cada re-scrape,
        evitando registros huérfanos de scrapes anteriores.

        Requiere que el Hotel ya exista en DB (llamar después de _upsert_hotel).
        """
        if not amenities:
            return
        try:
            with get_db() as session:
                hotel = (
                    session.query(Hotel)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if not hotel:
                    logger.warning(
                        "Cannot upsert amenities — Hotel not found for url_id=%s lang=%s",
                        url_obj.id, lang,
                    )
                    return

                # Delete existing rows for this hotel/language
                (
                    session.query(HotelAmenity)
                    .filter_by(hotel_id=hotel.id, language=lang)
                    .delete(synchronize_session=False)
                )

                # Bulk insert — deduplicate preserving order
                seen: set = set()
                for amenity_text in amenities:
                    t = amenity_text.strip()
                    if not t or t in seen:
                        continue
                    seen.add(t)
                    session.add(HotelAmenity(
                        hotel_id=hotel.id,
                        url_id=url_obj.id,
                        language=lang,
                        amenity=t[:512],
                    ))

                logger.debug(
                    "Amenities upserted for hotel_id=%s lang=%s: %d rows",
                    hotel.id, lang, len(seen),
                )

        except Exception as exc:
            logger.warning(
                "Failed to upsert HotelAmenity for %s/%s: %s",
                url_obj.id, lang, exc,
            )

    # ── STRUCT-008 ─────────────────────────────────────────────────────────────

    def _upsert_popular_services(
        self,
        url_obj: URLQueue,
        lang: str,
        popular_services: List[str],
    ) -> None:
        """
        STRUCT-008: Persiste servicios más populares en hotels_popular_services.

        Estrategia: DELETE WHERE (hotel_id, language) + INSERT bulk.
        """
        if not popular_services:
            return
        try:
            with get_db() as session:
                hotel = (
                    session.query(Hotel)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if not hotel:
                    logger.warning(
                        "Cannot upsert popular_services — Hotel not found for url_id=%s lang=%s",
                        url_obj.id, lang,
                    )
                    return

                (
                    session.query(HotelPopularService)
                    .filter_by(hotel_id=hotel.id, language=lang)
                    .delete(synchronize_session=False)
                )

                seen: set = set()
                for svc in popular_services:
                    t = svc.strip()
                    if not t or t in seen:
                        continue
                    seen.add(t)
                    session.add(HotelPopularService(
                        hotel_id=hotel.id,
                        url_id=url_obj.id,
                        language=lang,
                        popular_service=t[:512],
                    ))

                logger.debug(
                    "Popular services upserted for hotel_id=%s lang=%s: %d rows",
                    hotel.id, lang, len(seen),
                )

        except Exception as exc:
            logger.warning(
                "Failed to upsert HotelPopularService for %s/%s: %s",
                url_obj.id, lang, exc,
            )

    # ── STRUCT-006 ─────────────────────────────────────────────────────────────

    def _upsert_policies(
        self,
        url_obj: URLQueue,
        lang: str,
        policies: List[Dict[str, Any]],
    ) -> None:
        """
        STRUCT-006: Persiste políticas del alojamiento en hotels_policies.

        Estrategia: DELETE WHERE (hotel_id, language) + INSERT bulk.
        Cada elemento de policies es un dict con claves:
            policy_name    — nombre de la política (e.g. 'Check-in')
            policy_details — texto de detalle
        """
        if not policies:
            return
        try:
            with get_db() as session:
                hotel = (
                    session.query(Hotel)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if not hotel:
                    logger.warning(
                        "Cannot upsert policies — Hotel not found for url_id=%s lang=%s",
                        url_obj.id, lang,
                    )
                    return

                (
                    session.query(HotelPolicy)
                    .filter_by(hotel_id=hotel.id, language=lang)
                    .delete(synchronize_session=False)
                )

                seen_names: set = set()
                for policy in policies:
                    if not isinstance(policy, dict):
                        continue
                    name = str(policy.get("policy_name", "")).strip()
                    details = str(policy.get("policy_details", "")).strip()
                    if not name or name in seen_names:
                        continue
                    seen_names.add(name)
                    session.add(HotelPolicy(
                        hotel_id=hotel.id,
                        url_id=url_obj.id,
                        language=lang,
                        policy_name=name[:256],
                        policy_details=details or None,
                    ))

                logger.debug(
                    "Policies upserted for hotel_id=%s lang=%s: %d rows",
                    hotel.id, lang, len(seen_names),
                )

        except Exception as exc:
            logger.warning(
                "Failed to upsert HotelPolicy for %s/%s: %s",
                url_obj.id, lang, exc,
            )

    # ── STRUCT-007 ─────────────────────────────────────────────────────────────

    def _upsert_legal(
        self,
        url_obj: URLQueue,
        lang: str,
        legal: Dict[str, Any],
    ) -> None:
        """
        STRUCT-007: Persiste información legal en hotels_legal.

        Estrategia: upsert via UniqueConstraint (hotel_id, language).
        Un solo registro por hotel/idioma — si existe se actualiza.
        Campos: legal, legal_info, legal_details.
        """
        if not legal or not isinstance(legal, dict):
            return
        try:
            with get_db() as session:
                hotel = (
                    session.query(Hotel)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if not hotel:
                    logger.warning(
                        "Cannot upsert legal — Hotel not found for url_id=%s lang=%s",
                        url_obj.id, lang,
                    )
                    return

                existing = (
                    session.query(HotelLegal)
                    .filter_by(hotel_id=hotel.id, language=lang)
                    .first()
                )

                legal_title = str(legal.get("legal", "")).strip()[:256] or None
                legal_info = str(legal.get("legal_info", "")).strip() or None
                legal_details = str(legal.get("legal_details", "")).strip() or None

                if existing:
                    existing.legal = legal_title
                    existing.legal_info = legal_info
                    existing.legal_details = legal_details
                else:
                    session.add(HotelLegal(
                        hotel_id=hotel.id,
                        url_id=url_obj.id,
                        language=lang,
                        legal=legal_title,
                        legal_info=legal_info,
                        legal_details=legal_details,
                    ))

                logger.debug(
                    "Legal upserted for hotel_id=%s lang=%s",
                    hotel.id, lang,
                )

        except Exception as exc:
            logger.warning(
                "Failed to upsert HotelLegal for %s/%s: %s",
                url_obj.id, lang, exc,
            )

    # ── STRUCT-013 (v53) ────────────────────────────────────────────────────────

    def _upsert_fine_print(
        self,
        url_obj: URLQueue,
        lang: str,
        fine_print: str,
    ) -> None:
        """
        STRUCT-013 (v53): Persiste el HTML sanitizado del Fine Print en hotels_fine_print.

        Estrategia: upsert via UniqueConstraint (url_id, language).
        Un solo registro por hotel/idioma. Si existe, se actualiza el campo fp.

        El HTML ya ha sido sanitizado por extractor._extract_fine_print():
          - Etiquetas <p> preservadas (saltos de línea).
          - SVG, img, picture, source eliminados.
          - Atributos HTML eliminados de todas las etiquetas.

        Requiere que el Hotel ya exista en DB (llamar después de _upsert_hotel).
        """
        if not fine_print or not fine_print.strip():
            return
        try:
            with get_db() as session:
                hotel = (
                    session.query(Hotel)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if not hotel:
                    logger.warning(
                        "Cannot upsert fine_print — Hotel not found for url_id=%s lang=%s",
                        url_obj.id, lang,
                    )
                    return

                existing = (
                    session.query(HotelFinePrint)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if existing:
                    existing.fp = fine_print
                    existing.hotel_id = hotel.id
                else:
                    session.add(HotelFinePrint(
                        hotel_id=hotel.id,
                        url_id=url_obj.id,
                        language=lang,
                        fp=fine_print,
                    ))

                logger.debug(
                    "FinePrint upserted for hotel_id=%s lang=%s len=%d",
                    hotel.id, lang, len(fine_print),
                )

        except Exception as exc:
            logger.warning(
                "Failed to upsert HotelFinePrint for %s/%s: %s",
                url_obj.id, lang, exc,
            )

    # ── STRUCT-014 (v53) ────────────────────────────────────────────────────────

    def _upsert_all_services(
        self,
        url_obj: URLQueue,
        lang: str,
        all_services: List[str],
    ) -> None:
        """
        STRUCT-014 (v53): Persiste todos los servicios en hotels_all_services.

        Estrategia: DELETE WHERE (hotel_id, language) + INSERT bulk.
        Garantiza sincronización exacta con el HTML actual en cada re-scrape.

        Requiere que el Hotel ya exista en DB (llamar después de _upsert_hotel).
        """
        if not all_services:
            return
        try:
            with get_db() as session:
                hotel = (
                    session.query(Hotel)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if not hotel:
                    logger.warning(
                        "Cannot upsert all_services — Hotel not found for url_id=%s lang=%s",
                        url_obj.id, lang,
                    )
                    return

                # Delete existing rows for this hotel/language
                (
                    session.query(HotelAllService)
                    .filter_by(hotel_id=hotel.id, language=lang)
                    .delete(synchronize_session=False)
                )

                # Bulk insert — deduplicate preserving order
                seen: set = set()
                for svc_text in all_services:
                    t = svc_text.strip()
                    if not t or t in seen:
                        continue
                    seen.add(t)
                    session.add(HotelAllService(
                        hotel_id=hotel.id,
                        url_id=url_obj.id,
                        language=lang,
                        service=t[:512],
                    ))

                logger.debug(
                    "AllServices upserted for hotel_id=%s lang=%s: %d rows",
                    hotel.id, lang, len(seen),
                )

        except Exception as exc:
            logger.warning(
                "Failed to upsert HotelAllService for %s/%s: %s",
                url_obj.id, lang, exc,
            )

    # ── STRUCT-015 (v53) ────────────────────────────────────────────────────────

    def _upsert_faqs(
        self,
        url_obj: URLQueue,
        lang: str,
        faqs: List,
    ) -> None:
        """
        STRUCT-015 (v53): Persiste preguntas frecuentes en hotels_faqs.

        BUG-FAQ-ANSWERS (v56): acepta List[Dict[str, str]] (ask + answer)
        además del formato legacy List[str] (solo ask) para compatibilidad.

        Estrategia: DELETE WHERE (hotel_id, language) + INSERT bulk.
        Una fila por pregunta.

        Requiere que el Hotel ya exista en DB (llamar después de _upsert_hotel).
        """
        if not faqs:
            return
        try:
            with get_db() as session:
                hotel = (
                    session.query(Hotel)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if not hotel:
                    logger.warning(
                        "Cannot upsert faqs — Hotel not found for url_id=%s lang=%s",
                        url_obj.id, lang,
                    )
                    return

                # Delete existing rows for this hotel/language
                (
                    session.query(HotelFAQ)
                    .filter_by(hotel_id=hotel.id, language=lang)
                    .delete(synchronize_session=False)
                )

                # Bulk insert — deduplicate preserving order
                # BUG-FAQ-ANSWERS (v56): handle both Dict and str formats
                seen: set = set()
                for item in faqs:
                    if isinstance(item, dict):
                        question_text = item.get("ask", "").strip()
                        answer_text = item.get("answer", "").strip() or None
                    else:
                        # Legacy str format
                        question_text = str(item).strip()
                        answer_text = None

                    if not question_text or question_text in seen:
                        continue
                    seen.add(question_text)
                    session.add(HotelFAQ(
                        hotel_id=hotel.id,
                        url_id=url_obj.id,
                        language=lang,
                        ask=question_text,   # TEXT — sin truncar, máxima fidelidad
                        answer=answer_text,  # BUG-FAQ-ANSWERS (v56): respuesta del accordion
                    ))

                logger.debug(
                    "FAQs upserted for hotel_id=%s lang=%s: %d rows",
                    hotel.id, lang, len(seen),
                )

        except Exception as exc:
            logger.warning(
                "Failed to upsert HotelFAQ for %s/%s: %s",
                url_obj.id, lang, exc,
            )

    # ── STRUCT-016 (v53) ────────────────────────────────────────────────────────

    def _upsert_guest_reviews(
        self,
        url_obj: URLQueue,
        lang: str,
        guest_reviews: List[Dict[str, Any]],
    ) -> None:
        """
        STRUCT-016 (v53): Persiste categorías de reseñas en hotels_guest_reviews.

        Estrategia: DELETE WHERE (hotel_id, language) + INSERT bulk.
        Cada elemento de guest_reviews es un dict con claves:
            reviews_categories — nombre de la categoría (e.g. 'Limpieza')
            reviews_score      — puntuación de la categoría (e.g. '9.5')

        Requiere que el Hotel ya exista en DB (llamar después de _upsert_hotel).
        """
        if not guest_reviews:
            return
        try:
            with get_db() as session:
                hotel = (
                    session.query(Hotel)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if not hotel:
                    logger.warning(
                        "Cannot upsert guest_reviews — Hotel not found for url_id=%s lang=%s",
                        url_obj.id, lang,
                    )
                    return

                # Delete existing rows for this hotel/language
                (
                    session.query(HotelGuestReview)
                    .filter_by(hotel_id=hotel.id, language=lang)
                    .delete(synchronize_session=False)
                )

                seen_cats: set = set()
                for review in guest_reviews:
                    if not isinstance(review, dict):
                        continue
                    cat = str(review.get("reviews_categories", "")).strip()
                    score = str(review.get("reviews_score", "")).strip()
                    if not cat or cat in seen_cats:
                        continue
                    seen_cats.add(cat)
                    session.add(HotelGuestReview(
                        hotel_id=hotel.id,
                        url_id=url_obj.id,
                        language=lang,
                        reviews_categories=cat[:256],
                        reviews_score=score or None,
                    ))

                logger.debug(
                    "GuestReviews upserted for hotel_id=%s lang=%s: %d rows",
                    hotel.id, lang, len(seen_cats),
                )

        except Exception as exc:
            logger.warning(
                "Failed to upsert HotelGuestReview for %s/%s: %s",
                url_obj.id, lang, exc,
            )

    # ── STRUCT-017 (v53) ────────────────────────────────────────────────────────

    def _upsert_property_highlights(
        self,
        url_obj: URLQueue,
        lang: str,
        property_highlights: str,
    ) -> None:
        """
        BUG-PH-NORMALIZATION-001 FIX (v56): Persiste highlights de propiedad
        de forma normalizada — un registro por highlight por hotel/idioma.

        Cambio respecto a v53-v55:
          ANTES: 1 registro HTML por hotel/idioma (blob HTML con todos los items).
          AHORA: N registros de texto plano, uno por highlight individual.

        El extractor devuelve HTML sanitizado. Esta función lo parsea con
        BeautifulSoup, extrae el texto de cada <li> y persiste cada uno
        como registro independiente en hotels_property_highlights.

        Estrategia de upsert:
          - DELETE + INSERT por (hotel_id, language) para limpiar highlights
            obsoletos antes de reinsertar el set actualizado.
          - ON CONFLICT DO NOTHING via UniqueConstraint uq_hph_hotel_lang_highlight.

        Requiere que el Hotel ya exista en DB (llamar después de _upsert_hotel).
        """
        if not property_highlights or not property_highlights.strip():
            return

        # Parsear HTML y extraer textos individuales de cada <li>
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(property_highlights, "html.parser")
            items: list[str] = []
            for li in soup.find_all("li"):
                # Buscar div con texto dentro del <li> (estructura real del DOM)
                text_divs = li.find_all("div")
                text = ""
                for div in text_divs:
                    candidate = div.get_text(strip=True)
                    if candidate:
                        text = candidate
                        break
                if not text:
                    text = li.get_text(strip=True)
                if text and len(text) <= 512:
                    items.append(text)

            # Deduplicar preservando orden
            seen: set[str] = set()
            unique_items: list[str] = []
            for item in items:
                if item not in seen:
                    seen.add(item)
                    unique_items.append(item)

            if not unique_items:
                logger.debug(
                    "PropertyHighlights: no items extracted for url_id=%s lang=%s",
                    url_obj.id, lang,
                )
                return

        except Exception as exc:
            logger.warning(
                "PropertyHighlights HTML parse error for %s/%s: %s",
                url_obj.id, lang, exc,
            )
            return

        try:
            with get_db() as session:
                hotel = (
                    session.query(Hotel)
                    .filter_by(url_id=url_obj.id, language=lang)
                    .first()
                )
                if not hotel:
                    logger.warning(
                        "Cannot upsert property_highlights — Hotel not found for url_id=%s lang=%s",
                        url_obj.id, lang,
                    )
                    return

                # DELETE + INSERT: eliminar highlights anteriores y reinsertar set actual
                session.query(HotelPropertyHighlights).filter_by(
                    hotel_id=hotel.id, language=lang
                ).delete(synchronize_session="fetch")

                for item_text in unique_items:
                    session.add(HotelPropertyHighlights(
                        hotel_id=hotel.id,
                        url_id=url_obj.id,
                        language=lang,
                        highlight=item_text,
                    ))

                logger.debug(
                    "PropertyHighlights upserted for hotel_id=%s lang=%s items=%d",
                    hotel.id, lang, len(unique_items),
                )

        except Exception as exc:
            logger.warning(
                "Failed to upsert HotelPropertyHighlights for %s/%s: %s",
                url_obj.id, lang, exc,
            )

    # ── Lang status ────────────────────────────────────────────────────────────

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
            logger.warning("Failed to write ScrapingLog: %s", exc)

    def _mark_processing(self, url_obj: URLQueue) -> None:
        with get_db() as session:
            row = session.get(URLQueue, url_obj.id)
            if row:
                row.status = "processing"

    def _mark_done(
        self,
        url_obj: URLQueue,
        all_ok: bool,
        success_langs: Optional[List[str]] = None,
        failed_langs: Optional[List[str]] = None,
    ) -> None:
        """Mark URL as done/error and record language outcome lists."""
        with get_db() as session:
            row = session.get(URLQueue, url_obj.id)
            if row:
                row.status = "done" if all_ok else "error"
                row.scraped_at = datetime.now(timezone.utc)
                row.languages_completed = ",".join(success_langs or [])
                row.languages_failed    = ",".join(failed_langs  or [])
                row.updated_at = datetime.now(timezone.utc)

    def _mark_error(self, url_obj: URLQueue, error: str) -> None:
        with get_db() as session:
            row = session.get(URLQueue, url_obj.id)
            if row:
                row.status = "error"
                row.retry_count += 1
                row.last_error = error[:2000]
                if row.retry_count >= row.max_retries:
                    row.status = "error"
