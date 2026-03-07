"""
BookingScraper Pro v6.0 - Scraping Engines
==========================================
Two scraping back-ends:
  1. CloudScraperEngine  — fast HTTP requests (Cloudflare bypass)
  2. SeleniumEngine      — full browser fallback for heavy JS pages

Platform : Windows 11 + Python 3.11+

Corrections Applied (v46):
- BUG-002 related : Language detection refactored from complexity 23 → helpers.
- BUG-008 related : scrape_hotel() (Selenium) refactored from complexity 37.
- BUG-024 : cloudscraper session reset on 403 has a maximum reset counter
            to prevent infinite retry loops.
"""

from __future__ import annotations

import hashlib
import logging
import os
import random
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import cloudscraper
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from app.extractor import HotelData, HotelExtractor

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Result wrapper
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ScrapeResult:
    url        : str
    language   : str
    success    : bool
    data       : Optional[HotelData] = None
    error      : str                 = ""
    http_status: Optional[int]       = None
    engine     : str                 = "unknown"
    duration_ms: int                 = 0
    html_saved : bool                = False


# ─────────────────────────────────────────────────────────────────────────────
# User-agent pool (Windows Chrome user agents)
# ─────────────────────────────────────────────────────────────────────────────
_USER_AGENTS: list[str] = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
]


def _random_ua() -> str:
    return random.choice(_USER_AGENTS)


# ─────────────────────────────────────────────────────────────────────────────
# CloudScraper engine
# ─────────────────────────────────────────────────────────────────────────────

class CloudScraperEngine:
    """
    HTTP-based scraping using the cloudscraper library (Cloudflare bypass).

    BUG-024 FIX: Session reset on 403 is now bounded by MAX_SESSION_RESETS.
                  Without this limit the engine could loop forever on a URL
                  that permanently returns 403.
    """

    MAX_SESSION_RESETS = 3    # BUG-024 FIX: was unbounded
    REQUEST_TIMEOUT    = 30

    def __init__(self, delay_min: float = 2.0, delay_max: float = 8.0,
                 debug_html_dir: Optional[str] = None) -> None:
        self._delay_min      = delay_min
        self._delay_max      = delay_max
        self._debug_html_dir = Path(debug_html_dir) if debug_html_dir else None
        self._session        = self._new_session()
        self._session_resets = 0

    def _new_session(self) -> cloudscraper.CloudScraper:
        sess = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False}
        )
        sess.headers.update({
            "User-Agent"     : _random_ua(),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept"         : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })
        return sess

    def _reset_session(self) -> None:
        self._session_resets += 1
        logger.info("Resetting cloudscraper session (reset #%d)", self._session_resets)
        self._session = self._new_session()

    def scrape_hotel(self, url: str, language: str = "en",
                     max_retries: int = 3) -> ScrapeResult:
        """
        Fetch and extract a hotel page.

        BUG-024 FIX: 403 responses trigger a session reset, but only up to
        MAX_SESSION_RESETS times per session lifetime to avoid infinite loops.
        """
        t_start = time.monotonic()
        last_error = ""

        for attempt in range(max_retries):
            try:
                response = self._session.get(url, timeout=self.REQUEST_TIMEOUT)

                if response.status_code == 403:
                    if self._session_resets < self.MAX_SESSION_RESETS:
                        self._reset_session()
                        self._human_delay()
                        continue
                    else:
                        # BUG-024 FIX: stop retrying after limit reached
                        logger.warning(
                            "403 on %s after %d session resets — marking as error",
                            url, self._session_resets,
                        )
                        return ScrapeResult(
                            url=url, language=language, success=False,
                            error=f"Persistent 403 after {self._session_resets} session resets",
                            http_status=403, engine="cloudscraper",
                            duration_ms=int((time.monotonic() - t_start) * 1000),
                        )

                if response.status_code == 429:
                    wait = 30.0 * (2 ** attempt)
                    logger.warning("Rate-limited (429) on %s — waiting %.0fs", url, wait)
                    time.sleep(wait)
                    continue

                if response.status_code not in (200, 301, 302):
                    last_error = f"HTTP {response.status_code}"
                    self._human_delay()
                    continue

                html     = response.text
                detected = self._detect_language_from_html(html)
                if detected and detected != language:
                    logger.debug("Language mismatch on %s: expected %s, got %s", url, language, detected)

                data = HotelExtractor(html, url).extract()
                self._save_debug_html(url, language, html)

                return ScrapeResult(
                    url=url, language=language, success=True, data=data,
                    http_status=response.status_code, engine="cloudscraper",
                    duration_ms=int((time.monotonic() - t_start) * 1000),
                )

            except requests.exceptions.Timeout:
                last_error = f"Timeout (attempt {attempt+1})"
                logger.warning("%s — timeout on attempt %d", url, attempt + 1)

            except requests.exceptions.ConnectionError as exc:
                last_error = f"ConnectionError: {exc}"
                logger.warning("%s — connection error on attempt %d: %s", url, attempt + 1, exc)

            except requests.exceptions.SSLError as exc:
                # SSLError is generally non-transient; do not retry
                logger.error("%s — SSL error: %s", url, exc)
                return ScrapeResult(
                    url=url, language=language, success=False,
                    error=f"SSLError: {exc}", engine="cloudscraper",
                    duration_ms=int((time.monotonic() - t_start) * 1000),
                )

            self._human_delay()

        return ScrapeResult(
            url=url, language=language, success=False, error=last_error,
            engine="cloudscraper",
            duration_ms=int((time.monotonic() - t_start) * 1000),
        )

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _human_delay(self) -> None:
        time.sleep(random.uniform(self._delay_min, self._delay_max))

    # BUG-008 related: language detection refactored from 123-line / complexity-23 method
    def _detect_language_from_html(self, html: str) -> Optional[str]:
        return (
            self._lang_from_html_tag(html)
            or self._lang_from_meta(html)
            or self._lang_from_url_pattern(html)
        )

    @staticmethod
    def _lang_from_html_tag(html: str) -> Optional[str]:
        m = re.search(r'<html[^>]+lang=["\']([a-z]{2})', html, re.IGNORECASE)
        return m.group(1).lower() if m else None

    @staticmethod
    def _lang_from_meta(html: str) -> Optional[str]:
        m = re.search(r'<meta[^>]+content=["\'][a-z]{2}-([A-Z]{2})', html)
        if m:
            # Map country code back to base language (rough approximation)
            return m.group(0)[m.start():].split('"')[1][:2].lower()
        return None

    @staticmethod
    def _lang_from_url_pattern(html: str) -> Optional[str]:
        m = re.search(r'\.(\w{2}(?:-\w{2})?)"', html)
        if m:
            return m.group(1).split("-")[0].lower()
        return None

    def _save_debug_html(self, url: str, language: str, html: str) -> None:
        if not self._debug_html_dir:
            return
        try:
            self._debug_html_dir.mkdir(parents=True, exist_ok=True)
            slug = hashlib.md5(url.encode()).hexdigest()[:8]
            path = self._debug_html_dir / f"{slug}_{language}.html"
            path.write_text(html, encoding="utf-8", errors="replace")
        except OSError as exc:
            logger.debug("Could not save debug HTML: %s", exc)


# ─────────────────────────────────────────────────────────────────────────────
# Selenium engine
# ─────────────────────────────────────────────────────────────────────────────

class SeleniumEngine:
    """
    Full-browser scraping via Selenium + ChromeDriver.
    Used as fallback when CloudScraper fails (heavy JS / CAPTCHA).

    BUG-002 related: scrape_hotel() refactored from complexity 37 into helpers.
    """

    PAGE_LOAD_TIMEOUT = 30
    ELEMENT_TIMEOUT   = 10

    def __init__(self, headless: bool = True, debug_html_dir: Optional[str] = None,
                 delay_min: float = 2.0, delay_max: float = 6.0) -> None:
        self._headless       = headless
        self._debug_html_dir = Path(debug_html_dir) if debug_html_dir else None
        self._delay_min      = delay_min
        self._delay_max      = delay_max
        self._driver: Optional[webdriver.Chrome] = None

    # ── Driver lifecycle ────────────────────────────────────────────────────

    def _get_driver(self) -> webdriver.Chrome:
        if self._driver is None:
            self._driver = self._create_driver()
        return self._driver

    def _create_driver(self) -> webdriver.Chrome:
        opts = Options()
        if self._headless:
            opts.add_argument("--headless=new")  # Chrome 112+ headless mode
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument(f"--user-agent={_random_ua()}")
        opts.add_argument("--window-size=1920,1080")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        # Windows: ChromeDriverManager handles binary path automatically
        service = Service(ChromeDriverManager().install())
        driver  = webdriver.Chrome(service=service, options=opts)
        driver.set_page_load_timeout(self.PAGE_LOAD_TIMEOUT)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
        })
        logger.info("Selenium ChromeDriver initialised")
        return driver

    def quit(self) -> None:
        if self._driver:
            try:
                self._driver.quit()
            except Exception:
                pass
            self._driver = None

    def __enter__(self) -> "SeleniumEngine":
        return self

    def __exit__(self, *_) -> None:
        self.quit()

    # ── Public scrape ───────────────────────────────────────────────────────

    def scrape_hotel(self, url: str, language: str = "en",
                     max_retries: int = 2) -> ScrapeResult:
        """
        BUG-002 related: main function previously 228 lines / complexity 37.
        Refactored into: _load_page(), _handle_consent(), _wait_for_content().
        """
        t_start = time.monotonic()
        last_error = ""

        for attempt in range(max_retries):
            try:
                driver = self._get_driver()
                html, status = self._load_page(driver, url)
                if html is None:
                    last_error = f"Failed to load page (attempt {attempt+1})"
                    self._human_delay()
                    continue

                data = HotelExtractor(html, url).extract()
                self._save_debug_html(url, language, html)

                return ScrapeResult(
                    url=url, language=language, success=True, data=data,
                    http_status=status, engine="selenium",
                    duration_ms=int((time.monotonic() - t_start) * 1000),
                )

            except TimeoutException as exc:
                last_error = f"Selenium timeout: {exc}"
                logger.warning("%s — Selenium timeout attempt %d", url, attempt + 1)
                self.quit()  # recreate driver next attempt

            except WebDriverException as exc:
                last_error = f"WebDriver error: {exc}"
                logger.error("%s — WebDriver error: %s", url, exc)
                self.quit()

            self._human_delay()

        return ScrapeResult(
            url=url, language=language, success=False, error=last_error,
            engine="selenium",
            duration_ms=int((time.monotonic() - t_start) * 1000),
        )

    # ── Page loading helpers ─────────────────────────────────────────────────

    def _load_page(self, driver: webdriver.Chrome,
                   url: str) -> tuple[Optional[str], Optional[int]]:
        """Load URL and return (html, inferred_status)."""
        try:
            driver.get(url)
            self._handle_consent(driver)
            self._wait_for_content(driver)
            return driver.page_source, 200
        except TimeoutException:
            return None, None

    def _handle_consent(self, driver: webdriver.Chrome) -> None:
        """Dismiss cookie/consent overlays if present."""
        try:
            btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            btn.click()
            time.sleep(0.5)
        except TimeoutException:
            pass  # No consent banner — that's fine

    def _wait_for_content(self, driver: webdriver.Chrome) -> None:
        """Wait until a hotel name or key content element is visible."""
        WebDriverWait(driver, self.ELEMENT_TIMEOUT).until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2.pp-header__title")),
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='property-name']")),
            )
        )

    def _human_delay(self) -> None:
        time.sleep(random.uniform(self._delay_min, self._delay_max))

    def _save_debug_html(self, url: str, language: str, html: str) -> None:
        if not self._debug_html_dir:
            return
        try:
            self._debug_html_dir.mkdir(parents=True, exist_ok=True)
            slug = hashlib.md5(url.encode()).hexdigest()[:8]
            path = self._debug_html_dir / f"{slug}_{language}_selenium.html"
            path.write_text(html, encoding="utf-8", errors="replace")
        except OSError as exc:
            logger.debug("Could not save debug HTML: %s", exc)


# ─────────────────────────────────────────────────────────────────────────────
# Debug HTML purge utility
# ─────────────────────────────────────────────────────────────────────────────

def purge_debug_html(debug_dir: str, max_age_hours: float = 24.0) -> int:
    """
    Remove debug HTML files older than max_age_hours.
    Returns the number of files deleted.
    Windows: uses pathlib to avoid path separator issues.
    """
    debug_path = Path(debug_dir)
    if not debug_path.exists():
        return 0

    cutoff    = time.time() - (max_age_hours * 3600)
    deleted   = 0
    for f in debug_path.glob("*.html"):
        try:
            if f.stat().st_mtime < cutoff:
                f.unlink()
                deleted += 1
        except OSError as exc:
            logger.warning("Cannot delete %s: %s", f, exc)

    logger.info("Purged %d debug HTML files older than %.0fh from %s",
                deleted, max_age_hours, debug_path)
    return deleted
