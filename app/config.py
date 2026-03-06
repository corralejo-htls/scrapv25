"""
BookingScraper/app/config.py
Configuración centralizada - BookingScraper Pro
Windows 11 + Python 3.14.3 + Pydantic v2

CORRECCIONES v1.1:
  [FIX] DATABASE_URL: postgresql+psycopg:// (psycopg3, no psycopg2)
  [FIX] CELERY_WORKER_CONCURRENCY = 1 (Windows solo pool obligatorio)
  [NEW] Propiedad ENABLED_LANGUAGES: List[str] parseada desde CSV
  [FIX] VPN_ENABLED por defecto False (no bloquea arranque sin VPN)

CORRECCIONES v1.2 [FIX CRÍTICO - INGLÉS NUNCA SE GUARDABA]:
  [FIX #24] LANGUAGE_EXT["en"] = ".en" (antes "")
    EVIDENCIA: ejemplo CSV confirma URL correcta: hotel.en.html?lang=en-gb
    ANTES: hotel.html?lang=en-us → sin sufijo en ruta → bloqueado por Cloudflare
    AHORA: hotel.en.html?lang=en-gb → misma estructura que .es.html, .de.html
  [FIX #30] VPN_COUNTRIES: UK primero (antes US primero)
    Para IPs del Reino Unido + lang=en-gb → Booking.com sirve British English sin re-mapeo
"""

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    """Configuración general del sistema"""

    # ── SEGURIDAD ─────────────────────────────────────────────────
    # [FIX BUG-NEW-12] API_KEY para proteger endpoints críticos (ej: /scraping/force-now).
    # Vacío = sin protección (modo desarrollo). Configurar en .env para producción:
    #   API_KEY=tu-clave-secreta-aqui
    API_KEY: str = ""

    # ── APLICACIÓN ──────────────────────────────────────────────
    APP_NAME: str = "Booking Scraper Pro"
    APP_VERSION: str = "6.0.0"           # [FIX BUG-NEW-16] synced with main.py version="6.0.0"
    DEBUG: bool = False

    # ── POSTGRESQL ───────────────────────────────────────────────
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    # [FIX BUG-V5-006] Default vacío — fuerza configuración explícita en .env.
    # El centinela "change_me_in_dotenv" era visible en source control y causaba
    # intentos de conexión con credencial inválida en deployments mal configurados.
    DB_PASSWORD: str = ""
    DB_NAME: str = "booking_scraper"

    @property
    def DATABASE_URL(self) -> str:
        # ✅ FIX: postgresql+psycopg:// para psycopg3 (no postgresql://)
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # ── REDIS / MEMURAI ──────────────────────────────────────────
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # ── CELERY ───────────────────────────────────────────────────
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    # ✅ FIX: 1 es el único valor válido con pool='solo' en Windows
    CELERY_WORKER_CONCURRENCY: int = 1

    # ── VPN ──────────────────────────────────────────────────────
    # ✅ FIX: False por defecto → el sistema arranca sin VPN activa
    VPN_ENABLED: bool = False
    # [FIX v5.0] UK primero → IP del Reino Unido para hotel.en.html?lang=en-gb
    # Antes: US-first para en-us. Ahora: UK-first para en-gb (formato correcto).
    VPN_COUNTRIES: List[str] = ["UK", "US", "CA", "DE", "FR", "NL", "IT", "ES"]
    VPN_ROTATION_INTERVAL: int = 50
    # [BUG-001 FIX] Rotar VPN cada N hoteles (usado en _maybe_rotate_vpn).
    VPN_ROTATE_EVERY_N: int = 10
    # [BUG-004 FIX] Timeout máximo (segundos) para toda la secuencia de failover VPN.
    # Si se supera, el sistema entra en modo degradado (continúa sin VPN o lanza alerta).
    VPN_FAILOVER_TIMEOUT_SECS: int = 90

    # ── SCRAPING ─────────────────────────────────────────────────
    HEADLESS_BROWSER: bool = True  # [BUG-002] Siempre True en producción — evita suspensión por pantalla
    BROWSER_TIMEOUT: int = 30
    PAGE_LOAD_WAIT: int = 5
    SCROLL_ITERATIONS: int = 3
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 60          # segundos entre reintentos
    MIN_REQUEST_DELAY: float = 2.0
    MAX_REQUEST_DELAY: float = 5.0
    # False = httpx (más rápido); True = Selenium (JS dinámico)
    USE_SELENIUM: bool = False
    # [BUG-006 FIX] Workers concurrentes del ThreadPoolExecutor.
    # Valor 1 = secuencial (seguro, sin riesgo de ban).
    # Valor 2+ = paralelo (mayor throughput, mayor riesgo de detección).
    # ADVERTENCIA: aumentar requiere VPN_ROTATE_EVERY_N más bajo.
    SCRAPER_MAX_WORKERS: int = 1
    # [BUG-002 FIX] Intervalo del watchdog (segundos). Detecta suspensión por pantalla bloqueada.
    WATCHDOG_INTERVAL_SECS: int = 120

    # ── USER AGENTS ──────────────────────────────────────────────
    USER_AGENTS: List[str] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    ]

    # ── IDIOMAS ──────────────────────────────────────────────────
    # En .env: LANGUAGES_ENABLED=en,es,de,fr,it
    LANGUAGES_ENABLED: str = "en,es,de,fr,it"
    DEFAULT_LANGUAGE: str = "en"

    # [FIX HIGH-014] ISO 639-1 set defined at class level so both the
    # property and the model_validator use the same authoritative set.
    # Previously only _validate_settings validated languages; if the
    # settings object was mutated or re-read after startup (e.g. via
    # env var override in tests or a future reload mechanism), invalid
    # language codes would pass through the property silently.
    _VALID_ISO_639_1: set = {
        "af","sq","am","ar","hy","az","eu","be","bn","bs","bg","ca","zh","hr",
        "cs","da","nl","en","et","fi","fr","ka","de","el","gu","he","hi","hu",
        "is","id","ga","it","ja","kn","kk","km","ko","ky","lo","lv","lt","mk",
        "ms","ml","mt","mr","mn","ne","no","ps","fa","pl","pt","ro","ru","sr",
        "si","sk","sl","es","sw","sv","ta","te","th","tr","uk","ur","uz","vi",
    }

    @property
    def ENABLED_LANGUAGES(self) -> List[str]:
        """
        [FIX HIGH-014] Parses LANGUAGES_ENABLED and validates every code on
        each read. Raises ValueError for any invalid ISO 639-1 code so bad
        values are caught immediately, regardless of when they were introduced.

        This ensures validation is not limited to startup — it fires whenever
        the property is accessed, including after environment variable changes
        in test harnesses or future runtime-reload scenarios.
        """
        langs = [lang.strip() for lang in self.LANGUAGES_ENABLED.split(",") if lang.strip()]
        for lang in langs:
            if lang not in self._VALID_ISO_639_1:
                raise ValueError(
                    f"[HIGH-014] LANGUAGES_ENABLED contains invalid ISO 639-1 code: '{lang}'. "
                    f"Accepted codes: {sorted(self._VALID_ISO_639_1)}. "
                    "Update LANGUAGES_ENABLED in your .env file."
                )
        if not langs:
            raise ValueError(
                "[HIGH-014] LANGUAGES_ENABLED is empty. "
                "Provide at least one ISO 639-1 language code (e.g. LANGUAGES_ENABLED=en,es)."
            )
        return langs

    @model_validator(mode="after")
    def _validate_settings(self) -> "Settings":
        """
        [FIX BUG-V5-006] Valida DB_PASSWORD — rechaza arrancada si está vacío.
        [FIX BUG-V5-021] Valida ENABLED_LANGUAGES — solo códigos ISO 639-1 (2 letras).
        """
        # BUG-V5-006: DB_PASSWORD obligatorio
        if not self.DB_PASSWORD:
            raise ValueError(
                "DB_PASSWORD no puede estar vacío. "
                "Configura DB_PASSWORD en tu archivo .env o variable de entorno."
            )

        # BUG-V5-021: Validate each language using the class-level set.
        # [FIX HIGH-014] _validate_settings now delegates to ENABLED_LANGUAGES
        # property which already validates — duplicate validation removed.
        # Keeping this call so the model_validator still catches errors at startup
        # with a clear error message before the application starts serving.
        try:
            _ = self.ENABLED_LANGUAGES  # raises ValueError if any code is invalid
        except ValueError as lang_err:
            raise ValueError(str(lang_err)) from lang_err
        # ── [FIX ERR-CFG-001] Additional startup validations ─────────────────────
        # These catch common misconfiguration that would cause silent runtime failures.

        # BATCH_SIZE: must be in [1, 10] — the scraper dispatches at most MAX_BATCH_SIZE=10
        if not (1 <= self.BATCH_SIZE <= 10):
            raise ValueError(
                f"BATCH_SIZE={self.BATCH_SIZE} is out of range [1, 10]. "
                "Values > 10 exceed the MAX_BATCH_SIZE guard and will be silently capped. "
                "Values < 1 will cause the dispatcher to stall."
            )

        # MAX_RETRIES: excessive retries delay failed URLs and bloat scraping_logs
        if self.MAX_RETRIES < 0:
            raise ValueError(f"MAX_RETRIES={self.MAX_RETRIES} cannot be negative.")
        if self.MAX_RETRIES > 10:
            raise ValueError(
                f"MAX_RETRIES={self.MAX_RETRIES} exceeds recommended maximum of 10. "
                "High retry counts delay detection of permanently failing URLs. "
                "Set MAX_RETRIES <= 10 or explicitly acknowledge the risk."
            )

        # SCRAPER_MAX_WORKERS: On Windows with CELERY_WORKER_POOL=solo, max 1 is enforced.
        # More than 4 workers on a local machine risks overloading the network and CPU.
        if self.SCRAPER_MAX_WORKERS < 1:
            raise ValueError(f"SCRAPER_MAX_WORKERS={self.SCRAPER_MAX_WORKERS} must be >= 1.")
        if self.SCRAPER_MAX_WORKERS > 4:
            raise ValueError(
                f"SCRAPER_MAX_WORKERS={self.SCRAPER_MAX_WORKERS} > 4 on a local Windows machine "
                "risks network saturation and VPN instability. "
                "On Windows with CELERY_WORKER_POOL=solo, SCRAPER_MAX_WORKERS=1 is recommended."
            )

        # VPN_ROTATE_EVERY_N: too small causes excessive VPN rotations; too large defeats purpose
        if self.VPN_ROTATE_EVERY_N < 1:
            raise ValueError(f"VPN_ROTATE_EVERY_N={self.VPN_ROTATE_EVERY_N} must be >= 1.")
        if self.VPN_ROTATE_EVERY_N > 100:
            raise ValueError(
                f"VPN_ROTATE_EVERY_N={self.VPN_ROTATE_EVERY_N} > 100 may allow bot-detection "
                "patterns to accumulate before rotation. Recommended range: 5–50."
            )

        # [FIX ERR-CFG-001] Validate VPN_COUNTRIES against NordVPN supported codes.
        # Synchronized with vpn_manager_windows.py COUNTRY_NAMES dictionary.
        # Invalid country codes cause silent runtime failures in vpn.connect().
        _VALID_VPN_COUNTRIES = {
            "UK","US","CA","DE","FR","NL","IT","ES","SE","CH","AU","JP","SG","BR","IN",
            "NO","DK","FI","BE","AT","PL","CZ","HU","RO","PT","IE","NZ","MX","AR","ZA",
            "GR","TR","TW","HK","TH","MY","ID","IL","AE","KR","LT","LV","EE","SK","SI",
        }
        for country in self.VPN_COUNTRIES:
            if country not in _VALID_VPN_COUNTRIES:
                raise ValueError(
                    f"VPN_COUNTRIES contains invalid code: '{country}'. "
                    f"Valid NordVPN country codes: {sorted(_VALID_VPN_COUNTRIES)}. "
                    "Check vpn_manager_windows.py COUNTRY_NAMES for the full list."
                )

        # [FIX ERR-CONC-002] VPN serialized operations require single worker.
        # With SCRAPER_MAX_WORKERS > 1, multiple threads compete for _vpn_lock;
        # the 30s timeout causes RuntimeError + degraded mode — not the intended design.
        if self.VPN_ENABLED and self.SCRAPER_MAX_WORKERS > 1:
            raise ValueError(
                f"SCRAPER_MAX_WORKERS={self.SCRAPER_MAX_WORKERS} > 1 is incompatible with "
                "VPN_ENABLED=True. VPN operations require serialized access via a single worker. "
                "Set SCRAPER_MAX_WORKERS=1 when VPN_ENABLED=True."
            )

        return self

    # [FIX v5.1] LANGUAGE_EXT: 'en' usa sufijo '.en-gb' = hotel.en-gb.html?lang=en-gb
    # CAUSA RAÍZ CONFIRMADA: Booking.com con IPs europeas requiere sufijo de locale
    # completo '.en-gb' para servir British English. El sufijo corto '.en' genera una
    # URL que el CDN de Booking.com no reconoce como idioma canónico, produciendo
    # comportamiento inconsistente (redirección a idioma detectado por GeoIP o 404).
    # EVIDENCIA: log de scraping confirma URL incorrecta generada con ".en":
    #   INCORRECTO (v5.0): hotel.en.html?lang=en-gb
    #   CORRECTO   (v5.1): hotel.en-gb.html?lang=en-gb
    # COHERENCIA: LANG_COOKIE_LOCALE["en"]="en-gb" ya estaba correcto → ahora
    # el sufijo de ruta es coherente con el parámetro ?lang= y la cookie.
    # ANTES v4.x: "en" → "" → hotel.html?lang=en-us → BLOQUEADO por Cloudflare
    # ANTES v5.0: "en" → ".en" → hotel.en.html?lang=en-gb → URL no reconocida por CDN
    # AHORA v5.1: "en" → ".en-gb" → hotel.en-gb.html?lang=en-gb → URL canónica correcta
    LANGUAGE_EXT: dict = {
        "en": ".en-gb",
        "es": ".es",
        "fr": ".fr",
        "de": ".de",
        "it": ".it",
        "pt": ".pt",
        "nl": ".nl",
        "ru": ".ru",
        "ar": ".ar",
        "tr": ".tr",
        "hu": ".hu",
        "pl": ".pl",
        "zh": ".zh",
        "no": ".no",
        "fi": ".fi",
        "sv": ".sv",
        "da": ".da",
        "ja": ".ja",
        "ko": ".ko",
    }

    # ── XPATHS (especificación del proyecto) ─────────────────────
    XPATHS: dict = {
        "hotel_name":       "//div[@id='wrap-hotelpage-top']/div[2]/div[1]/div[2]/h2[1]",
        "address":          "//*[@id='wrap-hotelpage-top']/div[2]/div/div[3]/div/div/div/div/span[1]/button/div",
        "description":      "//p[@data-testid='property-description']",
        "reviews":          "//div[@data-testid='review-score-component']",
        "review_subscores": "//div[@data-testid='ReviewSubscoresDesktop']/following-sibling::div[1]",
        "facilities":       "//*[@id='hp_facilities_box']",
        "policies":         "//*[@id='policies']",
        "important_info":   "//*[@id='important_info']",
        "rooms":            "//*[@id='maxotelRoomArea']",
        "gallery":          "//div[@data-testid='GalleryGridViewModal-wrapper']",
        "hotel_page":       "//*[@id='b2hotelPage']",
    }

    # CSS Selectors alternativos
    CSS_SELECTORS: dict = {
        "gallery_button":  "[data-testid='gallery-button']",
        "gallery_images":  "img[data-testid='gallery-image']",
        "facility_items":  "div.facility-item",
        "room_cards":      "div.room-card",
    }

    # ── RUTAS ─────────────────────────────────────────────────────────────────
    # [FIX BUG-A-11] Paths were hardcoded to C:\\BookingScraper.
    # [FIX ERR-CFG-002] Changed from CWD-relative (os.path.join(".", "data"))
    # to config-file-relative paths. If the app is started from a different
    # working directory (Task Scheduler, IDE, shortcut), paths are now always
    # consistent regardless of CWD.
    #
    # Default: <repo_root>/data  (config.py is at app/config.py)
    # Override in .env:
    #   Windows: BASE_DATA_PATH=C:\\BookingScraper\\data
    #   Linux:   BASE_DATA_PATH=/opt/bookingscraper/data
    _CFG_DIR      = os.path.dirname(os.path.abspath(__file__))  # .../app/
    _REPO_ROOT    = os.path.dirname(_CFG_DIR)                    # .../BookingScraper/
    _DEFAULT_DATA = os.path.join(_REPO_ROOT, "data")

    BASE_DATA_PATH: str = _DEFAULT_DATA
    IMAGES_PATH:    str = os.path.join(_DEFAULT_DATA, "images")
    EXPORTS_PATH:   str = os.path.join(_DEFAULT_DATA, "exports")
    LOGS_PATH:      str = os.path.join(_DEFAULT_DATA, "logs")

    # [FIX CRIT-007] Debug HTML cleanup policy.
    # Files older than DEBUG_HTML_MAX_AGE_HOURS are deleted automatically by
    # the periodic cleanup task in scraper.py.
    # DEBUG_HTML_MAX_TOTAL_MB caps total debug directory size; oldest files
    # are evicted first when the cap is exceeded.
    DEBUG_HTML_MAX_AGE_HOURS: int = int(os.getenv("DEBUG_HTML_MAX_AGE_HOURS", "24"))
    DEBUG_HTML_MAX_TOTAL_MB:  int = int(os.getenv("DEBUG_HTML_MAX_TOTAL_MB",  "500"))

    # [FIX HIGH-005] Centralized error message truncation length.
    # Previously hardcoded to 2000 in 3 different files with no shared constant.
    # All error storage paths (scraper_service, completeness_service, models)
    # must use this constant to ensure consistent DB column sizing and log content.
    # The DB schema defines last_error as VARCHAR(2000) — changing this constant
    # requires a corresponding schema migration.
    MAX_ERROR_LEN: int = int(os.getenv("MAX_ERROR_LEN", "2000"))

    # ── RUTAS DE NAVEGADORES ──────────────────────────────────────────────────
    # [NEW-16] Rutas configurables via .env — sin paths de usuario específico.
    # Ejemplo: BROWSER_BRAVE_PATH=C:\\Program Files\\BraveSoftware\\...\\brave.exe
    BROWSER_BRAVE_PATH:  str = ""   # vacío = usar lista predeterminada en scraper.py
    BROWSER_OPERA_PATH:  str = ""
    BROWSER_CHROME_PATH: str = ""
    BROWSER_EDGE_PATH:   str = ""

    # ── DISPATCHER ────────────────────────────────────────────────────────────
    USE_CELERY_DISPATCHER: bool = False  # True=Celery, False=asyncio auto-dispatch

    # ── IMÁGENES ─────────────────────────────────────────────────
    IMAGE_QUALITY:    int = 85
    IMAGE_MAX_WIDTH:  int = 1920
    IMAGE_MAX_HEIGHT: int = 1080
    DOWNLOAD_IMAGES:  bool = True
    MAX_IMAGE_WORKERS: int = 5

    # ── BATCH ────────────────────────────────────────────────────
    BATCH_SIZE:           int = 5
    MAX_CONCURRENT_TASKS: int = 3

    # ── EXPORTACIÓN ──────────────────────────────────────────────
    EXPORT_FORMATS: List[str] = ["csv", "json", "excel"]

    # ── LOGGING ──────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> - "
        "<level>{message}</level>"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )


# Instancia global
settings = Settings()


def create_directories() -> None:
    """Crea los directorios de datos si no existen."""
    for path in [
        settings.BASE_DATA_PATH,
        settings.IMAGES_PATH,
        settings.EXPORTS_PATH,
        settings.LOGS_PATH,
    ]:
        os.makedirs(path, exist_ok=True)


# [REGRESS-04/BUG-06] create_directories() eliminado del nivel de módulo.
# PROBLEMA: se ejecutaba en cada import causando PermissionError en CI/Docker.
# SOLUCIÓN: llamar desde main.py lifespan con try/except.
