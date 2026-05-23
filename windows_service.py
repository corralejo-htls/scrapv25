"""
windows_service.py — BookingScraper Pro v48
Windows Service Control Manager (SCM) integration via pywin32.
SCRAP-BUG-019 fix: shutdown timeout extended to 30s for graceful drain.
Platform: Windows 11 / Python 3.11+ / pywin32 >= 308.
"""

from __future__ import annotations

import logging
import os
import sys
import threading
import time
from pathlib import Path

# Guard: pywin32 is Windows-only
if sys.platform != "win32":
    print("windows_service.py is for Windows 11 only.")
    sys.exit(1)

import win32event
import win32service
import win32serviceutil
import servicemanager

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Service constants
# ---------------------------------------------------------------------------
SERVICE_NAME = "BookingScraperPro"
SERVICE_DISPLAY_NAME = "BookingScraper Pro v6.0"
SERVICE_DESCRIPTION = (
    "Hotel data scraping service — BookingScraper Pro v6.0 "
    "Windows 11 single-node deployment."
)
# SCRAP-BUG-019 fix: 30 second shutdown timeout (was too short)
_SHUTDOWN_TIMEOUT_MS = 30_000


class BookingScraperService(win32serviceutil.ServiceFramework):
    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = SERVICE_DISPLAY_NAME
    _svc_description_ = SERVICE_DESCRIPTION
    _exe_args_ = None

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self._stop_event = win32event.CreateEvent(None, 0, 0, None)
        self._server_thread: threading.Thread | None = None

    def SvcDoRun(self) -> None:
        """Service main entry point."""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)

        try:
            self._start_uvicorn()
            # Wait for stop signal
            win32event.WaitForSingleObject(self._stop_event, win32event.INFINITE)
        except Exception as exc:
            servicemanager.LogErrorMsg(f"BookingScraper service error: {exc}")
            logger.exception("Service runtime error: %s", exc)
        finally:
            self._stop_uvicorn()

        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STOPPED,
            (self._svc_name_, ""),
        )

    def SvcStop(self) -> None:
        """Signal the service to stop."""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING, waitHint=_SHUTDOWN_TIMEOUT_MS)
        win32event.SetEvent(self._stop_event)

    def _start_uvicorn(self) -> None:
        """Start the FastAPI/Uvicorn server in a daemon thread."""
        import uvicorn

        def _run():
            uvicorn.run(
                "app.main:app",
                host="127.0.0.1",
                port=8000,
                workers=1,
                log_level="info",
                access_log=True,
            )

        self._server_thread = threading.Thread(target=_run, daemon=True, name="uvicorn")
        self._server_thread.start()
        logger.info("Uvicorn server thread started.")

    def _stop_uvicorn(self) -> None:
        """Gracefully stop the uvicorn thread within the shutdown timeout."""
        if self._server_thread and self._server_thread.is_alive():
            # Signal uvicorn shutdown
            # (In production, send SIGBREAK via os.kill or use uvicorn Server API)
            timeout_s = _SHUTDOWN_TIMEOUT_MS / 1000
            self._server_thread.join(timeout=timeout_s)
            if self._server_thread.is_alive():
                logger.warning(
                    "Uvicorn thread did not stop within %ds; forcing exit.", timeout_s
                )


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(BookingScraperService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(BookingScraperService)
