"""
BookingScraper Pro v6.0 - NordVPN Windows Manager
==================================================
Controls NordVPN via its Windows CLI (nordvpn.exe).
Platform : Windows 11 only — uses subprocess to call NordVPN CLI.

Corrections Applied (v46):
- BUG-004 : VPN + multi-worker incompatibility raised at config time (config.py).
            This module documents the single-worker requirement clearly.
- Lock timeout in _vpn_lock_ctx() increased to 60 s and is now configurable.
- Duplicate vpn_manager_factory() definition removed (was defined twice).
"""

from __future__ import annotations

import logging
import subprocess
import sys
import threading
import time
from contextlib import contextmanager
from typing import Generator, Optional

from app.vpn_manager import NullVPNManager, VPNManagerBase

logger = logging.getLogger(__name__)

if sys.platform != "win32":
    logger.warning("vpn_manager_windows imported on non-Windows platform — NordVPN CLI unavailable.")


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────
NORDVPN_EXE      = "nordvpn"     # Must be on PATH; set in Windows System Environment
DEFAULT_LOCK_TIMEOUT = 60        # seconds — increased from 30 to reduce thread exhaustion risk
MAX_CONNECT_WAIT     = 45        # seconds to wait for VPN to become active
POLL_INTERVAL        = 2.0       # seconds between status polls


# ─────────────────────────────────────────────────────────────────────────────
class CircuitBreaker:
    """Simple circuit breaker for VPN operations."""

    FAILURE_THRESHOLD = 5
    RECOVERY_TIMEOUT  = 120.0    # seconds before trying again after open

    def __init__(self) -> None:
        self._failures   = 0
        self._open_since : Optional[float] = None
        self._lock       = threading.Lock()

    @property
    def is_open(self) -> bool:
        with self._lock:
            if self._open_since is None:
                return False
            if time.monotonic() - self._open_since > self.RECOVERY_TIMEOUT:
                logger.info("Circuit breaker: recovery timeout elapsed, resetting")
                self._failures   = 0
                self._open_since = None
                return False
            return True

    def record_success(self) -> None:
        with self._lock:
            self._failures   = 0
            self._open_since = None

    def record_failure(self) -> None:
        with self._lock:
            self._failures += 1
            if self._failures >= self.FAILURE_THRESHOLD:
                self._open_since = time.monotonic()
                logger.error(
                    "VPN circuit breaker OPEN after %d failures", self._failures
                )


# ─────────────────────────────────────────────────────────────────────────────
class NordVPNManager(VPNManagerBase):
    """
    Manage NordVPN via CLI on Windows 11.

    IMPORTANT: NordVPN CLI is not thread-safe.
    Only use with SCRAPER_MAX_WORKERS=1 (enforced by config.py BUG-004 FIX).
    """

    def __init__(self, lock_timeout: float = DEFAULT_LOCK_TIMEOUT) -> None:
        self._lock         = threading.Lock()
        self._lock_timeout = lock_timeout
        self._circuit      = CircuitBreaker()

    # ── Lock context ─────────────────────────────────────────────────────────

    @contextmanager
    def _vpn_lock_ctx(self) -> Generator[None, None, None]:
        """
        Acquire the VPN lock with a configurable timeout.
        BUG-004 related: timeout increased from 30 s to 60 s and is now
        configurable in __init__ to reduce thread-pool exhaustion risk.
        Raises TimeoutError if lock cannot be acquired in time.
        """
        acquired = self._lock.acquire(timeout=self._lock_timeout)
        if not acquired:
            raise TimeoutError(
                f"Could not acquire VPN lock within {self._lock_timeout}s. "
                "Another thread may be stuck in a VPN operation."
            )
        try:
            yield
        finally:
            self._lock.release()

    # ── CLI helpers ──────────────────────────────────────────────────────────

    def _run(self, *args: str, timeout: int = 30) -> tuple[bool, str]:
        """Run nordvpn CLI command; return (success, stdout)."""
        if sys.platform != "win32":
            logger.warning("NordVPN CLI called on non-Windows platform")
            return False, ""
        try:
            result = subprocess.run(
                [NORDVPN_EXE, *args],
                capture_output=True, text=True,
                timeout=timeout,
                creationflags=subprocess.CREATE_NO_WINDOW,  # Windows: no console popup
            )
            output = (result.stdout + result.stderr).strip()
            return result.returncode == 0, output
        except FileNotFoundError:
            logger.error(
                "nordvpn.exe not found. Install NordVPN and ensure it is on PATH."
            )
            return False, "nordvpn.exe not found"
        except subprocess.TimeoutExpired:
            logger.error("nordvpn command timed out after %ds", timeout)
            return False, "timeout"
        except OSError as exc:
            logger.error("OS error running nordvpn: %s", exc)
            return False, str(exc)

    # ── Public API ───────────────────────────────────────────────────────────

    def is_connected(self) -> bool:
        _, output = self._run("status")
        return "connected" in output.lower()

    def get_current_ip(self) -> Optional[str]:
        _, output = self._run("status")
        import re
        m = re.search(r"IP:\s*([\d.]+)", output)
        return m.group(1) if m else None

    def connect(self, country: Optional[str] = None) -> bool:
        if self._circuit.is_open:
            logger.error("VPN circuit breaker is OPEN — skipping connect attempt")
            return False
        try:
            with self._vpn_lock_ctx():
                cmd = ["connect"]
                if country:
                    cmd.append(country.upper())
                ok, out = self._run(*cmd, timeout=MAX_CONNECT_WAIT + 5)
                if not ok:
                    logger.error("VPN connect failed: %s", out)
                    self._circuit.record_failure()
                    return False

                # Poll until actually connected
                deadline = time.monotonic() + MAX_CONNECT_WAIT
                while time.monotonic() < deadline:
                    if self.is_connected():
                        logger.info("VPN connected%s", f" to {country}" if country else "")
                        self._circuit.record_success()
                        return True
                    time.sleep(POLL_INTERVAL)

                logger.error("VPN did not become active within %ds", MAX_CONNECT_WAIT)
                self._circuit.record_failure()
                return False

        except TimeoutError as exc:
            logger.error("VPN lock timeout during connect: %s", exc)
            self._circuit.record_failure()
            return False

    def disconnect(self) -> bool:
        try:
            with self._vpn_lock_ctx():
                ok, out = self._run("disconnect")
                if ok:
                    logger.info("VPN disconnected")
                else:
                    logger.warning("VPN disconnect may have failed: %s", out)
                return ok
        except TimeoutError as exc:
            logger.error("VPN lock timeout during disconnect: %s", exc)
            return False

    def rotate(self, country: Optional[str] = None) -> bool:
        """Disconnect then reconnect to rotate to a new server."""
        logger.info("VPN rotation requested")
        self.disconnect()
        time.sleep(2.0)
        return self.connect(country)
