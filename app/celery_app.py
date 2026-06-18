"""
celery_app.py — BookingScraper Pro v6.0.0 Build 127
VERSION-RECONCILE-001 (Build 127): cabecera sincronizada con el BUILD_VERSION canonico (app/__init__.py = 127). Sin cambios funcionales.
Windows 11: Celery uses solo pool (not prefork — multiprocessing on Windows
requires spawn start method, causes issues with SQLAlchemy engines in tests).
Memurai is the recommended Redis-compatible broker for Windows.

BUG-TASK-STORM-001 (Build 115, diagnosis):
  When the worker dies (watchdog os._exit(1)) and the Beat keeps running,
  Redis accumulates one `scrape_pending_urls` message every 30 seconds
  (no TTL on Redis List queue entries — this is by design in Celery/Redis).
  On worker restart, all accumulated messages (300-2700 observed) are consumed
  in a rapid burst (~30s). They all return {status: idle, pending: 0} harmlessly
  but pollute logs and delay the first real scrape tick.
  Fix: start_celery.bat purges queues before each restart (not first start).
  Manual fix available via purge_queues.bat.
  Config: worker_prefetch_multiplier=1 (explicitly set — prevents fetching
  multiple tasks ahead; with pool=solo already implicit but explicit is clearer).
"""

from __future__ import annotations

import sys
from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

cfg = get_settings()

celery_app = Celery(
    "bookingscraper",
    broker=cfg.CELERY_BROKER_URL,
    backend=cfg.CELERY_RESULT_BACKEND,
    include=["app.tasks"],
)

celery_app.conf.update(
    # Serialisation
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    # Timezone
    timezone="UTC",
    enable_utc=True,
    # Windows 11: solo pool avoids multiprocessing issues on desktop
    # For production throughput use: worker_pool="prefork" with if __name__ guard
    worker_pool="solo" if sys.platform == "win32" else "prefork",
    worker_concurrency=1 if sys.platform == "win32" else cfg.SCRAPER_MAX_WORKERS,
    # Task routing (SCRAP-BUG-028 fix)
    task_routes={
        "tasks.ensure_log_partitions": {"queue": "maintenance"},
        "tasks.purge_old_debug_html": {"queue": "maintenance"},
        "tasks.collect_system_metrics": {"queue": "monitoring"},
        "tasks.reset_stale_processing_urls": {"queue": "maintenance"},
    },
    # Queue declarations
    task_default_queue="default",
    # Beat schedule
    beat_schedule={
        "ensure-partitions-daily": {
            "task": "tasks.ensure_log_partitions",
            "schedule": crontab(hour=0, minute=5),
            "kwargs": {"months_ahead": 2},
        },
        "purge-debug-html-hourly": {
            "task": "tasks.purge_old_debug_html",
            "schedule": crontab(minute=30),
        },
        "collect-metrics-every-5min": {
            "task": "tasks.collect_system_metrics",
            "schedule": 300.0,
        },
        "reset-stale-urls-every-30min": {
            "task": "tasks.reset_stale_processing_urls",
            "schedule": 1800.0,
        },
        # ── Auto-scraping ─────────────────────────────────────────────────
        # Comprueba URLs pendientes cada 30 segundos y lanza un batch
        # si hay trabajo. Si el batch anterior sigue activo, el tick
        # se omite silenciosamente (flag Redis con TTL de 280s).
        # Para desactivar: comenta las 4 líneas siguientes.
        "auto-scrape-pending-every-30s": {
            "task": "tasks.scrape_pending_urls",
            "schedule": 30.0,           # segundos
            "options": {"queue": "default"},
        },
    },
    # Reliability
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_track_started=True,
    result_expires=86400,
    broker_connection_retry_on_startup=True,
    # BUG-TASK-STORM-001-FIX (Build 115): explicit prefetch=1.
    # With pool=solo this is already implicit (only 1 task runs at a time),
    # but setting it explicitly prevents Celery from fetching multiple tasks
    # from Redis before the previous one completes — reduces burst consumption
    # of accumulated backlog messages on restart.
    worker_prefetch_multiplier=1,
)
