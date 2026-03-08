"""
extractor.py — BookingScraper Pro v48
Fixes applied:
  BUG-014 / SCRAP-BUG-014: BeautifulSoup parser falls back gracefully.
  BUG-107 / SCRAP-BUG-007: Language detection tries multiple strategies.
  Platform               : Windows 11 compatible (no POSIX deps).
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup, FeatureNotFound

from app.config import get_settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Parser selection — BUG-014 / SCRAP-BUG-014 fix
# ---------------------------------------------------------------------------

def _make_soup(html: str) -> BeautifulSoup:
    """
    Create BeautifulSoup with lxml, falling back to html.parser.
    BUG-014 fix: lxml is preferred for speed but html.parser (stdlib)
    is always available as a fallback.
    """
    for parser in ("lxml", "html.parser"):
        try:
            return BeautifulSoup(html, parser)
        except FeatureNotFound:
            logger.debug("Parser '%s' unavailable, trying next.", parser)
    # This path should never be reached (html.parser is stdlib)
    return BeautifulSoup(html, "html.parser")


# ---------------------------------------------------------------------------
# Language detection — BUG-107 fix: multi-strategy
# ---------------------------------------------------------------------------

_LANG_META_PATTERNS: List[re.Pattern] = [
    re.compile(r'<html[^>]+lang=["\']([a-z]{2}(?:-[a-z]{2,4})?)["\']', re.IGNORECASE),
    re.compile(r'<meta[^>]+http-equiv=["\']content-language["\'][^>]+content=["\']([a-z]{2}(?:-[a-z]{2,4})?)["\']', re.IGNORECASE),
    re.compile(r'<meta[^>]+content=["\']([a-z]{2}(?:-[a-z]{2,4})?)["\'][^>]+http-equiv=["\']content-language["\']', re.IGNORECASE),
]


def detect_language(html: str, url: str = "") -> Optional[str]:
    """
    Detect the content language of an HTML page using multiple strategies.

    Strategy order:
    1. <html lang="xx"> attribute
    2. <meta http-equiv="Content-Language"> tag
    3. URL language path component (e.g. /hotel.es.html → 'es')
    4. og:locale meta tag
    5. Return None if undetermined

    BUG-107 fix: all strategies attempted, not just one meta tag.
    """
    if not html:
        return None

    # Strategy 1 & 2: regex on raw HTML (faster than full parse for this)
    for pattern in _LANG_META_PATTERNS:
        match = pattern.search(html[:2000])  # Check only head section
        if match:
            lang = match.group(1).lower()[:2]
            logger.debug("Language detected via meta/html-attr: %s", lang)
            return lang

    # Strategy 3: BeautifulSoup og:locale
    try:
        soup = _make_soup(html[:5000])
        og_locale = soup.find("meta", attrs={"property": "og:locale"})
        if og_locale and og_locale.get("content"):
            lang = str(og_locale["content"]).lower()[:2]
            logger.debug("Language detected via og:locale: %s", lang)
            return lang

        # Strategy 4: <meta name="language">
        meta_lang = soup.find("meta", attrs={"name": re.compile(r"^language$", re.I)})
        if meta_lang and meta_lang.get("content"):
            lang = str(meta_lang["content"]).lower()[:2]
            logger.debug("Language detected via meta[name=language]: %s", lang)
            return lang

    except Exception as exc:
        logger.debug("Language detection via BeautifulSoup failed: %s", exc)

    # Strategy 5: URL path analysis
    if url:
        url_lang = _lang_from_url(url)
        if url_lang:
            logger.debug("Language detected via URL: %s", url_lang)
            return url_lang

    logger.debug("Language undetermined for URL: %s", url)
    return None


def _lang_from_url(url: str) -> Optional[str]:
    """Extract ISO 639-1 code from Booking.com URL path pattern."""
    # Match .es.html or .en-gb.html patterns
    match = re.search(r"\.([a-z]{2})(?:-[a-z]{2,4})?\.html", url, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return None


# ---------------------------------------------------------------------------
# Data extractors
# ---------------------------------------------------------------------------

class HotelExtractor:
    """Extract structured hotel data from Booking.com HTML."""

    def __init__(self, html: str, url: str = "", language: str = "en") -> None:
        self.soup = _make_soup(html)
        self.url = url
        self.language = language
        self._cfg = get_settings()

    def extract_all(self) -> Dict[str, Any]:
        """Extract all available hotel fields and return as dict."""
        data: Dict[str, Any] = {
            "url": self.url,
            "language": self.language,
            "hotel_name": self._extract_name(),
            "address": self._extract_address(),
            "description": self._extract_description(),
            "review_score": self._extract_review_score(),
            "review_count": self._extract_review_count(),
            "star_rating": self._extract_star_rating(),
            "city": self._extract_city(),
            "country": self._extract_country(),
            "latitude": self._extract_latitude(),
            "longitude": self._extract_longitude(),
            "amenities": self._extract_amenities(),
            "photos": self._extract_photo_urls(),
        }
        return {k: v for k, v in data.items() if v is not None}

    def _safe_text(self, selector_result: Any) -> Optional[str]:
        """Safely extract text from a BeautifulSoup result."""
        if selector_result is None:
            return None
        try:
            text = selector_result.get_text(strip=True)
            return text[:self._cfg.MAX_ERROR_LEN] if text else None
        except Exception:
            return None

    def _extract_name(self) -> Optional[str]:
        xp = self._cfg.XPATHS.get("hotel_name", "")
        # Try multiple selectors with fallback
        for selector in [
            {"attrs": {"data-testid": "title"}},
            {"class_": re.compile(r"pp-header__title", re.I)},
            {"id": "hp_hotel_name"},
        ]:
            el = self.soup.find(True, **selector)  # type: ignore
            if el:
                return self._safe_text(el)
        # Fallback: <h1> or <h2> containing "hotel"
        for tag in self.soup.find_all(["h1", "h2"], limit=5):
            text = self._safe_text(tag)
            if text and len(text) > 3:
                return text
        return None

    def _extract_address(self) -> Optional[str]:
        el = self.soup.find(attrs={"data-testid": "address"})
        return self._safe_text(el)

    def _extract_description(self) -> Optional[str]:
        el = self.soup.find(attrs={"data-testid": "property-description"})
        if el:
            return self._safe_text(el)
        # Fallback
        el = self.soup.find("div", {"id": "property_description_content"})
        return self._safe_text(el)

    def _extract_review_score(self) -> Optional[float]:
        try:
            el = self.soup.find(attrs={"data-testid": "review-score"})
            if el:
                text = el.get_text(strip=True)
                match = re.search(r"(\d+[.,]\d+)", text)
                if match:
                    return float(match.group(1).replace(",", "."))
        except Exception as exc:
            logger.debug("review_score extraction failed: %s", exc)
        return None

    def _extract_review_count(self) -> Optional[int]:
        try:
            patterns = [
                re.compile(r"(\d[\d,\.]+)\s*review", re.IGNORECASE),
                re.compile(r"(\d[\d,\.]+)\s*opinion", re.IGNORECASE),
                re.compile(r"(\d[\d,\.]+)\s*Bewertung", re.IGNORECASE),
            ]
            text = self.soup.get_text()
            for pattern in patterns:
                match = pattern.search(text)
                if match:
                    count_str = match.group(1).replace(",", "").replace(".", "")
                    return int(count_str)
        except Exception as exc:
            logger.debug("review_count extraction failed: %s", exc)
        return None

    def _extract_star_rating(self) -> Optional[float]:
        try:
            el = self.soup.find(attrs={"data-testid": "rating-stars"})
            if el:
                stars = el.find_all("svg")
                return float(len(stars)) if stars else None
        except Exception:
            pass
        return None

    def _extract_city(self) -> Optional[str]:
        try:
            breadcrumbs = self.soup.find_all(attrs={"data-testid": re.compile(r"breadcrumb")})
            if len(breadcrumbs) >= 2:
                return self._safe_text(breadcrumbs[-2])
        except Exception:
            pass
        return None

    def _extract_country(self) -> Optional[str]:
        try:
            breadcrumbs = self.soup.find_all(attrs={"data-testid": re.compile(r"breadcrumb")})
            if breadcrumbs:
                return self._safe_text(breadcrumbs[0])
        except Exception:
            pass
        return None

    def _extract_latitude(self) -> Optional[float]:
        try:
            el = self.soup.find("a", {"data-atlas-latlng": True})
            if el:
                latlng = el["data-atlas-latlng"].split(",")
                return float(latlng[0])
        except Exception:
            pass
        return None

    def _extract_longitude(self) -> Optional[float]:
        try:
            el = self.soup.find("a", {"data-atlas-latlng": True})
            if el:
                latlng = el["data-atlas-latlng"].split(",")
                return float(latlng[1]) if len(latlng) > 1 else None
        except Exception:
            pass
        return None

    def _extract_amenities(self) -> List[str]:
        try:
            els = self.soup.find_all(attrs={"data-testid": "facility-list-item"})
            return [self._safe_text(el) for el in els if self._safe_text(el)]
        except Exception:
            return []

    def _extract_photo_urls(self) -> List[str]:
        try:
            imgs = self.soup.find_all("img", attrs={"data-testid": re.compile(r"photo", re.I)})
            urls = []
            for img in imgs:
                src = img.get("src") or img.get("data-src")
                if src and src.startswith("http"):
                    urls.append(src)
            return urls[:50]  # Cap at 50 images
        except Exception:
            return []
