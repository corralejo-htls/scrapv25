"""
celery_app.py — BookingScraper Pro v48
Windows 11: Celery uses prefork pool with spawn start method.
Memurai is the recommended Redis-compatible broker for Windows.
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
    },
    # Reliability
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_track_started=True,
    result_expires=86400,
    broker_connection_retry_on_startup=True,
)
