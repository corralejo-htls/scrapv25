"""
main.py — BookingScraper Pro v6.0.0 build 53
Fixes applied:
  SCRAP-BUG-001: Rate limiter uses time-based TTL to bound dictionary growth.
  SCRAP-BUG-003: All POSIX signal references removed; Windows-compatible log rotation used.
  SCRAP-BUG-024: URL validation strengthened with regex + netloc check.
  BUG-002       : force-now lock fallback warns that multi-process mode is unsafe.
  SCRAP-CON-003 : Redis health-check uses shared connection pool (not new conn per call).
  STRUCT-009    : /urls/load-csv — soporta formato 3 columnas (external_ref, url, external_url).
                  Parseo actualizado: id_col=0, url_col=1, ext_url_col=2.
                  INSERT actualizado para persistir external_url cuando la columna existe.
  STRUCT-010    : url_queue.hotel_id_booking eliminado — _url_queue_has_external_ref()
                  reemplazada por _get_url_queue_columns() (detección genérica).
  STRUCT-011    : audit log query — h.city reemplazado por h.address_city.
                  Columnas de respuesta y CSV actualizadas (address_city en lugar de city).
  STRUCT-012    : audit log query — h.country eliminado. Usar h.address_country si se necesita.
  FIX-IMPORT-001: json, logging.handlers, urlunparse, func consolidated at module level.
                  sa_inspect confirmed at module level (prevents NameError in
                  _get_url_queue_columns). Duplicated in-function imports removed:
                  lines 69, 255, 514, 832, 1003-1004, 1103, 1147-1150.
                  sa_text alias → text; dt alias → datetime; _json alias → json.
  Platform      : Windows 11 / ProactorEventLoop / Windows Defender Firewall port 5432.
"""

from __future__ import annotations

import asyncio
import json
import logging
import logging.handlers
import os
import re
import sys
import threading
import time
import uuid
from uuid import UUID
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse, urlunparse

import csv
import io
import redis as redis_lib
import uvicorn
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse, HTMLResponse
from pydantic import BaseModel, Field

# FIX-IMPORT-001: func and sa_inspect consolidated at module level.
# Previous versions imported these inside individual endpoint functions,
# causing NameError when sa_inspect was referenced in _get_url_queue_columns().
from sqlalchemy import func, inspect as sa_inspect, text
from app import APP_VERSION, BUILD_VERSION
from app.config import get_settings
from app.database import dispose_engine, get_db, get_pool_status, test_connection
from app.models import (
    Base, Hotel, HotelAllService, HotelDescription, HotelExtraInfo,
    HotelFAQ, HotelFinePrint, HotelGuestReview, HotelIndividualReview,
    HotelLegal, HotelNearbyPlace, HotelPolicy, HotelPopularService,
    HotelPropertyHighlights, HotelRoomType, HotelSEO,
    ScrapingLog, URLLanguageStatus, URLQueue,
)
# BUG-API-MAIN-001-FIX (Build 84): Added 5 missing model imports:
#   HotelAllService, HotelFAQ, HotelFinePrint, HotelGuestReview,
#   HotelPropertyHighlights — these tables were populated by _persist_hotel_data()
#   but never queried in get_hotel(), making their data invisible via API.
from app.scraper_service import ScraperService
from app.api_payload_builder import ApiPayloadBuilder
from app.export_ui import build_export_ui_html

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Windows 11: ProactorEventLoop required for subprocess support
# ---------------------------------------------------------------------------
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# ---------------------------------------------------------------------------
# Logging setup (Windows-compatible — RotatingFileHandler, not logrotate)
# ---------------------------------------------------------------------------

def _setup_logging() -> None:
    """Configure rotating file + console logging for Windows 11."""
    cfg = get_settings()
    cfg.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    cfg.LOGS_DEBUG_DIR.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(getattr(logging, cfg.LOG_LEVEL, logging.INFO))

    fmt = logging.Formatter(
        fmt='{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":%(message)s}',
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    root.addHandler(ch)

    # Rotating file handler (Windows-compatible — no logrotate signal needed)
    fh = logging.handlers.RotatingFileHandler(
        filename=cfg.LOGS_DIR / "bookingscraper.log",
        maxBytes=cfg.LOG_MAX_BYTES,
        backupCount=cfg.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    fh.setFormatter(fmt)
    root.addHandler(fh)

    # Windows Event Log (optional — requires pywin32)
    try:
        nt_handler = logging.handlers.NTEventLogHandler("BookingScraper Pro")
        nt_handler.setLevel(logging.WARNING)
        root.addHandler(nt_handler)
    except Exception:
        pass  # Not available in all environments


# ---------------------------------------------------------------------------
# Rate limiter — BUG-102 / SCRAP-BUG-001 fix: TTL-based cleanup
# ---------------------------------------------------------------------------

_rate_lock = threading.Lock()
# Structure: {ip: (window_start_ts, count)}
_rate_buckets: Dict[str, Tuple[float, int]] = {}
_RATE_LIMIT_RPS = 10
_RATE_WINDOW_S = 1.0
_RATE_BUCKET_TTL_S = 300.0  # evict idle IPs after 5 minutes

def _cleanup_rate_buckets(now: float) -> None:
    """Evict stale IP entries to prevent unbounded memory growth."""
    stale = [
        ip for ip, (ts, _) in _rate_buckets.items()
        if (now - ts) > _RATE_BUCKET_TTL_S
    ]
    for ip in stale:
        del _rate_buckets[ip]


async def rate_limit_middleware(request: Request, call_next: Any) -> Any:
    """Per-IP rate limiter with bounded memory footprint."""
    client_ip = request.client.host if request.client else "unknown"
    now = time.monotonic()

    with _rate_lock:
        # Periodic cleanup (1% of requests trigger full scan — amortised O(1))
        if len(_rate_buckets) % 100 == 0:
            _cleanup_rate_buckets(now)

        ts, count = _rate_buckets.get(client_ip, (now, 0))

        if (now - ts) >= _RATE_WINDOW_S:
            # New window
            _rate_buckets[client_ip] = (now, 1)
        elif count >= _RATE_LIMIT_RPS:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded. Maximum 10 requests per second."},
            )
        else:
            _rate_buckets[client_ip] = (ts, count + 1)

    return await call_next(request)


# ---------------------------------------------------------------------------
# Force-now distributed lock
# ---------------------------------------------------------------------------

_force_now_thread_lock = threading.Lock()
_redis_pool: Optional[redis_lib.ConnectionPool] = None


def _get_redis_pool() -> Optional[redis_lib.ConnectionPool]:
    """Shared Redis connection pool — SCRAP-CON-003 fix."""
    global _redis_pool
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
        except Exception as exc:
            logger.warning("Could not create Redis pool: %s", exc)
    return _redis_pool


def _acquire_force_now_lock(ttl_seconds: int = 300) -> bool:
    """
    Acquire a distributed lock for force-now scraping.
    BUG-002 fix: falls back to threading.Lock() with an explicit warning
    that this is NOT safe under multi-worker uvicorn deployments.
    """
    try:
        pool = _get_redis_pool()
        if pool:
            r = redis_lib.Redis(connection_pool=pool)
            acquired = r.set("force_now_lock", "1", nx=True, ex=ttl_seconds)
            return bool(acquired)
    except Exception as exc:
        logger.warning(
            "Redis lock unavailable (%s). Falling back to threading.Lock(). "
            "WARNING: This fallback is NOT safe if uvicorn is running with "
            "--workers > 1. Duplicate scraping batches may be dispatched.",
            exc,
        )

    # In-process fallback — single-worker only
    return _force_now_thread_lock.acquire(blocking=False)


def _release_force_now_lock() -> None:
    try:
        pool = _get_redis_pool()
        if pool:
            r = redis_lib.Redis(connection_pool=pool)
            r.delete("force_now_lock")
            return
    except Exception:
        pass
    if _force_now_thread_lock.locked():
        try:
            _force_now_thread_lock.release()
        except RuntimeError:
            pass


# ---------------------------------------------------------------------------
# URL validation — SCRAP-BUG-024 fix
# ---------------------------------------------------------------------------

_BOOKING_HOST_RE = re.compile(r"^(?:www\.)?booking\.com$", re.IGNORECASE)
_VALID_URL_RE = re.compile(
    r"^https://(?:www\.)?booking\.com/hotel/[a-z]{2}/[^?#]{3,}(?:\.html)?(?:\?[^#]*)?$",
    re.IGNORECASE,
)

# BUG-URL-LANG: detect language suffix in path — e.g. .es, .it, .en-gb, .pt-pt, .zh-cn
# Pattern matches: /hotel/XX/name.LANG.html  or  ?lang=XX  query param
_LANG_SUFFIX_IN_PATH_RE = re.compile(
    r'\.[a-z]{2}(?:-[a-z]{2,4})?(?=\.html)',
    re.IGNORECASE,
)
_LANG_QUERY_RE = re.compile(r'[?&]lang=[^&]*', re.IGNORECASE)


def _normalize_booking_url(url: str) -> str:
    """
    BUG-URL-LANG: Strip language suffix and ?lang= query param from Booking.com URL.

    Examples:
      .es.html?lang=es  →  .html
      .en-gb.html       →  .html
      .pt-pt.html       →  .html

    Booking.com canonical format (no language suffix) returns the page in the
    language determined by the Accept-Language header sent by the scraper.
    Language-suffixed URLs redirect or 404 when accessed from certain VPN IPs.
    """
    try:
        parsed = urlparse(url)
        # Strip .es / .en-gb / .pt-pt etc. before .html in path
        clean_path = _LANG_SUFFIX_IN_PATH_RE.sub('', parsed.path)
        # Strip ?lang=es or &lang=es query param
        clean_query = _LANG_QUERY_RE.sub('', parsed.query).strip('&')
        return urlunparse((
            parsed.scheme, parsed.netloc, clean_path,
            parsed.params, clean_query, '',
        ))
    except Exception:
        return url


def _url_has_lang_suffix(url: str) -> bool:
    """Return True if URL contains a language suffix that needs normalization."""
    try:
        parsed = urlparse(url)
        return bool(
            _LANG_SUFFIX_IN_PATH_RE.search(parsed.path)
            or _LANG_QUERY_RE.search(parsed.query)
        )
    except Exception:
        return False


def _validate_booking_url(url: str) -> bool:
    """Validate that a URL is a well-formed Booking.com hotel page."""
    if not url or len(url) > 2048:
        return False
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    if parsed.scheme != "https":
        return False
    if not _BOOKING_HOST_RE.match(parsed.netloc):
        return False
    if not parsed.path.startswith("/hotel/"):
        return False
    # Reject javascript:, data:, etc. masquerading via redirect paths
    if re.search(r"[<>\"'\\]", url):
        return False
    return True


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class ScrapeRequest(BaseModel):
    url_ids: Optional[List[str]] = None
    max_workers: Optional[int] = Field(default=None, ge=1, le=4)


class URLCreateRequest(BaseModel):
    urls: List[str] = Field(..., min_length=1, max_length=1000)


class URLResponse(BaseModel):
    id: str
    url: str
    status: str
    retry_count: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    _setup_logging()
    cfg = get_settings()
    logger.info(
        "Starting %s v%s build %d | platform=win32",
        cfg.APP_NAME, cfg.APP_VERSION, cfg.BUILD_VERSION,
    )
    if not test_connection():
        logger.warning("Database not reachable on startup — check PostgreSQL service.")
    yield
    dispose_engine()
    logger.info("BookingScraper shutdown complete.")


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="BookingScraper Pro",
    version=APP_VERSION,
    description="Hotel data scraping API — Windows 11 single-node deployment.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.middleware("http")(rate_limit_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1",
                   "http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# ---------------------------------------------------------------------------
# API-key dependency
# ---------------------------------------------------------------------------

def _check_api_key(request: Request) -> None:
    cfg = get_settings()
    if not cfg.REQUIRE_API_KEY:
        return
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer ") or auth[7:] != cfg.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/health", tags=["System"])
def health_check() -> Dict[str, Any]:
    db_ok = test_connection()
    pool = get_pool_status()
    redis_ok = False
    try:
        pool_obj = _get_redis_pool()
        if pool_obj:
            r = redis_lib.Redis(connection_pool=pool_obj)
            redis_ok = r.ping()
    except Exception:
        pass

    overall = "healthy" if (db_ok and redis_ok) else "degraded"
    # Return 503 for degraded so load-balancers/monitors detect the problem
    http_status = 200 if overall == "healthy" else 503
    return JSONResponse(
        status_code=http_status,
        content={
            "status": overall,
            "version": APP_VERSION,
            "build": BUILD_VERSION,
            "database": "up" if db_ok else "down",
            "redis": "up" if redis_ok else "down",
            "pool": pool,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


# ---------------------------------------------------------------------------
# URL management
# ---------------------------------------------------------------------------

@app.post("/urls/load", tags=["URLs"], dependencies=[Depends(_check_api_key)])
def load_urls(payload: URLCreateRequest) -> Dict[str, Any]:
    """Load hotel URLs into the scraping queue after validation."""
    # BUG-LOAD-URLS-001-FIX (Build 86): Dead loop with undefined '_valid' removed.
    # The loop populated 'valid'/'invalid' from raw (pre-normalization) URLs and
    # referenced the undefined name '_valid', raising NameError on any valid URL.
    # Both lists were immediately overwritten by the normalization pass below,
    # making the loop entirely redundant. Removed without semantic loss.

    # BUG-URL-LANG: normalize URLs (strip .es.html → .html, ?lang=es)
    normalized_count = 0
    normalized_urls = []
    for u in payload.urls:
        if _url_has_lang_suffix(u):
            normalized_urls.append(_normalize_booking_url(u))
            normalized_count += 1
        else:
            normalized_urls.append(u)

    valid = [u for u in normalized_urls if _validate_booking_url(u)]
    invalid = [u for u in normalized_urls if not _validate_booking_url(u)]

    inserted = 0
    with get_db() as session:
        for url in valid:
            existing = session.query(URLQueue).filter_by(url=url).first()
            if not existing:
                session.add(URLQueue(url=url, base_url=url))
                inserted += 1

    return {
        "inserted": inserted,
        "duplicates": len(valid) - inserted,
        "invalid": invalid,
        "normalized": normalized_count,
    }


def _get_url_queue_columns() -> set:
    """
    Retorna el conjunto de columnas existentes en url_queue.
    Reemplaza _url_queue_has_external_ref() para soportar detección
    de múltiples columnas: external_ref (v49+) y external_url (v52+).

    STRUCT-009 (v52): añade detección de external_url.
    STRUCT-010 (v52): hotel_id_booking eliminado de url_queue.
    """
    try:
        engine = _get_engine_for_inspect()
        cols = {c["name"] for c in sa_inspect(engine).get_columns("url_queue")}
        return cols
    except Exception:
        return set()


def _get_engine_for_inspect():
    """Helper para obtener engine en contexto de inspección."""
    from app.database import _get_engine
    return _get_engine()


@app.post(
    "/urls/load-csv",
    tags=["URLs"],
    summary="Load URLs from CSV file",
    dependencies=[Depends(_check_api_key)],
)
async def load_urls_csv(
    file: UploadFile = File(
        ...,
        description=(
            "CSV file with hotel URLs. "
            "Accepted formats: one URL per line, or a column named "
            "'url' / 'URL' / 'urls' / 'URLs'. "
            "Max size: 5 MB. Encoding: UTF-8."
        ),
    ),
) -> Dict[str, Any]:
    """
    Upload a CSV file to load hotel URLs into the scraping queue.

    **CSV formats accepted:**
    - **Format A (v52 — 3 cols):** `external_ref,url,external_url` — sin cabecera, ID numérico,
      URL de Booking.com, URL externa opcional.
    - **Format A-legacy (2 cols):** `external_ref,url` — sin cabecera, ID numérico + URL.
    - **Format B:** columna nombrada `url` / `URL` / `urls` / `URLs` — cabecera auto-detectada.
    - **Format C:** una URL por línea, sin cabecera.

    **Format A (3 cols) ejemplo:**
    ```
    1001,https://www.booking.com/hotel/es/melia-fuerteventura.html,https://www.otrawebS01.com/hotel/melia
    1002,https://www.booking.com/hotel/es/riu-palace-tres-islas.html,
    ```

    **Limits:** 5 MB max file size, 5 000 URLs per upload.
    """
    MAX_FILE_BYTES = 5 * 1024 * 1024  # 5 MB
    MAX_URLS       = 5_000

    # Validate content type
    allowed_types = {
        "text/csv", "text/plain", "application/csv",
        "application/vnd.ms-excel", "application/octet-stream",
    }
    if file.content_type and file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"Tipo de archivo no soportado: {file.content_type}. "
                "Sube un archivo .csv o .txt."
            ),
        )

    # Read raw bytes
    raw = await file.read(MAX_FILE_BYTES + 1)
    if len(raw) > MAX_FILE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Archivo demasiado grande. Máximo permitido: 5 MB.",
        )

    # Decode
    # BUG-SHADOW-001: variable renombrada a csv_content para evitar shadowing de
    # sqlalchemy.text importado en la línea 492. El nombre 'text' como variable local
    # sobreescribía la función sqlalchemy.text, causando TypeError en los INSERT posteriores.
    try:
        csv_content = raw.decode("utf-8")
    except UnicodeDecodeError:
        try:
            csv_content = raw.decode("latin-1")
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="No se pudo decodificar el archivo. Usa codificación UTF-8.",
            )

    # Parse CSV
    lines = csv_content.splitlines()
    if not lines:
        raise HTTPException(status_code=400, detail="El archivo CSV está vacío.")

    reader   = csv.reader(lines)
    all_rows = list(reader)

    # ── Detección de formato ──────────────────────────────────────────────────
    # Formato A v52 (3 cols): external_ref, url, external_url — 1ª col numérica
    # Formato A-legacy (2 cols): external_ref, url — 1ª col numérica
    # Formato B: cabecera con columna 'url'/'URL'/'urls'/'URLs'
    # Formato C: columna única sin cabecera, cada línea es una URL
    # ─────────────────────────────────────────────────────────────────────────

    url_col      = None
    id_col       = None   # columna del id externo (solo formato A)
    ext_url_col  = None   # STRUCT-009: columna de URL externa (formato A v52, 3 cols)
    start_row    = 0

    if all_rows:
        header = [c.strip().lower() for c in all_rows[0]]
        url_col_names = {"url", "urls", "hotel_url", "booking_url", "link", "enlace"}

        # Formato B: cabecera nombrada
        for idx, col in enumerate(header):
            if col in url_col_names:
                url_col   = idx
                start_row = 1
                break

        # Formato A: sin cabecera, primera columna es ID numérico
        if url_col is None and len(all_rows[0]) >= 2:
            first_cell = all_rows[0][0].strip()
            if first_cell.isdigit():
                id_col    = 0
                url_col   = 1
                start_row = 0   # sin cabecera
                # STRUCT-009: 3ª columna = external_url (si existe)
                if len(all_rows[0]) >= 3:
                    ext_url_col = 2

    # Formato C: columna única
    if url_col is None:
        url_col   = 0
        start_row = 0

    # (ext_id_or_None, url, external_url_or_None)
    raw_triples: List[Tuple[Optional[str], str, Optional[str]]] = []
    for row in all_rows[start_row:]:
        if not row:
            continue
        if url_col < len(row):
            candidate = row[url_col].strip().strip('"').strip("'")
            if candidate:
                ext_id = (
                    row[id_col].strip()
                    if (id_col is not None and id_col < len(row))
                    else None
                )
                # STRUCT-009: extraer external_url si columna existe y tiene valor
                raw_ext_url = (
                    row[ext_url_col].strip().strip('"').strip("'")
                    if (ext_url_col is not None and ext_url_col < len(row))
                    else ""
                )
                external_url: Optional[str] = None
                if raw_ext_url and (
                    raw_ext_url.startswith("http://") or raw_ext_url.startswith("https://")
                ) and len(raw_ext_url) <= 2048:
                    external_url = raw_ext_url

                raw_triples.append((ext_id, candidate, external_url))
        if len(raw_triples) >= MAX_URLS:
            break

    # Compatibilidad: raw_pairs sigue siendo el alias de las dos primeras columnas
    raw_pairs: List[Tuple[Optional[str], str]] = [(t[0], t[1]) for t in raw_triples]
    raw_urls = [url for _, url in raw_pairs]

    if not raw_urls:
        raise HTTPException(
            status_code=400,
            detail=(
                "No se encontraron URLs en el archivo. "
                "Asegúrate de que la columna se llame 'url' o que las URLs "
                "estén en la primera columna."
            ),
        )

    # BUG-URL-LANG: normalize URLs (strip .es.html → .html, ?lang=es, etc.)
    # FIX-CSV-EXT-001: construir el mapa url_normalizada -> (ext_id, external_url)
    # DESPUÉS de normalizar, no antes. El mapa previo usaba URLs raw como claves
    # y el lookup se hacía con URLs normalizadas → ext_id siempre resultaba None.
    normalized_count = 0
    # (ext_id, url_normalizada, external_url)
    normalized_triples: List[Tuple[Optional[str], str, Optional[str]]] = []
    for ext_id_raw, u, ext_url in raw_triples:
        if _url_has_lang_suffix(u):
            normalized_triples.append((ext_id_raw, _normalize_booking_url(u), ext_url))
            normalized_count += 1
        else:
            normalized_triples.append((ext_id_raw, u, ext_url))

    # Validate and build final lookup — claves ya son URLs normalizadas
    url_to_ext: Dict[str, Optional[str]] = {}
    url_to_ext_url: Dict[str, Optional[str]] = {}   # STRUCT-009
    normalized_raw: List[str] = []
    for ext_id_raw, norm_url, ext_url in normalized_triples:
        normalized_raw.append(norm_url)
        if norm_url not in url_to_ext:          # primera aparición gana
            url_to_ext[norm_url] = ext_id_raw
            url_to_ext_url[norm_url] = ext_url

    valid   = [u for u in normalized_raw if _validate_booking_url(u)]
    invalid = [u for u in normalized_raw if not _validate_booking_url(u)]

    # STRUCT-009/010 (v52): detección genérica de columnas disponibles
    existing_cols = _get_url_queue_columns()
    has_ext_ref = "external_ref" in existing_cols
    has_ext_url = "external_url" in existing_cols   # STRUCT-009

    # FIX-CSV-EXT-002 / STRUCT-009 (v52):
    # ON CONFLICT (url) DO UPDATE SET
    #     external_ref = EXCLUDED.external_ref,
    #     external_url = EXCLUDED.external_url
    #   WHERE url_queue.external_ref IS NULL
    # Garantiza:
    #   a) URL nueva con ext_id   → INSERT con external_ref y external_url
    #   b) URL existente sin ref  → UPDATE external_ref y external_url
    #   c) URL existente con ref  → sin cambio (WHERE IS NULL protege)
    #   d) URL nueva sin ext_id   → INSERT solo URL (Formato B/C)
    inserted = 0
    updated  = 0
    skipped  = 0
    with get_db() as session:
        for url in valid:
            ext_id   = url_to_ext.get(url)
            ext_url  = url_to_ext_url.get(url)   # STRUCT-009; puede ser None

            if has_ext_ref and ext_id is not None:
                # Construir columnas y parámetros según columnas disponibles
                if has_ext_url:
                    sql_str = (
                        "INSERT INTO url_queue (url, base_url, external_ref, external_url) "
                        "VALUES (:url, :url, :ext_id, :ext_url) "
                        "ON CONFLICT (url) DO UPDATE "
                        "    SET external_ref = EXCLUDED.external_ref, "
                        "        external_url = EXCLUDED.external_url "
                        "WHERE url_queue.external_ref IS NULL "
                        "RETURNING (xmax = 0) AS is_insert"
                    )
                    params = {"url": url, "ext_id": ext_id, "ext_url": ext_url}
                else:
                    sql_str = (
                        "INSERT INTO url_queue (url, base_url, external_ref) "
                        "VALUES (:url, :url, :ext_id) "
                        "ON CONFLICT (url) DO UPDATE "
                        "    SET external_ref = EXCLUDED.external_ref "
                        "WHERE url_queue.external_ref IS NULL "
                        "RETURNING (xmax = 0) AS is_insert"
                    )
                    params = {"url": url, "ext_id": ext_id}

                result     = session.execute(text(sql_str), params)
                row_result = result.fetchone()
                if row_result is None:
                    skipped += 1          # URL existente con external_ref ya grabado
                elif row_result[0]:
                    inserted += 1         # INSERT nuevo
                else:
                    updated += 1          # UPDATE de external_ref NULL → valor

            else:
                # Formato B / C / schema sin external_ref: solo insertar URL
                result = session.execute(
                    text(
                        "INSERT INTO url_queue (url, base_url) "
                        "VALUES (:url, :url) "
                        "ON CONFLICT (url) DO NOTHING"
                    ),
                    {"url": url},
                )
                if result.rowcount == 1:
                    inserted += 1
                else:
                    skipped += 1

    # BUG-LOG-001: logger usa formato %-style internamente.
    logger.info(
        "load-csv completado — insertadas: %d  external_ref actualizado: %d  "
        "sin cambios: %d  invalidas: %d",
        inserted, updated, skipped, len(invalid),
    )

    fmt_detected = (
        "id,url,external_url" if (id_col is not None and ext_url_col is not None)
        else ("id,url" if id_col is not None
              else ("header" if start_row == 1
                    else "url_only"))
    )

    return {
        "filename":        file.filename,
        "total_rows":      len(raw_triples),
        "normalized":      normalized_count,
        "inserted":        inserted,
        "updated_ref":     updated,
        "duplicates":      skipped,
        "invalid":         invalid[:50],
        "invalid_count":   len(invalid),
        "format_detected": fmt_detected,
    }


@app.get("/urls", tags=["URLs"], dependencies=[Depends(_check_api_key)])
def list_urls(
    status_filter: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    with get_db() as session:
        q = session.query(URLQueue)
        if status_filter:
            q = q.filter(URLQueue.status == status_filter)
        rows = q.order_by(URLQueue.created_at.desc()).offset(offset).limit(limit).all()
    return [
        {
            "id": str(r.id), "url": r.url, "status": r.status,
            "retry_count": r.retry_count, "created_at": r.created_at.isoformat(),
        }
        for r in rows
    ]


@app.delete("/urls/{url_id}", tags=["URLs"], dependencies=[Depends(_check_api_key)])
def delete_url(url_id: str) -> Dict[str, str]:
    try:
        uid = uuid.UUID(url_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format.")
    with get_db() as session:
        row = session.get(URLQueue, uid)
        if not row:
            raise HTTPException(status_code=404, detail="URL not found.")
        session.delete(row)
    return {"deleted": url_id}


# ---------------------------------------------------------------------------
# Scraping control
# ---------------------------------------------------------------------------

@app.post("/scraping/force-now", tags=["Scraping"], dependencies=[Depends(_check_api_key)])
def force_scrape_now(payload: ScrapeRequest) -> Dict[str, Any]:
    """Dispatch a scraping batch immediately."""
    if not _acquire_force_now_lock():
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="A scraping batch is already in progress.",
        )
    try:
        cfg = get_settings()
        workers = payload.max_workers or cfg.SCRAPER_MAX_WORKERS
        service = ScraperService()
        # BUG-DISPATCH-001-FIX (Build 86): dispatch_batch() accepts no kwargs.
        # Passing url_ids/max_workers caused TypeError on every /scraping/force-now call.
        # max_workers is already read from config inside dispatch_batch() via
        # getattr(cfg, "SCRAPER_MAX_WORKERS", 2) — no override needed here.
        result = service.dispatch_batch()
        return {"status": "dispatched", "result": result}
    except Exception as exc:
        logger.exception("force-now scraping failed: %s", exc)
        raise HTTPException(status_code=500, detail="Scraping batch failed. Check logs.")
    finally:
        _release_force_now_lock()


@app.get("/scraping/status", tags=["Scraping"], dependencies=[Depends(_check_api_key)])
def scraping_status() -> Dict[str, Any]:
    with get_db() as session:
        counts = (
            session.query(URLQueue.status, func.count(URLQueue.id))
            .group_by(URLQueue.status)
            .all()
        )
    return {"url_status_counts": {s: c for s, c in counts}}


# ---------------------------------------------------------------------------
# Hotel data
# ---------------------------------------------------------------------------

@app.get("/hotels", tags=["Hotels"], dependencies=[Depends(_check_api_key)])
def list_hotels(
    language: Optional[str] = None,
    address_city: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    with get_db() as session:
        q = session.query(Hotel)
        if language:
            q = q.filter(Hotel.language == language)
        if address_city:
            # STRUCT-011 (v52): filtro renombrado de city a address_city
            q = q.filter(Hotel.address_city.ilike(f"%{address_city}%"))
        rows = q.order_by(Hotel.created_at.desc()).offset(offset).limit(limit).all()
    return [
        {
            "id": str(h.id), "name": h.hotel_name,
            "address_city": h.address_city,   # STRUCT-011
            # STRUCT-012: country eliminado — usar address_country
            "address_country": h.address_country,
            "language": h.language,
            "review_score": h.review_score, "star_rating": h.star_rating,
        }
        for h in rows
    ]


@app.get("/hotels/{hotel_id}", tags=["Hotels"], dependencies=[Depends(_check_api_key)])
def get_hotel(hotel_id: str) -> Dict[str, Any]:
    try:
        hid = uuid.UUID(hotel_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format.")
    with get_db() as session:
        row = session.get(Hotel, hid)
        if not row:
            raise HTTPException(status_code=404, detail="Hotel not found.")

        # STRUCT-001: description from hotels_description
        desc_row = (
            session.query(HotelDescription)
            .filter_by(hotel_id=hid, language=row.language)
            .first()
        )

        # STRUCT-008: popular_services from hotels_popular_services
        popular_rows = (
            session.query(HotelPopularService)
            .filter_by(hotel_id=hid, language=row.language)
            .order_by(HotelPopularService.id)
            .all()
        )

        # STRUCT-006: policies from hotels_policies
        policy_rows = (
            session.query(HotelPolicy)
            .filter_by(hotel_id=hid, language=row.language)
            .order_by(HotelPolicy.id)
            .all()
        )

        # STRUCT-007: legal from hotels_legal
        legal_row = (
            session.query(HotelLegal)
            .filter_by(hotel_id=hid, language=row.language)
            .first()
        )

        # ── v76 satellite tables ──────────────────────────────────────────
        # BUG-MAIN-001-FIX (v76 patch): queries for new tables added in v76.
        # These models were imported but never queried — all v76 data was
        # invisible to API consumers.

        # STRUCT-021: extra info
        extra_info_row = (
            session.query(HotelExtraInfo)
            .filter_by(hotel_id=hid, language=row.language)
            .first()
        )

        # STRUCT-022: nearby places
        nearby_rows = (
            session.query(HotelNearbyPlace)
            .filter_by(hotel_id=hid, language=row.language)
            .order_by(HotelNearbyPlace.id)
            .all()
        )

        # STRUCT-023: room types (normalized)
        room_type_rows = (
            session.query(HotelRoomType)
            .filter_by(hotel_id=hid, language=row.language)
            .order_by(HotelRoomType.id)
            .all()
        )

        # STRUCT-024: SEO meta tags
        seo_row = (
            session.query(HotelSEO)
            .filter_by(hotel_id=hid, language=row.language)
            .first()
        )

        # STRUCT-025: individual guest reviews
        individual_review_rows = (
            session.query(HotelIndividualReview)
            .filter_by(hotel_id=hid, language=row.language)
            .order_by(HotelIndividualReview.id)
            .all()
        )

        # BUG-API-MAIN-001-FIX (Build 84): 5 satellite tables populated but never
        # queried in this endpoint — their data was invisible to API consumers.
        # Same silent-discard pattern as BUG-PERSIST-001/002/003 on the write side.

        # STRUCT-013: fine print HTML block
        fine_print_row = (
            session.query(HotelFinePrint)
            .filter_by(hotel_id=hid, language=row.language)
            .first()
        )

        # STRUCT-014: all services / facilities (full list)
        all_service_rows = (
            session.query(HotelAllService)
            .filter_by(hotel_id=hid, language=row.language)
            .order_by(HotelAllService.id)
            .all()
        )

        # STRUCT-015: FAQ question/answer pairs
        faq_rows = (
            session.query(HotelFAQ)
            .filter_by(hotel_id=hid, language=row.language)
            .order_by(HotelFAQ.id)
            .all()
        )

        # STRUCT-016: guest review category scores (Cleanliness, Comfort, etc.)
        guest_review_rows = (
            session.query(HotelGuestReview)
            .filter_by(hotel_id=hid, language=row.language)
            .order_by(HotelGuestReview.id)
            .all()
        )

        # STRUCT-017: property highlights (category + detail pairs)
        highlight_rows = (
            session.query(HotelPropertyHighlights)
            .filter_by(hotel_id=hid, language=row.language)
            .order_by(HotelPropertyHighlights.id)
            .all()
        )

        return {
            "id": str(row.id),
            "url": row.url,
            "name": row.hotel_name,
            "address_city": row.address_city,      # STRUCT-011 (v52): renombrado desde city
            # STRUCT-012 (v52): country eliminado — address_country es la fuente canónica
            "language": row.language,
            "latitude": row.latitude,
            "longitude": row.longitude,
            "street_address": row.street_address,
            "address_locality": row.address_locality,
            "address_country": row.address_country,
            "postal_code": row.postal_code,
            "star_rating": row.star_rating,
            "review_score": row.review_score,
            "review_count": row.review_count,
            "rating_value": row.rating_value,
            "best_rating": row.best_rating,
            "main_image_url": row.main_image_url,
            "short_description": row.short_description,
            # GAP-EXTRACT-001-FIX (v76 patch)
            "accommodation_type": row.accommodation_type,
            # STRUCT-019/020 (v76)
            "price_range": row.price_range,
            "rooms_quantity": row.rooms_quantity,
            # STRUCT-001
            "description": desc_row.description if desc_row else None,
            # STRUCT-008
            "popular_services": [p.popular_service for p in popular_rows],
            # STRUCT-006
            "policies": [
                {"policy_name": p.policy_name, "policy_details": p.policy_details}
                for p in policy_rows
            ],
            # STRUCT-007
            "legal": {
                "legal": legal_row.legal,
                "legal_info": legal_row.legal_info,
                "legal_details": legal_row.legal_details,
            } if legal_row else None,
            # STRUCT-021 (v76)
            "extra_info": extra_info_row.extra_info if extra_info_row else None,
            # STRUCT-022 (v76)
            # BUG-API-MAIN-002-FIX (Build 84): category_code added to nearby_places dict.
            # The field exists in the model and is written by _upsert_hotel_nearby_places()
            # but was never included in the API response.
            "nearby_places": [
                {
                    "place_name":    p.place_name,
                    "distance":      p.distance,
                    "category":      p.category,
                    "category_code": p.category_code,
                }
                for p in nearby_rows
            ],
            # STRUCT-023 (v76)
            "room_types": [
                {
                    "room_name":   r.room_name,
                    "description": r.description,
                    "facilities":  r.facilities or [],
                    "adults":      r.adults,
                    "children":    r.children,
                    "images":      r.images or [],
                    "info":        r.info,
                }
                for r in room_type_rows
            ],
            # STRUCT-024 (v76)
            "seo": {
                "seo_description": seo_row.seo_description,
                "keywords":        seo_row.keywords,
            } if seo_row else None,
            # STRUCT-025 (v76 patch)
            "individual_reviews": [
                {
                    "reviewer_name":    r.reviewer_name,
                    "score":            float(r.score) if r.score is not None else None,
                    "title":            r.title,
                    "positive_comment": r.positive_comment,
                    "negative_comment": r.negative_comment,
                    "reviewer_country": r.reviewer_country,
                    "booking_id":       r.booking_id,
                }
                for r in individual_review_rows
            ],
            # BUG-API-MAIN-001-FIX (Build 84): 5 tables previously invisible in API response.
            # STRUCT-013: fine print
            "fine_print": fine_print_row.fp if fine_print_row else None,
            # STRUCT-014: all services/facilities (with category)
            "all_services": [
                {
                    "service":          s.service,
                    "service_category": s.service_category,
                }
                for s in all_service_rows
            ],
            # STRUCT-015: FAQs
            "faqs": [
                {
                    "ask":    f.ask,
                    "answer": f.answer,
                }
                for f in faq_rows
            ],
            # STRUCT-016: guest review category scores
            "guest_reviews": [
                {
                    "reviews_categories": g.reviews_categories,
                    "reviews_score":      g.reviews_score,
                }
                for g in guest_review_rows
            ],
            # STRUCT-017: property highlights
            "property_highlights": [
                {
                    "highlight_category": h.highlight_category,
                    "highlight_detail":   h.highlight_detail,
                }
                for h in highlight_rows
            ],
            "scrape_engine": row.scrape_engine,
            "created_at": row.created_at.isoformat(),
            "updated_at": row.updated_at.isoformat(),
        }


# ---------------------------------------------------------------------------
# API Payload Builder — GAP-API-001-FIX (Build 85)
# ---------------------------------------------------------------------------

@app.get(
    "/hotels/url/{url_id}/api-payload",
    tags=["Hotels"],
    summary="Build API payload from DB records (format: _API_.md)",
    dependencies=[Depends(_check_api_key)],
)
def get_hotel_api_payload(url_id: str) -> Dict[str, Any]:
    """
    Construye y devuelve el payload JSON completo en formato _API_.md para
    una URL de hotel identificada por **url_id**.

    Agrega datos de 14 tablas de la base de datos, aplica todas las
    transformaciones de campos requeridas y devuelve una estructura multilingual
    lista para consumo externo.

    **Estructura de respuesta:**
    ```json
    {
      "data": {
        "name":   {"en": "...", "es": "..."},
        "rating": 4,
        "geoPosition": {"latitude": 41.1, "longitude": 20.7},
        "services":   {"en": [...], "es": [...]},
        ...
      },
      "args": {
        "locales": ["en", "es", "de", "fr", "it", "pt"],
        ...
      }
    }
    ```

    **Errores:**
    - `400` — url_id con formato UUID inválido
    - `404` — No existen registros hotels para este url_id
    - `500` — Error interno durante la construcción del payload
    """
    # GAP-API-001-FIX (Build 85): endpoint nuevo — delega en ApiPayloadBuilder
    try:
        uid = uuid.UUID(url_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format for url_id.")

    try:
        with get_db() as session:
            builder = ApiPayloadBuilder(session)
            payload = builder.build_payload(uid)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        logger.exception("ApiPayloadBuilder failed for url_id=%s: %s", url_id, exc)
        raise HTTPException(
            status_code=500,
            detail=f"Internal error building API payload: {exc}",
        )

    return payload


# ---------------------------------------------------------------------------
# Audit Logs — centralised download for operational audit
# ---------------------------------------------------------------------------

@app.get(
    "/logs/audit",
    tags=["System"],
    summary="Download audit log",
    dependencies=[Depends(_check_api_key)],
)
def download_audit_log(
    format: str = "csv",
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    event_type: Optional[str] = None,
    status_filter: Optional[str] = None,
    url_id: Optional[str] = None,
    limit: int = 10000,
) -> Response:
    """
    Download a centralised audit log combining scraping events, URL queue
    states, and hotel extraction results.

    **Parameters:**
    - `format`: `csv` (default) or `json`
    - `date_from` / `date_to`: ISO date strings e.g. `2026-03-01`
    - `event_type`: filter by event type (`scrape_failed`, `scrape_success`, `upsert_failed`)
    - `status_filter`: filter by status (`done`, `error`, `processing`, `pending`)
    - `url_id`: filter by specific URL UUID
    - `limit`: max rows (default 10 000)

    **Returns:** downloadable file attachment (`audit_log.csv` or `audit_log.json`).

    **Columns:** event_id, scraped_at, url_id, hotel_id, url, language,
    event_type, status, duration_ms, error_message, url_status, retry_count,
    hotel_name, address_city, review_score
    """
    # ── Validate format ───────────────────────────────────────────────────────
    if format not in ("csv", "json"):
        raise HTTPException(status_code=400, detail="format must be 'csv' or 'json'")

    # ── Validate limit ────────────────────────────────────────────────────────
    if limit > 100_000:
        raise HTTPException(status_code=400, detail="limit cannot exceed 100 000")

    # ── Build query ───────────────────────────────────────────────────────────
    conditions = []
    params: Dict[str, Any] = {}

    if date_from:
        try:
            datetime.fromisoformat(date_from)
            conditions.append("sl.scraped_at >= :date_from")
            params["date_from"] = date_from
        except ValueError:
            raise HTTPException(status_code=400, detail="date_from must be ISO format: YYYY-MM-DD")

    if date_to:
        try:
            datetime.fromisoformat(date_to)
            conditions.append("sl.scraped_at < :date_to")
            params["date_to"] = date_to
        except ValueError:
            raise HTTPException(status_code=400, detail="date_to must be ISO format: YYYY-MM-DD")

    if event_type:
        conditions.append("sl.event_type = :event_type")
        params["event_type"] = event_type

    if status_filter:
        conditions.append("sl.status = :status_filter")
        params["status_filter"] = status_filter

    if url_id:
        try:
            uuid.UUID(url_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="url_id must be a valid UUID")
        conditions.append("sl.url_id = :url_id")
        params["url_id"] = url_id

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    params["limit"] = limit

    sql = text(f"""
        SELECT
            sl.id              AS event_id,
            sl.scraped_at      AS scraped_at,
            sl.url_id          AS url_id,
            sl.hotel_id        AS hotel_id,
            uq.url             AS url,
            sl.language        AS language,
            sl.event_type      AS event_type,
            sl.status          AS status,
            sl.duration_ms     AS duration_ms,
            sl.error_message   AS error_message,
            uq.status          AS url_queue_status,
            uq.retry_count     AS retry_count,
            h.hotel_name       AS hotel_name,
            h.address_city     AS address_city,
            h.review_score     AS review_score
        FROM scraping_logs sl
        LEFT JOIN url_queue  uq ON uq.id = sl.url_id
        LEFT JOIN hotels     h  ON h.id  = sl.hotel_id
        {where_clause}
        ORDER BY sl.scraped_at DESC
        LIMIT :limit
    """)

    with get_db() as session:
        rows = session.execute(sql, params).fetchall()

    if not rows:
        if format == "json":
            return Response(
                content='{"rows": [], "total": 0}',
                media_type="application/json",
                headers={"Content-Disposition": "attachment; filename=audit_log.json"},
            )
        else:
            return Response(
                content="event_id,scraped_at,url_id,hotel_id,url,language,event_type,status,duration_ms,error_message,url_queue_status,retry_count,hotel_name,address_city,review_score\n",
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=audit_log.csv"},
            )

    columns = [
        "event_id", "scraped_at", "url_id", "hotel_id", "url", "language",
        "event_type", "status", "duration_ms", "error_message",
        "url_queue_status", "retry_count", "hotel_name", "address_city", "review_score",
    ]

    # ── Serialise ─────────────────────────────────────────────────────────────
    if format == "json":
        data = []
        for row in rows:
            record = {}
            for col, val in zip(columns, row):
                if hasattr(val, "isoformat"):
                    record[col] = val.isoformat()
                elif val is None:
                    record[col] = None
                else:
                    record[col] = str(val)
            data.append(record)
        body = json.dumps({"rows": data, "total": len(data)}, ensure_ascii=False, indent=2)
        return Response(
            content=body,
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=audit_log.json"},
        )

    else:  # CSV
        buf = io.StringIO()
        writer = csv.writer(buf, lineterminator="\n")
        writer.writerow(columns)
        for row in rows:
            writer.writerow([
                v.isoformat() if hasattr(v, "isoformat") else ("" if v is None else str(v))
                for v in row
            ])
        return Response(
            content=buf.getvalue(),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": "attachment; filename=audit_log.csv"},
        )


@app.get(
    "/logs/audit/summary",
    tags=["System"],
    summary="Audit log summary statistics",
    dependencies=[Depends(_check_api_key)],
)
def audit_log_summary() -> Dict[str, Any]:
    """
    Returns summary statistics for the audit log:
    total events, breakdown by event_type and status, last 24h counts,
    average scrape duration, top error messages.
    """
    with get_db() as session:
        # Event type breakdown
        event_counts = session.execute(text(
            "SELECT event_type, COUNT(*) FROM scraping_logs GROUP BY event_type"
        )).fetchall()

        # Status breakdown
        status_counts = session.execute(text(
            "SELECT status, COUNT(*) FROM scraping_logs GROUP BY status"
        )).fetchall()

        # Last 24h
        last_24h = session.execute(text(
            "SELECT COUNT(*) FROM scraping_logs "
            "WHERE scraped_at >= NOW() - INTERVAL \'24 hours\'"
        )).scalar() or 0

        # Average duration
        avg_dur = session.execute(text(
            "SELECT ROUND(AVG(duration_ms)::numeric, 0) FROM scraping_logs WHERE duration_ms IS NOT NULL"
        )).scalar()

        # Top 10 error messages — LEFT(error_message,500) agrupa por origen
        # sin fragmentar por stack traces distintos del mismo error
        top_errors = session.execute(text(
            "SELECT LEFT(error_message, 500) AS msg, COUNT(*) AS cnt "
            "FROM scraping_logs "
            "WHERE error_message IS NOT NULL AND TRIM(error_message) != '' "
            "GROUP BY LEFT(error_message, 500) ORDER BY cnt DESC LIMIT 10"
        )).fetchall()

        # URL queue summary
        url_summary = session.execute(text(
            "SELECT status, COUNT(*) FROM url_queue GROUP BY status"
        )).fetchall()

        # Hotels count
        hotel_count = session.execute(text("SELECT COUNT(*) FROM hotels")).scalar() or 0

    return {
        "hotels_total":     hotel_count,
        "events_by_type":   {k: v for k, v in event_counts},
        "events_by_status": {k: v for k, v in status_counts},
        "events_last_24h":  last_24h,
        "avg_duration_ms":  int(avg_dur) if avg_dur else None,
        "top_errors":       [{"message": m[:200], "count": c} for m, c in top_errors],
        "url_queue":        {k: v for k, v in url_summary},
    }



# ---------------------------------------------------------------------------
# API Export endpoints (Build 92 — STRUCT-EXPORT-003)
#
# Redesign: panel HTML de usuario servido en /export/ui.
# Nuevos endpoints orientados a external_ref (ID del sistema externo),
# que es el identificador que el usuario ve y maneja.
#
# Menú en /docs (tag "Export"):
#   GET  /export/ui                → panel HTML de exportación para el usuario
#   GET  /export/config            → ver configuración actual de la API externa
#   POST /export/config            → actualizar credenciales en tiempo de ejecución
#   GET  /export/resolve           → resolver external_ref → url_id + estado idiomas
#   POST /export/preview/refs      → dry-run por lista de external_ref
#   POST /export/send/refs         → enviar por lista de external_ref
#   POST /export/send/csv          → enviar desde archivo CSV (columna external_ref)
#   GET  /export/preview/{url_id}  → dry-run por url_id interno (compatibilidad)
#   GET  /export/preview           → dry-run todos los hoteles completados
#   POST /export/send/{url_id}     → enviar por url_id interno (compatibilidad)
#   POST /export/send              → enviar todos los hoteles completados
# ---------------------------------------------------------------------------

# ── Pydantic bodies ──────────────────────────────────────────────────────────

class ExportConfigBody(BaseModel):
    """Cuerpo para actualizar credenciales de la API externa en tiempo de ejecución."""
    ext_api_base_url: str = Field(
        ...,
        example="https://web.com/api",
        description="URL base de la API externa (ej. https://web.com/api)",
    )
    ext_api_key: str = Field(
        ...,
        example="543-clave-api",
        description="Clave de autenticación de la API externa",
    )
    ext_api_default_languages: str = Field(
        default="en,es",
        example="en,es",
        description="Idiomas por defecto separados por coma (en siempre incluido)",
    )


class ExportSendBody(BaseModel):
    """Cuerpo para personalizar una exportación (todos los parámetros opcionales)."""
    languages: Optional[str] = Field(
        default=None,
        example="en,es",
        description="Idiomas a incluir separados por coma. NULL = usar EXT_API_DEFAULT_LANGUAGES",
    )
    fields: Optional[str] = Field(
        default=None,
        example="name,address,scoreReview,images,categoryScoreReview",
        description="Campos a incluir separados por coma. NULL = campos recomendados",
    )
    dry_run: bool = Field(
        default=False,
        description="true = generar payload sin enviar a la API externa",
    )



class ExportByRefsBody(BaseModel):
    """
    Cuerpo para exportar/previsualizar por lista de external_ref.

    STRUCT-EXPORT-003 (Build 92): el usuario identifica los hoteles por
    external_ref (ID del sistema externo), no por url_id interno.
    El backend resuelve external_ref → url_id antes de procesar.

    Regla de negocio: hoteles con idiomas incompletos son excluidos
    automáticamente; nunca se envían a la API.
    """
    external_refs: List[str] = Field(
        ...,
        example=["77643", "78615", "78575"],
        description="Lista de external_ref a exportar",
    )
    languages: Optional[str] = Field(
        default=None,
        example="en,es",
        description="Idiomas separados por coma. NULL = usar EXT_API_DEFAULT_LANGUAGES",
    )
    fields: Optional[str] = Field(
        default=None,
        example="name,address,scoreReview,images,categoryScoreReview",
        description="Campos separados por coma. NULL = campos recomendados",
    )
    dry_run: bool = Field(
        default=False,
        description="true = generar payload sin enviar a la API externa",
    )



# ── GET /export/ui ────────────────────────────────────────────────────────────

@app.get(
    "/export/ui",
    tags=["Export"],
    summary="Panel HTML de exportación para el usuario",
    response_class=HTMLResponse,
)
def export_ui_page() -> HTMLResponse:
    """
    Sirve el panel HTML de exportación de datos a la API externa.

    Acceso: **http://localhost:8000/export/ui**

    El panel permite al usuario:
    - Seleccionar hoteles por `external_ref` (individual, lista, CSV)
    - Configurar qué campos incluir en el payload
    - Visualizar el payload antes de enviar (dry-run)
    - Enviar los datos a la API externa

    No requiere autenticación Bearer — el panel llama internamente
    a los endpoints de exportación.
    """
    return HTMLResponse(content=build_export_ui_html(), status_code=200)


# ── GET /export/resolve ───────────────────────────────────────────────────────

@app.get(
    "/export/resolve",
    tags=["Export"],
    summary="Resolver external_ref a url_id con estado de idiomas",
    dependencies=[Depends(_check_api_key)],
)
def export_resolve(
    refs: Optional[str] = None,
    mode: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convierte una lista de `external_ref` a sus `url_id` internos y devuelve
    el estado de completitud de idiomas para cada hotel.

    **Uso desde el panel UI:**
    - `?refs=77643,78615,78575` — lista separada por comas
    - `?mode=all`               — todos los hoteles con status=done

    **Respuesta por hotel:**
    - `external_ref`    — ID del sistema externo
    - `found`           — si el external_ref existe en url_queue
    - `url_id`          — UUID interno (null si not found)
    - `hotel_name`      — nombre del hotel en inglés
    - `languages_done`  — idiomas con status=done en url_language_status
    - `is_complete`     — true si los 6 idiomas (en,es,de,fr,it,pt) están done

    **Regla de negocio:** solo los hoteles con `is_complete=true` son
    aptos para exportación. Los incompletos nunca se envían a la API.
    """
    ALL_LANGS = ["en", "es", "de", "fr", "it", "pt"]

    with get_db() as session:
        if mode == "all":
            rows = session.query(URLQueue).filter(URLQueue.status == "done").all()
            ref_list = [r.external_ref for r in rows if r.external_ref]
        elif refs:
            ref_list = [r.strip() for r in refs.split(",") if r.strip()]
        else:
            return {"hotels": [], "total": 0}

        hotels = _resolve_external_refs(session, ref_list, ALL_LANGS)

    return {
        "hotels": hotels,
        "total": len(hotels),
        "valid": sum(1 for h in hotels if h["is_complete"]),
        "excluded": sum(1 for h in hotels if h["found"] and not h["is_complete"]),
        "not_found": sum(1 for h in hotels if not h["found"]),
    }


# ── POST /export/preview/refs ─────────────────────────────────────────────────

@app.post(
    "/export/preview/refs",
    tags=["Export"],
    summary="Vista previa del payload por lista de external_ref (dry run)",
    dependencies=[Depends(_check_api_key)],
)
def export_preview_by_refs(body: ExportByRefsBody) -> Dict[str, Any]:
    """
    Genera y devuelve el payload de cada hotel indicado por `external_ref`
    **sin enviarlo** a la API externa.

    Hoteles con idiomas incompletos son excluidos automáticamente.

    **Body:**
    - `external_refs` — lista de external_ref (obligatorio)
    - `languages`     — idiomas separados por coma (defecto: `EXT_API_DEFAULT_LANGUAGES`)
    - `fields`        — campos a incluir (defecto: todos los recomendados)
    - `dry_run`       — debe ser `true` para este endpoint

    **Respuesta:**
    - `results[]` — un objeto por hotel con `external_ref`, `hotel_name`,
      `url_id`, `payload`, `validation_errors`, `status`, `reason`
    - `summary`   — totales: total, success, skipped, failed
    """
    from app.api_export_system import APIConfig, APIExporter, APIField, ExportSelection, ExportTemplate
    ALL_LANGS = ["en", "es", "de", "fr", "it", "pt"]
    cfg        = get_settings()
    lang_list  = _parse_languages(body.languages, cfg)
    field_list = _parse_fields(body.fields)
    template   = ExportTemplate(name="preview_refs", fields=field_list, languages=lang_list)
    api_config = APIConfig()

    with get_db() as session:
        resolved = _resolve_external_refs(session, body.external_refs, ALL_LANGS)
        results  = []

        for h in resolved:
            if not h["found"]:
                results.append({
                    "external_ref": h["external_ref"],
                    "hotel_name":   None,
                    "url_id":       None,
                    "status":       "error",
                    "reason":       f"external_ref '{h['external_ref']}' no encontrado en url_queue",
                    "payload":      None,
                    "validation_errors": [],
                })
                continue

            if not h["is_complete"]:
                results.append({
                    "external_ref": h["external_ref"],
                    "hotel_name":   h["hotel_name"],
                    "url_id":       h["url_id"],
                    "status":       "skip",
                    "reason":       f"Idiomas incompletos: completados={h['languages_done']}",
                    "payload":      None,
                    "validation_errors": [],
                })
                continue

            uid = UUID(h["url_id"])
            sel = ExportSelection()
            sel.add_url_id(uid)
            res = APIExporter(session, api_config, template, sel).export_single(uid, dry_run=True)
            results.append({
                "external_ref":      h["external_ref"],
                "hotel_name":        h["hotel_name"],
                "url_id":            h["url_id"],
                "status":            "error" if res.get("error") else "ok",
                "reason":            res.get("error"),
                "payload":           res.get("payload"),
                "validation_errors": res.get("validation_errors", []),
            })

    ok      = sum(1 for r in results if r["status"] == "ok")
    skipped = sum(1 for r in results if r["status"] == "skip")
    failed  = sum(1 for r in results if r["status"] == "error")
    return {
        "results": results,
        "summary": {
            "total":   len(results),
            "success": ok,
            "skipped": skipped,
            "failed":  failed,
            "dry_run": True,
        },
    }


# ── POST /export/send/refs ────────────────────────────────────────────────────

@app.post(
    "/export/send/refs",
    tags=["Export"],
    summary="Enviar a la API externa por lista de external_ref",
    dependencies=[Depends(_check_api_key)],
)
def export_send_by_refs(body: ExportByRefsBody) -> Dict[str, Any]:
    """
    Envía los datos de cada hotel indicado por `external_ref` a la API externa.

    Hoteles con idiomas incompletos son excluidos automáticamente y
    aparecen en `results` con `status=skip`.

    **Requisito previo:** credenciales configuradas en `.env`
    (`EXT_API_BASE_URL` + `EXT_API_KEY`) o via `POST /export/config`.

    **Body:**
    - `external_refs` — lista de external_ref (obligatorio)
    - `languages`     — idiomas (defecto: `EXT_API_DEFAULT_LANGUAGES`)
    - `fields`        — campos a incluir (defecto: todos los recomendados)
    - `dry_run`       — `false` para envío real; `true` equivale a preview/refs

    **Respuesta:**
    - `results[]`    — estado por hotel: status=ok/skip/error, response_status HTTP
    - `summary`      — totales: total, success, skipped, failed
    """
    from app.api_export_system import APIConfig, APIExporter, APIField, ExportSelection, ExportTemplate
    ALL_LANGS = ["en", "es", "de", "fr", "it", "pt"]
    cfg       = get_settings()
    base      = getattr(cfg, "EXT_API_BASE_URL", "")
    key       = getattr(cfg, "EXT_API_KEY", "")

    if not body.dry_run and (not base or not key):
        raise HTTPException(
            status_code=400,
            detail="EXT_API_BASE_URL y EXT_API_KEY no configurados. "
                   "Edita .env o usa POST /export/config.",
        )

    lang_list  = _parse_languages(body.languages, cfg)
    field_list = _parse_fields(body.fields)
    template   = ExportTemplate(name="send_refs", fields=field_list, languages=lang_list)
    api_config = APIConfig(base_url=base or "dry", api_key=key or "dry")

    with get_db() as session:
        resolved = _resolve_external_refs(session, body.external_refs, ALL_LANGS)
        results  = []

        for h in resolved:
            if not h["found"]:
                results.append({
                    "external_ref":  h["external_ref"],
                    "hotel_name":    None,
                    "url_id":        None,
                    "status":        "error",
                    "reason":        f"external_ref '{h['external_ref']}' no encontrado",
                    "response_status": None,
                })
                continue

            if not h["is_complete"]:
                results.append({
                    "external_ref":  h["external_ref"],
                    "hotel_name":    h["hotel_name"],
                    "url_id":        h["url_id"],
                    "status":        "skip",
                    "reason":        f"Idiomas incompletos: {h['languages_done']}",
                    "response_status": None,
                })
                continue

            uid = UUID(h["url_id"])
            sel = ExportSelection()
            sel.add_url_id(uid)
            res = APIExporter(session, api_config, template, sel).export_single(uid, dry_run=body.dry_run)

            results.append({
                "external_ref":    h["external_ref"],
                "hotel_name":      h["hotel_name"],
                "url_id":          h["url_id"],
                "status":          "error" if res.get("error") else "ok",
                "reason":          res.get("error"),
                "response_status": res.get("response_status"),
            })

    ok      = sum(1 for r in results if r["status"] == "ok")
    skipped = sum(1 for r in results if r["status"] == "skip")
    failed  = sum(1 for r in results if r["status"] == "error")
    return {
        "results": results,
        "summary": {
            "total":   len(results),
            "success": ok,
            "skipped": skipped,
            "failed":  failed,
            "dry_run": body.dry_run,
        },
    }


# ── POST /export/send/csv ─────────────────────────────────────────────────────

@app.post(
    "/export/send/csv",
    tags=["Export"],
    summary="Enviar a la API externa desde archivo CSV (columna external_ref)",
    dependencies=[Depends(_check_api_key)],
)
async def export_send_csv(
    file:      UploadFile = File(..., description="CSV con columna única external_ref"),
    languages: str        = "",
    fields:    str        = "",
    dry_run:   bool       = False,
) -> Dict[str, Any]:
    """
    Parsea un archivo CSV con una columna de `external_ref` y envía cada
    hotel a la API externa.

    **Formato CSV aceptado:**
    - Una columna, un external_ref por fila
    - Con o sin cabecera `external_ref`
    - Separadores: coma, punto y coma, tabulador o nueva línea
    - Ejemplo: `77643\n78615\n78575` ó `77643,78615,78575`

    Hoteles con idiomas incompletos son excluidos automáticamente.

    **Form fields:**
    - `file`      — archivo CSV (obligatorio)
    - `languages` — idiomas separados por coma (vacío = `EXT_API_DEFAULT_LANGUAGES`)
    - `fields`    — campos a incluir (vacío = campos recomendados)
    - `dry_run`   — `false` para envío real

    Internamente delega a `export_send_by_refs` tras parsear el CSV.
    """
    # Read and parse CSV
    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")

    import re as _re
    lines = _re.split(r"[\r\n,;\t]+", text)
    external_refs = [
        ln.strip().strip('"').strip("'")
        for ln in lines
        if ln.strip() and not re.match(r"^external_ref$", ln.strip(), re.IGNORECASE)
    ]

    if not external_refs:
        raise HTTPException(
            status_code=422,
            detail="El CSV no contiene external_ref válidos. "
                   "Formato esperado: una columna, un ID por fila.",
        )

    cfg        = get_settings()
    lang_list  = _parse_languages(languages or None, cfg)
    body       = ExportByRefsBody(
        external_refs=external_refs,
        languages=",".join(lang_list),
        fields=fields or None,
        dry_run=dry_run,
    )
    return export_send_by_refs(body)


# ── GET /export/config ───────────────────────────────────────────────────────

@app.get(
    "/export/config",
    tags=["Export"],
    summary="Ver configuración actual de la API externa",
    dependencies=[Depends(_check_api_key)],
)
def get_export_config() -> Dict[str, Any]:
    """
    Muestra la configuración actual de la API externa leída desde `.env`.

    Para modificar: edita `.env` y reinicia el servidor, o usa
    **POST /export/config** para actualizar en tiempo de ejecución
    (vigente hasta próximo reinicio).

    Estado `ready=true` indica que ambas credenciales están configuradas.
    """
    cfg = get_settings()
    base = getattr(cfg, "EXT_API_BASE_URL", "")
    key  = getattr(cfg, "EXT_API_KEY", "")
    langs = getattr(cfg, "EXT_API_DEFAULT_LANGUAGES", "en,es")
    return {
        "ext_api_base_url":           base or "(no configurado)",
        "ext_api_key":                ("***" + key[-4:]) if len(key) > 4 else ("(no configurado)" if not key else "***"),
        "ext_api_default_languages":  langs,
        "ready":                      bool(base and key),
        "note": "Edita .env para cambiar permanentemente. "
                "Usa POST /export/config para actualizar sin reiniciar.",
    }


# ── POST /export/config ──────────────────────────────────────────────────────

@app.post(
    "/export/config",
    tags=["Export"],
    summary="Actualizar credenciales de la API externa (en tiempo de ejecución)",
    dependencies=[Depends(_check_api_key)],
)
def set_export_config(body: ExportConfigBody) -> Dict[str, Any]:
    """
    Actualiza las credenciales de la API externa **sin reiniciar el servidor**.

    ⚠️ El cambio es **temporal** (en memoria). Para hacerlo permanente,
    edita el archivo `.env`:
    ```
    EXT_API_BASE_URL=https://web.com/api
    EXT_API_KEY=543-clave-api
    EXT_API_DEFAULT_LANGUAGES=en,es
    ```

    Útil para probar credenciales antes de editar `.env`.
    """
    cfg = get_settings()
    object.__setattr__(cfg, "EXT_API_BASE_URL",           body.ext_api_base_url.strip())
    object.__setattr__(cfg, "EXT_API_KEY",                body.ext_api_key.strip())
    object.__setattr__(cfg, "EXT_API_DEFAULT_LANGUAGES",  body.ext_api_default_languages.strip())
    key = body.ext_api_key.strip()
    return {
        "updated": True,
        "ext_api_base_url":          body.ext_api_base_url.strip(),
        "ext_api_key":               ("***" + key[-4:]) if len(key) > 4 else "***",
        "ext_api_default_languages": body.ext_api_default_languages.strip(),
        "note": "Credenciales activas en memoria. Edita .env para hacerlas permanentes.",
    }


# ── GET /export/preview/{url_id} ─────────────────────────────────────────────

@app.get(
    "/export/preview/{url_id}",
    tags=["Export"],
    summary="Vista previa del payload de un hotel (dry run)",
    dependencies=[Depends(_check_api_key)],
)
def export_preview_single(
    url_id: str,
    languages: Optional[str] = None,
    fields:    Optional[str] = None,
) -> Dict[str, Any]:
    """
    Genera y devuelve el payload completo de **un hotel** en formato `_API_.md`
    **sin enviarlo** a la API externa.

    Útil para revisar el payload antes de enviar.

    **Parámetros opcionales:**
    - `languages`: idiomas separados por coma (ej. `en,es`). Por defecto: `EXT_API_DEFAULT_LANGUAGES`
    - `fields`: campos a incluir (ej. `name,address,scoreReview`). Por defecto: todos los recomendados

    **Respuesta incluye:**
    - `payload` — el JSON listo para enviar a la API
    - `hotel_id` — `hotel_id_booking` de Booking.com (usado en la URL de la API)
    - `validation_errors` — lista de campos vacíos o inválidos
    """
    from app.api_export_system import APIConfig, APIExporter, APIField, ExportSelection, ExportTemplate
    cfg = get_settings()
    try:
        uid = UUID(url_id)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"url_id inválido: {url_id}")

    lang_list = _parse_languages(languages, cfg)
    field_list = _parse_fields(fields)

    template = ExportTemplate(name="preview", fields=field_list, languages=lang_list)
    selection = ExportSelection(); selection.add_url_id(uid)
    with get_db() as session:
        result = APIExporter(session, APIConfig(), template, selection).export_single(uid, dry_run=True)
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# ── GET /export/preview ───────────────────────────────────────────────────────

@app.get(
    "/export/preview",
    tags=["Export"],
    summary="Vista previa del payload de todos los hoteles completados (dry run)",
    dependencies=[Depends(_check_api_key)],
)
def export_preview_batch(
    languages: Optional[str] = None,
    fields:    Optional[str] = None,
) -> Dict[str, Any]:
    """
    Genera payloads para **todos los hoteles** con `status=done`
    **sin enviarlos** a la API externa.

    Devuelve resumen con `total`, `success`, `failed` y lista de errores.

    **Parámetros opcionales:**
    - `languages`: idiomas separados por coma. Por defecto: `EXT_API_DEFAULT_LANGUAGES`
    - `fields`: campos a incluir. Por defecto: todos los recomendados
    """
    from app.api_export_system import APIConfig, APIExporter, APIField, ExportSelection, ExportTemplate
    cfg = get_settings()
    lang_list  = _parse_languages(languages, cfg)
    field_list = _parse_fields(fields)
    template   = ExportTemplate(name="preview_batch", fields=field_list, languages=lang_list)
    with get_db() as session:
        selection = ExportSelection.from_db_all_pending(session)
        if not selection.url_ids:
            return {"total": 0, "message": "No hay hoteles con status=done"}
        result = APIExporter(session, APIConfig(), template, selection).export_batch(dry_run=True)
    result["dry_run"] = True
    return result


# ── POST /export/send/{url_id} ────────────────────────────────────────────────

@app.post(
    "/export/send/{url_id}",
    tags=["Export"],
    summary="Enviar UN hotel a la API externa",
    dependencies=[Depends(_check_api_key)],
)
def export_send_single(
    url_id: str,
    body: Optional[ExportSendBody] = None,
) -> Dict[str, Any]:
    """
    Envía los datos de **un hotel** a la API externa usando las credenciales
    configuradas en `.env` (`EXT_API_BASE_URL` + `EXT_API_KEY`).

    **Requisito previo:** configurar credenciales en `.env` o via
    `POST /export/config`.

    **Body (opcional):**
    - `languages`: idiomas a exportar (defecto: `EXT_API_DEFAULT_LANGUAGES`)
    - `fields`: campos a incluir (defecto: campos recomendados)
    - `dry_run`: `false` (defecto) — para previsualizar sin enviar usa `GET /export/preview/{url_id}`
    """
    from app.api_export_system import APIConfig, APIExporter, APIField, ExportSelection, ExportTemplate
    cfg = get_settings()
    base = getattr(cfg, "EXT_API_BASE_URL", "")
    key  = getattr(cfg, "EXT_API_KEY", "")
    if not base or not key:
        raise HTTPException(
            status_code=400,
            detail="EXT_API_BASE_URL y EXT_API_KEY no configurados. "
                   "Edita .env o usa POST /export/config.",
        )
    try:
        uid = UUID(url_id)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"url_id inválido: {url_id}")

    b = body or ExportSendBody()
    lang_list  = _parse_languages(b.languages, cfg)
    field_list = _parse_fields(b.fields)
    template   = ExportTemplate(name="send_single", fields=field_list, languages=lang_list)
    api_config = APIConfig(base_url=base, api_key=key)
    selection  = ExportSelection(); selection.add_url_id(uid)

    with get_db() as session:
        result = APIExporter(session, api_config, template, selection).export_single(uid, dry_run=b.dry_run)
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# ── POST /export/send ─────────────────────────────────────────────────────────

@app.post(
    "/export/send",
    tags=["Export"],
    summary="Enviar TODOS los hoteles completados a la API externa",
    dependencies=[Depends(_check_api_key)],
)
def export_send_batch(body: Optional[ExportSendBody] = None) -> Dict[str, Any]:
    """
    Envía **todos los hoteles** con `status=done` a la API externa usando las
    credenciales configuradas en `.env`.

    **Requisito previo:** configurar credenciales en `.env` o via
    `POST /export/config`.

    **Flujo recomendado:**
    1. `GET /export/config` → verificar credenciales configuradas
    2. `GET /export/preview` → revisar payloads antes de enviar
    3. `POST /export/send` → ejecutar envío

    **Body (opcional):**
    - `languages`: idiomas a exportar (defecto: `EXT_API_DEFAULT_LANGUAGES`)
    - `fields`: campos a incluir (defecto: campos recomendados)
    - `dry_run`: `true` para previsualizar sin enviar (equivale a `GET /export/preview`)
    """
    from app.api_export_system import APIConfig, APIExporter, APIField, ExportSelection, ExportTemplate
    cfg  = get_settings()
    base = getattr(cfg, "EXT_API_BASE_URL", "")
    key  = getattr(cfg, "EXT_API_KEY", "")
    b    = body or ExportSendBody()

    if not b.dry_run and (not base or not key):
        raise HTTPException(
            status_code=400,
            detail="EXT_API_BASE_URL y EXT_API_KEY no configurados. "
                   "Edita .env o usa POST /export/config.",
        )

    lang_list  = _parse_languages(b.languages, cfg)
    field_list = _parse_fields(b.fields)
    template   = ExportTemplate(name="send_batch", fields=field_list, languages=lang_list)
    api_config = APIConfig(base_url=base or "dry", api_key=key or "dry")

    with get_db() as session:
        selection = ExportSelection.from_db_all_pending(session)
        if not selection.url_ids:
            return {"total": 0, "message": "No hay hoteles con status=done"}
        result = APIExporter(session, api_config, template, selection).export_batch(dry_run=b.dry_run)

    return result


# ── Helpers privados ─────────────────────────────────────────────────────────


# ── _resolve_external_refs ────────────────────────────────────────────────────

def _resolve_external_refs(
    session,
    refs: List[str],
    all_langs: List[str],
) -> List[Dict[str, Any]]:
    """
    Convierte una lista de external_ref a objetos con url_id, nombre y
    estado de completitud de idiomas.

    Lógica de completitud:
      - Consulta url_language_status WHERE status='done' para cada url_id.
      - is_complete = True si TODOS los idiomas de all_langs están done.

    Usado por: /export/resolve, /export/preview/refs, /export/send/refs,
               /export/send/csv.
    """
    results: List[Dict[str, Any]] = []

    for ref in refs:
        row = (
            session.query(URLQueue)
            .filter(URLQueue.external_ref == ref)
            .first()
        )

        if not row:
            results.append({
                "external_ref":  ref,
                "found":         False,
                "url_id":        None,
                "hotel_name":    None,
                "languages_done": [],
                "is_complete":   False,
            })
            continue

        lang_rows = (
            session.query(URLLanguageStatus)
            .filter(
                URLLanguageStatus.url_id == row.id,
                URLLanguageStatus.status == "done",
            )
            .all()
        )
        langs_done = [lr.language for lr in lang_rows]
        is_complete = all(lg in langs_done for lg in all_langs)

        hotel = (
            session.query(Hotel)
            .filter(Hotel.url_id == row.id, Hotel.language == "en")
            .first()
        )

        results.append({
            "external_ref":   ref,
            "found":          True,
            "url_id":         str(row.id),
            "hotel_name":     hotel.hotel_name if hotel else None,
            "languages_done": langs_done,
            "is_complete":    is_complete,
        })

    return results


def _parse_languages(languages_str: Optional[str], cfg) -> List[str]:
    if languages_str:
        return [ln.strip() for ln in languages_str.split(",") if ln.strip()]
    default = getattr(cfg, "EXT_API_DEFAULT_LANGUAGES", "en,es")
    return [ln.strip() for ln in default.split(",") if ln.strip()]


def _parse_fields(fields_str: Optional[str]):
    from app.api_export_system import APIField
    if not fields_str:
        return APIField.recommended()
    try:
        return [APIField(f.strip()) for f in fields_str.split(",") if f.strip()]
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Campo inválido: {exc}")

# ---------------------------------------------------------------------------
# Entrypoint (single-worker — Windows 11 desktop deployment)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Windows 11: single worker recommended for desktop deployment
    # Use NSSM or windows_service.py for production service registration
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        workers=1,  # Single worker for Windows desktop — see BUG-002
        log_level="info",
        access_log=True,
    )
