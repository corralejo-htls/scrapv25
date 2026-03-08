"""
scraper.py — BookingScraper Pro v48
Fixes applied:
  BUG-004 / BUG-106: build_language_url fixed — no double-.html stripping.
  BUG-106           : SHA-256 replaces MD5 for filename generation.
  BUG-008           : BOOKING_BYPASS_COOKIES not captured at import time.
  BUG-013           : _is_blocked wrapped in try/except; structured detection.
  BUG-018           : USER_AGENTS_WIN weighted by realistic market share.
  SCRAP-BUG-008     : WebDriver manager download optional — offline mode supported.
  SCRAP-SEC-003     : Debug HTML files saved to isolated directory only.
  CloudScraper      : _session_resets counter protected by lock.
  Platform          : Windows 11 / Selenium 4 / ProactorEventLoop.
"""

from __future__ import annotations

import hashlib
import logging
import os
import random
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse, urljoin

import cloudscraper
import requests
from bs4 import BeautifulSoup

from app.config import get_settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# User-Agent pool — BUG-018 fix: weighted by market share
# ---------------------------------------------------------------------------
# Weights reflect approximate Windows browser market share (StatCounter 2024)
_USER_AGENTS_WIN: List[Tuple[str, float]] = [
    # Chrome ~65%
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", 0.25),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", 0.20),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36", 0.10),
    # Edge ~12%
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0", 0.12),
    # Firefox ~8%
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0", 0.08),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0", 0.05),
    # Safari Windows (legacy) ~2%
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15", 0.02),
    # Remaining
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36", 0.18),
]

_UA_POPULATION = [ua for ua, _ in _USER_AGENTS_WIN]
_UA_WEIGHTS = [w for _, w in _USER_AGENTS_WIN]


def _random_user_agent() -> str:
    """Select a user agent weighted by real-world market share."""
    return random.choices(_UA_POPULATION, weights=_UA_WEIGHTS, k=1)[0]


# ---------------------------------------------------------------------------
# Block detection signals
# ---------------------------------------------------------------------------

_BLOCK_SIGNALS: List[str] = [
    "cf-browser-verification",
    "enable javascript",
    "access denied",
    "captcha",
    "your ip address",
    "please verify you are a human",
    "security check",
    "blocked",
    "too many requests",
    "robot",
    "automated access",
]


def _is_blocked(html: str) -> bool:
    """
    Detect if page indicates bot blocking.
    BUG-013 fix: wrapped in try/except; returns True on parse errors
    to trigger retry rather than processing garbage HTML.
    """
    try:
        lower = html.lower()
        return any(signal in lower for signal in _BLOCK_SIGNALS)
    except Exception as exc:
        logger.warning("_is_blocked parsing failed: %s — treating as blocked.", exc)
        return True


# ---------------------------------------------------------------------------
# URL language builder — BUG-004 fix
# ---------------------------------------------------------------------------

# Match language suffix ONLY when followed by .html at end of path (before query/fragment)
_LANG_SUFFIX_RE = re.compile(
    r"(\.[a-z]{2}(?:-[a-z]{2,4})?)(\.html)?(?=[?#]|$)",
    re.IGNORECASE,
)


def build_language_url(base_url: str, lang_code: str) -> str:
    """
    Build a language-specific Booking.com URL.

    BUG-004 fix: handles URLs that already have a language suffix or that
    lack the .html extension without creating double-suffix issues.

    Examples:
      build_language_url("https://booking.com/hotel.html", "de")
        → "https://booking.com/hotel.de.html"
      build_language_url("https://booking.com/hotel.es.html", "de")
        → "https://booking.com/hotel.de.html"
      build_language_url("https://booking.com/hotel.es", "de")
        → "https://booking.com/hotel.de.html"
    """
    cfg = get_settings()
    lang_ext = cfg.get_language_ext(lang_code)

    parsed = urlparse(base_url)
    path = parsed.path

    # Strip any existing language suffix (with or without .html)
    # Then canonicalise: always append .<lang>.html
    match = _LANG_SUFFIX_RE.search(path)
    if match:
        # Remove existing language suffix (+optional .html)
        path = path[: match.start()]

    # Remove trailing .html if present (we will re-add it)
    if path.lower().endswith(".html"):
        path = path[:-5]

    new_path = f"{path}.{lang_ext}.html"

    new_url = parsed._replace(path=new_path).geturl()
    return new_url


# ---------------------------------------------------------------------------
# Filename hashing — BUG-106 fix: SHA-256 replaces MD5
# ---------------------------------------------------------------------------

def url_to_filename(url: str, extension: str = ".html") -> str:
    """Generate a safe, collision-resistant filename from a URL using SHA-256."""
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:32]
    return f"{digest}{extension}"


# ---------------------------------------------------------------------------
# Debug HTML saving — SCRAP-SEC-003 fix
# ---------------------------------------------------------------------------

def _save_debug_html(html: str, url: str, tag: str = "debug") -> Optional[Path]:
    """
    Save debug HTML to the isolated debug directory only.
    Never saves to a web-accessible path.
    """
    cfg = get_settings()
    if not cfg.DEBUG_HTML_SAVE:
        return None
    try:
        filename = url_to_filename(url, extension=f"_{tag}.html")
        # SCRAP-SEC-003: always save to dedicated debug dir, never to cwd or public paths
        target = cfg.DEBUG_HTML_DIR / filename
        target.write_text(html, encoding="utf-8", errors="replace")
        logger.debug("Debug HTML saved: %s", target)
        return target
    except OSError as exc:
        logger.warning("Could not save debug HTML: %s", exc)
        return None


# ---------------------------------------------------------------------------
# CloudScraper engine
# ---------------------------------------------------------------------------

class CloudScraperEngine:
    """
    HTTP scraping engine using cloudscraper for Cloudflare bypass.
    Thread-safe session management for use within ThreadPoolExecutor.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._session: Optional[cloudscraper.CloudScraper] = None
        self._session_resets: int = 0  # Protected by _lock
        self._reset_after = 50  # Requests per session before forced rotation

    def _get_or_create_session(self) -> cloudscraper.CloudScraper:
        """Return current session; create if not exists."""
        with self._lock:
            if self._session is None:
                self._session = self._new_session()
            return self._session

    def _new_session(self) -> cloudscraper.CloudScraper:
        sess = cloudscraper.create_scraper(
            browser={
                "browser": "chrome",
                "platform": "windows",
                "mobile": False,
            },
        )
        sess.headers.update({
            "User-Agent": _random_user_agent(),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
        })
        return sess

    def _reset_session(self) -> None:
        """Force a new session (e.g. after block detection)."""
        with self._lock:
            self._session = self._new_session()
            self._session_resets += 1  # Protected by lock — BUG-008 fix
            logger.debug("CloudScraper session reset #%d", self._session_resets)

    def get_bypass_cookies(self) -> Dict[str, str]:
        """
        BUG-008 fix: cookies are constructed on every call, not captured
        at import time, so GA IDs are fresh per request.
        """
        return {
            "_ga": f"GA1.2.{random.randint(100000000, 999999999)}.{int(time.time()) - random.randint(0, 86400)}",
            "_ga_XXXXXXXXXX": f"GS1.1.{int(time.time())}.1.1.{int(time.time())}.0.0.0",
            "bk_uid": hashlib.sha256(str(random.random()).encode()).hexdigest()[:16],
        }

    def scrape(self, url: str, retries: int = 3) -> Optional[str]:
        """Fetch a URL and return HTML or None on failure."""
        cfg = get_settings()
        session = self._get_or_create_session()

        for attempt in range(1, retries + 1):
            try:
                response = session.get(
                    url,
                    timeout=cfg.SCRAPER_REQUEST_TIMEOUT,
                    cookies=self.get_bypass_cookies(),
                    allow_redirects=True,
                )
                response.raise_for_status()
                html = response.text

                if _is_blocked(html):
                    logger.warning("Block detected on attempt %d for %s", attempt, url)
                    self._reset_session()
                    time.sleep(cfg.SCRAPER_RETRY_DELAY * attempt)
                    continue

                _save_debug_html(html, url, tag=f"cs_ok_{attempt}")
                return html

            except requests.exceptions.RequestException as exc:
                logger.warning(
                    "CloudScraper attempt %d/%d failed for %s: [%s] %s",
                    attempt, retries, url, type(exc).__name__, exc,
                )
                if attempt < retries:
                    time.sleep(cfg.SCRAPER_RETRY_DELAY * attempt)
                    self._reset_session()

        logger.error("CloudScraper exhausted retries for %s", url)
        return None


# ---------------------------------------------------------------------------
# Selenium engine (optional)
# ---------------------------------------------------------------------------

class SeleniumEngine:
    """
    Selenium-based scraping engine for JavaScript-heavy pages.
    SCRAP-BUG-008 fix: supports offline ChromeDriver via CHROMEDRIVER_PATH env var.
    """

    def __init__(self) -> None:
        self._driver_path: Optional[str] = os.environ.get("CHROMEDRIVER_PATH")

    def _get_driver(self) -> Any:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service

        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument(f"--user-agent={_random_user_agent()}")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        if self._driver_path:
            service = Service(executable_path=self._driver_path)
        else:
            # Automatic download (requires internet)
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
            except ImportError:
                raise RuntimeError(
                    "webdriver-manager not installed and CHROMEDRIVER_PATH not set. "
                    "Either set CHROMEDRIVER_PATH or install webdriver-manager."
                )

        return webdriver.Chrome(service=service, options=opts)

    def scrape(self, url: str) -> Optional[str]:
        cfg = get_settings()
        driver = None
        try:
            driver = self._get_driver()
            driver.set_page_load_timeout(cfg.SCRAPER_REQUEST_TIMEOUT)
            driver.get(url)
            time.sleep(2)  # Allow JS to render
            html = driver.page_source

            if _is_blocked(html):
                logger.warning("Selenium blocked for %s", url)
                return None

            _save_debug_html(html, url, tag="selenium_ok")
            return html

        except Exception as exc:
            logger.error("Selenium error for %s: [%s] %s", url, type(exc).__name__, exc)
            return None
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass
