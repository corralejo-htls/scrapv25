"""
BookingScraper Pro v6.0 - Windows Service
==========================================
Registers and runs the FastAPI application as a Windows Service
via the Service Control Manager (SCM) using pywin32.

Platform : Windows 11 only
Requires : pip install pywin32

Usage:
  python windows_service.py install    # Register service
  python windows_service.py start      # Start service
  python windows_service.py stop       # Stop service
  python windows_service.py remove     # Unregister service
  python windows_service.py debug      # Run in console (for testing)
"""

from __future__ import annotations

import logging
import os
import sys
import threading
import time
from pathlib import Path

# Ensure project root on path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

if sys.platform != "win32":
    print("windows_service.py is for Windows 11 only.", file=sys.stderr)
    sys.exit(1)

try:
    import win32event
    import win32service
    import win32serviceutil
    import servicemanager
except ImportError:
    print("pywin32 not installed. Run: pip install pywin32", file=sys.stderr)
    sys.exit(1)

logger = logging.getLogger(__name__)


class BookingScraperService(win32serviceutil.ServiceFramework):
    """
    Windows Service wrapper for BookingScraper Pro FastAPI application.
    Integrates with Windows Service Control Manager for auto-start and
    graceful shutdown.
    """
    _svc_name_         = "BookingScraperPro"
    _svc_display_name_ = "BookingScraper Pro v6.0"
    _svc_description_  = "Booking.com hotel data scraping service"

    def __init__(self, args):
        super().__init__(args)
        self._stop_event  = win32event.CreateEvent(None, 0, 0, None)
        self._server      = None
        self._server_thread: threading.Thread | None = None

    def SvcDoRun(self) -> None:
        """Service main loop — called by SCM when service starts."""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        logger.info("BookingScraper Pro service starting")

        self._start_uvicorn()

        # Wait until stop signal
        win32event.WaitForSingleObject(self._stop_event, win32event.INFINITE)
        self._stop_uvicorn()

        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STOPPED,
            (self._svc_name_, ""),
        )
        logger.info("BookingScraper Pro service stopped")

    def SvcStop(self) -> None:
        """Called by SCM to request graceful shutdown."""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self._stop_event)
        logger.info("Stop signal received")

    def _start_uvicorn(self) -> None:
        """Start Uvicorn in a daemon thread."""
        import uvicorn
        from app.config import get_settings
        cfg = get_settings()

        config = uvicorn.Config(
            "app.main:app",
            host     =cfg.APP_HOST,
            port     =cfg.APP_PORT,
            workers  =1,
            loop     ="asyncio",
            log_level=cfg.LOG_LEVEL.lower(),
        )
        self._server = uvicorn.Server(config)
        self._server_thread = threading.Thread(
            target=self._server.run,
            daemon=True,
            name="uvicorn-main",
        )
        self._server_thread.start()
        logger.info("Uvicorn started on %s:%s", cfg.APP_HOST, cfg.APP_PORT)

    def _stop_uvicorn(self) -> None:
        """Gracefully shut down Uvicorn."""
        if self._server:
            self._server.should_exit = True
        if self._server_thread and self._server_thread.is_alive():
            self._server_thread.join(timeout=15)
        logger.info("Uvicorn stopped")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(BookingScraperService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(BookingScraperService)
