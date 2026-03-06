"""
BookingScraper/app/vpn_manager_windows.py
Gestor NordVPN para Windows - BookingScraper Pro
Windows 11 + Python 3.14.3

CORRECCIONES v1.1:
  [FIX] _connect_manual: input() BLOQUEANTE eliminado
  [FIX] shell=True con lista de args reemplazado por shell=False + string unico
  [FIX] __del__: captura AttributeError si __init__ fallo a medias
  [NEW] Parametro interactive=False para modo Celery (sin prompts de usuario)
  [NEW] connect_or_raise(): para uso en tareas automatizadas

CORRECCIONES v2.3:
  [FIX CRITICO] verify_vpn_active(): cuando original_ip='Unknown' O current='Unknown'
               asumir VPN activa en lugar de inactiva.
               CAUSA RAIZ de ERR_NAME_NOT_RESOLVED: 10 threads simultaneos agotaban
               los servicios externos de IP (rate-limit), todos devolvian 'Unknown',
               verify_vpn_active() retornaba False, y los 10 threads intentaban
               reconectar a 10 paises distintos simultaneamente -> DNS inestable ->
               Brave no podia resolver booking.com -> ERR_NAME_NOT_RESOLVED en todo.
  [FIX CRITICO] get_current_ip(): anadida cache de 30s con threading.Lock.
               Evita que multiples threads simultaneos saturen los servicios externos.
"""

import subprocess
import time
import random
import platform
import os
import sys
import threading
from typing import Optional, Dict

import requests
from loguru import logger

# [FIX-022 / WIN-002] Suppress console window creation for all subprocess calls.
# Without CREATE_NO_WINDOW, each nordvpn CLI call spawns a visible console window
# that flashes briefly on screen — disruptive for background scraping sessions.
# On Linux/macOS the attribute does not exist, so we fall back to 0 (no-op).
_CREATE_NO_WINDOW: int = getattr(subprocess, "CREATE_NO_WINDOW", 0)

# winreg solo disponible en Windows
try:
    import winreg
    _WINREG_AVAILABLE = True
except ImportError:
    _WINREG_AVAILABLE = False


class NordVPNManagerWindows:
    """Gestor de NordVPN para Windows 11"""

    # Países disponibles con sus nombres completos
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

    def __init__(
        self,
        method: str = "auto",
        interactive: bool = False,          # ✅ NEW: False = modo Celery (sin input())
        max_connections_per_server: int = 50,
    ):
        """
        Args:
            method:       'auto' | 'cli' | 'app' | 'manual'
            interactive:  True = permite prompts de usuario (modo consola)
                          False = lanza excepción si se necesita acción manual
            max_connections_per_server: rotación automática al alcanzar este límite
        """
        self.interactive = interactive
        self.max_connections_per_server = max_connections_per_server
        self.current_server: Optional[str] = None
        self.current_ip:     Optional[str] = None
        self.original_ip:    Optional[str] = None
        self.connection_count = 0

        # Cache de IP para evitar saturar servicios externos con multiples threads
        self._ip_cache_value: str   = "Unknown"
        self._ip_cache_time:  float = 0.0
        self._ip_cache_ttl:   float = 5.0   # [FIX HIGH-007] Reduced from 30s: post-rotation
        # the old IP must not linger in cache — 5s ensures fresh reads within one poll cycle.
        self._ip_cache_lock   = threading.Lock()

        # [BUG-001 FIX] Metadatos de la última rotación para que scraper_service
        # pueda persistir el evento en vpn_rotations sin acoplar DB a este módulo.
        self.last_rotation_info: dict = {
            "old_ip":          None,
            "new_ip":          None,
            "country":         None,
            "rotation_reason": None,
            "requests_count":  0,
            "success":         False,
            "error_message":   None,
        }

        self.method = self._detect_method() if method == "auto" else method

        self._detect_original_ip()

        logger.info(
            f"VPN Manager Windows inicializado | método={self.method} "
            f"| interactive={interactive} | sistema={platform.version()}"
        )

    # ── DETECCIÓN AUTOMÁTICA ───────────────────────────────────────────────────

    def _detect_method(self) -> str:
        """Detecta el método VPN disponible en el sistema."""

        # ✅ FIX: shell=False con string único (no lista con shell=True)
        try:
            # [FIX v2.4] shell=False + lista de args. En Windows, nordvpn.exe
            # esta en el PATH del sistema; no se necesita shell=True.
            result = subprocess.run(
                ["nordvpn", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=False,
                creationflags=_CREATE_NO_WINDOW,   # [FIX-022] no console flash on Windows
            )
            if result.returncode == 0:
                logger.info("✓ NordVPN CLI detectado")
                return "cli"
        except Exception:
            pass

        # Verificar app de escritorio en el registro de Windows
        if _WINREG_AVAILABLE:
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                    0,
                    winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
                )
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        if "NordVPN" in display_name:
                            logger.info("✓ NordVPN App de escritorio detectada")
                            return "app"
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(key)
            except Exception:
                pass

        logger.warning("⚠️ NordVPN no detectado, usando modo manual")
        return "manual"

    def _detect_original_ip(self):
        """Captura la IP original antes de conectar VPN."""
        try:
            self.original_ip = self.get_current_ip()
            logger.info(f"IP original: {self.original_ip}")
        except Exception:
            self.original_ip = None
            logger.warning("⚠️ No se pudo detectar IP original")

    # ── CONEXIÓN ──────────────────────────────────────────────────────────────

    def connect(self, country: Optional[str] = None) -> bool:
        """
        Conecta a NordVPN.

        Args:
            country: Código de país ('US', 'DE', etc.) o None para aleatorio.

        Returns:
            True si la conexión fue exitosa.
        """
        if country is None:
            country = random.choice(list(self.COUNTRY_NAMES.keys()))

        country_name = self.COUNTRY_NAMES.get(country, country)
        logger.info(f"Conectando a {country_name} ({country})...")

        if self.method == "cli":
            return self._connect_via_cli(country_name)
        elif self.method == "app":
            return self._connect_via_app(country_name)
        else:
            return self._connect_manual(country_name)

    def connect_or_raise(self, country: Optional[str] = None) -> None:
        """
        Igual que connect() pero lanza excepción si falla.
        Útil en tareas Celery donde un fallo debe propagar error.
        """
        if not self.connect(country):
            raise ConnectionError(
                f"No se pudo conectar a NordVPN "
                f"(método={self.method}, país={country})"
            )

    def _connect_via_cli(self, country: str) -> bool:
        """
        Connect to NordVPN using the NordVPN CLI executable.

        [FIX BUG-V11-009] Full parameter, return and security documentation added.

        Executes `nordvpn connect <country>` as a subprocess with shell=False
        (list-form args) to prevent shell injection. The country code always
        originates from `settings.VPN_COUNTRIES` (a controlled list), never
        from user input, so injection risk is already mitigated at the source.

        Args:
            country (str): NordVPN country code (e.g. 'US', 'DE', 'UK').
                           Must be one of the values in settings.VPN_COUNTRIES.

        Returns:
            bool: True if the CLI reports a successful connection.
                  False if the command times out, returns non-zero exit code,
                  or NordVPN CLI is not found in PATH.

        Raises:
            Never — all subprocess errors are caught and return False.
        """
        try:
            # Desconectar primero
            # [FIX v2.4] shell=False con lista de args. El pais viene de
            # settings.VPN_COUNTRIES (lista controlada), nunca de input usuario.
            # Aun asi, usar lista es la practica correcta.
            subprocess.run(
                ["nordvpn", "-d"],
                capture_output=True,
                timeout=30,
                shell=False,
                creationflags=_CREATE_NO_WINDOW,   # [FIX-022]
            )
            time.sleep(3)

            # Conectar
            logger.info(f"Conectando CLI a {country}...")
            # [FIX LOW-002+CRIT-005] shell=False duplicado eliminado.
            # country validado en config._validate_settings() contra NordVPN country codes.
            result = subprocess.run(
                ["nordvpn", "-c", "-g", country],
                capture_output=True,
                text=True,
                timeout=60,
                shell=False,
                creationflags=_CREATE_NO_WINDOW,
            )

            connected = (
                result.returncode == 0
                or "connected" in result.stdout.lower()
            )

            if connected:
                # [FIX v2.3] Cerrar popup "¿Pausar la conexion automatica?"
                # que aparece cada vez que NordVPN cambia de servidor
                self._dismiss_nordvpn_popup()
                time.sleep(10)
                new_ip = self.get_current_ip()
                if new_ip != self.original_ip and new_ip != "Unknown":
                    self.current_server = country
                    self.current_ip = new_ip
                    self.connection_count = 0
                    logger.success(f"✓ Conectado a {country} — IP: {new_ip}")
                    return True
                else:
                    logger.error("✗ VPN CLI conectó pero IP no cambió")
                    return False
            else:
                logger.error(f"✗ Error CLI: {result.stderr.strip()}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("✗ Timeout al conectar VPN CLI (60s)")
            return False
        except Exception as e:
            logger.error(f"✗ Error CLI: {e}")
            return False

    def _dismiss_nordvpn_popup(self):
        """
        [FIX v2.3] Cierra el popup que NordVPN muestra cada vez que cambia
        de servidor: "Pausar la conexion automatica en esta sesion?"
        Usa PowerShell para encontrar la ventana y enviar ESC (Cancelar).
        [FIX BUG-V7-010] Checks PowerShell availability before attempting to run it.
        Gracefully skips on systems where PowerShell is not installed (Windows Nano
        Server, hardened configs, certain containerized Windows environments).
        """
        import shutil
        # [FIX BUG-V7-010] Guard: verify PowerShell is available before invoking it.
        # On Windows Nano Server, hardened configurations, or Docker containers,
        # 'powershell' may not be on PATH. Without this guard, FileNotFoundError
        # would propagate (or be silently ignored) on every VPN rotation.
        ps_executable = shutil.which("powershell") or shutil.which("pwsh")
        if not ps_executable:
            logger.debug(
                "[BUG-V7-010] _dismiss_nordvpn_popup skipped: "
                "PowerShell ('powershell' / 'pwsh') not found on PATH. "
                "NordVPN popup may remain open."
            )
            return

        try:
            ps_script = (
                "Add-Type -AssemblyName System.Windows.Forms; "
                "$proc = Get-Process -Name 'NordVPN' -ErrorAction SilentlyContinue; "
                "if ($proc) { "
                "  $wsh = New-Object -ComObject WScript.Shell; "
                "  $wsh.AppActivate('NordVPN'); "
                "  Start-Sleep -Milliseconds 500; "
                "[System.Windows.Forms.SendKeys]::SendWait('{ESC}'); "
                "}"
            )
            result = subprocess.run(
                [ps_executable, "-NoProfile", "-NonInteractive", "-Command", ps_script],
                capture_output=True,
                timeout=5,
                creationflags=_CREATE_NO_WINDOW,   # [FIX-022] suppress console window
            )
            # [FIX BUG-V6-012] Log failure instead of silently swallowing.
            if result.returncode != 0:
                logger.debug(
                    f"[BUG-V6-012] _dismiss_nordvpn_popup: PowerShell exited with "
                    f"code {result.returncode}. stderr={result.stderr.decode(errors='replace')[:200]}"
                )
        except Exception as e:
            # Non-critical — popup dismissal failure should not abort VPN rotation
            logger.debug(f"[BUG-V6-012/V7-010] _dismiss_nordvpn_popup failed (non-critical): {e}")

    def _connect_via_app(self, country: str) -> bool:
        """
        La app de escritorio de NordVPN no tiene API pública en Windows.
        Delega a manual (con protección contra bloqueo).
        """
        logger.warning("⚠️ NordVPN app de escritorio no tiene API pública, usando manual")
        return self._connect_manual(country)

    def _connect_manual(self, country: str) -> bool:
        """
        ✅ FIX: input() solo se llama si interactive=True.
        En modo Celery (interactive=False) lanza excepción explicativa.
        """
        if not self.interactive:
            # ✅ FIX: No bloquear el worker de Celery
            raise RuntimeError(
                f"Conexión VPN manual requerida para {country}, pero "
                "interactive=False (modo Celery). "
                "Conecta NordVPN manualmente antes de iniciar el worker, "
                "o establece VPN_ENABLED=False en .env."
            )

        # [FIX LOW-006] Interactive console prompts routed through logger so
        # they appear in Loguru's output pipeline (rotation, retention).
        # input() retained — this code path only executes when interactive=True
        # (manual console mode); Celery workers never reach this branch.
        logger.info("[VPN] " + "=" * 56)
        logger.info("[VPN] 🔐 CONEXIÓN MANUAL REQUERIDA")
        logger.info("[VPN] " + "=" * 56)
        logger.info("[VPN]   1. Abre la aplicación NordVPN")
        logger.info("[VPN]   2. Conecta manualmente a: {}", country)
        logger.info("[VPN]   3. Espera a que la conexión se establezca")
        logger.info("[VPN] 👉 Presiona ENTER cuando estés conectado...")
        logger.info("[VPN] " + "=" * 56)
        input()

        time.sleep(2)
        new_ip = self.get_current_ip()

        if new_ip != self.original_ip and new_ip != "Unknown":
            self.current_server = country
            self.current_ip = new_ip
            self.connection_count = 0
            logger.success(f"✓ VPN manual verificada — IP: {new_ip}")
            return True

        logger.warning("[VPN] ⚠️ IP no cambió: actual={}  original={}", new_ip, self.original_ip)
        logger.info("[VPN] ¿Continuar de todas formas? (s/n): ")
        return input().strip().lower() == "s"

    # ── DESCONEXIÓN ───────────────────────────────────────────────────────────

    def disconnect(self) -> None:
        """Desconecta la VPN."""
        try:
            if self.method == "cli":
                # [FIX v2.4] shell=False
                subprocess.run(
                    ["nordvpn", "-d"],
                    capture_output=True,
                    timeout=30,
                    shell=False,
                    creationflags=_CREATE_NO_WINDOW,   # [FIX-022]
                )
                logger.info("✓ VPN desconectada (CLI)")
            elif self.interactive:
                # [FIX LOW-006] Route manual disconnect prompts through logger
                logger.info("[VPN] " + "=" * 56)
                logger.info("[VPN] 🔓 DESCONEXIÓN MANUAL REQUERIDA")
                logger.info("[VPN] " + "=" * 56)
                logger.info("[VPN]   1. Abre la aplicación NordVPN")
                logger.info("[VPN]   2. Haz clic en 'Disconnect'")
                logger.info("[VPN] 👉 Presiona ENTER cuando hayas desconectado...")
                input()

            self.current_server = None
            self.current_ip = None

        except Exception as e:
            logger.warning(f"Error al desconectar VPN: {e}")

    # ── ROTACIÓN ──────────────────────────────────────────────────────────────

    def rotate(self, avoid_current: bool = True, reason: str = "periodica") -> bool:
        """
        Rota la conexión a un servidor diferente.

        Args:
            avoid_current: Si True, evita el país actual.
            reason: Motivo de la rotación (se persiste en last_rotation_info).
        """
        logger.info("🔄 Rotando VPN...")
        old_ip = self.current_ip or self.get_current_ip()
        old_requests = self.connection_count
        self.disconnect()
        time.sleep(5)

        available = list(self.COUNTRY_NAMES.keys())
        if avoid_current and self.current_server:
            # Buscar código del servidor actual
            curr_code = next(
                (k for k, v in self.COUNTRY_NAMES.items() if v == self.current_server),
                None,
            )
            if curr_code and curr_code in available:
                available.remove(curr_code)

        new_country = random.choice(available) if available else random.choice(
            list(self.COUNTRY_NAMES.keys())
        )

        success = self.connect(new_country)
        new_ip = self.current_ip if success else None

        # [BUG-001 FIX] Registrar metadatos de rotación — scraper_service persiste en BD.
        self.last_rotation_info = {
            "old_ip":          old_ip,
            "new_ip":          new_ip,
            "country":         self.COUNTRY_NAMES.get(new_country, new_country),
            "rotation_reason": reason,
            "requests_count":  old_requests,
            "success":         success,
            "error_message":   None if success else f"connect({new_country}) devolvió False",
        }

        if success:
            # [FIX HIGH-007] Invalidate IP cache immediately after rotation so that
            # the next call to get_current_ip() performs a live lookup instead of
            # returning the old (pre-rotation) address. Without this, verify_vpn_active()
            # could report a false negative for up to _ip_cache_ttl seconds.
            with self._ip_cache_lock:
                self._ip_cache_time = 0.0
            logger.success(f"✓ Rotación exitosa → {self.COUNTRY_NAMES[new_country]}")
        else:
            logger.error("✗ Falló la rotación de VPN")
        return success

    def auto_rotate_if_needed(self) -> bool:
        """Rota automáticamente si se alcanzó el límite de conexiones."""
        self.connection_count += 1
        if self.connection_count >= self.max_connections_per_server:
            logger.warning(
                f"⚠️ Límite alcanzado ({self.max_connections_per_server} conexiones)"
            )
            return self.rotate()
        return False

    # ── VERIFICACIÓN ──────────────────────────────────────────────────────────

    # ── VERIFICACION ─────────────────────────────────────────────────────────

    def get_current_ip(self) -> str:
        """
        Obtiene la IP publica actual.
        [FIX v2.3] Cache de 30s: evita que multiples threads simultaneos saturen
                   los servicios externos y devuelvan timeout -> 'Unknown'.
        """
        with self._ip_cache_lock:
            now = time.time()
            if now - self._ip_cache_time < self._ip_cache_ttl and self._ip_cache_value != "Unknown":
                return self._ip_cache_value   # devolver caché fresco

        # [FIX BUG-V6-015] HTTP timeout is now configurable via VPN_IP_CHECK_TIMEOUT_SECONDS
        # (default: 8s). Hardcoded values are incompatible with slow/fast network tuning.
        _ip_timeout = int(os.getenv("VPN_IP_CHECK_TIMEOUT_SECONDS", "8"))
        services = [
            "https://api.ipify.org?format=text",
            "https://ifconfig.me/ip",
            "https://icanhazip.com",
            "https://ipinfo.io/ip",
            "https://checkip.amazonaws.com",
        ]
        result = "Unknown"
        for service in services:
            try:
                resp = requests.get(service, timeout=_ip_timeout, verify=True)  # [FIX ERR-SEC-002] explicit TLS verification (system CA store)
                if resp.status_code == 200:
                    result = resp.text.strip()
                    break
            except Exception:
                continue

        with self._ip_cache_lock:
            self._ip_cache_value = result
            self._ip_cache_time  = time.time()

        if result == "Unknown":
            logger.warning("⚠️ No se pudo obtener IP actual")
        return result

    def verify_vpn_active(self) -> bool:
        """
        Verifica que la IP actual sea diferente a la original.

        [FIX v2.3] Lógica corregida:
          - original_ip='Unknown' → no hay baseline, asumir activa
          - current='Unknown'    → no podemos verificar, asumir activa
            (mejor falso positivo que reconectar 10 veces simultáneamente)
          - current == original_ip → VPN inactiva (IP real expuesta)

        [FIX-020 / HIGH-011] original_ip read under _ip_cache_lock to prevent
        TOCTOU race. Without the lock, a concurrent call to _detect_original_ip()
        (e.g., during rotation) could overwrite self.original_ip between the check
        and the comparison below, producing a false-positive "VPN active" result.
        """
        # [FIX-020] Read original_ip atomically under lock — prevents TOCTOU race
        with self._ip_cache_lock:
            original = self.original_ip

        # Sin baseline no podemos comparar → asumir activa
        if not original or original == "Unknown":
            logger.warning("⚠️ IP original desconocida, asumiendo VPN activa")
            return True

        current = self.get_current_ip()
        self.current_ip = current

        # No pudimos consultar IP externa → no asumir caída
        if current == "Unknown":
            logger.warning("⚠️ No se pudo verificar IP — asumiendo VPN activa para no reconectar en falso")
            return True

        if current != original:
            logger.info(f"✓ VPN activa — IP: {current}")
            return True

        logger.warning(f"⚠️ VPN inactiva | IP={current} == original={original}")
        return False

    def reconnect_if_disconnected(self) -> bool:
        """
        Verify VPN connectivity and reconnect if the tunnel has dropped.

        [FIX BUG-V11-009] Full documentation added.

        Checks whether the VPN is currently active via `verify_vpn_active()`.
        If the tunnel is down, attempts to reconnect to `self.current_server`.

        Returns:
            bool: True if the VPN is (or was restored to) an active state.
                  False if the reconnection attempt fails.

        Raises:
            Never — connection errors are handled internally by connect().
        """
        if not self.verify_vpn_active():
            logger.warning("🔄 VPN caída, reconectando...")
            return self.connect(self.current_server)
        return True

    # ── ESTADO ────────────────────────────────────────────────────────────────

    def get_status(self) -> Dict:
        """Estado completo de la VPN."""
        is_active = self.verify_vpn_active()
        return {
            "method":           self.method,
            "interactive":      self.interactive,
            "connected":        is_active,
            "server":           self.current_server,
            "current_ip":       self.current_ip,
            "original_ip":      self.original_ip,
            "connection_count": self.connection_count,
            "max_connections":  self.max_connections_per_server,
        }

    def print_status(self):
        """[FIX LOW-006] Logs VPN status through Loguru instead of print()."""
        s = self.get_status()
        logger.info("[VPN] " + "=" * 56)
        logger.info("[VPN] 📊 ESTADO DE VPN")
        logger.info("[VPN] " + "=" * 56)
        logger.info("[VPN]   Método:      {}", s['method'])
        logger.info("[VPN]   Conectada:   {}", '✓ Sí' if s['connected'] else '✗ No')
        logger.info("[VPN]   Servidor:    {}", s['server'] or 'N/A')
        logger.info("[VPN]   IP actual:   {}", s['current_ip'] or 'N/A')
        logger.info("[VPN]   IP original: {}", s['original_ip'] or 'N/A')
        logger.info("[VPN]   Conexiones:  {}/{}", s['connection_count'], s['max_connections'])
        logger.info("[VPN] " + "=" * 56)

    # ── CONTEXT MANAGER ───────────────────────────────────────────────────────

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def __del__(self):
        """✅ FIX: Seguro aunque __init__ haya fallado a medias."""
        try:
            method = getattr(self, "method", None)
            if method == "cli":
                self.disconnect()
        except Exception:
            pass


# =============================================================================
# [FIX BUG-V9-004] vpn_manager_factory
# scraper_service.py imports `vpn_manager_factory` from `app.vpn_manager`.
# The module `app/vpn_manager.py` was absent; the Windows implementation lives
# in `app/vpn_manager_windows.py`.  Adding the factory here and exporting it
# means `from app.vpn_manager import vpn_manager_factory` works when
# vpn_manager.py is absent (scraper_service.py does a runtime import).
#
# The factory creates a singleton NordVPNManagerWindows instance and
# returns it, abstracting the Windows-specific class name from callers.
# =============================================================================

_vpn_singleton: "NordVPNManagerWindows | None" = None
_vpn_singleton_lock = __import__("threading").Lock()


def vpn_manager_factory(interactive: bool = False) -> "NordVPNManagerWindows":
    """
    Return the singleton NordVPNManagerWindows instance (thread-safe).

    Creates the instance on first call. Subsequent calls return the same
    object, which is safe because NordVPNManagerWindows maintains its own
    internal lock for connection operations.

    Args:
        interactive (bool): If True, the manager may prompt for user input
            during initial connection setup. Set False for production/daemon
            use. Defaults to False.

    Returns:
        NordVPNManagerWindows: Ready-to-use VPN manager singleton.

    Raises:
        RuntimeError: If NordVPN is not available on this system and the
            first connection attempt fails immediately.
    """
    # [FIX ERR-CONC-004] The original pattern held _vpn_singleton_lock during
    # NordVPNManagerWindows.__init__(), which calls _detect_original_ip() — a
    # network operation. If that hangs, ALL callers block indefinitely.
    #
    # Fix: acquire the lock ONLY for the double-check + assignment.
    # The expensive init runs OUTSIDE the lock on a temporary local variable.
    # A second guard (already_created) prevents duplicate initialization.
    global _vpn_singleton

    # Fast path: already initialized (no lock needed — read is atomic on CPython)
    if _vpn_singleton is not None:
        return _vpn_singleton

    # Slow path: initialize outside lock, then assign under lock
    _VPN_INIT_TIMEOUT = float(os.environ.get("VPN_INIT_TIMEOUT_SECONDS", "30"))
    _candidate = None
    try:
        import threading as _threading
        _init_error = [None]
        _init_done  = _threading.Event()

        def _do_init():
            try:
                _init_error[0] = None
                nonlocal _candidate
                _candidate = NordVPNManagerWindows(
                    method="auto",
                    interactive=interactive,
                )
            except Exception as exc:
                _init_error[0] = exc
            finally:
                _init_done.set()

        t = _threading.Thread(target=_do_init, daemon=True, name="vpn-init")
        t.start()
        if not _init_done.wait(timeout=_VPN_INIT_TIMEOUT):
            logger.error(
                "[CONC-004] VPN singleton init timed out after %ss — "
                "NordVPN may be unresponsive. Returning None.",
                _VPN_INIT_TIMEOUT,
            )
            return None
        if _init_error[0] is not None:
            raise _init_error[0]
    except Exception as exc:
        logger.error("[CONC-004] VPN singleton init failed: %s", exc)
        return None

    # Assign under lock only after successful init (fast, no network calls)
    with _vpn_singleton_lock:
        if _vpn_singleton is None:   # second check — another thread may have beaten us
            _vpn_singleton = _candidate
            logger.info("[vpn_manager_factory] NordVPNManagerWindows singleton created.")
    return _vpn_singleton


# ── TEST STANDALONE ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    logger.add(sys.stdout, colorize=True)
    logger.add("vpn_windows_test.log", rotation="10 MB")

    # [FIX LOW-006] All output routed through Loguru — consistent with application logging
    logger.info("[VPN TEST] " + "=" * 50)
    logger.info("[VPN TEST]    NORDVPN MANAGER — TEST WINDOWS 11")
    logger.info("[VPN TEST] " + "=" * 50)

    # interactive=True solo para prueba manual
    vpn = NordVPNManagerWindows(method="auto", interactive=True)
    vpn.print_status()

    logger.info("[VPN TEST] Iniciando test de conexión a US...")
    if vpn.connect("US"):
        vpn.print_status()
        logger.info("[VPN TEST] Rotando a DE...")
        vpn.rotate()
        vpn.print_status()
        vpn.disconnect()
    else:
        logger.error("[VPN TEST] ✗ Test de conexión falló")

    logger.info("[VPN TEST] " + "=" * 50)
    logger.info("[VPN TEST]    TEST COMPLETADO")
    logger.info("[VPN TEST] " + "=" * 50)
