"""
BookingScraper Pro v6.0 - Celery Application
============================================
Platform : Windows 11 — must run with --pool=threads
           (gevent / prefork not supported on Windows)

Usage:
    celery -A app.celery_app worker --pool=threads --concurrency=4 --loglevel=info
"""

from __future__ import annotations

import logging

from celery import Celery

logger = logging.getLogger(__name__)


def _settings():
    from app.config import get_settings
    return get_settings()


def create_celery() -> Celery:
    cfg = _settings()

    app = Celery(
        "bookingscraper",
        broker        =cfg.CELERY_BROKER_URL,
        backend       =cfg.CELERY_RESULT_BACKEND,
        include       =["app.tasks"],
    )

    app.conf.update(
        # Serialisation
        task_serializer        ="json",
        result_serializer      ="json",
        accept_content         =["json"],
        # Timezone
        timezone               ="UTC",
        enable_utc             =True,
        # Windows-compatible worker settings
        worker_pool            ="threads",       # REQUIRED on Windows
        worker_concurrency     =cfg.SCRAPER_MAX_WORKERS,
        # Task behaviour
        task_acks_late         =True,
        task_reject_on_worker_lost=True,
        task_track_started     =True,
        # Result TTL
        result_expires         =3600,            # 1 hour
        # Retry
        task_max_retries       =3,
        task_default_retry_delay=60,             # seconds
        # Rate limiting (be polite to Booking.com)
        task_default_rate_limit="30/m",
        # Broker connection retry (Windows Memurai may restart)
        broker_connection_retry_on_startup=True,
        broker_connection_retry =True,
        broker_connection_max_retries=10,
    )

    # Beat schedule — periodic maintenance tasks
    app.conf.beat_schedule = {
        "reset-stale-urls": {
            "task"    : "app.tasks.reset_stale_processing_urls",
            "schedule": 300.0,    # every 5 minutes
        },
        "create-log-partitions": {
            "task"    : "app.tasks.ensure_log_partitions",
            "schedule": 86400.0,  # daily
        },
    }

    return app


celery_app = create_celery()
