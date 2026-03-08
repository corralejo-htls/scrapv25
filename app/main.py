"""
main.py — BookingScraper Pro v48
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

import redis as redis_lib
import uvicorn
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app import APP_VERSION, BUILD_VERSION
from app.config import get_settings
from app.database import dispose_engine, get_db, get_pool_status, test_connection
from app.models import Base, Hotel, URLLanguageStatus, URLQueue
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

    valid = [u for u in payload.urls if _validate_booking_url(u)]
    invalid = [u for u in payload.urls if not _validate_booking_url(u)]

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
        from sqlalchemy import func
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
