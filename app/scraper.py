# =============================================================================
# app/scraper.py — BookingScraper Pro v6.0.0 Build 98
# =============================================================================
# BUILD 98 — BUG-EXTRACT-IT-001-FIX
#   Root cause: _fetch_with_selenium() iteraba 4 selectores CSS secuencialmente,
#   cada uno con su propio WebDriverWait(content_wait_s). Si los 3 primeros
#   selectores no coincidían (caso habitual en páginas IT, DE, FR que usan
#   h1.pp-header__title), cada timeout acumulaba content_wait_s (default 10 s)
#   antes de probar el siguiente → latencia observada 15–75 s (outliers >120 s).
#
#   Fix: reemplazar el bucle for con un único WebDriverWait usando EC.any_of()
#   que dispara en paralelo todos los selectores. Si CUALQUIERA aparece antes
#   de content_wait_s, se resuelve inmediatamente.
#   Peor caso anterior: 4 × 10 s = 40 s
#   Peor caso nuevo:    1 × 10 s = 10 s  (reducción 75%)
#
#   EC.any_of() disponible desde selenium >= 4.0 (proyecto usa >= 4.27.0).
#
# BUILD 70 — BUG-VPN-006-FIX
#   Root cause: NordVPN GUI opens the system DEFAULT browser (Brave) for
#   OAuth re-auth or help pages. When Selenium also uses Brave, both share
#   the same user profile → NordVPN's browser tabs appear inside the Selenium-
#   controlled window, corrupting the scraping session.
#
#   Fix: Selenium Brave now uses a dedicated isolated profile at
#   SELENIUM_BRAVE_PROFILE_DIR (config field, default: data/brave_profile).
#   NordVPN opens the system Brave with its DEFAULT profile (different path)
#   → tabs opened by NordVPN go to a SEPARATE Brave process, never touching
#   the Selenium-controlled instance.
#
#   Additional flags to prevent the Selenium Brave from loading external content:
#     --no-default-browser-check  : prevents first-run browser prompt
#     --disable-default-apps      : disables preloaded app shortcuts
#     --no-first-run              : skips first-run setup
#
# BUILD 75 — BUG-URL-001-FIX: Correct Booking.com URL format
#   Root cause: build_language_url() generated .html?lang=en-gb
#   Correct format confirmed from canonical URLs in pruebas/ HTML files:
#     .en-gb.html?lang=en-gb  (language code embedded in filename)
#   Impact: Booking.com serves a 301 redirect from the old format to the
#   canonical URL. Selenium follows the redirect but loses the Accept-Language
#   header set via CDP, causing occasional language mismatches. Direct
#   canonical URL avoids the redirect entirely.
#   Fix: build_language_url() now embeds lang_code in .html filename.
#
# BUILD 74 — SIMPLIFICATION: remove isolated Brave profile
#   SELENIUM_BRAVE_PROFILE_DIR removed. Brave uses its default system profile.
#   This was the behaviour before Build 70 and it worked correctly.
#   Since Brave is used EXCLUSIVELY by this application:
#     - No conflict with NordVPN browser tabs (handled by _enforce_single_tab)
#     - No stale profile accumulation (system profile is stable)
#     - No DevToolsActivePort timeout (default profile = instant startup)
#   Removed: _prepare_fresh_profile(), --user-data-dir, --bwsi
#   Kept:    _enforce_single_tab(), anti-hang flags, pywin32 popup dismiss
#
# BUILD 73 — BUG-BRAVE-001-FIX (superseded by BUILD 74)
#   Root cause: --user-data-dir=data/brave_profile (Build 70 BUG-VPN-006-FIX)
#   causes Brave to accumulate profile state across sessions. On next startup,
#   Brave processes stale profile data (Preferences, Local State, cache) and
#   takes 60+ seconds to initialize → ChromeDriver DevTools timeout →
#   "DevToolsActivePort file doesn't exist" on 100% of attempts.
#   Fix: _prepare_fresh_profile() wipes data/brave_profile completely before
#   every webdriver.Chrome() call. Fresh empty profile = instant Brave startup.
#   Additional anti-hang flags added to _build_chrome_options().
#
# BUILD 72 — BUG-SCRAPER-OS-001-FIX (preserved)
# BUILD 71 — BUG-VPN-007-FIX
#   Root cause: reset_browser() calls driver.quit() during VPN rotation, which
#   kills the Brave process but leaves behind a Chromium SingletonLock file in
#   data/brave_profile/. The next _get_driver() call finds the lock and Brave
#   exits immediately → "session not created: DevToolsActivePort file doesn't
#   exist". Observed: 192 consecutive SessionNotCreatedException errors in the
#   Build 70 production log.
#   Fix: _clear_profile_singletons() removes SingletonLock, SingletonSocket,
#   and SingletonCookie from the profile dir before every webdriver.Chrome()
#   instantiation. Called from _get_driver() when self._driver is None.
#
# BUILD 67 — BUG-SCRAPER-001-FIX (preserved)
# BUILD 64 — BUG-PERF-001-FIX (preserved)
# BUILD 63 — CLOUDSCRAPER ELIMINATED (preserved)
# BUILD 62 — BUG-LANG-002-FIX (preserved)
# BUILD 61 — BUG-LANG-001-FIX (preserved)
# =============================================================================

from __future__ import annotations

import hashlib
import logging
import os
import re
import threading
import time
from pathlib import Path
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app.config import get_settings

logger = logging.getLogger(__name__)

# =============================================================================
# CONSTANTS
# =============================================================================

# ISO 639-1 → Booking.com URL language suffix
LANG_URL_MAP: dict[str, str] = {
    "en": "en-gb",
    "es": "es",
    "de": "de",
    "fr": "fr",
    "it": "it",
    "pt": "pt-pt",
    "nl": "nl",
    "pl": "pl",
    "ru": "ru",
    "zh": "zh-cn",
    "ja": "ja",
    "ko": "ko",
}

# ISO 639-1 → Accept-Language header value (BUG-LANG-002 fix)
LANG_TO_ACCEPT_LANGUAGE: dict[str, str] = {
    "en": "en-GB,en;q=0.9,en-US;q=0.8",
    "es": "es-ES,es;q=0.9",
    "de": "de-DE,de;q=0.9",
    "fr": "fr-FR,fr;q=0.9",
    "it": "it-IT,it;q=0.9",
    "pt": "pt-PT,pt;q=0.9,pt-BR;q=0.8",
    "nl": "nl-NL,nl;q=0.9",
    "pl": "pl-PL,pl;q=0.9",
    "ru": "ru-RU,ru;q=0.9",
    "zh": "zh-CN,zh;q=0.9",
    "ja": "ja-JP,ja;q=0.9",
    "ko": "ko-KR,ko;q=0.9",
}

# Minimum bytes expected from a real Booking.com hotel page (150k–500k typical)
_SHORT_HTML_DEFAULT_THRESHOLD: int = 5_000

# Block page indicators detectable by Selenium (Cloudflare JS challenge
# and Booking.com anti-bot pages).
# BUG-SCRAPER-001-FIX (Build 67): Booking.com "Max challenge attempts exceeded"
# page was not in this list. driver.page_source after that page hangs 30+
# minutes because Booking.com JS keeps the browser in perpetual loading state.
_BLOCK_INDICATORS: tuple[str, ...] = (
    "just a moment",
    "checking your browser",
    "enable javascript and cookies",
    "ddos-guard",
    "access denied",
    "cf-browser-verification",
    "ray id",
    # Booking.com anti-bot challenge pages (BUG-SCRAPER-001-FIX)
    "max challenge attempts exceeded",
    "please refresh the page to try again",
    "security check to continue",
    "too many requests",
)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def build_language_url(base_url: str, lang: str) -> str:
    """
    Build a language-specific Booking.com URL.

    BUG-URL-001-FIX (Build 75): Booking.com canonical URL format embeds the
    language code directly in the HTML filename:
      Correct:  .../hotel-name.en-gb.html?lang=en-gb
      Previous: .../hotel-name.html?lang=en-gb   ← triggers 301 redirect

    Evidence: canonical URLs extracted from pruebas/ HTML files confirm the
    embedded format for all languages (de, en-gb, es, it, fr, pt-pt).

    The 301 redirect was causing Selenium to lose the CDP Accept-Language
    header set by BUG-LANG-002-FIX, occasionally producing language mismatches.

    Args:
        base_url: Base hotel URL (any format — with or without existing lang).
        lang:     ISO 639-1 language code (e.g. "de", "en").

    Returns:
        Canonical URL with lang code in filename + ?lang= query param.
    """
    lang_code = LANG_URL_MAP.get(lang, lang)
    url = base_url.rstrip("/")

    # Strip any existing query string
    if "?" in url:
        url = url.split("?")[0].rstrip("&")

    # Strip any existing embedded lang code: hotel.de.html → hotel.html
    # Pattern: .<lang_code>.html at end of path
    url = re.sub(r"\.[a-z]{2}(?:-[a-z]{2,4})?\.html$", ".html", url, flags=re.IGNORECASE)

    # Ensure base URL ends with .html (add if missing)
    if not url.lower().endswith(".html"):
        url = url + ".html"

    # Embed lang_code in filename: hotel.html → hotel.en-gb.html
    url = re.sub(r"\.html$", f".{lang_code}.html", url, flags=re.IGNORECASE)

    return f"{url}?lang={lang_code}"


def _is_blocked(html: str) -> bool:
    """Return True if HTML is a Cloudflare block/challenge page."""
    if not html:
        return True
    lower = html.lower()
    return any(indicator in lower for indicator in _BLOCK_INDICATORS)


def _is_hotel_page(html: str) -> bool:
    """Return True if HTML looks like a real Booking.com hotel page."""
    if not html or len(html) < 10_000:
        return False
    required = ("booking.com", "aggregateRating")
    return all(marker in html for marker in required)


def _detect_page_language(html: str) -> Optional[str]:
    """
    Extract the page language from Booking.com HTML.

    Checks (in order):
      1. <html lang="XX"> attribute
      2. <meta property="og:locale"> tag

    Returns the 2-letter ISO 639-1 code, or None if undetectable.
    """
    # Strategy 1: <html lang="...">
    m = re.search(r'<html[^>]+\blang=["\']([a-z]{2})', html, re.IGNORECASE)
    if m:
        return m.group(1).lower()

    # Strategy 2: og:locale meta
    m = re.search(
        r'property=["\']og:locale["\'][^>]+content=["\']([a-z]{2})',
        html,
        re.IGNORECASE,
    )
    if m:
        return m.group(1).lower()

    # Strategy 3: content-language meta
    m = re.search(
        r'http-equiv=["\']content-language["\'][^>]+content=["\']([a-z]{2})',
        html,
        re.IGNORECASE,
    )
    if m:
        return m.group(1).lower()

    return None


def _save_debug_html(html: str, url: str, tag: str) -> None:
    """
    Persist raw HTML to disk for post-mortem analysis.
    Only active when DEBUG_HTML_SAVE=true in config.
    """
    try:
        cfg = get_settings()
        if not getattr(cfg, "DEBUG_HTML_SAVE", False):
            return
        debug_dir = Path("data") / "debug_html"
        debug_dir.mkdir(parents=True, exist_ok=True)
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        path = debug_dir / f"{tag}_{url_hash}.html"
        path.write_text(html, encoding="utf-8", errors="replace")
        logger.debug("Debug HTML saved: %s (%d bytes)", path, len(html))
    except Exception as exc:
        logger.warning("_save_debug_html failed: %s", exc)


# =============================================================================
# SeleniumEngine — SOLE SCRAPING ENGINE (Build 63)
# =============================================================================

class SeleniumEngine:
    """
    Selenium/Brave WebDriver scraping engine.

    Build 63: Promoted to sole engine. CloudScraperEngine removed.
    Build 62: BUG-LANG-002 — _set_language_headers(), reset_browser().
    Build 61: BUG-LANG-001 — Short HTML fast-fail.

    Thread safety: all driver interactions are serialised via self._lock.
    One shared Brave instance per process; reset_browser() discards it
    after VPN rotation so the next call recreates it with a clean profile.
    """

    def __init__(self) -> None:
        self._driver: Optional[webdriver.Chrome] = None
        self._lock: threading.Lock = threading.Lock()
        self._cfg = get_settings()
        self._blocked_count: int = 0

    # ── Driver lifecycle ──────────────────────────────────────────────────────

    def _build_chrome_options(self) -> webdriver.ChromeOptions:
        """Construct Chrome/Brave options with anti-detection settings."""
        cfg = self._cfg
        options = webdriver.ChromeOptions()

        brave_path: Optional[str] = getattr(cfg, "BRAVE_PATH", None)
        if brave_path:
            options.binary_location = brave_path

        headless: bool = getattr(cfg, "HEADLESS_BROWSER", False)
        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        options.add_experimental_option("useAutomationExtension", False)

        # Prevent first-run setup dialogs and default-browser prompts
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-default-apps")

        # ── BUG-BRAVE-001-FIX: Anti-initialization-hang flags (Build 73) ──────
        # Prevent Brave from spending time on network/sync/updates during startup.
        # Each of these can stall Brave initialization beyond ChromeDriver's 60s timeout.
        options.add_argument("--disable-component-update")       # no extension updates on start
        options.add_argument("--disable-background-networking")  # no background network calls
        options.add_argument("--disable-sync")                   # no account sync
        options.add_argument("--disable-translate")              # no translation service init
        options.add_argument("--safebrowsing-disable-auto-update")  # no safe-browsing DB update
        options.add_argument("--disable-client-side-phishing-detection")  # no phishing init
        options.add_argument("--metrics-recording-only")         # minimal metrics
        options.add_argument("--disable-features=OptimizationGuideModelDownloading,"
                             "OptimizationHintsFetching,OptimizationTargetPrediction,"
                             "OptimizationHints")                # no ML model downloads

        return options

    def _enforce_single_tab(self) -> None:
        """
        RULE (Build 71): Brave must have exactly ONE tab at all times.
        If more than one tab is open it is a system error.
        Closes every window_handle after the first. Called from _get_driver()
        after init and from _fetch_with_selenium() before every driver.get().
        Must be called from within self._lock.
        """
        if self._driver is None:
            return
        try:
            handles = self._driver.window_handles
            if len(handles) <= 1:
                return
            logger.warning(
                "RULE-SINGLE-TAB: %d tabs detected — expected 1. Closing extras.",
                len(handles),
            )
            keep = handles[0]
            for handle in handles[1:]:
                try:
                    self._driver.switch_to.window(handle)
                    self._driver.close()
                    logger.info("RULE-SINGLE-TAB: Closed extra tab %s", handle)
                except Exception as exc:
                    logger.warning("RULE-SINGLE-TAB: Could not close tab %s: %s", handle, exc)
            self._driver.switch_to.window(keep)
        except Exception as exc:
            logger.warning("RULE-SINGLE-TAB: tab enforcement skipped: %s", exc)

    def _get_driver(self) -> webdriver.Chrome:
        """
        Lazy-initialise and return the Chrome/Brave WebDriver.
        Assumes called from within self._lock.
        BUILD 74: uses default system Brave profile (no --user-data-dir).
        RULE-SINGLE-TAB: enforces exactly one tab after init.
        """
        if self._driver is None:
            options = self._build_chrome_options()
            chromedriver_path: Optional[str] = getattr(
                self._cfg, "CHROMEDRIVER_PATH", None
            )

            if chromedriver_path:
                from selenium.webdriver.chrome.service import Service

                service = Service(executable_path=chromedriver_path)
                self._driver = webdriver.Chrome(
                    service=service, options=options
                )
            else:
                self._driver = webdriver.Chrome(options=options)

            # Remove webdriver navigator flag
            self._driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver',"
                " {get: () => undefined})"
            )
            logger.info("Selenium: Brave started")
            self._enforce_single_tab()  # RULE-SINGLE-TAB: ensure clean state on init

        return self._driver

    def _reinit_driver(self) -> None:
        """
        Restart the WebDriver to clear all browser state.
        Assumes called from within self._lock.
        """
        try:
            if self._driver:
                self._driver.quit()
        except Exception as exc:
            logger.debug("_reinit_driver quit error (ignored): %s", exc)
        finally:
            self._driver = None
        logger.info("Selenium: driver reinitialized (clean state)")

    def reset_browser(self) -> bool:
        """
        BUG-LANG-002-FIX: Fully restart Brave after VPN rotation.

        Called by ScraperService._process_url() immediately after any forced
        VPN rotation. Ensures the next scrape uses a completely clean browser
        profile (no cached DNS, no TLS session resumption, no stale cookies).

        Returns True on success, False if the quit itself raised an error
        (caller should log a warning but proceed — the next _get_driver()
        call will still create a fresh instance via the None guard).
        """
        logger.info(
            "BUG-LANG-002-FIX: Restarting Selenium browser after VPN rotation."
        )
        success = True
        with self._lock:
            if self._driver is not None:
                try:
                    self._driver.quit()
                    logger.debug(
                        "BUG-LANG-002-FIX: Old driver quit successfully."
                    )
                except Exception as exc:
                    logger.warning(
                        "BUG-LANG-002-FIX: driver.quit() error (ignored): %s",
                        exc,
                    )
                    success = False
                finally:
                    self._driver = None

        log_fn = logger.info if success else logger.warning
        log_fn(
            "BUG-LANG-002-FIX: Browser reset %s — "
            "next request will spawn a fresh driver.",
            "complete" if success else "with errors",
        )
        return success

    def quit(self) -> None:
        """Quit the WebDriver and release all resources."""
        with self._lock:
            if self._driver:
                try:
                    self._driver.quit()
                except Exception as exc:
                    logger.warning("SeleniumEngine.quit() error: %s", exc)
                finally:
                    self._driver = None

    # ── Language header injection (BUG-LANG-002) ──────────────────────────────

    def _set_language_headers(
        self, driver: webdriver.Chrome, lang: str
    ) -> None:
        """
        BUG-LANG-002-FIX: Reset language state before every driver.get().

        Booking.com determines page language by priority:
          1. bkng_lang session cookie  ← HIGHEST (overrides URL param)
          2. Accept-Language header    ← Medium
          3. ?lang=XX URL parameter   ← LOWEST (ignored when cookies exist)

        This method eliminates (1) and enforces (2) so the URL parameter
        becomes the effective language selector.

        Must be called INSIDE the retry loop, immediately before driver.get().
        Assumes called from within self._lock.
        """
        accept_lang = LANG_TO_ACCEPT_LANGUAGE.get(lang, f"{lang};q=0.9")

        # Inject Accept-Language via Chrome DevTools Protocol
        try:
            driver.execute_cdp_cmd("Network.enable", {})
            driver.execute_cdp_cmd(
                "Network.setExtraHTTPHeaders",
                {"headers": {"Accept-Language": accept_lang}},
            )
            logger.debug(
                "BUG-LANG-002-FIX: CDP Accept-Language='%s' for lang=%s",
                accept_lang,
                lang,
            )
        except Exception as exc:
            logger.warning(
                "BUG-LANG-002-FIX: CDP header injection failed (%s) "
                "for lang=%s — falling back to cookie-only reset",
                exc,
                lang,
            )

        # Wipe all Booking.com session cookies (removes bkng_lang)
        try:
            driver.delete_all_cookies()
            logger.debug(
                "BUG-LANG-002-FIX: All cookies deleted before lang=%s", lang
            )
        except Exception as exc:
            logger.warning(
                "BUG-LANG-002-FIX: delete_all_cookies() failed: %s", exc
            )

    # ── Facilities expansion helper ───────────────────────────────────────────

    # BUG-SVC-001-FIX: Booking.com renders only the "Most popular facilities"
    # block (~10 items) in the initial DOM.  The full list (up to ~100+ items)
    # is injected via JavaScript only AFTER the user clicks a "See all N
    # facilities" button.  Without this click the extractor always receives a
    # truncated view, explaining the 87-99% coverage gap reported in the audit.
    #
    # Selectors validated against EN/ES/DE/IT/FR/PT page variants:
    #   • Anchor/button containing data-testid="facility-list-toggle"
    #   • Any <a> or <button> whose visible text matches _SEE_ALL_FAC_RE
    #   • Legacy: href fragment "#hp_facilities_box"
    #   • Legacy: element matching CSS "#hp_facilities_box" (scroll-to reveal)
    _SEE_ALL_FAC_RE: re.Pattern = re.compile(
        r"""
        ^(\s*)(
            See\s+all                     # EN
          | Ver\s+(los\s+|todos\s+(los\s+)?)? \d  # ES: "Ver los 101 servicios"
          | Ver\s+todos                   # ES alt
          | Alle\s+\d+\s+Einrichtungen    # DE
          | Alle\s+anzeigen               # DE alt
          | Voir\s+(les\s+)?\d+           # FR
          | Vedi\s+tutti                  # IT
          | Mostra\s+tutti                # IT alt
          | Ver\s+todas                   # PT
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    def _expand_facilities(self, driver: webdriver.Chrome) -> bool:
        """
        BUG-SVC-001-FIX: Click the 'See all N facilities' button so that
        Booking.com injects the full facilities section into the DOM before
        page_source is captured.

        Strategy:
          1. data-testid="facility-list-toggle" (most stable — React attr)
          2. Text-match via _SEE_ALL_FAC_RE on <a>/<button> elements
          3. href="#hp_facilities_box" anchor (legacy pages)

        After a successful click, waits up to 10 s for
        data-testid="property-section--facilities" to appear.

        Returns True if the expansion succeeded, False if the button was not
        found or an error occurred (non-fatal — caller proceeds with partial DOM).
        """
        fac_wait_s: float = 10.0

        # ── Strategy 1: data-testid attribute ────────────────────────────────
        try:
            btn = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='facility-list-toggle']"
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            driver.execute_script("arguments[0].click();", btn)
            WebDriverWait(driver, fac_wait_s).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "[data-testid='property-section--facilities']")
                )
            )
            logger.info("BUG-SVC-001-FIX: facilities expanded via data-testid toggle")
            return True
        except (NoSuchElementException, TimeoutException, WebDriverException):
            pass

        # ── Strategy 2: text-match on <a> and <button> ───────────────────────
        try:
            candidates = driver.find_elements(
                By.CSS_SELECTOR, "a, button"
            )
            for elem in candidates:
                try:
                    text = elem.text.strip()
                except WebDriverException:
                    continue
                if text and self._SEE_ALL_FAC_RE.match(text):
                    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                    driver.execute_script("arguments[0].click();", elem)
                    WebDriverWait(driver, fac_wait_s).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "[data-testid='property-section--facilities']")
                        )
                    )
                    logger.info(
                        "BUG-SVC-001-FIX: facilities expanded via text-match: %r", text
                    )
                    return True
        except (TimeoutException, WebDriverException):
            pass
        except Exception as exc:
            logger.debug("BUG-SVC-001: strategy2 error: %s", exc)

        # ── Strategy 3: href="#hp_facilities_box" anchor (legacy) ────────────
        try:
            btn = driver.find_element(
                By.CSS_SELECTOR, "a[href='#hp_facilities_box']"
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            driver.execute_script("arguments[0].click();", btn)
            WebDriverWait(driver, fac_wait_s).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#hp_facilities_box")
                )
            )
            logger.info("BUG-SVC-001-FIX: facilities expanded via #hp_facilities_box anchor")
            return True
        except (NoSuchElementException, TimeoutException, WebDriverException):
            pass

        logger.debug("BUG-SVC-001: no 'See all facilities' button found — partial DOM")
        return False

    # ── Gallery helpers ───────────────────────────────────────────────────────

    def _open_gallery(self, driver: webdriver.Chrome) -> int:
        """
        Click the first hotel image to open the full gallery and
        scroll to load all image thumbnails.

        Returns the number of unique images loaded.
        """
        gallery_selector = "img[src*='bstatic.com/xdata/images/hotel/']"
        try:
            trigger = driver.find_element(By.CSS_SELECTOR, gallery_selector)
            trigger.click()
            time.sleep(1.5)

            # Scroll to load all lazy images
            last_count = 0
            for _ in range(15):
                imgs = driver.find_elements(By.CSS_SELECTOR, gallery_selector)
                count = len(imgs)
                if count == last_count:
                    break
                last_count = count
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight)"
                )
                time.sleep(1)

            # Deduplicate by src
            srcs = {
                img.get_attribute("src")
                for img in driver.find_elements(By.CSS_SELECTOR, gallery_selector)
                if img.get_attribute("src")
            }
            unique = len(srcs)
            logger.info(
                "Gallery opened via: %s", gallery_selector
            )
            logger.info("Gallery: %d images loaded after scroll", last_count)
            logger.info("Gallery: %d unique image URLs extracted", unique)
            return unique

        except (NoSuchElementException, WebDriverException) as exc:
            logger.debug("Gallery not opened: %s", exc)
            return 0

    def _extract_hotel_photos_js(self, driver: webdriver.Chrome) -> int:
        """
        Extract rich photo metadata from the hotelPhotos JavaScript variable.
        Returns count of photos found.
        """
        try:
            photos_js: Optional[object] = driver.execute_script(
                "return typeof hotelPhotos !== 'undefined' ? hotelPhotos : null;"
            )
            if photos_js and isinstance(photos_js, list):
                count = len(photos_js)
                logger.info(
                    "hotelPhotos JS: %d photos extracted from page source",
                    count,
                )
                return count
        except Exception as exc:
            logger.debug("hotelPhotos JS extraction failed: %s", exc)
        return 0

    # ── Core scraping ─────────────────────────────────────────────────────────

    def _fetch_with_selenium(
        self,
        url: str,
        lang: str,
        attempt: int,
        max_retries: int,
    ) -> Optional[str]:
        """
        Execute one Selenium page fetch within the thread lock.

        Sequence:
          1. BUG-LANG-002-FIX: Set Accept-Language + clear cookies
          2. BUG-PERF-001-FIX: Italian pre-scrape delay
          3. driver.set_page_load_timeout (BUG-PERF-001-FIX)
          4. driver.get(url)
          5. Wait for hotel content (BUG-PERF-001-FIX: per-selector timeout capped)
          6. Language verification (mismatch → retry)
          7. Short HTML check (BUG-LANG-001 fast-fail)
          8. Gallery open + photo JS extraction
          9. Return final page_source

        Assumes called from outside self._lock (acquires it internally).
        """
        cfg = self._cfg
        short_threshold: int = getattr(
            cfg, "SHORT_HTML_THRESHOLD", _SHORT_HTML_DEFAULT_THRESHOLD
        )
        page_timeout: int = getattr(cfg, "SCRAPER_REQUEST_TIMEOUT", 30)

        # BUG-PERF-001-FIX: Use a dedicated per-selector wait timeout.
        # Previously page_timeout (30 s) was used for ALL 4 CSS selectors:
        # worst case = 4 × 30 s = 120 s before proceeding with partial load.
        # Observed: it=144.0 s and it=124.6 s in the 2026-04-01 run.
        # New field SELENIUM_CONTENT_WAIT_TIMEOUT_S defaults to 10 s →
        # worst case = 4 × 10 s = 40 s.  SCRAPER_REQUEST_TIMEOUT is now used
        # exclusively for driver.set_page_load_timeout() below.
        content_wait_s: float = getattr(
            cfg, "SELENIUM_CONTENT_WAIT_TIMEOUT_S", 10.0
        )

        # BUG-PERF-001-FIX: Italian pre-scrape delay.
        # Italian pages show avg 73.7 s vs 49-64 s for other languages and
        # 15.4% of Italian scrapes exceeded 120 s.  A short pre-scrape pause
        # reduces anti-bot challenge accumulation across the session.
        if lang == "it":
            it_delay: float = getattr(cfg, "LANG_SCRAPE_DELAY_IT", 5.0)
            if it_delay > 0:
                logger.info(
                    "BUG-PERF-001-FIX: Italian pre-scrape delay %.1f s "
                    "before %s", it_delay, url,
                )
                time.sleep(it_delay)

        with self._lock:
            driver = self._get_driver()
            self._enforce_single_tab()  # RULE-SINGLE-TAB: close any stray tabs before fetch

            # BUG-PERF-001-FIX: Cap the total navigation time.
            # Without this, driver.get() can block indefinitely on slow pages.
            driver.set_page_load_timeout(page_timeout)

            # ── BUG-LANG-002-FIX: Reset language state ─────────────────────
            if getattr(cfg, "SELENIUM_RESET_LANG_ON_EACH_REQUEST", True):
                self._set_language_headers(driver, lang)

            # ── Navigate ────────────────────────────────────────────────────
            try:
                driver.get(url)
            except WebDriverException as exc:
                logger.warning(
                    "Selenium: driver.get() failed (attempt %d/%d): %s",
                    attempt, max_retries, exc,
                )
                return None

            # ── Wait for hotel content ──────────────────────────────────────
            # BUG-EXTRACT-IT-001-FIX (Build 98): sustituye el bucle for de 4
            # WebDriverWait secuenciales por un único EC.any_of() que evalúa
            # todos los selectores en paralelo dentro de content_wait_s.
            #
            # Antes (Build 97): peor caso = 4 × content_wait_s = 40 s
            # (si los 3 primeros selectores timeout y el 4° coincide)
            # Ahora (Build 98):  peor caso = 1 × content_wait_s = 10 s
            # (cualquier selector que coincida resuelve el wait inmediatamente)
            #
            # Nota: BUG-PERF-001-FIX (Build 64) redujo content_wait_s de 30 s
            # a 10 s; BUG-EXTRACT-IT-001-FIX elimina la multiplicación × 4.
            hotel_selectors = (
                "h2[data-testid='title']",
                "#hp_hotel_name",
                ".hp__hotel-name",
                "h1.pp-header__title",
            )
            loaded = False
            try:
                # EC.any_of(): resuelve True en cuanto cualquier condición
                # se cumpla; levanta TimeoutException si ninguna se cumple
                # dentro de content_wait_s. Disponible en selenium >= 4.0.
                WebDriverWait(driver, content_wait_s).until(
                    EC.any_of(
                        *[
                            EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                            for sel in hotel_selectors
                        ]
                    )
                )
                loaded = True
            except TimeoutException:
                loaded = False

            if not loaded:
                # BUG-SCRAPER-001-FIX: stop ongoing page load BEFORE reading
                # page_source. Booking.com/Cloudflare challenge pages run JS
                # indefinitely — driver.page_source hangs 30+ min without this.
                try:
                    driver.execute_script("window.stop()")
                except Exception:
                    pass
                # Check for Cloudflare / Booking.com challenge
                page_low = driver.page_source.lower()
                if any(ind in page_low for ind in _BLOCK_INDICATORS):
                    logger.warning(
                        "Selenium: Cloudflare challenge detected "
                        "(attempt %d/%d) — reinitializing browser for %s",
                        attempt, max_retries, url,
                    )
                    self._reinit_driver()
                    return None
                logger.warning(
                    "Selenium: timeout waiting for hotel content "
                    "(attempt %d/%d) — proceeding with partial load for %s",
                    attempt, max_retries, url,
                )

            # BUG-SCRAPER-001-FIX: stop page load before reading source to
            # prevent infinite hang on challenge pages that passed indicator check.
            try:
                driver.execute_script("window.stop()")
            except Exception:
                pass
            html = driver.page_source

            # ── BUG-LANG-001-FIX: Short HTML fast-fail ─────────────────────
            html_len = len(html)
            if html_len < short_threshold:
                logger.warning(
                    "BUG-LANG-001-FIX: Short HTML (%d bytes) — "
                    "block page detected, skipping remaining retries for %s",
                    html_len, url,
                )
                _save_debug_html(html, url, f"short_html_selenium_a{attempt}")
                with threading.Lock():
                    self._blocked_count += 1
                return None

            # ── Language verification ───────────────────────────────────────
            detected = _detect_page_language(html)
            lang_iso = lang.split("-")[0].lower()

            if detected and detected not in (lang_iso, "x-default", "en"):
                # Allow 'en' as fallback for some hotels regardless of lang
                logger.warning(
                    "Selenium language mismatch: requested=%s got=%s",
                    lang, detected,
                )
                return None

            # ── Verify it's a real hotel page ───────────────────────────────
            if not _is_hotel_page(html):
                logger.warning(
                    "Selenium: page does not look like a hotel page for %s",
                    url,
                )
                return None

            # ── BUG-SVC-001-FIX: Expand full facilities list ────────────────
            # Must run BEFORE page_source is captured so the extractor sees
            # the full data-testid="property-section--facilities" block.
            self._expand_facilities(driver)

            # ── Gallery / photo extraction ──────────────────────────────────
            self._open_gallery(driver)
            photo_count = self._extract_hotel_photos_js(driver)
            if photo_count > 0:
                logger.info(
                    "Gallery: %d photos with full metadata (hotelPhotos JS)",
                    photo_count,
                )

            return driver.page_source

    def scrape(self, url: str, lang: str) -> Optional[str]:
        """
        Scrape a Booking.com hotel page in the specified language.

        Build 63: Sole engine — no CloudScraper fallback.
        Retries up to MAX_LANG_RETRIES times with exponential backoff.

        Args:
            url:  Language-specific Booking.com URL.
            lang: ISO 639-1 language code (e.g. "de", "fr").

        Returns:
            Full page HTML on success, None on all retries exhausted.
        """
        cfg = self._cfg
        max_retries: int = getattr(cfg, "MAX_LANG_RETRIES", 3)
        retry_delay: float = getattr(cfg, "SCRAPER_RETRY_DELAY", 2.0)

        for attempt in range(1, max_retries + 1):
            try:
                html = self._fetch_with_selenium(url, lang, attempt, max_retries)
                if html is not None:
                    return html

                if attempt < max_retries:
                    wait = retry_delay * attempt
                    logger.info(
                        "Selenium retry %d -- waiting %ds -- %s",
                        attempt + 1,
                        int(wait),
                        url,
                    )
                    time.sleep(wait)

            except Exception as exc:
                logger.error(
                    "Selenium unexpected error (attempt %d/%d) for %s: %s",
                    attempt, max_retries, url, exc, exc_info=True,
                )
                if attempt < max_retries:
                    time.sleep(retry_delay * attempt)

        logger.error("Selenium language retries exhausted for %s", url)
        return None
