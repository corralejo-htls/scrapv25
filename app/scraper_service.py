"""
scraper_service.py — BookingScraper Pro v6.0.0 build 51
========================================================
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

from app.config import get_settings
from app.database import get_db
from app.extractor import HotelExtractor, detect_language
from app.models import (
    Hotel, HotelAmenity, HotelDescription, HotelLegal, HotelPolicy,
    HotelPopularService, ScrapingLog, URLLanguageStatus, URLQueue,
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

            self._mark_done(url_obj, all_ok=True)
            self._stats.record(succeeded=True)

        except Exception as exc:
            logger.error("_process_url failed for %s: [%s] %s", url_id_str, type(exc).__name__, exc)
            self._mark_error(url_obj, str(exc)[:2000])
            self._stats.record(failed=True)
        finally:
            _release_url(url_id_str)

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
                    downloaded, total = downloader.download_photo_batch(
                        hotel_id=hotel_uuid,
                        photos=gallery_photos,
                    )
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
