# app/config.py — BookingScraper Pro v6.0.0 Build 120
# BUILD 120 — BUG-DB-READONLY-001-FIX: get_readonly_db() usaba "BEGIN READ ONLY" (incorrecto
#              en SQLAlchemy 2.0 + psycopg3 — genera "already in transaction" warning y
#              NO aplica el modo read-only). Fix: sustituir por "SET TRANSACTION READ ONLY".
#              app/database.py. Impacto producción=0 (función sin importadores activos).
#
# BUILD 118 — BUG-VPN-001-FIX: dos nuevos campos de configuración VPN:
#   VPN_CB_UNKNOWN_IP_AS_SUCCESS: controla si "Unknown" del check de IP
#     se trata como éxito (True, default) o fallo (False, legacy) cuando
#     el CLI de NordVPN confirmó la conexión. Evita que timeouts DNS de
#     api.ipify.org disparen el circuit breaker.
#   VPN_CB_COOLDOWN_S: cooldown del circuit breaker VPN (antes hardcodeado
#     a 300s). Permite ajuste operacional sin modificar código.
# BUILD 118 — BUG-RETRY-001-FIX: ver scraper_service.py.
# BUILD 116 — NAV-TIMEOUT-001-FIX: NAVIGATION_TIMEOUT_S — timeout en daemon
#              thread para driver.get(url) en _fetch_with_selenium(). Bloqueo
#              indefinido confirmado en INC-2026-0602-BROWSER-FREEZE-001.
# BUILD 116 — BUG-DNS-RACE-001-FIX: VPN_DNS_STABILIZE_DELAY_S — delay post-
#              conexión VPN para estabilización DNS. Evidencia: 6 fallos
#              NameResolutionError cf.bstatic.com en INC-2026-0602-BROWSER-FREEZE-001.
# BUILD 115 — BUG-BROWSER-RESTART-HANG-001: driver.quit() se bloqueaba
#              indefinidamente en Windows 11 cuando Brave estaba atascado en
#              una página de desafío. reset_browser() quedaba colgado dentro
#              de self._lock. Observado 2026-06-02 16:02:55 → watchdog 16:03:04.
#              Fix: quit() en daemon thread con join(BROWSER_QUIT_TIMEOUT_S=30).
#              Si timeout, psutil fuerza el kill del proceso.
# BUILD 115 — BUG-BROWSER-LAUNCH-HANG-001: webdriver.Chrome() puede bloquearse
#              si Brave/ChromeDriver no responden. Fix: launch en daemon thread
#              con join(BROWSER_LAUNCH_TIMEOUT_S=60).
# BUILD 115 — BUG-CHAL-DETECT-002: _url_has_challenge_params() solo verificaba
#              antes de driver.get(). Booking.com puede redirigir a chal_t= DESPUÉS
#              de la carga. Fix: check driver.current_url post-navegación en
#              _fetch_with_selenium() y _open_gallery().
# BUILD 115 — BUG-GALLERY-CHAL-001: clic en galería puede desencadenar redirect
#              de desafío. Fix: check current_url en _open_gallery() y
#              GalleryModalExtractor.extract() cuando url != None.
# BUILD 115 — BUG-BLOCK-IND-002: _BLOCK_INDICATORS sin strings de Cloudflare
#              genéricos. Añadidos: "verifying your browser", "please wait while
#              we verify", "chal_t" (HTML embebido), "challenge".
# BUILD 115 — BUG-WORKER-NORESTART-001: worker no se reiniciaba tras os._exit(1).
#              Beat acumulaba tareas 2h45m (16:03→18:49) sin consumidor.
#              Fix: start_celery.bat con bucle de reinicio automático (exit!=0).
# BUILD 114 — BUG-VPN-HANG-001: subprocess.run(capture_output=True, timeout=N) en
#              Windows 11 puede bloquearse indefinidamente (6+ h) cuando nordvpn.exe
#              lanza procesos hijo que heredan los pipes stdout/stderr. Al expirar
#              el timeout, subprocess mata el proceso padre pero los hijos mantienen
#              los pipes abiertos — communicate() espera EOF para siempre. El worker
#              Celery queda congelado y el Beat acumula tareas en la cola sin que
#              nadie las procese. Incidente documentado: INC-2026-0602-RADISSON-001,
#              tarea d1c14507, colgado 02:16:23→08:16:07 (6h silencio).
#              Fix (BUG-VPN-HANG-001-FIX): _subprocess_run_safe() wrappea el
#              subprocess en un daemon thread; join(timeout) proporciona corte de
#              tiempo garantizado independientemente del estado de los pipes.
#              Nuevos toggles: VPN_SUBPROCESS_TIMEOUT_S, VPN_ROTATE_TIMEOUT_S.
# BUILD 114 — BUG-TASK-HANG-001: Celery time_limit/soft_time_limit con pool=solo en
#              Windows 11 no funcionan (implementados vía señales POSIX SIGKILL/SIGUSR1
#              no disponibles en Windows). La tarea d1c14507 corrió 6h sin ser matada
#              aunque time_limit=300. Fix: watchdog threading.Timer dentro de la tarea
#              con TASK_WATCHDOG_TIMEOUT_S (default 600s). Nuevo toggle añadido.
# BUILD 114 — BUG-CHAL-DETECT-001: URLs con parámetros de bot-detection de Booking.com
#              (chal_t=, force_referer=) no se detectaban antes de driver.get(), lo que
#              causaba cargas de página indefinidas. Fix: detección temprana en
#              _fetch_with_selenium() — abortar y rotar VPN antes de intentar cargar.
# BUILD 114 — CFG-VPN-INTERVAL-001: VPN_ROTATION_INTERVAL aumentado de 50s a 120s.
#              Intervalo de 50s era demasiado agresivo con 2 hilos simultáneos,
#              causando rotaciones casi continuas y mayor probabilidad de bot-detection.
# BUILD 113 — BUG-VPN-POPUP-DIRECT-001: popup «¿Pausar la conexión automática?»
#              aparece en cada rotación VPN. rotate() llamaba nordvpn -d antes
#              de conectar, lo que activa el diálogo de pausa de auto-conexión.
#              Fix: rotate() llama nordvpn -c -g "country" directamente (sin
#              disconnect previo), igual que el benchmark validado
#              extraer_imagenes.py. Popup eliminado por diseño. Nuevo toggle:
#              VPN_ROTATE_SKIP_DISCONNECT (default True).
# BUILD 112 — BUG-CONFIG-SYNC-001: BUILD_VERSION default desincronizado (107 vs 111).
#              El campo Pydantic devolvía 107 cuando BUILD_VERSION no estaba en .env.
#              Default actualizado a 112. Nota añadida en el campo.
# BUILD 112 — BUG-ONLYTITLE-001: args.onlyTitle hardcodeado a True en el payload.
#              api_payload_builder.py y api_export_system.py enviaban siempre
#              onlyTitle=True, silenciando todos los campos de data[] excepto
#              name/longDescription en la API externa. Nuevo toggle:
#              API_EXPORT_ONLY_TITLE (default False — producción completa).
# BUILD 111 — BUG-SVC-POPULAR-CAT-001: service_category vacía en el fallback
#              "Most popular facilities". Auditoría verificada contra
#              pruebas/_table__hotels_all_services__.csv: 510 servicios (0,77%)
#              en 53 pares (hotel,idioma) quedaban con service_category=""
#              porque, cuando TODAS las estrategias de facility-group-container
#              fallan, el único origen es property-most-popular-facilities-wrapper
#              (Strategy 4), que descartaba la cabecera <h3> del bloque. El
#              encabezado existe en el DOM ("Most popular facilities" /
#              "Instalaciones más populares" / …) y se extrae VERBATIM (sin
#              inferencia ni traducción — coherente con Build 103). Nuevo toggle:
#              SVC_POPULAR_FALLBACK_CATEGORY_ENABLED. Coordinado con
#              app/extractor.py y app/__init__.py. schema_v77_complete.sql NO
#              cambia (no se añade NOT NULL: rompería la recreación de BD).
# BUILD 110 — BUG-GALLERY-MODAL-001: robustez de captura del modal de galería.
#              Auditoría: 35.7% de hoteles (50/140) acababan con 0 fotos
#              gallery_visible (modal no abierto) → el payload recaía en el
#              superconjunto. Nuevos toggles: GALLERY_MODAL_DISMISS_CONSENT,
#              GALLERY_MODAL_OPEN_RETRIES, API_IMAGES_STRICT_GALLERY.
#              Coordinado con image_classifier.py (prep de página + reintentos)
#              y api_payload_builder.py (modo estricto opcional).
# BUILD 109 — BUG-IMG-CLASS-001: clasificación de imágenes (galería vs no-galería).
#              Nuevos toggles: IMAGE_CLASSIFICATION_ENABLED, API_IMAGES_GALLERY_ONLY,
#              GALLERY_MODAL_TIMEOUT_S, GALLERY_MODAL_SCROLL_ITERATIONS,
#              GALLERY_MODAL_SCROLL_PAUSE_S. Coordinado con schema/models/
#              extractor(scraper)/image_downloader/api_payload_builder/image_classifier.
# BUILD 108 — BUG-IMG-NAME-001: campo name_jpg en image_downloads (sin cambios
#              funcionales en config.py; build coordinado en schema/models/image_downloader).
# BUILD 107 — BUG-IMG-DERIVE-001-FIX: extractor deriva 3 tallas de imagen
#              (max200/max1024x768/max1280x900) reutilizando el token k=.
#              highres 49,3%->100%, thumb 93,1%->100%. No limita la extracción.
# BUILD 106 — BUG-EN-LAZY-001-FIX: scraper.py multi-scroll retry loop (3×8s).
#             BUG-IMG-CAP-002-FIX: image_downloader.py task cap removed.
# =============================================================================
# BUILD 101 — BUG-SVC-NULL-001-FIX: Expanded _SERVICE_CATEGORY_RULES + _add() auto-inference
# BUILD 100 — Technical Audit Build
# BUILD 99 — BUG-SVC-DOM-001-FIX: DOM strategies primary; Apollo JSON fallback
# BUILD 98 — BUG-SVC-002 + BUG-EXTRACT-IT-001 + GAP-EXPORT-001 FIXES
# BUILD 97 — BUG-HTML-FP-001 + BUG-CATMAP-001 + BUG-LOCALES-EN-001 FIXES
#   api_payload_builder.py: toConsider HTML→plaintext, category map 5 entradas,
#   args.locales en-first, primary desde registro 'en'.
#
# BUILD 64 — BUG-DATA-001 + BUG-PERF-001 FIXES
#   Added: SELENIUM_CONTENT_WAIT_TIMEOUT_S (BUG-PERF-001)
#          LANG_SCRAPE_DELAY_IT             (BUG-PERF-001)
#
# BUILD 63 — CLOUDSCRAPER ELIMINATED
#   MAX_LANG_RETRIES: repurposed as Selenium retry count (was CloudScraper)
#   SCRAPER_RETRY_DELAY: repurposed as Selenium backoff (was CloudScraper)
#   Descriptions updated; defaults unchanged.
#
# BUILD 62 — BUG-LANG-002 FIX
#   Added: SELENIUM_RESET_LANG_ON_EACH_REQUEST
#          SELENIUM_RESTART_AFTER_VPN_ROTATE
#          SELENIUM_LANG_VERIFY_TIMEOUT_S
#
# BUILD 61 — BUG-LANG-001 FIX
#   Added: LANG_SCRAPE_DELAY, LANG_SCRAPE_JITTER,
#          MAX_CONSECUTIVE_LANG_FAILURES, SHORT_HTML_THRESHOLD
# =============================================================================

from __future__ import annotations

import secrets
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


# ---------------------------------------------------------------------------
# Canonical VPN country list (module-level constant)
# ---------------------------------------------------------------------------
# BUG-IMPORT-003 (Build 63-fix):
#   vpn_manager_windows.py:39 imports this frozenset directly from app.config:
#     from app.config import get_settings, _VALID_VPN_COUNTRIES
#   The constant was removed accidentally in Build 63 during the CloudScraper
#   cleanup, causing every ScraperService instantiation to raise ImportError
#   even when VPN_ENABLED=False (NullVPNManager imports the same module).
#
#   Naming conventions included:
#     - Space form   → matches COUNTRY_NAMES dict in vpn_manager_windows.py
#                      (e.g. "United Kingdom", "United States")
#     - Underscore   → matches env.example / .env format
#                      (e.g. "United_Kingdom", "United_States")
#   Both variants are accepted so that _validate_country() succeeds regardless
#   of whether the user wrote the country with spaces or underscores in .env.
_VALID_VPN_COUNTRIES: frozenset = frozenset({
    # ── Single-word countries ──────────────────────────────────────────────
    "Spain",
    "Germany",
    "France",
    "Netherlands",
    "Italy",
    "Canada",
    "Sweden",
    "Switzerland",
    "Norway",
    "Denmark",
    "Poland",
    "Austria",
    "Belgium",
    "Portugal",
    "Finland",
    "Romania",
    "Hungary",
    "Japan",
    "Australia",
    "Singapore",
    "Brazil",
    # ── Multi-word — space form (COUNTRY_NAMES dict in vpn_manager_windows) ─
    "United Kingdom",
    "United States",
    # ── Multi-word — underscore form (env.example / .env format) ──────────
    "United_Kingdom",
    "United_States",
})


class Settings(BaseSettings):
    """
    Centralised application configuration via Pydantic Settings.
    All values are loaded from the .env file (or environment variables).
    """

    # ── Application identity ───────────────────────────────────────────────────
    # BUG-CFG-001 (Build 63-fix): verify_system.py accedía a s.APP_NAME,
    #   s.APP_VERSION y s.BUILD_VERSION pero estos atributos no existían en
    #   Settings, causando AttributeError en el chequeo de configuración.
    #   Se exponen aquí con defaults alineados a app/__init__.py.
    APP_NAME: str = Field(
        default="BookingScraper Pro",
        description="Application display name.",
    )
    APP_VERSION: str = Field(
        default="6.0.0",
        description="Application semantic version (SemVer).",
    )
    BUILD_VERSION: int = Field(
        default=120,
        description=(
            "Incremental build number. "
            "⚠️ MANTENER SINCRONIZADO con BUILD_VERSION en app/__init__.py "
            "al inicio de cada ciclo de build."
        ),
    )

    # ── Security ──────────────────────────────────────────────────────────────
    SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(48),
        description="Application secret key. Regenerate with: "
                    "python -c \"import secrets; print(secrets.token_urlsafe(48))\"",
    )
    API_KEY: str = Field(default="", description="API authentication key (optional).")
    REQUIRE_API_KEY: bool = Field(
        default=False,
        description="Enforce API_KEY on all API endpoints.",
    )

    # ── Database ──────────────────────────────────────────────────────────────
    DB_HOST: str = Field(default="localhost", description="PostgreSQL hostname.")
    DB_PORT: int = Field(default=5432, description="PostgreSQL port.")
    DB_NAME: str = Field(default="bookingscraper", description="PostgreSQL database name.")
    DB_USER: str = Field(description="PostgreSQL username (required).")
    DB_PASSWORD: str = Field(description="PostgreSQL password (required).")

    # Connection pool — Windows 11: max_connections=50 in postgresql.conf
    DB_POOL_SIZE: int = Field(
        default=10, ge=1, le=50,
        description="SQLAlchemy connection pool size.",
    )
    DB_MAX_OVERFLOW: int = Field(
        default=5, ge=0, le=20,
        description="Max overflow connections above DB_POOL_SIZE.",
    )
    DB_POOL_TIMEOUT: int = Field(
        default=30, ge=5, le=120,
        description="Seconds to wait for a pool connection before raising.",
    )
    DB_POOL_RECYCLE: int = Field(
        default=3600, ge=60,
        description="Recycle connections older than this many seconds.",
    )

    # ── Redis / Memurai ───────────────────────────────────────────────────────
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis/Memurai connection URL.",
    )
    REDIS_MAX_CONNECTIONS: int = Field(
        default=20, ge=5, le=100,
        description="Maximum Redis connection pool size.",
    )
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Celery broker URL.",
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/1",
        description="Celery result backend URL.",
    )

    # ── Scraper ───────────────────────────────────────────────────────────────
    SCRAPER_MAX_WORKERS: int = Field(
        default=2, ge=1, le=10,
        description="Number of parallel URL workers (ThreadPoolExecutor).",
    )
    SCRAPER_REQUEST_TIMEOUT: int = Field(
        default=30, ge=5, le=120,
        description="Selenium page load timeout in seconds.",
    )

    # Build 63: these fields are now Selenium-specific (CloudScraper removed)
    SCRAPER_RETRY_DELAY: float = Field(
        default=2.0, ge=0.5, le=30.0,
        description="[Build 63: Selenium] Base delay (seconds) between retries. "
                    "Actual wait = SCRAPER_RETRY_DELAY × attempt_number.",
    )
    MAX_RETRIES: int = Field(
        default=3, ge=1, le=10,
        description="Maximum retries per URL at the batch dispatcher level.",
    )
    MAX_LANG_RETRIES: int = Field(
        default=3, ge=1, le=10,
        description="[Build 63: Selenium] Maximum retries per language per URL. "
                    "Previously used by CloudScraper; now applies to Selenium.",
    )

    # ── Browser / Selenium ────────────────────────────────────────────────────
    HEADLESS_BROWSER: bool = Field(
        default=False,
        description="Run browser headless (true=production, false=debug).",
    )
    BRAVE_PATH: Optional[str] = Field(
        default=None,
        description="Full path to Brave browser binary. "
                    "If None, uses system Chrome.",
    )
    CHROMEDRIVER_PATH: Optional[str] = Field(
        default=None,
        description="Full path to ChromeDriver executable. "
                    "If None, uses PATH-detected driver.",
    )

    # ── BUG-LANG-001 FIX (Build 61) ───────────────────────────────────────────
    LANG_SCRAPE_DELAY: float = Field(
        default=10.0, ge=0.0, le=120.0,
        description="BUG-LANG-001-FIX: Base delay (seconds) between consecutive "
                    "language requests for the same URL. Simulates human reading "
                    "time between pages. Reduces bot-detection by Cloudflare.",
    )
    LANG_SCRAPE_JITTER: float = Field(
        default=5.0, ge=0.0, le=30.0,
        description="BUG-LANG-001-FIX: Random jitter (0..N seconds) added to "
                    "LANG_SCRAPE_DELAY. Prevents predictable request intervals.",
    )
    MAX_CONSECUTIVE_LANG_FAILURES: int = Field(
        default=1, ge=1, le=6,
        description="BUG-LANG-001-FIX [Build 62: 2→1]: Force VPN rotation after "
                    "this many consecutive language failures. Combined with the "
                    "ip_known_blocked flag in scraper_service.py, VPN rotates "
                    "before the second failed language attempt.",
    )
    SHORT_HTML_THRESHOLD: int = Field(
        default=5_000, ge=1_000, le=20_000,
        description="BUG-LANG-001-FIX: HTML responses smaller than this (bytes) "
                    "are classified as Cloudflare challenge pages and discarded "
                    "immediately. Real Booking.com pages are 150k–500k bytes.",
    )

    # ── BUG-PERF-001 FIX (Build 64) ───────────────────────────────────────────
    # Root cause: WebDriverWait iterates over 4 CSS selectors × 30 s each =
    # worst-case 120 s per language pass when no selector matches (partial load).
    # Observed: it=144.0 s and it=124.6 s in the 2026-04-01 run (15.4% outlier).
    # Italian consistently slowest: avg 73.7 s, stddev 29.5 s vs 5.6-12.7 s
    # for other languages.  Two fixes:
    #   1. SELENIUM_CONTENT_WAIT_TIMEOUT_S: reduces per-selector wait from 30 s
    #      to a configurable shorter value (default 10 s → worst-case 40 s).
    #   2. LANG_SCRAPE_DELAY_IT: extra pre-scrape pause for Italian to reduce
    #      anti-bot challenge probability accumulated during the session.
    SELENIUM_CONTENT_WAIT_TIMEOUT_S: float = Field(
        default=10.0, ge=2.0, le=60.0,
        description=(
            "BUG-PERF-001-FIX: Seconds each CSS selector in the hotel-content "
            "wait loop is allowed to wait before trying the next one. "
            "With 4 selectors, worst-case total = 4 x this value. "
            "Previously this was SCRAPER_REQUEST_TIMEOUT (30 s) -> 120 s worst case. "
            "Default 10 s -> 40 s worst case. Raise only if pages consistently "
            "load slower than 10 s on your network."
        ),
    )
    LANG_SCRAPE_DELAY_IT: float = Field(
        default=5.0, ge=0.0, le=60.0,
        description=(
            "BUG-PERF-001-FIX: Extra pre-scrape delay (seconds) applied "
            "exclusively to the Italian language pass. Italian pages show "
            "avg 73.7 s vs 49-64 s for other languages (stddev 29.5 s, "
            "2 outliers > 120 s in 13 scrapes = 15.4%). The delay spaces "
            "Italian requests further apart to reduce anti-bot challenge risk."
        ),
    )

    # ── BUG-LANG-002 FIX (Build 62) ───────────────────────────────────────────
    SELENIUM_RESET_LANG_ON_EACH_REQUEST: bool = Field(
        default=True,
        description="BUG-LANG-002-FIX: When True, SeleniumEngine injects the "
                    "correct Accept-Language header via CDP and calls "
                    "delete_all_cookies() before every driver.get(). Prevents "
                    "Booking.com session cookies (bkng_lang) from overriding the "
                    "?lang=XX URL parameter.",
    )
    SELENIUM_RESTART_AFTER_VPN_ROTATE: bool = Field(
        default=True,
        description="BUG-LANG-002-FIX: When True, ScraperService calls "
                    "selenium_engine.reset_browser() after every forced VPN "
                    "rotation. Guarantees a clean browser profile: no cached DNS, "
                    "no TLS session resumption, no stale Booking.com cookies.",
    )
    SELENIUM_LANG_VERIFY_TIMEOUT_S: float = Field(
        default=5.0, ge=1.0, le=30.0,
        description="Seconds to wait for language verification after page load.",
    )

    # ── BUG-VPN-006-FIX (Build 70) ────────────────────────────────────────────
    # Isolated Brave profile for Selenium.  NordVPN opens the SYSTEM DEFAULT
    # browser profile; by giving Selenium a different user-data-dir these two
    # Brave instances never share a profile or window, preventing NordVPN's
    # OAuth / help-center tabs from appearing inside the scraping session.
    # Set to empty string "" to disable (Selenium uses system default profile).
    SELENIUM_BRAVE_PROFILE_DIR: str = Field(
        default="",  # BUILD 74: disabled — use default system Brave profile
        description=(
            "BUG-VPN-006-FIX: Dedicated Brave user-data-dir for the Selenium "
            "scraping session. NordVPN opens the system default browser profile; "
            "this path keeps both Brave instances fully isolated so NordVPN's "
            "nordaccount.com tabs never appear inside the Selenium window. "
            "Set to '' to disable (reverts to shared system profile). "
            "Directory is created automatically if it does not exist."
        ),
    )

    # ── VPN — NordVPN ─────────────────────────────────────────────────────────
    VPN_ENABLED: bool = Field(
        default=True,
        description="Enable NordVPN rotation for IP diversity.",
    )
    VPN_COUNTRIES: str = Field(
        default="Spain,Germany,France,Netherlands,Italy,United_Kingdom,Canada,Sweden",
        description="Comma-separated list of NordVPN countries to rotate through.",
    )
    VPN_ROTATION_INTERVAL: int = Field(
        default=120, ge=10, le=600,
        description="Minimum seconds between routine VPN rotations. "
                    "CFG-VPN-INTERVAL-001 (Build 114): raised from 50 to 120s — "
                    "50s was too aggressive for 2 concurrent threads, causing near-"
                    "continuous rotations that increased bot-detection probability. "
                    "Forced rotations (ip_known_blocked) bypass this gate.",
    )
    VPN_ROTATE_SKIP_DISCONNECT: bool = Field(
        default=True,
        description=(
            "Build 113 (BUG-VPN-POPUP-DIRECT-001-FIX): si True (default), "
            "rotate() omite nordvpn -d y llama nordvpn -c -g 'country' "
            "directamente. Elimina el popup «¿Pausar la conexión automática?» "
            "que NordVPN muestra cuando auto-connect está activo. "
            "False = comportamiento legacy (disconnect + connect) para "
            "entornos con auto-connect desactivado o que requieran la "
            "desconexión explícita por política de red. "
            "Verificado contra pruebas/extraer_imagenes.py (141 hoteles, 0 popups)."
        ),
    )

    # BUG-VPN-HANG-001-FIX (Build 114): Timeouts para prevenir colgados de subprocess
    # en Windows 11. subprocess.run(capture_output=True, timeout=N) puede colgar
    # indefinidamente cuando nordvpn.exe crea procesos hijo que heredan los pipes.
    VPN_SUBPROCESS_TIMEOUT_S: int = Field(
        default=45, ge=10, le=120,
        description=(
            "BUG-VPN-HANG-001-FIX (Build 114): Timeout en segundos para las "
            "llamadas subprocess a nordvpn.exe. Implementado como daemon thread "
            "(no como subprocess.run timeout) para garantizar corte en Windows "
            "aunque procesos hijo mantengan los pipes abiertos. "
            "45s es suficiente para que nordvpn.exe complete; 60s original "
            "podía colgar indefinidamente."
        ),
    )

    VPN_ROTATE_TIMEOUT_S: int = Field(
        default=90, ge=20, le=300,
        description=(
            "BUG-VPN-HANG-001-FIX (Build 114): Timeout máximo en segundos para "
            "una operación completa de rotación VPN (subprocess + sleeps + IP check). "
            "Si rotate() no completa en este tiempo, el hilo watchdog considera la "
            "rotación fallida y el proceso continúa sin rotación. "
            "Implementado vía threading.Thread.join(timeout) en scraper_service.py."
        ),
    )

    TASK_WATCHDOG_TIMEOUT_S: int = Field(
        default=600, ge=60, le=7200,
        description=(
            "BUG-TASK-HANG-001-FIX (Build 114): Timeout del watchdog threading.Timer "
            "dentro de scrape_pending_urls. Celery time_limit/soft_time_limit usan "
            "señales POSIX (SIGKILL/SIGUSR1) que NO están disponibles en Windows 11 "
            "con pool=solo — son completamente no funcionales. Este watchdog reemplaza "
            "esa protección con un threading.Timer que llama os._exit(1) si la tarea "
            "no completa en TASK_WATCHDOG_TIMEOUT_S segundos. "
            "Default 600s (10 min): batches legítimos de 2 URLs completan en <10 min. "
            "Un colgado de 6 horas es inaceptable; 10 min es conservador pero efectivo."
        ),
    )

    # BUG-BROWSER-RESTART-HANG-001-FIX / BUG-BROWSER-LAUNCH-HANG-001-FIX (Build 115)
    # Timeouts para operaciones de driver Selenium que pueden bloquearse en Windows 11.
    BROWSER_QUIT_TIMEOUT_S: int = Field(
        default=30, ge=5, le=120,
        description=(
            "BUG-BROWSER-RESTART-HANG-001-FIX (Build 115): Timeout en segundos para "
            "driver.quit() en reset_browser(). En Windows 11, si Brave está atascado "
            "en una página de desafío JavaScript (chal_t=), driver.quit() puede "
            "bloquearse indefinidamente ya que ChromeDriver espera que Brave responda "
            "al comando de cierre y Brave nunca lo hace. "
            "Fix: quit() se ejecuta en un daemon thread; si no completa en "
            "BROWSER_QUIT_TIMEOUT_S, psutil mata los procesos Brave/ChromeDriver "
            "forzosamente para liberar self._lock. Default 30s."
        ),
    )
    BROWSER_LAUNCH_TIMEOUT_S: int = Field(
        default=60, ge=10, le=300,
        description=(
            "BUG-BROWSER-LAUNCH-HANG-001-FIX (Build 115): Timeout en segundos para "
            "la instanciación de webdriver.Chrome() en _get_driver(). En Windows 11, "
            "si Brave o ChromeDriver no responden durante la inicialización (p. ej. "
            "tras una rotación VPN cuando el sistema de red aún está estabilizándose), "
            "webdriver.Chrome() puede bloquearse sin límite de tiempo mientras se "
            "mantiene self._lock. Fix: Chrome() se lanza en un daemon thread; si no "
            "responde en BROWSER_LAUNCH_TIMEOUT_S, se lanza WebDriverException y el "
            "idioma falla de forma limpia para reintentarse en el siguiente batch. "
            "Default 60s."
        ),
    )

    NAVIGATION_TIMEOUT_S: int = Field(
        default=45, ge=10, le=120,
        description=(
            "NAV-TIMEOUT-001-FIX (Build 116): Timeout en segundos para la llamada "
            "driver.get(url) en _fetch_with_selenium(). Booking.com/Cloudflare pueden "
            "servir una página de desafío que carga inmediatamente (sin disparar "
            "TimeoutException en el WebDriverWait de contenido) pero luego entra en "
            "un loop JS infinito que bloquea driver.page_source y execute_script() "
            "indefinidamente. Fix: driver.get() se ejecuta en un daemon thread con "
            "join(NAVIGATION_TIMEOUT_S). En timeout, se intenta window.stop() "
            "(best-effort) y se retorna None para que el idioma falle limpiamente. "
            "Incidente de referencia: INC-2026-0602-BROWSER-FREEZE-001. "
            "Default 45s (conservador: driver.set_page_load_timeout=30s + margen)."
        ),
    )

    VPN_DNS_STABILIZE_DELAY_S: float = Field(
        default=5.0, ge=0.0, le=30.0,
        description=(
            "BUG-DNS-RACE-001-FIX (Build 116): Segundos de espera adicional después "
            "de que rotate() retorna True, antes de ejecutar cualquier petición de red "
            "que dependa de DNS. NordVPN reporta 'connected' antes de que el routing "
            "DNS del SO esté completamente actualizado; las consultas DNS disparadas "
            "en los primeros ~2-3 segundos tras la conexión pueden resolver contra la "
            "interfaz anterior. Evidencia: 6 fallos NameResolutionError para "
            "cf.bstatic.com en INC-2026-0602-BROWSER-FREEZE-001 (L2843-2845 del log). "
            "Valor 0.0 deshabilita el delay (no recomendado si VPN_ENABLED=true). "
            "Default 5.0s."
        ),
    )

    VPN_CB_UNKNOWN_IP_AS_SUCCESS: bool = Field(
        default=True,
        description=(
            "BUG-VPN-001-FIX (Build 118): Controla cómo se trata un resultado "
            "'Unknown' del servicio de verificación IP (api.ipify.org, etc.) cuando "
            "el CLI de NordVPN SÍ confirmó la conexión (rc=0 / 'connected' en stdout). "
            "True (default): se trata como éxito → record_success() → circuit breaker "
            "NO se incrementa. Se emite WARNING en el log. Esta es la causa raíz del "
            "lockout del CB en Build 115: 3 timeouts DNS de api.ipify.org (slow DNS "
            "post-VPN-connect) dispararon record_failure() x3 → CB abierto, aunque "
            "NordVPN había conectado correctamente cada vez. "
            "False (legacy): Unknown se trata como fallo → record_failure() → "
            "comportamiento anterior al Build 118. Solo usar en entornos donde los "
            "servicios de verificación IP son siempre fiables."
        ),
    )

    VPN_CB_COOLDOWN_S: float = Field(
        default=300.0, ge=10.0, le=3600.0,
        description=(
            "BUG-VPN-001-FIX (Build 118): Segundos de cooldown del circuit breaker "
            "VPN antes de que se cierre automáticamente tras abrirse por fallos "
            "consecutivos. Antes hardcodeado a 300s en VPNCircuitBreaker.__init__. "
            "Ahora configurable para ajuste operacional sin cambios de código. "
            "Valor más bajo (ej. 60s): recuperación más rápida tras fallos transitorios. "
            "Valor más alto (ej. 600s): más protección contra tormentas de errores. "
            "Rango válido: 10 - 3600 | Default: 300s."
        ),
    )
    # ==========================================================================
    # ENABLED_LANGUAGES define qué idiomas se scrapeán.
    # TODA la configuración de traducción, categorización y mapeos de idioma
    # vive en el archivo JSON indicado por LANGUAGES_CONFIG_FILE.
    # No hay hardcoding de idiomas en ningún módulo Python.
    #
    # Al añadir un nuevo idioma a ENABLED_LANGUAGES:
    #   1. Añadir el código ISO 639-1 a ENABLED_LANGUAGES (ej: "ru")
    #   2. Completar TODAS las secciones de languages.json para ese idioma:
    #      lang_url_codes, lang_accept_headers, room_level_category_labels,
    #      category_key_map (todos los api_keys), category_labels,
    #      facility_group_map (todos los group_ids)
    #   3. Reiniciar el sistema — el validador LanguageConfigValidator
    #      BLOQUEA el arranque si cualquier sección está incompleta.
    # ==========================================================================

    ENABLED_LANGUAGES: str = Field(
        default="en,es,de,it,fr,pt",
        description=(
            "Comma-separated ISO 639-1 language codes to scrape. "
            "'en' is mandatory and always processed first. "
            "Adding a language here REQUIRES completing all sections "
            "in LANGUAGES_CONFIG_FILE for that language. "
            "The startup validator BLOCKS launch if coverage is incomplete."
        ),
    )

    LANGUAGES_CONFIG_FILE: str = Field(
        default="languages.json",
        description=(
            "Path to the JSON file with ALL language-dependent dictionaries. "
            "Absolute path or relative to project root. "
            "Single source of truth — no language data is hardcoded in Python. "
            "Sections: lang_url_codes, lang_accept_headers, "
            "room_level_category_labels, category_key_map, category_labels, "
            "facility_group_map, service_category_rules, see_all_patterns."
        ),
    )
    # ── Logging ───────────────────────────────────────────────────────────────
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Python logging level (DEBUG, INFO, WARNING, ERROR).",
    )
    LOG_MAX_BYTES: int = Field(
        default=10_485_760,
        description="Max log file size in bytes before rotation (default: 10 MB).",
    )
    LOG_BACKUP_COUNT: int = Field(
        default=5,
        description="Number of rotated log files to keep.",
    )

    # ── Debug ─────────────────────────────────────────────────────────────────
    DEBUG: bool = Field(
        default=False,
        description="Enable debug mode (verbose output).",
    )
    DEBUG_HTML_SAVE: bool = Field(
        default=False,
        description="Persist raw HTML for failed/blocked requests to disk. "
                    "Increases disk usage; enable only for troubleshooting.",
    )
    DEBUG_HTML_MAX_AGE_HOURS: int = Field(
        default=24,
        description="Hours to retain saved debug HTML files before purge.",
    )

    # ── Filesystem paths ──────────────────────────────────────────────────────
    # BUG-CFG-002 (Build 63-fix): main.py, tasks.py and image_downloader.py
    #   access cfg.LOGS_DIR, cfg.LOGS_DEBUG_DIR, cfg.IMAGES_DIR and
    #   cfg.DEBUG_HTML_DIR as Path objects.  These were not declared in
    #   Settings, causing AttributeError at application startup.
    #   Defaults mirror the directory structure created by verify_system.py
    #   and visible under the project root on Windows 11.
    LOGS_DIR: Path = Field(
        default=Path("logs"),
        description="Directory for rotating application log files. "
                    "Relative to the project root (C:\\BookingScraper).",
    )
    LOGS_DEBUG_DIR: Path = Field(
        default=Path("data/logs/debug"),
        description="Directory for debug-level log artefacts.",
    )
    IMAGES_DIR: Path = Field(
        default=Path("data/images"),
        description="Root directory for downloaded hotel images. "
                    "Sub-directories are created per hotel_id at runtime.",
    )
    DEBUG_HTML_DIR: Path = Field(
        default=Path("data/debug_html"),
        description="Directory where _save_debug_html() persists raw HTML "
                    "for blocked/short responses when DEBUG_HTML_SAVE=true.",
    )

    # ── Image classification (Build 109 — BUG-IMG-CLASS-001) ──────────────────
    # Clasifica cada foto como gallery_visible (exportable a la API) o no-galería
    # (conservada por subcategoría). El conjunto de galería se captura en vivo
    # abriendo el modal durante el pase EN (mismo algoritmo validado por
    # pruebas/extraer_imagenes.py). Si se desactiva, todas las fotos quedan como
    # gallery_visible=False/subcategory='unknown' y el payload recae en el
    # conjunto histórico (ver API_IMAGES_GALLERY_ONLY).
    IMAGE_CLASSIFICATION_ENABLED: bool = Field(
        default=True,
        description="Activa la captura del modal de galería + clasificación de "
                    "fotos en el pase EN (Build 109).",
    )
    API_IMAGES_GALLERY_ONLY: bool = Field(
        default=True,
        description="Si True, el payload images[] incluye SOLO fotos "
                    "gallery_visible=TRUE, ordenadas por gallery_order. Red de "
                    "seguridad: si un hotel no tiene galería, recae en todas las "
                    "descargas 'done'.",
    )
    GALLERY_MODAL_TIMEOUT_S: float = Field(
        default=25.0, ge=5.0, le=120.0,
        description="Timeout (s) de espera del wrapper del modal de galería.",
    )
    GALLERY_MODAL_SCROLL_ITERATIONS: int = Field(
        default=8, ge=1, le=40,
        description="Iteraciones de scroll dentro del modal (replica "
                    "extraer_imagenes.py: 8 × 1.5 s).",
    )
    GALLERY_MODAL_SCROLL_PAUSE_S: float = Field(
        default=1.5, ge=0.2, le=10.0,
        description="Pausa (s) entre iteraciones de scroll del modal.",
    )
    # ── Build 110 (BUG-GALLERY-MODAL-001) — robustez de captura del modal ─────
    # Auditoría Build 109→110: 50/140 hoteles (35.7%) terminaron con 0 fotos
    # gallery_visible porque el modal NO se abrió en vivo (p. ej. Topazz 76033:
    # 56 fotos, todas js_array). Causas verificadas contra el código:
    #   (a) NO se descarta el overlay de consentimiento (OneTrust); además, las
    #       cookies se borran antes de CADA fetch (BUG-LANG-002-FIX), por lo que
    #       el banner reaparece y nunca se acepta → intercepta el clic del abridor.
    #   (b) _open_gallery() hace clic en la <img> hero → deja un lightbox de una
    #       sola foto abierto antes de la captura de la rejilla.
    #   (c) tras el pre-scroll a document.body.scrollHeight la página queda ABAJO,
    #       lejos del abridor hero.
    # extraer_imagenes.py (referencia validada) NO sufre esto: trabaja sobre una
    # página recién cargada, acepta consentimiento y opera cerca del top.
    GALLERY_MODAL_DISMISS_CONSENT: bool = Field(
        default=True,
        description="Antes de abrir el modal: hace scroll al top, descarta el "
                    "overlay de consentimiento (OneTrust/Booking) y envía ESC "
                    "para cerrar lightbox/overlays parásitos. Reduce los fallos "
                    "de apertura del modal (Build 110).",
    )
    GALLERY_MODAL_OPEN_RETRIES: int = Field(
        default=3, ge=1, le=8,
        description="Nº de intentos de abrir+renderizar el modal de galería "
                    "antes de degradar a 'sin galería' (Build 110).",
    )
    API_IMAGES_STRICT_GALLERY: bool = Field(
        default=False,
        description="Si True y API_IMAGES_GALLERY_ONLY=True, un hotel SIN fotos "
                    "gallery_visible exporta images[] VACÍO en lugar de recaer "
                    "en el superconjunto. Alinea el envío con el objetivo "
                    "(solo galería) a costa de poder enviar 0 imágenes para "
                    "hoteles cuyo modal falló. Default False = conserva la red "
                    "de seguridad histórica (Build 110).",
    )

    # ── Build 112 (BUG-ONLYTITLE-001) — control del flag onlyTitle en API ────
    # Auditoría Build 111→112: api_payload_builder.build_payload() y
    # ExportTemplate.args_config tenían "onlyTitle": True hardcodeado.
    # La API externa interpreta onlyTitle=True como "solo actualizar el campo
    # name/title"; con True, todos los demás campos de data[] son ignorados por
    # la API aunque estén presentes en el payload. Todos los hoteles exportados
    # en producción recibían onlyTitle=True, silenciando los 20 campos restantes.
    # Default False = producción completa (todos los campos de data[] procesados).
    # Poner True solo para pruebas de conexión inicial con la API externa.
    API_EXPORT_ONLY_TITLE: bool = Field(
        default=False,
        description=(
            "Si True, el payload exportado incluye args.onlyTitle=True, "
            "indicando a la API externa que solo procese el campo name/title. "
            "Default False = todos los campos de data[] son procesados por la API. "
            "Usar True únicamente para pruebas de conexión (Build 112)."
        ),
    )

    # ── Build 111 (BUG-SVC-POPULAR-CAT-001) — categoría del fallback popular ──
    # Auditoría Build 110→111 (verificada contra pruebas/_table__hotels_all_
    # services__.csv): 510 servicios (0,77%) en 53 pares (hotel,idioma) quedaban
    # con service_category="" porque, cuando TODAS las estrategias de
    # facility-group-container fallan, el único origen de servicios es el bloque
    # property-most-popular-facilities-wrapper (Strategy 4), que descartaba su
    # cabecera <h3>. El encabezado existe VERBATIM en el DOM ("Most popular
    # facilities" / "Instalaciones más populares" / …). Activar este toggle hace
    # que Strategy 4 lo extraiga y lo asigne como service_category. NO es
    # inferencia ni traducción: es texto literal del DOM, coherente con la
    # política Build 103. Default True.
    SVC_POPULAR_FALLBACK_CATEGORY_ENABLED: bool = Field(
        default=True,
        description="Si True, el fallback 'property-most-popular-facilities-"
                    "wrapper' (Strategy 4 de _extract_all_services) extrae la "
                    "cabecera <h3> del bloque VERBATIM y la usa como "
                    "service_category, en lugar de dejarla vacía. Reduce el "
                    "0,77% de service_category vacías cuando las estrategias de "
                    "facility-group-container no encuentran nada (Build 111).",
    )

    # ── Extraction limits ─────────────────────────────────────────────────────
    # BUG-CFG-003 (Build 63-fix): extractor.py:563 truncates text via
    #   text[:self._cfg.MAX_ERROR_LEN] — field was missing from Settings.
    MAX_ERROR_LEN: int = Field(
        default=10_000, ge=100, le=500_000,
        description="Maximum characters returned by HotelExtractor._safe_text(). "
                    "Prevents unbounded string storage for malformed pages.",
    )

    # ── Database OLAP timeout ─────────────────────────────────────────────────
    # BUG-CFG-004 (Build 63-fix): database.py:144 reads cfg.STMT_TIMEOUT_OLAP_MS
    #   in get_serializable_db() to set SET LOCAL statement_timeout.
    #   Field was missing from Settings.
    STMT_TIMEOUT_OLAP_MS: int = Field(
        default=30_000, ge=1_000, le=300_000,
        description="Statement timeout (milliseconds) applied inside "
                    "get_serializable_db() via SET LOCAL statement_timeout. "
                    "Prevents runaway OLAP queries from blocking the pool. "
                    "Windows 11: conservative default (30 s) — raise only if "
                    "analytical queries regularly exceed this threshold.",
    )

    # ── External API export (Build 91) ───────────────────────────────────
    # Credentials for the external hotel API (_API_.md format).
    # Set in .env — exposed as read-only via GET /export/config.
    # STRUCT-EXPORT-002: centralised config eliminates the need to pass
    # base_url/api_key_ext on every POST /export/batch call.
    EXT_API_BASE_URL: str = Field(
        default="",
        description="Base URL of the external hotel API (e.g. https://web.com/api). Set in .env.",
    )
    EXT_API_KEY: str = Field(
        default="",
        description="API key for the external hotel API (e.g. 543-clave-api). Set in .env.",
    )
    # STRUCT-EXPORT-003 (Build 93): default vacío → el sistema usa ENABLED_LANGUAGES
    # automáticamente como idiomas de exportación (fuente de verdad = idiomas scrapeados).
    # Establecer explícitamente solo para restringir a un subconjunto (ej. "en,es").
    EXT_API_DEFAULT_LANGUAGES: str = Field(
        default="",
        description=(
            "Idiomas de exportación separados por coma. "
            "Dejar vacío (por defecto) para usar ENABLED_LANGUAGES automáticamente: "
            "se exportan todos los idiomas scrapeados. "
            "Establecer solo para restringir a un subconjunto, ej. 'en,es'. "
            "'en' siempre incluido."
        ),
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

    @property
    def database_url(self) -> str:
        """
        Compute the SQLAlchemy connection URL from individual DB_* fields.

        BUG-CFG-005 (Build 63-fix): database.py:45 accesses cfg.database_url
        as a property.  It was not declared in Settings, causing AttributeError
        every time _get_engine() was called (i.e. on every DB operation).

        Driver: psycopg v3 (postgresql+psycopg) — matches requirements.txt.
        Password is URL-encoded to handle special characters safely.
        """
        from urllib.parse import quote_plus
        password = quote_plus(self.DB_PASSWORD)
        return (
            f"postgresql+psycopg://{self.DB_USER}:{password}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached Settings singleton."""
    return Settings()


def reset_settings() -> None:
    """Force Settings re-instantiation (used in tests)."""
    get_settings.cache_clear()
