# =============================================================================
# app/config.py — BookingScraper Pro v6.0.0 Build 64
# =============================================================================
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
        default=79,
        description="Incremental build number.",
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
        default=50, ge=10, le=600,
        description="Minimum seconds between routine VPN rotations. "
                    "Forced rotations (ip_known_blocked) bypass this gate.",
    )

    # ── Languages ─────────────────────────────────────────────────────────────
    ENABLED_LANGUAGES: str = Field(
        default="en,es,de,it,fr,pt",
        description="Comma-separated ISO 639-1 language codes to scrape. "
                    "'en' is always processed first regardless of order.",
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
