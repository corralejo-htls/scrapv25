"""
BookingScraper/app/celery_app.py
Celery application factory — BookingScraper Pro
Windows 11 + Python 3.14.3

[FIX BUG-V9-007] This file was completely absent from the repository.
Both app/tasks.py and scripts/verify_system.py import from app.celery_app,
causing ImportError at startup and making the entire Celery task system
inoperative.

USAGE:
    Worker:  celery -A app.celery_app worker --pool=solo --loglevel=info
    Beat:    celery -A app.celery_app beat --loglevel=info
    Status:  celery -A app.celery_app status
"""

from __future__ import annotations

import os
from celery import Celery
from celery.schedules import crontab

# ---------------------------------------------------------------------------
# Read broker/backend from environment directly (avoids importing the full
# settings object here, which would trigger DB connection validation early).
# ---------------------------------------------------------------------------
_BROKER  = os.getenv("CELERY_BROKER_URL",  "redis://localhost:6379/0")
_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
_CONCURRENCY = int(os.getenv("CELERY_WORKER_CONCURRENCY", "1"))

# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
celery_app = Celery(
    "bookingscraper",
    broker=_BROKER,
    backend=_BACKEND,
    include=["app.tasks"],          # auto-discover task module
)

# ---------------------------------------------------------------------------
# Configuration
# [Windows] solo pool is mandatory — multiprocessing is not supported on Win.
# [FIX BUG-V9-007] worker_pool set to 'solo' by default; overridable via CLI.
# ---------------------------------------------------------------------------
celery_app.conf.update(
    # Serialization
    task_serializer          = "json",
    result_serializer        = "json",
    accept_content           = ["json"],
    # Timezone
    timezone                 = "UTC",
    enable_utc               = True,
    # Worker
    worker_pool              = "solo",        # Windows 11 — no fork support
    worker_concurrency       = _CONCURRENCY,
    worker_prefetch_multiplier = 1,           # fair distribution, prevent starvation
    # Task behaviour
    task_acks_late           = True,          # re-queue on worker crash
    task_reject_on_worker_lost = True,        # safety: reject if worker dies mid-task
    task_track_started       = True,          # expose STARTED state to monitoring
    # Result expiry
    result_expires           = 3600,          # 1 hour
    # Broker connection pool
    broker_connection_retry_on_startup = True,
    broker_pool_limit        = 5,
    # Soft / hard time limits (seconds)
    task_soft_time_limit     = 540,
    task_time_limit          = 600,
)

# ---------------------------------------------------------------------------
# Beat schedule
# ---------------------------------------------------------------------------
celery_app.conf.beat_schedule = {
    # Dispatch pending URLs every 30 seconds
    # [FIX BUG-16-018] expires was 25s but schedule is 30s.
    # If the worker is briefly overloaded, the task was published at T+0, expired
    # at T+25, but the worker only picked it up at T+28 — task silently discarded.
    # Fix: expires = schedule × 2 (60s). Allows one full missed cycle before
    # discarding, preventing systematic processing gaps under normal load while
    # still protecting against stale task accumulation during extended outages.
    "process-pending-urls-every-30s": {
        "task":     "app.tasks.process_pending_urls",
        "schedule": 30.0,          # seconds
        "args":     (5,),          # batch_size = 5
        "options":  {"expires": 60},   # 2× schedule — safe margin
    },
    # Save system metrics every 5 minutes
    # [FIX BUG-16-018] expires was 280s (< 300s schedule). Same pattern fixed.
    "save-system-metrics-every-5m": {
        "task":     "app.tasks.save_system_metrics",
        "schedule": 300.0,         # seconds
        "options":  {"expires": 600},  # 2× schedule
    },
    # Clean up old logs daily at 03:00 UTC
    "cleanup-old-logs-daily-03h": {
        "task":     "app.tasks.cleanup_old_logs",
        "schedule": crontab(hour=3, minute=0),
        "args":     (30,),         # days_to_keep = 30
        "options":  {"expires": 3600},
    },
    # [FIX ERR-CONC-001] Reset URLs stuck in 'processing' every 5 minutes.
    # Covers crash recovery: URLs left in 'processing' after a process kill
    # are unblocked without requiring a manual restart.
    "reset-stale-urls-every-5m": {
        "task":     "app.tasks.reset_stale_urls",
        "schedule": 300.0,         # 5 minutes
        "options":  {"expires": 600},
    },
    # [FIX MED-004] Create next month's scraping_logs partition on 1st at 01:00 UTC.
    # Prevents INSERT failures on the first day of each new month.
    "create-next-partition-monthly": {
        "task":     "app.tasks.create_next_partition",
        "schedule": crontab(day_of_month=1, hour=1, minute=0),
        "options":  {"expires": 7200},
    },
}
