"""
main.py — BookingScraper Pro v49
Fixes applied:
  SCRAP-BUG-001: Rate limiter uses time-based TTL to bound dictionary growth.
  SCRAP-BUG-003: All POSIX signal references removed; Windows-compatible log rotation used.
  SCRAP-BUG-024: URL validation strengthened with regex + netloc check.
  BUG-002       : force-now lock fallback warns that multi-process mode is unsafe.
  SCRAP-CON-003 : Redis health-check uses shared connection pool (not new conn per call).
  Platform      : Windows 11 / ProactorEventLoop / Windows Defender Firewall port 5432.
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import sys
import threading
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import csv
import io
import redis as redis_lib
import uvicorn
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse
from pydantic import BaseModel, Field

from sqlalchemy import text
from app import APP_VERSION, BUILD_VERSION
from app.config import get_settings
from app.database import dispose_engine, get_db, get_pool_status, test_connection
from app.models import Base, Hotel, ScrapingLog, URLLanguageStatus, URLQueue
from app.scraper_service import ScraperService

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
    import logging.handlers

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
    from urllib.parse import urlunparse
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
    allow_origins=["http://localhost", "http://127.0.0.1"],
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
    valid, invalid = [], []
    for url in payload.urls:
        (_valid if _validate_booking_url(url) else invalid).append(url)  # type: ignore

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


def _url_queue_has_external_ref() -> bool:
    """
    Detecta en tiempo de ejecucion si url_queue.external_ref existe.
    Necesario para compatibilidad entre esquemas v48 y v49.
    """
    try:
        from app.database import _get_engine
        engine = _get_engine()
        cols = [c["name"] for c in sa_inspect(engine).get_columns("url_queue")]
        return "external_ref" in cols
    except Exception:
        return False


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
    - **Format A (new):** `id_externo,url` — no header, first column numeric ID, second column URL
    - **Format B:** column named `url` / `URL` / `urls` / `URLs` — header auto-detected
    - **Format C:** one URL per line, no header

    **Format A example:**
    ```
    1001,https://www.booking.com/hotel/es/melia-fuerteventura.es.html
    1002,https://www.booking.com/hotel/es/riu-palace-tres-islas.es.html
    ```

    **Limits:** 5 MB max file size, 5 000 URLs per upload.
    """
    from sqlalchemy import text  # noqa: PLC0415
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

    # ── Deteccion de formato ──────────────────────────────────────────────────
    # Formato A (nuevo): id_externo,url  — primera columna numerica, segunda URL
    # Formato B: cabecera con columna 'url'/'URL'/'urls'/'URLs'
    # Formato C: columna unica sin cabecera, cada linea es una URL
    # ─────────────────────────────────────────────────────────────────────────

    url_col   = None
    id_col    = None   # columna del id externo (solo formato A)
    start_row = 0

    if all_rows:
        header = [c.strip().lower() for c in all_rows[0]]
        url_col_names = {"url", "urls", "hotel_url", "booking_url", "link", "enlace"}

        # Formato B: cabecera nombrada
        for idx, col in enumerate(header):
            if col in url_col_names:
                url_col   = idx
                start_row = 1
                break

        # Formato A: sin cabecera, primera columna es ID numerico
        if url_col is None and len(all_rows[0]) >= 2:
            first_cell = all_rows[0][0].strip()
            if first_cell.isdigit():
                id_col    = 0
                url_col   = 1
                start_row = 0   # no hay cabecera

    # Formato C: columna unica
    if url_col is None:
        url_col   = 0
        start_row = 0

    raw_pairs: List[Tuple[Optional[str], str]] = []  # (ext_id_or_None, url)
    for row in all_rows[start_row:]:
        if not row:
            continue
        if url_col < len(row):
            candidate = row[url_col].strip().strip('"').strip("'")
            if candidate:
                ext_id = row[id_col].strip() if (id_col is not None and id_col < len(row)) else None
                raw_pairs.append((ext_id, candidate))
        if len(raw_pairs) >= MAX_URLS:
            break

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
    # FIX-CSV-EXT-001: construir el mapa url_normalizada -> ext_id DESPUES de
    # normalizar, no antes. El mapa previo usaba URLs raw como claves y el lookup
    # se hacía con URLs normalizadas → ext_id siempre resultaba None.
    normalized_count = 0
    normalized_pairs: List[Tuple[Optional[str], str]] = []  # (ext_id, url_normalizada)
    for ext_id_raw, u in raw_pairs:
        if _url_has_lang_suffix(u):
            normalized_pairs.append((ext_id_raw, _normalize_booking_url(u)))
            normalized_count += 1
        else:
            normalized_pairs.append((ext_id_raw, u))

    # Validate and build final lookup — claves ya son URLs normalizadas
    url_to_ext: Dict[str, Optional[str]] = {}
    normalized_raw: List[str] = []
    for ext_id_raw, norm_url in normalized_pairs:
        normalized_raw.append(norm_url)
        if norm_url not in url_to_ext:          # primera aparicion gana
            url_to_ext[norm_url] = ext_id_raw

    valid   = [u for u in normalized_raw if _validate_booking_url(u)]
    invalid = [u for u in normalized_raw if not _validate_booking_url(u)]

    has_ext = _url_queue_has_external_ref()

    # FIX-CSV-EXT-002 (BUG-LOAD-001 aplicado al endpoint HTTP):
    # ON CONFLICT (url) DO UPDATE SET external_ref = EXCLUDED.external_ref
    #   WHERE url_queue.external_ref IS NULL
    # Garantiza:
    #   a) URL nueva con ext_id   → INSERT con external_ref
    #   b) URL existente sin ref  → UPDATE external_ref
    #   c) URL existente con ref  → sin cambio (WHERE IS NULL protege)
    #   d) URL nueva sin ext_id   → INSERT sin external_ref (formato C)
    # Se elimina el SELECT previo (session.query.filter_by) porque era innecesario
    # y añadía una round-trip extra a la DB por cada URL.
    inserted = 0
    updated  = 0
    skipped  = 0
    with get_db() as session:
        for url in valid:
            ext_id = url_to_ext.get(url)
            if has_ext:
                if ext_id is not None:
                    result = session.execute(
                        text(
                            "INSERT INTO url_queue (url, base_url, external_ref) "
                            "VALUES (:url, :url, :ext_id) "
                            "ON CONFLICT (url) DO UPDATE "
                            "    SET external_ref = EXCLUDED.external_ref "
                            "WHERE url_queue.external_ref IS NULL "
                            "RETURNING (xmax = 0) AS is_insert"
                        ),
                        {"url": url, "ext_id": ext_id},
                    )
                    row_result = result.fetchone()
                    if row_result is None:
                        skipped += 1          # URL existente con external_ref ya grabado
                    elif row_result[0]:
                        inserted += 1         # INSERT nuevo
                    else:
                        updated += 1          # UPDATE de external_ref NULL → valor
                else:
                    # Formato C o Formato B sin columna id: insertar solo URL
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
            else:
                # Columna external_ref no existe en schema: fallback seguro
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
    # Los {} provocaban TypeError y pérdida del log entry.
    logger.info(
        "load-csv completado — insertadas: %d  external_ref actualizado: %d  "
        "sin cambios: %d  invalidas: %d",
        inserted, updated, skipped, len(invalid),
    )

    return {
        "filename":        file.filename,
        "total_rows":      len(raw_pairs),
        "normalized":      normalized_count,
        "inserted":        inserted,
        "updated_ref":     updated,
        "duplicates":      skipped,
        "invalid":         invalid[:50],
        "invalid_count":   len(invalid),
        "format_detected": "id,url" if id_col is not None else ("header" if start_row == 1 else "url_only"),
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
        result = service.dispatch_batch(url_ids=payload.url_ids, max_workers=workers)
        return {"status": "dispatched", "result": result}
    except Exception as exc:
        logger.exception("force-now scraping failed: %s", exc)
        raise HTTPException(status_code=500, detail="Scraping batch failed. Check logs.")
    finally:
        _release_force_now_lock()


@app.get("/scraping/status", tags=["Scraping"], dependencies=[Depends(_check_api_key)])
def scraping_status() -> Dict[str, Any]:
    with get_db() as session:
        from sqlalchemy import inspect as sa_inspect, func
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
    city: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    with get_db() as session:
        q = session.query(Hotel)
        if language:
            q = q.filter(Hotel.language == language)
        if city:
            q = q.filter(Hotel.city.ilike(f"%{city}%"))
        rows = q.order_by(Hotel.created_at.desc()).offset(offset).limit(limit).all()
    return [
        {
            "id": str(h.id), "name": h.hotel_name, "city": h.city,
            "country": h.country, "language": h.language,
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
        return {
            "id": str(row.id), "url": row.url, "name": row.hotel_name,
            "city": row.city, "country": row.country, "language": row.language,
            "address": row.address, "latitude": row.latitude, "longitude": row.longitude,
            "star_rating": row.star_rating, "review_score": row.review_score,
            "review_count": row.review_count, "description": row.description,
            "amenities": row.amenities, "policies": row.policies,
            "scrape_engine": row.scrape_engine, "created_at": row.created_at.isoformat(),
        }



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
    hotel_name, city, country, review_score
    """
    from sqlalchemy import inspect as sa_inspect, text as sa_text
    from datetime import datetime as dt, timezone

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
            dt.fromisoformat(date_from)
            conditions.append("sl.scraped_at >= :date_from")
            params["date_from"] = date_from
        except ValueError:
            raise HTTPException(status_code=400, detail="date_from must be ISO format: YYYY-MM-DD")

    if date_to:
        try:
            dt.fromisoformat(date_to)
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

    sql = sa_text(f"""
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
            h.city             AS city,
            h.country          AS country,
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
                content="event_id,scraped_at,url_id,hotel_id,url,language,event_type,status,duration_ms,error_message,url_queue_status,retry_count,hotel_name,city,country,review_score\n",
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=audit_log.csv"},
            )

    columns = [
        "event_id", "scraped_at", "url_id", "hotel_id", "url", "language",
        "event_type", "status", "duration_ms", "error_message",
        "url_queue_status", "retry_count", "hotel_name", "city", "country", "review_score",
    ]

    # ── Serialise ─────────────────────────────────────────────────────────────
    if format == "json":
        import json as _json
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
        body = _json.dumps({"rows": data, "total": len(data)}, ensure_ascii=False, indent=2)
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
    from sqlalchemy import inspect as sa_inspect, func, text as sa_text

    with get_db() as session:
        # Event type breakdown
        event_counts = session.execute(sa_text(
            "SELECT event_type, COUNT(*) FROM scraping_logs GROUP BY event_type"
        )).fetchall()

        # Status breakdown
        status_counts = session.execute(sa_text(
            "SELECT status, COUNT(*) FROM scraping_logs GROUP BY status"
        )).fetchall()

        # Last 24h
        last_24h = session.execute(sa_text(
            "SELECT COUNT(*) FROM scraping_logs "
            "WHERE scraped_at >= NOW() - INTERVAL \'24 hours\'"
        )).scalar() or 0

        # Average duration
        avg_dur = session.execute(sa_text(
            "SELECT ROUND(AVG(duration_ms)::numeric, 0) FROM scraping_logs WHERE duration_ms IS NOT NULL"
        )).scalar()

        # Top 10 error messages — LEFT(error_message,500) agrupa por origen
        # sin fragmentar por stack traces distintos del mismo error
        top_errors = session.execute(sa_text(
            "SELECT LEFT(error_message, 500) AS msg, COUNT(*) AS cnt "
            "FROM scraping_logs "
            "WHERE error_message IS NOT NULL AND TRIM(error_message) != '' "
            "GROUP BY LEFT(error_message, 500) ORDER BY cnt DESC LIMIT 10"
        )).fetchall()

        # URL queue summary
        url_summary = session.execute(sa_text(
            "SELECT status, COUNT(*) FROM url_queue GROUP BY status"
        )).fetchall()

        # Hotels count
        hotel_count = session.execute(sa_text("SELECT COUNT(*) FROM hotels")).scalar() or 0

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
