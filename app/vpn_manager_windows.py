"""
vpn_manager_windows.py — BookingScraper Pro v48
Fixes applied:
  SCRAP-BUG-010: Subprocess input sanitised; shell=False enforced.
  BUG-108      : Subprocess failures include full stderr/returncode context.
  SCRAP-CON-001: Circuit breaker atomicity improved.
  Platform     : NordVPN CLI on Windows 11; no POSIX signals.
"""

from __future__ import annotations

import logging
import random
import re
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from app.config import _VALID_VPN_COUNTRIES, get_settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# NordVPN CLI path — Windows 11 default
# ---------------------------------------------------------------------------
_NORDVPN_DEFAULT_PATH = Path("C:/Program Files/NordVPN/NordVPN.exe")

# Allowed country name pattern — strict allowlist
_COUNTRY_RE = re.compile(r"^[A-Za-z][A-Za-z_]{1,30}$")


def _validate_country(country: str) -> str:
    """
    Validate VPN country name against canonical list.
    SCRAP-BUG-010 fix: rejects any value not in the approved set.
    """
    if country not in _VALID_VPN_COUNTRIES:
        raise ValueError(
            f"Country '{country}' is not in the approved VPN country list. "
            f"Valid options: {sorted(_VALID_VPN_COUNTRIES)}"
        )
    if not _COUNTRY_RE.match(country):
        raise ValueError(f"Country name '{country}' contains invalid characters.")
    return country


# ---------------------------------------------------------------------------
# Circuit breaker
# ---------------------------------------------------------------------------

@dataclass
class CircuitBreaker:
    """
    Simple circuit breaker for VPN operations.
    State transitions: CLOSED → OPEN (on failures) → HALF-OPEN → CLOSED
    BUG: is_open check + state change made atomic via lock.
    """
    failure_threshold: int = 5
    reset_timeout_s: float = 120.0

    _failures: int = field(default=0, init=False)
    _open_since: Optional[float] = field(default=None, init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    @property
    def is_open(self) -> bool:
        with self._lock:
            return self._is_open_unsafe()

    def _is_open_unsafe(self) -> bool:
        """Check open state WITHOUT acquiring lock (caller must hold lock)."""
        if self._open_since is None:
            return False
        if (time.monotonic() - self._open_since) >= self.reset_timeout_s:
            # Auto-reset to half-open
            self._open_since = None
            self._failures = 0
            return False
        return True

    def record_success(self) -> None:
        with self._lock:
            self._failures = 0
            self._open_since = None

    def record_failure(self) -> None:
        with self._lock:
            self._failures += 1
            if self._failures >= self.failure_threshold and self._open_since is None:
                self._open_since = time.monotonic()
                logger.warning(
                    "VPN circuit breaker OPENED after %d failures.", self._failures
                )

    def try_acquire(self) -> bool:
        """
        Atomically check open state and return True if action is allowed.
        BUG fix: check + conditional as a single atomic operation.
        """
        with self._lock:
            if self._is_open_unsafe():
                return False
            return True


# ---------------------------------------------------------------------------
# VPN Manager
# ---------------------------------------------------------------------------

class NordVPNManager:
    """
    Manages NordVPN rotation via the NordVPN CLI on Windows 11.
    SCRAP-CON-001: Single lock prevents concurrent VPN state changes.
    """

    def __init__(self) -> None:
        self._cfg = get_settings()
        self._lock = threading.Lock()
        self._current_country: Optional[str] = None
        self._circuit_breaker = CircuitBreaker()
        self._nordvpn_path = _NORDVPN_DEFAULT_PATH
        self._last_rotation: float = 0.0

    # ── Public interface ──────────────────────────────────────────────────────

    def connect(self, country: Optional[str] = None) -> bool:
        """Connect to VPN. Returns True on success."""
        if not self._circuit_breaker.try_acquire():
            logger.warning("VPN circuit breaker is OPEN. Skipping connect.")
            return False

        target = country or random.choice(self._cfg.VPN_COUNTRIES)
        try:
            _validate_country(target)
        except ValueError as exc:
            logger.error("VPN connect rejected: %s", exc)
            return False

        with self._lock:
            return self._run_connect(target)

    def disconnect(self) -> bool:
        """Disconnect from VPN. Returns True on success."""
        with self._lock:
            return self._run_disconnect()

    def rotate(self) -> bool:
        """Disconnect and reconnect to a different country."""
        countries = list(self._cfg.VPN_COUNTRIES)
        if self._current_country and self._current_country in countries:
            countries.remove(self._current_country)
        if not countries:
            countries = list(self._cfg.VPN_COUNTRIES)

        new_country = random.choice(countries)
        self.disconnect()
        time.sleep(2)
        return self.connect(new_country)

    def should_rotate(self) -> bool:
        """Check if rotation interval has elapsed."""
        return (time.monotonic() - self._last_rotation) >= self._cfg.VPN_ROTATION_INTERVAL

    def get_current_country(self) -> Optional[str]:
        return self._current_country

    # ── Private helpers ───────────────────────────────────────────────────────

    def _run_connect(self, country: str) -> bool:
        """
        Execute NordVPN connect command.
        BUG-108 fix: captures stderr and returncode for diagnostic logging.
        SCRAP-BUG-010 fix: uses list arguments (shell=False) to prevent injection.
        """
        # Validated above — safe to use as list argument (no shell injection possible)
        cmd = [str(self._nordvpn_path), "-c", f"-g", country]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                shell=False,  # CRITICAL: shell=False prevents injection
                check=False,  # We handle returncode manually
            )

            if result.returncode == 0:
                self._current_country = country
                self._last_rotation = time.monotonic()
                self._circuit_breaker.record_success()
                logger.info("VPN connected to %s", country)
                return True
            else:
                # BUG-108 fix: include returncode and stderr in log
                logger.error(
                    "NordVPN connect failed: country=%s returncode=%d stderr=%r stdout=%r",
                    country, result.returncode,
                    result.stderr[:500] if result.stderr else "",
                    result.stdout[:200] if result.stdout else "",
                )
                self._circuit_breaker.record_failure()
                return False

        except subprocess.TimeoutExpired:
            logger.error("NordVPN connect timed out for country=%s", country)
            self._circuit_breaker.record_failure()
            return False
        except FileNotFoundError:
            logger.error(
                "NordVPN executable not found at %s. "
                "Install NordVPN or set VPN_ENABLED=false.",
                self._nordvpn_path,
            )
            self._circuit_breaker.record_failure()
            return False
        except OSError as exc:
            logger.error(
                "NordVPN subprocess error: [%s] %s", type(exc).__name__, exc
            )
            self._circuit_breaker.record_failure()
            return False

    def _run_disconnect(self) -> bool:
        cmd = [str(self._nordvpn_path), "-d"]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                shell=False,
                check=False,
            )
            if result.returncode == 0:
                self._current_country = None
                logger.info("VPN disconnected.")
                return True
            else:
                logger.warning(
                    "NordVPN disconnect returned code %d: stderr=%r",
                    result.returncode, result.stderr[:200] if result.stderr else "",
                )
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:
            logger.error("VPN disconnect failed: [%s] %s", type(exc).__name__, exc)
            return False


# ---------------------------------------------------------------------------
# Null VPN manager (when VPN_ENABLED=false)
# ---------------------------------------------------------------------------

class NullVPNManager:
    """No-op VPN manager for deployments without VPN."""
    def connect(self, country: Optional[str] = None) -> bool:
        return True
    def disconnect(self) -> bool:
        return True
    def rotate(self) -> bool:
        return True
    def should_rotate(self) -> bool:
        return False
    def get_current_country(self) -> Optional[str]:
        return None


def get_vpn_manager():
    """Factory: return real or null VPN manager based on config."""
    cfg = get_settings()
    if cfg.VPN_ENABLED:
        return NordVPNManager()
    return NullVPNManager()
