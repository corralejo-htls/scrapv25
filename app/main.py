"""
BookingScraper Pro v6.0
=======================
FastAPI application entry point for the BookingScraper Pro hotel data system.
Platform : Windows 11 + Uvicorn (ProactorEventLoop)

Corrections Applied (v46):
- BUG-008 : Version string is "6.0.0" everywhere — no more v4.0 / v6.0 drift.
- BUG-020 : POSIX signal handlers (SIGUSR1/SIGUSR2) not available on Windows.
            Log rotation uses RotatingFileHandler; graceful shutdown via
            Uvicorn's built-in Windows CTRL_C_EVENT handling.
"""

from __future__ import annotations

import logging
import logging.handlers
import os
import sys
import time
from pathlib import Path
from typing import Any, Optional
from contextlib import asynccontextmanager
import threading

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# ─────────────────────────────────────────────────────────────────────────────
# Logging setup (BUG-020 FIX: RotatingFileHandler instead of logrotate/SIGUSR)
# ─────────────────────────────────────────────────────────────────────────────

def _configure_logging() -> None:
    from app.config import get_settings
    cfg = get_settings()

    log_dir = cfg.LOG_PATH
    log_dir.mkdir(parents=True, exist_ok=True)

    fmt = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)s [%(threadName)s]: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # File handler — Windows RotatingFileHandler (no logrotate / SIGUSR1)
    fh = logging.handlers.RotatingFileHandler(
        filename   =log_dir / "bookingscraper.log",
        maxBytes   =cfg.LOG_MAX_BYTES,
        backupCount=cfg.LOG_BACKUP_COUNT,
        encoding   ="utf-8",
    )
    fh.setFormatter(fmt)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)

    # Windows Event Log (optional — pywin32 required)
    handlers: list[logging.Handler] = [fh, ch]
    if sys.platform == "win32":
        try:
            nt_handler = logging.handlers.NTEventLogHandler("BookingScraperPro")
            nt_handler.setLevel(logging.WARNING)
            handlers.append(nt_handler)
        except Exception:
            pass  # pywin32 not installed — skip Windows Event Log

    root = logging.getLogger()
    root.setLevel(getattr(logging, cfg.LOG_LEVEL.upper(), logging.INFO))
    for h in handlers:
        root.addHandler(h)


_configure_logging()
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Rate limiting (per-IP)
# ─────────────────────────────────────────────────────────────────────────────
_rate_buckets: dict[str, tuple[float, int]] = {}
_rate_lock    = threading.Lock()
RATE_LIMIT_RPS = 10

def _check_rate_limit(ip: str) -> bool:
    now = time.monotonic()
    with _rate_lock:
        last_ts, count = _rate_buckets.get(ip, (now, 0))
        if now - last_ts >= 1.0:
            _rate_buckets[ip] = (now, 1)
            return True
        if count >= RATE_LIMIT_RPS:
            return False
        _rate_buckets[ip] = (last_ts, count + 1)
        return True


# ─────────────────────────────────────────────────────────────────────────────
# Lifespan (replaces deprecated on_event startup/shutdown)
# ─────────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup / shutdown."""
    from app.config import get_settings
    from app.database import test_connection
    cfg = get_settings()
    logger.info("BookingScraper Pro %s starting — platform: %s", cfg.APP_VERSION, sys.platform)
    cfg.create_directories()
    try:
        test_connection()
    except Exception as exc:
        logger.critical("Database connection failed at startup: %s", exc)
        raise
    logger.info("Startup complete")
    yield
    logger.info("Shutdown complete")


# ─────────────────────────────────────────────────────────────────────────────
# Application
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title      ="BookingScraper Pro",
    description="Booking.com hotel data scraping system — Windows 11 edition",
    version    ="6.0.0",   # BUG-008 FIX: single authoritative version
    docs_url   ="/docs",
    redoc_url  ="/redoc",
    lifespan   =lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins    =["http://localhost", "http://127.0.0.1"],
    allow_methods    =["GET", "POST"],
    allow_headers    =["*"],
    allow_credentials=False,
)


# ─────────────────────────────────────────────────────────────────────────────
# Request models
# ─────────────────────────────────────────────────────────────────────────────

class ScrapeRequest(BaseModel):
    urls     : list[str]      = Field(..., min_length=1, max_length=500)
    languages: list[str]      = Field(default=["en"])
    priority : int            = Field(default=5, ge=1, le=10)


class QueueStatusResponse(BaseModel):
    pending   : int
    processing: int
    done      : int
    error     : int
    skipped   : int
    total     : int


# ─────────────────────────────────────────────────────────────────────────────
# URL validation
# ─────────────────────────────────────────────────────────────────────────────

def validate_and_normalize_booking_url(raw: str) -> Optional[str]:
    """
    Validate a Booking.com hotel URL.
    Returns normalised URL or None if invalid.
    """
    import re
    from urllib.parse import urlparse, urlunparse

    if not raw or not isinstance(raw, str):
        return None
    url = raw.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    if parsed.netloc.replace("www.", "") not in ("booking.com",):
        return None
    if not parsed.path or parsed.path == "/":
        return None

    # Normalise: always https, always www.
    normalised = urlunparse(parsed._replace(
        scheme="https",
        netloc="www.booking.com",
    ))
    return normalised


# ─────────────────────────────────────────────────────────────────────────────
# Dependency
# ─────────────────────────────────────────────────────────────────────────────

async def rate_limit_dep(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")


# ─────────────────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/health", tags=["monitoring"])
async def health_check() -> dict:
    """
    Health check endpoint.
    Returns DB, Redis, and pool status.
    """
    from app.database import get_pool_status, test_connection
    health: dict[str, Any] = {
        "status" : "ok",
        "version": "6.0.0",
        "platform": sys.platform,
    }

    # Database
    try:
        test_connection(max_retries=1)
        health["database"] = "ok"
        health["pool"]     = get_pool_status()
    except Exception as exc:
        health["database"] = f"error: {exc}"
        health["status"]   = "degraded"

    # Redis
    try:
        import redis as _redis
        from app.config import get_settings
        cfg = get_settings()
        r = _redis.Redis(host=cfg.REDIS_HOST, port=cfg.REDIS_PORT, socket_timeout=2)
        r.ping()
        health["redis"] = "ok"
    except Exception as exc:
        health["redis"]  = f"error: {exc}"
        health["status"] = "degraded"

    code = status.HTTP_200_OK if health["status"] == "ok" else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(content=health, status_code=code)


@app.post("/api/scrape", tags=["scraping"],
          dependencies=[Depends(rate_limit_dep)])
async def submit_scrape(req: ScrapeRequest) -> dict:
    """Submit URLs for scraping."""
    from app.database import get_db
    from app.models import URLQueue

    cfg = __import__("app.config", fromlist=["get_settings"]).get_settings()
    valid_langs = set(cfg.ENABLED_LANGUAGES)
    requested_langs = [l for l in req.languages if l in valid_langs]
    if not requested_langs:
        raise HTTPException(status_code=400, detail=f"No valid languages. Valid: {sorted(valid_langs)}")

    normalised_urls: list[str] = []
    rejected: list[str] = []
    for raw in req.urls:
        clean = validate_and_normalize_booking_url(raw)
        if clean:
            normalised_urls.append(clean)
        else:
            rejected.append(raw)

    if not normalised_urls:
        raise HTTPException(status_code=400, detail="No valid Booking.com URLs provided")

    queued = 0
    with get_db() as session:
        for url in normalised_urls:
            for lang in requested_langs:
                try:
                    entry = URLQueue(
                        url      =url,
                        language =lang,
                        priority =req.priority,
                        status   ="pending",
                    )
                    session.add(entry)
                    session.flush()
                    queued += 1
                except Exception:
                    session.rollback()

    return {
        "queued"  : queued,
        "rejected": rejected,
        "languages": requested_langs,
    }


@app.get("/api/queue", response_model=QueueStatusResponse, tags=["monitoring"])
async def queue_status() -> QueueStatusResponse:
    """Return scraping queue status counts."""
    from app.database import get_db
    from sqlalchemy import func as sqlfunc
    from app.models import URLQueue as UQ

    with get_db() as session:
        rows = (
            session.query(UQ.status, sqlfunc.count(UQ.id))
            .group_by(UQ.status)
            .all()
        )
    counts = {r[0]: r[1] for r in rows}
    total  = sum(counts.values())
    return QueueStatusResponse(
        pending   =counts.get("pending",    0),
        processing=counts.get("processing", 0),
        done      =counts.get("done",       0),
        error     =counts.get("error",      0),
        skipped   =counts.get("skipped",    0),
        total     =total,
    )


@app.get("/api/hotels", tags=["data"])
async def list_hotels(
    city    : Optional[str] = Query(None),
    country : Optional[str] = Query(None),
    language: str           = Query("en"),
    limit   : int           = Query(50, ge=1, le=500),
    offset  : int           = Query(0, ge=0),
) -> dict:
    """Query scraped hotels with optional filters."""
    from app.database import get_db
    from app.models import Hotel as HotelModel

    with get_db() as session:
        q = session.query(HotelModel).filter(HotelModel.language == language)
        if city:
            q = q.filter(HotelModel.city.ilike(f"%{city}%"))
        if country:
            q = q.filter(HotelModel.country.ilike(f"%{country}%"))
        total = q.count()
        hotels= q.offset(offset).limit(limit).all()

    return {
        "total"  : total,
        "offset" : offset,
        "limit"  : limit,
        "items"  : [
            {
                "id"          : str(h.id),
                "hotel_name"  : h.hotel_name,
                "city"        : h.city,
                "country"     : h.country,
                "review_score": float(h.review_score) if h.review_score else None,
                "star_rating" : float(h.star_rating)  if h.star_rating  else None,
                "language"    : h.language,
                "scraped_at"  : h.scraped_at.isoformat() if h.scraped_at else None,
            }
            for h in hotels
        ],
    }


@app.get("/api/hotels/{hotel_id}", tags=["data"])
async def get_hotel(hotel_id: str) -> dict:
    """Return full detail for a single hotel."""
    import uuid as _uuid
    from app.database import get_db
    from app.models import Hotel as HotelModel

    try:
        hid = _uuid.UUID(hotel_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid hotel_id format")

    with get_db() as session:
        h = session.query(HotelModel).filter(HotelModel.id == hid).first()
    if not h:
        raise HTTPException(status_code=404, detail="Hotel not found")

    return {
        "id"           : str(h.id),
        "url"          : h.url,
        "language"     : h.language,
        "hotel_name"   : h.hotel_name,
        "hotel_id_ext" : h.hotel_id_ext,
        "star_rating"  : float(h.star_rating)  if h.star_rating  else None,
        "review_score" : float(h.review_score) if h.review_score else None,
        "review_count" : h.review_count,
        "address"      : h.address,
        "city"         : h.city,
        "country"      : h.country,
        "latitude"     : float(h.latitude)  if h.latitude  else None,
        "longitude"    : float(h.longitude) if h.longitude else None,
        "amenities"    : h.amenities,
        "room_types"   : h.room_types,
        "policies"     : h.policies,
        "photos"       : h.photos,
        "scrape_status": h.scrape_status,
        "scrape_engine": h.scrape_engine,
        "scraped_at"   : h.scraped_at.isoformat() if h.scraped_at else None,
    }


@app.get("/api/stats", tags=["monitoring"])
async def scraping_stats() -> dict:
    """Return overall scraping statistics."""
    from app.database import get_db
    from sqlalchemy import func as sqlfunc
    from app.models import Hotel as HotelModel, URLQueue as UQ

    with get_db() as session:
        hotel_count    = session.query(sqlfunc.count(HotelModel.id)).scalar()
        queue_pending  = session.query(sqlfunc.count(UQ.id)).filter(UQ.status == "pending").scalar()
        queue_done     = session.query(sqlfunc.count(UQ.id)).filter(UQ.status == "done").scalar()

    return {
        "hotels_scraped": hotel_count,
        "queue_pending" : queue_pending,
        "queue_done"    : queue_done,
        "version"       : "6.0.0",
    }


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Windows multiprocessing guard
    import multiprocessing
    multiprocessing.freeze_support()

    from app.config import get_settings
    cfg = get_settings()

    uvicorn.run(
        "app.main:app",
        host       =cfg.APP_HOST,
        port       =cfg.APP_PORT,
        workers    =1,               # Windows: single worker with Uvicorn
        loop       ="asyncio",       # ProactorEventLoop on Windows
        log_level  =cfg.LOG_LEVEL.lower(),
        access_log =True,
        reload     =(cfg.APP_ENV == "development"),
    )
