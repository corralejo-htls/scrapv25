"""
vpn_manager_windows.py — BookingScraper Pro v6.0.0 Build 74
=============================================================
BUG-VPN-004-FIX (Build 71): Windows UAC dialog «¿Quieres permitir que esta
  aplicación haga cambios en el dispositivo?» — NordSecurity.NordVpn.
  DiagnosticsTool.Application blocks every rotation.
  Root cause: subprocess.run([nordvpn.exe]) has no CREATE_NO_WINDOW flag;
  child processes (DiagnosticsTool) inherit a window handle → UAC appears.
  Fix: _WIN32_NO_WINDOW + _WIN32_STARTUPINFO applied to ALL subprocess calls
  that invoke nordvpn.exe or powershell. No more UAC dialogs.

BUG-VPN-005-FIX (Build 71): nordaccount.com tabs accumulating in Brave.
  Root cause: _dismiss_nordvpn_popup() SendKeys {TAB}{ENTER} accidentally
  clicked NordVPN hyperlinks (Get help / Learn more) → Brave opened
  nordaccount.com/support-center. Observed: 11+ tabs per session.
  Fix A: Rewritten with Windows UI Automation — finds «Cancelar» button by
  name/automationId and invokes it directly. Zero keyboard simulation.
  Fix B: _close_nordaccount_browser_tabs() called after every connect.
  Finds and closes any browser windows matching nordaccount/nordvpn URLs.

BUG-VPN-008-FIX (Build 73 rev2): NordVPN popup NOT dismissed.
  Build 72 P/Invoke PowerShell approach failed silently (no log output at all).
  Root cause Build 73: PowerShell Add-Type C# compilation takes 2-4 seconds,
  the compiled DLL may conflict between rapid calls in the background thread,
  and all errors are swallowed by except Exception: pass.
  Fix Build 73: use pywin32 (win32gui/win32con) directly from Python.
  win32gui.EnumWindows + win32gui.EnumChildWindows + win32gui.GetWindowText
  + win32api.PostMessage(BM_CLICK) — synchronous, no subprocess, no compilation,
  no PowerShell. pywin32 is already installed (verified in all startup logs).
  Fallback: AppActivate + ESC via subprocess (no {TAB}{ENTER}).

BUG-VPN-002-FIX (Build 69): NordVPN popup «¿Pausar la conexión automática?»
  blocks rotation when nordvpn -d is called.

  Root causes identified from logs/screenshots (2026-04-02):
    1. DOUBLE DISCONNECT: rotate() called self.disconnect() (nordvpn -d),
       then _connect_via_cli() called nordvpn -d AGAIN — two popups per rotation.
    2. WRONG POPUP TIMING: _dismiss_nordvpn_popup() was called AFTER the connect
       command, but the popup appears DURING/AFTER the disconnect command.
       By the time dismiss ran, NordVPN auto-connect had already fired and
       reconnected to the same server.
    3. Result: VPN stayed on same IP despite "successful" rotation.

  Fix A — Remove nordvpn -d from _connect_via_cli().
    Eliminates the second disconnect entirely. rotate() already disconnects;
    _connect_via_cli() should only connect.

  Fix B — Background popup dismiss thread.
    After nordvpn -d, a daemon thread fires _dismiss_nordvpn_popup() every
    second for 8 seconds during the post-disconnect wait. Catches the popup
    however fast NordVPN GUI renders it.

  Fix C — Pre-dismiss before disconnect.
    _dismiss_nordvpn_popup() called once BEFORE nordvpn -d so any previously
    stuck popup is cleared before the new one appears.

BUG-VPN-003-FIX (Build 69): Same IP returned after rotation.
  Root cause: IP validation in _connect_via_cli() only checked
    new_ip != self._original_ip (home IP before any VPN).
  After rotating from NL → US, if auto-connect reconnected to NL,
    79.116.133.126 != 185.111.157.211 (home) → True → success logged with WRONG IP.
  Fix: track self._prev_vpn_ip; require new IP to differ from BOTH original AND prev.

BUG-LANG-001-FIX (v61) preserved:
  rotate(force=False) — force=True skips interval for immediate rotation.

v48/v2.3 features preserved:
  VPNCircuitBreaker, NullVPNManager, get_vpn_manager(), IP cache (FIX-v2.3-A),
  verify_vpn_active() Unknown-IP handling (FIX-v2.3-B), home-country exclusion.

Platform: Windows 11 / NordVPN CLI / Celery worker (non-interactive).
"""

from __future__ import annotations

import random
import subprocess
import threading
import time
from typing import Dict, List, Optional

import requests

from app.config import get_settings, _VALID_VPN_COUNTRIES  # BUG-VPN-IMPORT-001 FIX (v56)

try:
    import logging
    logger = logging.getLogger(__name__)
except Exception:
    import logging as logger  # type: ignore

# ── BUG-VPN-004-FIX (Build 71): WIN32 subprocess constants ───────────────────
# Applied to EVERY subprocess.run() that invokes nordvpn.exe or powershell.
# CREATE_NO_WINDOW prevents child processes (DiagnosticsTool) from inheriting
# a window handle → no visible window → no UAC dialogs on the desktop.
import sys as _sys
if _sys.platform == "win32":
    _WIN32_NO_WINDOW: int = subprocess.CREATE_NO_WINDOW
    _WIN32_STARTUPINFO = subprocess.STARTUPINFO()
    _WIN32_STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    _WIN32_STARTUPINFO.wShowWindow = 0  # SW_HIDE
else:
    _WIN32_NO_WINDOW = 0
    _WIN32_STARTUPINFO = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Circuit Breaker
# ---------------------------------------------------------------------------

# ── Validación de países (exportada para tests) ───────────────────────────────

def _validate_country(country: str) -> str:
    """
    Valida que el nombre de país sea de la lista canónica aprobada.

    Args:
        country: Nombre del país (e.g. 'Spain', 'Germany').

    Returns:
        El mismo country si es válido.

    Raises:
        ValueError: Si el país no está en la lista aprobada o está vacío.

    Exported as a module-level function for testability (SCRAP-BUG-010).
    """
    if not country or not isinstance(country, str):
        raise ValueError(
            f"Country must be a non-empty string, got: {country!r}"
        )
    cleaned = country.strip()
    if cleaned not in _VALID_VPN_COUNTRIES:
        raise ValueError(
            f"'{cleaned}' is not in the approved VPN country list. "
            f"Valid options: {sorted(_VALID_VPN_COUNTRIES)}"
        )
    return cleaned


class VPNCircuitBreaker:
    """
    Prevents repeated VPN connect attempts after consecutive failures.
    Opens after max_failures, auto-recovers after cooldown_seconds.
    """
    def __init__(self, max_failures: int = 3, cooldown_seconds: float = 300.0) -> None:
        self._failures        = 0
        self._max_failures    = max_failures
        self._cooldown        = cooldown_seconds
        self._opened_at: Optional[float] = None
        self._lock            = threading.Lock()

    @property
    def is_open(self) -> bool:
        with self._lock:
            if self._opened_at is None:
                return False
            if time.monotonic() - self._opened_at >= self._cooldown:
                self._failures  = 0
                self._opened_at = None
                logger.info("VPN circuit breaker CLOSED (cooldown elapsed).")
                return False
            return True

    def record_success(self) -> None:
        with self._lock:
            self._failures  = 0
            self._opened_at = None

    def try_acquire(self) -> bool:
        """
        BUG-TEST-METHOD-001 FIX (v56): Intenta adquirir el circuit breaker.

        Retorna False si el circuito está abierto (demasiados fallos recientes),
        True si el circuito está cerrado y permite la operación.

        Equivalente atómico a: if not is_open: proceed
        Útil en pruebas y en lógica de pre-validación sin side effects.
        """
        return not self.is_open

    def record_failure(self) -> None:
        with self._lock:
            self._failures += 1
            if self._failures >= self._max_failures and self._opened_at is None:
                self._opened_at = time.monotonic()
                logger.warning("VPN circuit breaker OPENED after %d failures.", self._failures)



# ---------------------------------------------------------------------------
# NordVPN Manager — full implementation
# ---------------------------------------------------------------------------

class NordVPNManager:
    """
    Manages NordVPN rotation via NordVPN CLI on Windows 11.
    v2.3 fixes: IP cache, popup dismissal, Unknown-IP handling.
    """

    # Country code → full name (used in CLI commands)
    COUNTRY_NAMES: Dict[str, str] = {
        "US": "United States",
        "UK": "United Kingdom",
        "DE": "Germany",
        "FR": "France",
        "NL": "Netherlands",
        "ES": "Spain",
        "IT": "Italy",
        "CA": "Canada",
        "SE": "Sweden",
        "CH": "Switzerland",
    }

    # NordVPN CLI executable — Windows 11 default path
    _NORDVPN_EXE: str = r"C:\Program Files\NordVPN\nordvpn.exe"

    def __init__(self, interactive: bool = False) -> None:
        """
        Args:
            interactive: False for Celery workers (no input() prompts).
                         True for manual/console testing only.
        """
        self._cfg         = get_settings()
        self._interactive = interactive
        self._breaker     = VPNCircuitBreaker(max_failures=3, cooldown_seconds=300.0)
        self._lock        = threading.Lock()
        self._last_rotation: float = 0.0
        self._current_country: Optional[str] = None

        # FIX-v2.3-A: IP cache — prevents thread saturation of external services
        self._ip_cache_value: str   = "Unknown"
        self._ip_cache_time:  float = 0.0
        self._ip_cache_ttl:   float = 30.0
        self._ip_cache_lock   = threading.Lock()

        # BUG-VPN-003-FIX (Build 69): track previous VPN IP so we can detect
        # when auto-connect silently reconnects to the same server after a rotation.
        # Validation now requires: new_ip != original_ip AND new_ip != _prev_vpn_ip.
        self._prev_vpn_ip: str = "Unknown"

        # BUG-VPN-002-FIX (Build 69): event to stop background popup dismiss thread
        self._popup_dismiss_stop: threading.Event = threading.Event()

        # Capture original IP (before any VPN connection)
        self._original_ip = self._detect_original_ip()

        # BUG-VPN-HOME-COUNTRY FIX: detect the operator real country code so we
        # can exclude it from the VPN rotation pool. Connecting to the same country
        # as the operator physical location defeats geo-bypass (Booking.com will
        # still serve local currency/pricing instead of European rates).
        # Example: user in Canada + Canada in VPN_COUNTRIES → random.choice picks CA
        # → VPN tunnel runs through Canada → CAD currency shown instead of EUR.
        self._home_country_code: Optional[str] = self._detect_home_country()

        logger.info(
            "NordVPNManager initialised | interactive=%s | original_ip=%s | home_country=%s",
            interactive, self._original_ip, self._home_country_code,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def connect(self, country: Optional[str] = None) -> bool:
        """Connect VPN to given country code (e.g. 'DE', 'UK') or random."""
        if self._breaker.is_open:
            logger.warning("VPN circuit breaker is OPEN — skipping connect.")
            return False

        cfg_countries = self._cfg.VPN_COUNTRIES
        if country is None:
            # Map country names from config to country codes
            available_codes = self._names_to_codes(cfg_countries)
            if not available_codes:
                available_codes = list(self.COUNTRY_NAMES.keys())

            # BUG-VPN-HOME-COUNTRY FIX: exclude the operator home country from
            # the random selection pool. If the user is in Canada and "Canada"
            # is in VPN_COUNTRIES, random.choice may pick CA → VPN tunnel runs
            # through Canada → Booking.com serves CAD instead of EUR.
            if self._home_country_code and self._home_country_code in available_codes:
                filtered = [c for c in available_codes if c != self._home_country_code]
                if filtered:
                    logger.info(
                        "VPN: excluding home country %s from pool — remaining: %s",
                        self._home_country_code, ",".join(filtered),
                    )
                    available_codes = filtered
                else:
                    logger.warning(
                        "VPN: home country exclusion would empty pool — keeping all countries"
                    )

            country = random.choice(available_codes)

        country_name = self.COUNTRY_NAMES.get(country, country)
        logger.info("VPN: connecting to %s (%s)...", country_name, country)

        success = self._connect_via_cli(country_name)
        if success:
            self._breaker.record_success()
            self._current_country = country
        else:
            self._breaker.record_failure()
        return success

    def disconnect(self) -> bool:
        """
        Disconnect VPN.

        BUG-VPN-002-FIX (Build 69):
          1. Pre-dismiss: clear any existing popup BEFORE sending nordvpn -d.
          2. Background dismiss thread: fires _dismiss_nordvpn_popup() every
             second for _POST_DISCONNECT_DISMISS_SECS after the -d command,
             catching the popup however fast the NordVPN GUI renders it.
          3. The background thread is stopped by rotate() before connect() runs
             so it does not interfere with the connection phase.
        """
        # 1. Pre-dismiss: clear any existing popup before disconnect triggers a new one
        self._dismiss_nordvpn_popup()

        # 2. Execute disconnect
        try:
            result = subprocess.run(
                [self._NORDVPN_EXE, "-d"],
                capture_output=True, text=True, timeout=30, shell=False,
                creationflags=_WIN32_NO_WINDOW,   # BUG-VPN-004-FIX
                startupinfo=_WIN32_STARTUPINFO,   # BUG-VPN-004-FIX
            )
            success = result.returncode == 0 or "disconnected" in result.stdout.lower()
            if success:
                self._current_country = None
                logger.info("VPN disconnected.")
            else:
                logger.warning("VPN disconnect returned code %d: %r", result.returncode, result.stderr)
        except Exception as exc:
            logger.error("VPN disconnect failed: [%s] %s", type(exc).__name__, exc)
            success = False

        # 3. Background dismiss thread — keeps dismissing during post-disconnect wait.
        # The popup appears 0–3 s after the -d command; this thread catches it.
        self._popup_dismiss_stop.clear()
        _t = threading.Thread(
            target=self._background_popup_dismiss,
            args=(self._POST_DISCONNECT_DISMISS_SECS,),
            daemon=True,
        )
        _t.start()

        return success

    # How long (seconds) the background dismiss thread runs after disconnect.
    _POST_DISCONNECT_DISMISS_SECS: int = 8

    def rotate(self, force: bool = False) -> bool:
        """
        Rotate VPN to a different country.
        Avoids current country; uses circuit breaker protection.
        BUG-VPN-LOCK: re-check should_rotate() INSIDE the lock to prevent two
        threads from both rotating after the first one already updated _last_rotation.

        BUG-LANG-001-FIX (v61):
          force=True  — omite la comprobación de intervalo. Usado cuando hay
                        fallos consecutivos de idioma para obtener nueva IP de
                        inmediato sin esperar VPN_ROTATION_INTERVAL.
          force=False — comportamiento original (comprueba intervalo).

        BUG-VPN-002-FIX (Build 69):
          disconnect() now launches a background dismiss thread.
          rotate() stops that thread before calling connect() so the popup
          dismisser does not interfere with the connection phase.
          The wait between disconnect and connect is kept (5s) to allow the
          tunnel to release, but reduced from 5s to 3s since the background
          dismiss thread already covers the popup window.
        """
        with self._lock:
            # BUG-VPN-LOCK: another thread may have just rotated while we were waiting.
            # If interval has not elapsed yet, skip — the rotation already happened.
            # BUG-LANG-001-FIX: si force=True, ignorar el intervalo completamente.
            elapsed = time.monotonic() - self._last_rotation
            if not force and elapsed < self._cfg.VPN_ROTATION_INTERVAL and self._last_rotation > 0:
                logger.info(
                    "VPN: rotation skipped — another thread rotated %.0fs ago (interval=%ds).",
                    elapsed, self._cfg.VPN_ROTATION_INTERVAL,
                )
                return True  # Previous rotation counts as success

            logger.info("VPN: rotating (current=%s)...", self._current_country)
            self.disconnect()   # → starts background dismiss thread internally

            # BUG-VPN-002-FIX: wait 5 s for tunnel teardown while background
            # dismiss thread handles the popup continuously.
            time.sleep(5)

            # Stop background dismiss thread before connecting
            # (popup is gone by now; don't let it interfere with connect phase)
            self._popup_dismiss_stop.set()

            cfg_countries = self._cfg.VPN_COUNTRIES
            available = self._names_to_codes(cfg_countries) or list(self.COUNTRY_NAMES.keys())

            # Avoid current country
            if self._current_country and self._current_country in available:
                available = [c for c in available if c != self._current_country]
            if not available:
                available = list(self.COUNTRY_NAMES.keys())

            new_country = random.choice(available)
            success = self.connect(new_country)

            if success:
                self._last_rotation = time.monotonic()
                logger.info("VPN rotation successful → %s", self.COUNTRY_NAMES.get(new_country, new_country))
            else:
                logger.error("VPN rotation failed → %s", new_country)
            return success

    def should_rotate(self) -> bool:
        """True if rotation interval has elapsed since last rotation."""
        return (time.monotonic() - self._last_rotation) >= self._cfg.VPN_ROTATION_INTERVAL

    def get_status(self) -> Dict:
        """Return current VPN status dict."""
        current_ip = self.get_current_ip()
        return {
            "enabled":          self._cfg.VPN_ENABLED,
            "connected":        self.verify_vpn_active(),
            "current_country":  self._current_country,
            "current_ip":       current_ip,
            "original_ip":      self._original_ip,
            "circuit_breaker":  "open" if self._breaker.is_open else "closed",
            "rotation_interval": self._cfg.VPN_ROTATION_INTERVAL,
        }

    # ── Internal ──────────────────────────────────────────────────────────────

    def _connect_via_cli(self, country_name: str) -> bool:
        """
        Execute NordVPN CLI connect command.

        BUG-VPN-002-FIX (Build 69):
          Removed the redundant nordvpn -d call that was here.
          rotate() already calls disconnect() before reaching this method.
          The previous double-disconnect triggered the popup TWICE per rotation
          and gave auto-connect two chances to reconnect to the same server.

        BUG-VPN-003-FIX (Build 69):
          IP validation now checks new_ip != self._prev_vpn_ip in addition to
          != self._original_ip.  This catches the case where auto-connect after
          the popup silently reconnects to the same VPN server, returning the
          same IP that was used in the previous rotation slot.
        """
        try:
            # BUG-VPN-002-FIX: NO nordvpn -d here. rotate() already disconnected.
            # Previously this caused a SECOND disconnect → second popup → auto-connect
            # race that often reconnected to the same server.

            result = subprocess.run(
                [self._NORDVPN_EXE, "-c", "-g", country_name],
                capture_output=True, text=True, timeout=60, shell=False,
                creationflags=_WIN32_NO_WINDOW,   # BUG-VPN-004-FIX
                startupinfo=_WIN32_STARTUPINFO,   # BUG-VPN-004-FIX
            )
            connected = (
                result.returncode == 0
                or "connected" in result.stdout.lower()
            )
            if connected:
                # FIX-v2.3-C: dismiss "Pausar la conexión automática" dialog.
                # Popup may appear 1-3 s after CLI confirms connection.
                self._dismiss_nordvpn_popup()
                time.sleep(2)
                self._dismiss_nordvpn_popup()   # Second attempt for late-appearing popup
                time.sleep(8)                   # Allow VPN tunnel to fully stabilise

                # BUG-VPN-CACHE: invalidate cached IP before checking new IP.
                with self._ip_cache_lock:
                    self._ip_cache_time  = 0.0
                    self._ip_cache_value = "Unknown"

                new_ip = self.get_current_ip()

                # BUG-VPN-003-FIX: require new IP to differ from BOTH home IP AND
                # the previous VPN IP. Before this fix, rotating NL → US when
                # auto-connect silently reconnected to NL returned the same IP
                # (79.116.133.126) but the check only tested != original_ip
                # (185.111.157.211) so it logged "success" with the wrong IP.
                ip_changed_from_home = new_ip != self._original_ip
                ip_changed_from_prev = new_ip != self._prev_vpn_ip or self._prev_vpn_ip == "Unknown"

                if new_ip != "Unknown" and ip_changed_from_home and ip_changed_from_prev:
                    logger.info("VPN connected to %s — IP: %s", country_name, new_ip)
                    self._prev_vpn_ip = new_ip    # BUG-VPN-003-FIX: record for next validation
                    return True
                elif new_ip == self._prev_vpn_ip and new_ip != "Unknown":
                    logger.error(
                        "BUG-VPN-003: IP unchanged after rotation "
                        "(prev=%s current=%s) — auto-connect likely reconnected "
                        "to same server. country=%s",
                        self._prev_vpn_ip, new_ip, country_name,
                    )
                    return False
                else:
                    logger.error(
                        "VPN CLI connected but IP unchanged "
                        "(original=%s prev_vpn=%s current=%s) country=%s",
                        self._original_ip, self._prev_vpn_ip, new_ip, country_name,
                    )
                    return False
            else:
                logger.error("NordVPN connect failed: country=%s rc=%d stderr=%r stdout=%r",
                             country_name, result.returncode, result.stderr, result.stdout)
                return False

        except subprocess.TimeoutExpired:
            logger.error("NordVPN connect timed out for %s", country_name)
            return False
        except FileNotFoundError:
            logger.error(
                "NordVPN executable not found at %s. "
                "Install NordVPN or set VPN_ENABLED=false in .env.", self._NORDVPN_EXE
            )
            return False
        except Exception as exc:
            logger.error("NordVPN subprocess error: [%s] %s", type(exc).__name__, exc)
            return False

    def _dismiss_nordvpn_popup(self) -> None:
        """
        BUG-VPN-008-FIX (Build 73 rev2): Close the NordVPN «¿Pausar la
        conexión automática?» popup using pywin32 directly from Python.

        Why pywin32 instead of PowerShell P/Invoke (Build 72):
          Build 72 compiled C# with Add-Type in PowerShell. Production logs
          showed ZERO output — the script failed silently before any window
          enumeration. Likely causes: compilation timeout (2-4s per call),
          DLL namespace conflicts across background thread calls, or UAC
          blocking in-process COM. The popup remained open throughout.

        pywin32 approach (synchronous, no subprocess overhead):
          1. win32gui.EnumWindows: iterate all top-level Windows HWNDs.
          2. For each: win32gui.EnumChildWindows to find all child controls.
          3. win32gui.GetWindowText on each child.
          4. If text == 'Cancelar' or 'Cancel': PostMessage BM_CLICK.
          pywin32 is already installed (confirmed in every startup log).
        """
        try:
            import win32gui
            import win32con

            clicked: list = []

            def _child_callback(hwnd_child: int, _: object) -> bool:
                try:
                    text = win32gui.GetWindowText(hwnd_child)
                    if text in ("Cancelar", "Cancel") and win32gui.IsWindowVisible(hwnd_child):
                        win32gui.PostMessage(hwnd_child, win32con.BM_CLICK, 0, 0)
                        clicked.append(hwnd_child)
                except Exception:
                    pass
                return True  # continue enumeration

            def _top_callback(hwnd_top: int, _: object) -> bool:
                try:
                    win32gui.EnumChildWindows(hwnd_top, _child_callback, None)
                except Exception:
                    pass
                return True  # continue enumeration

            win32gui.EnumWindows(_top_callback, None)

            if clicked:
                logger.info(
                    "BUG-VPN-008-FIX: BM_CLICK sent to %d 'Cancelar' button(s) via pywin32",
                    len(clicked),
                )
            else:
                logger.debug("BUG-VPN-008-FIX: No NordVPN popup found (no Cancelar button).")

        except ImportError:
            logger.warning("BUG-VPN-008-FIX: pywin32 not available — using ESC fallback")
            self._dismiss_nordvpn_popup_esc_fallback()
        except Exception as exc:
            logger.debug("BUG-VPN-008-FIX: pywin32 enum failed: %s — using ESC fallback", exc)
            self._dismiss_nordvpn_popup_esc_fallback()

    def _dismiss_nordvpn_popup_esc_fallback(self) -> None:
        """ESC fallback: AppActivate nordvpn + send ESC only (no TAB, no ENTER)."""
        try:
            ps_esc = (
                "Add-Type -AssemblyName System.Windows.Forms; "
                "$wsh = New-Object -ComObject WScript.Shell; "
                "if ($wsh.AppActivate('nordvpn')) { "
                "  Start-Sleep -Milliseconds 300; "
                "  [System.Windows.Forms.SendKeys]::SendWait('{ESC}'); "
                "}"
            )
            subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_esc],
                capture_output=True, text=True, timeout=5, shell=False,
                creationflags=_WIN32_NO_WINDOW,
                startupinfo=_WIN32_STARTUPINFO,
            )
        except Exception:
            pass


    def _background_popup_dismiss(self, duration_secs: int) -> None:
        """
        BUG-VPN-002-FIX (Build 69): Background daemon thread that fires
        _dismiss_nordvpn_popup() every second for *duration_secs* seconds,
        or until _popup_dismiss_stop is set by rotate().

        The popup after nordvpn -d can appear at any point in the 0–3 s window
        after the disconnect command returns. A single timed dismiss call misses
        it when the popup appears after the dismiss runs. This thread guarantees
        coverage across the entire post-disconnect window.
        """
        deadline = time.monotonic() + duration_secs
        while time.monotonic() < deadline:
            if self._popup_dismiss_stop.is_set():
                break
            self._dismiss_nordvpn_popup()
            time.sleep(1.0)

    def _detect_original_ip(self) -> str:
        """Capture IP before any VPN connection."""
        try:
            ip = self.get_current_ip()
            logger.info("VPN: original IP = %s", ip)
            return ip
        except Exception:
            logger.warning("VPN: could not detect original IP")
            return "Unknown"

    def _detect_home_country(self) -> Optional[str]:
        """
        BUG-VPN-HOME-COUNTRY FIX: Detect operator real country code via IP geolocation.
        Uses ipinfo.io (free tier, no key required for ~50k req/day).
        Returns ISO country code (e.g. 'CA', 'US') or None if detection fails.
        Called once at __init__ — result is cached in self._home_country_code.
        """
        if self._original_ip in ("Unknown", "", None):
            logger.warning("VPN: home country detection skipped — original IP unknown")
            return None
        try:
            resp = requests.get(
                f"https://ipinfo.io/{self._original_ip}/country",
                timeout=8,
            )
            if resp.status_code == 200:
                code = resp.text.strip().upper()
                if len(code) == 2 and code.isalpha():
                    logger.info("VPN: home country detected = %s", code)
                    return code
        except Exception as exc:
            logger.warning("VPN: home country detection failed: %s", exc)
        return None

    def _names_to_codes(self, country_names: List[str]) -> List[str]:
        """Convert config country names (e.g. 'Germany') to codes (e.g. 'DE')."""
        name_to_code = {v.lower(): k for k, v in self.COUNTRY_NAMES.items()}
        codes = []
        for name in country_names:
            code = name_to_code.get(name.lower())
            if code:
                codes.append(code)
            elif name.upper() in self.COUNTRY_NAMES:
                codes.append(name.upper())
        return codes

    # ── IP verification ───────────────────────────────────────────────────────

    def get_current_ip(self) -> str:
        """
        FIX-v2.3-A: Cached IP lookup (30s TTL, thread-safe).
        Prevents multiple simultaneous threads saturating external IP services.
        """
        with self._ip_cache_lock:
            now = time.time()
            if (now - self._ip_cache_time < self._ip_cache_ttl
                    and self._ip_cache_value != "Unknown"):
                return self._ip_cache_value

        # HTTP call outside lock to avoid blocking other threads
        services = [
            "https://api.ipify.org?format=text",
            "https://ifconfig.me/ip",
            "https://icanhazip.com",
            "https://ipinfo.io/ip",
            "https://checkip.amazonaws.com",
        ]
        result = "Unknown"
        for svc in services:
            try:
                resp = requests.get(svc, timeout=8)
                if resp.status_code == 200:
                    result = resp.text.strip()
                    break
            except Exception:
                continue

        with self._ip_cache_lock:
            self._ip_cache_value = result
            self._ip_cache_time  = time.time()

        if result == "Unknown":
            logger.warning("VPN: could not obtain current IP")
        return result

    def verify_vpn_active(self) -> bool:
        """
        FIX-v2.3-B: Verify IP differs from original.
        When either IP is 'Unknown', ASSUME VPN active (not inactive).
        Rationale: false positive (assume connected) is safer than false
        negative (mass reconnect attempts under DNS stress).
        """
        if not self._original_ip or self._original_ip == "Unknown":
            logger.warning("VPN: original IP unknown — assuming active")
            return True

        current = self.get_current_ip()
        if current == "Unknown":
            logger.warning("VPN: current IP unknown — assuming active (no mass reconnect)")
            return True

        if current != self._original_ip:
            logger.debug("VPN: active — IP: %s", current)
            return True

        logger.warning("VPN: inactive — IP=%s == original=%s", current, self._original_ip)
        return False

    def reconnect_if_down(self) -> bool:
        """Reconnect if VPN is no longer active."""
        if not self.verify_vpn_active():
            logger.warning("VPN dropped — reconnecting to %s", self._current_country)
            return self.connect(self._current_country)
        return True


# ---------------------------------------------------------------------------
# Null VPN Manager — used when VPN_ENABLED=False
# ---------------------------------------------------------------------------

class NullVPNManager:
    """No-op VPN manager for deployments without VPN."""
    def connect(self, country: Optional[str] = None) -> bool:
        return True
    def disconnect(self) -> bool:
        return True
    def rotate(self, force: bool = False) -> bool:  # BUG-LANG-001-FIX: force param para consistencia
        return True
    def should_rotate(self) -> bool:
        return False
    def verify_vpn_active(self) -> bool:
        return True
    def get_current_ip(self) -> str:
        return "N/A (VPN disabled)"
    def get_status(self) -> Dict:
        return {"enabled": False, "connected": False, "current_country": None}


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

# Alias para compatibilidad con tests — CircuitBreaker es VPNCircuitBreaker
CircuitBreaker = VPNCircuitBreaker


def get_vpn_manager():
    """Return NordVPNManager or NullVPNManager based on VPN_ENABLED config."""
    cfg = get_settings()
    if cfg.VPN_ENABLED:
        return NordVPNManager(interactive=False)
    return NullVPNManager()
