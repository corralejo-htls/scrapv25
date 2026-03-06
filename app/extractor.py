"""
BookingScraper/app/extractor.py
HTML Extraction Engine — BookingScraper Pro
Windows 11 + Python 3.14.3

[FIX BUG-V9-001] This module was completely absent from the repository.
Both scraper.py CloudScraper (line 561) and Selenium (line 942) backends
import BookingExtractor at runtime, causing ModuleNotFoundError during every
scraping operation regardless of successful HTTP page retrieval.

CONTRACT:
    extractor = BookingExtractor(html_content: str, language: str)
    data: dict = extractor.extract_all()

    extract_all() returns a dict with keys:
        name, address, description, rating, total_reviews, rating_category,
        review_scores, services, facilities, house_rules, important_info,
        rooms, images_urls

DESIGN:
    - BeautifulSoup4 (primary parser: lxml with html.parser fallback)
      lxml is 2-10x faster for large HTML (1-3MB Booking.com pages).
    - Multiple CSS selector / attribute strategies per field with graceful fallback
    - All extraction errors are isolated: one failing field never breaks others
    - Returns None for missing fields; callers use data.get("field") safely
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Union

# [FIX ERR-PERF-004] Prefer lxml parser (C extension, 2-10x faster for large HTML).
# Falls back to html.parser if lxml is not installed.
try:
    import lxml  # noqa: F401 — presence check
    _BS4_PARSER = "lxml"
except ImportError:
    _BS4_PARSER = "html.parser"  # fallback: pure Python

from bs4 import BeautifulSoup
from loguru import logger


# ---------------------------------------------------------------------------
# Rating-category label maps  (8 languages — mirrors scraper_service.py)
# ---------------------------------------------------------------------------
_RATING_LABELS: Dict[str, Dict[str, str]] = {
    "en": {
        "exceptional": "Exceptional", "superb": "Superb",
        "fabulous": "Fabulous", "very good": "Very Good",
        "good": "Good", "pleasant": "Pleasant",
        "okay": "Okay", "poor": "Poor",
    },
    "es": {
        "excepcional": "Excepcional", "sobresaliente": "Sobresaliente",
        "fabuloso": "Fabuloso", "muy bien": "Muy Bien",
        "bien": "Bien", "agradable": "Agradable",
        "aceptable": "Aceptable", "malo": "Malo",
    },
    "de": {
        "ausgezeichnet": "Ausgezeichnet", "hervorragend": "Hervorragend",
        "fabelhaft": "Fabelhaft", "sehr gut": "Sehr Gut",
        "gut": "Gut", "angenehm": "Angenehm",
        "okay": "Okay", "schlecht": "Schlecht",
    },
    "fr": {
        "exceptionnel": "Exceptionnel", "superbe": "Superbe",
        "fabuleux": "Fabuleux", "très bien": "Très Bien",
        "bien": "Bien", "agréable": "Agréable",
        "passable": "Passable", "médiocre": "Médiocre",
    },
    "it": {
        "eccezionale": "Eccezionale", "magnifico": "Magnifico",
        "favoloso": "Favoloso", "molto buono": "Molto Buono",
        "buono": "Buono", "piacevole": "Piacevole",
        "discreto": "Discreto", "scarso": "Scarso",
    },
    "pt": {
        "excepcional": "Excepcional", "soberbo": "Soberbo",
        "fabuloso": "Fabuloso", "muito bom": "Muito Bom",
        "bom": "Bom", "agradável": "Agradável",
        "razoável": "Razoável", "fraco": "Fraco",
    },
    "nl": {
        "uitzonderlijk": "Uitzonderlijk", "geweldig": "Geweldig",
        "fantastisch": "Fantastisch", "heel goed": "Heel Goed",
        "goed": "Goed", "prettig": "Prettig",
        "redelijk": "Redelijk", "slecht": "Slecht",
    },
    "ru": {
        "исключительно": "Исключительно", "великолепно": "Великолепно",
        "чудесно": "Чудесно", "очень хорошо": "Очень Хорошо",
        "хорошо": "Хорошо", "приятно": "Приятно",
        "нормально": "Нормально", "плохо": "Плохо",
    },
}


# ---------------------------------------------------------------------------
# BookingExtractor
# ---------------------------------------------------------------------------

# ─────────────────────────────────────────────────────────────────────────────
# [FIX CRIT-008] Pydantic validation schema for extractor output.
# Validates JSONB-bound fields before INSERT to prevent malformed data in DB.
# All JSONB columns have CHECK constraints in PostgreSQL but validation here
# provides earlier feedback and more descriptive error messages.
# ─────────────────────────────────────────────────────────────────────────────
try:
    from pydantic import BaseModel, field_validator, model_validator
    _PYDANTIC_AVAILABLE = True
except ImportError:
    _PYDANTIC_AVAILABLE = False
    BaseModel = object  # type: ignore


if _PYDANTIC_AVAILABLE:
    class HotelExtractSchema(BaseModel):
        """Validation schema for BookingExtractor.extract_all() output."""
        name:            Optional[str]        = None
        address:         Optional[str]        = None
        description:     Optional[str]        = None
        rating:          Optional[float]      = None
        total_reviews:   Optional[int]        = None
        rating_category: Optional[str]        = None
        review_scores:   Optional[Dict[str, Any]]  = None
        services:        Optional[List[str]]       = None
        facilities:      Optional[Dict[str, Any]]  = None
        house_rules:     Optional[str]        = None
        important_info:  Optional[str]        = None
        rooms:           Optional[List[Any]]       = None
        images_urls:     Optional[List[str]]       = None

        @field_validator("rating")
        @classmethod
        def rating_in_range(cls, v: Optional[float]) -> Optional[float]:
            if v is not None and not (0.0 <= v <= 10.0):
                raise ValueError(f"rating={v} outside valid range [0.0, 10.0]")
            return v

        @field_validator("services", mode="before")
        @classmethod
        def services_must_be_list_of_str(cls, v):
            if v is None:
                return []
            if not isinstance(v, list):
                raise ValueError(f"services must be list, got {type(v).__name__}")
            return [str(item) for item in v if item is not None]

        @field_validator("facilities", mode="before")
        @classmethod
        def facilities_must_be_dict(cls, v):
            if v is None:
                return {}
            if not isinstance(v, dict):
                raise ValueError(f"facilities must be dict, got {type(v).__name__}")
            return v

        @field_validator("review_scores", mode="before")
        @classmethod
        def review_scores_must_be_dict(cls, v):
            if v is None:
                return {}
            if not isinstance(v, dict):
                raise ValueError(f"review_scores must be dict, got {type(v).__name__}")
            return v

        @field_validator("images_urls", mode="before")
        @classmethod
        def images_must_be_list_of_str(cls, v):
            if v is None:
                return []
            if not isinstance(v, list):
                raise ValueError(f"images_urls must be list, got {type(v).__name__}")
            return [str(url) for url in v if url]

        @field_validator("rooms", mode="before")
        @classmethod
        def rooms_must_be_list(cls, v):
            if v is None:
                return []
            if not isinstance(v, list):
                raise ValueError(f"rooms must be list, got {type(v).__name__}")
            return v


def validate_hotel_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    [FIX CRIT-008] Validate and normalize extractor output before DB INSERT.
    
    Raises:
        ValueError: if required structure constraints are violated.
    
    Returns:
        dict: Validated and normalized data dict (same keys, corrected types).
    """
    if not _PYDANTIC_AVAILABLE:
        # Without pydantic, apply minimal type coercion manually
        if data.get("services") is not None and not isinstance(data["services"], list):
            data["services"] = []
        if data.get("facilities") is not None and not isinstance(data["facilities"], dict):
            data["facilities"] = {}
        if data.get("review_scores") is not None and not isinstance(data["review_scores"], dict):
            data["review_scores"] = {}
        if data.get("images_urls") is not None and not isinstance(data["images_urls"], list):
            data["images_urls"] = []
        return data
    
    validated = HotelExtractSchema(**data)
    return validated.model_dump()


class BookingExtractor:
    """
    Extracts structured hotel data from a Booking.com HTML page.

    Args:
        html_content (str): Raw HTML string of the hotel page.
        language (str): ISO 639-1 language code (e.g. 'en', 'es').

    Usage:
        extractor = BookingExtractor(html_content, language="en")
        data = extractor.extract_all()
    """

    # [FIX CRIT-008] Block page detection signals — checked BEFORE BeautifulSoup
    # parsing. Matching any of these in a small HEAD slice indicates a
    # CAPTCHA, block page, or error page — not hotel content.
    _BLOCK_SIGNALS_PRE = (
        "just a moment",
        "enable javascript and cookies",
        "ddos-guard",
        "cf-browser-verification",
        "challenge-running",
        "captcha",
        "access denied",
        "403 forbidden",
        "blocked",
    )
    # Minimum expected content size for a valid hotel page (bytes)
    _MIN_CONTENT_BYTES = 20_000

    def __init__(self, html_content: str, language: str = "en") -> None:
        self._html    = html_content
        self._lang    = language.lower()

        # [FIX CRIT-008] Pre-parse validation: detect block/CAPTCHA/error pages
        # BEFORE passing to BeautifulSoup. This prevents garbage data extraction
        # from non-hotel pages and provides clear diagnostic logging.
        self._validate_html_pre_parse(html_content)

        # [FIX ERR-PERF-004] Use lxml if available (2-10x faster for large HTML).
        self._soup    = BeautifulSoup(html_content, _BS4_PARSER)
        self._result: Dict[str, Any] = {}

    def _validate_html_pre_parse(self, html: str) -> None:
        """
        [FIX CRIT-008] Validate HTML content before parsing.

        Checks for:
        1. Minimum content size (CAPTCHA pages are 30-80KB; hotel pages 1-3MB)
        2. Known block/CAPTCHA signal strings in the first 10KB of the document

        Raises:
            ValueError: if the HTML is identified as a non-hotel page.
        """
        if not html or not html.strip():
            raise ValueError("[CRIT-008] Empty HTML content received — nothing to extract.")

        content_len = len(html.encode("utf-8", errors="replace"))
        if content_len < self._MIN_CONTENT_BYTES:
            raise ValueError(
                f"[CRIT-008] HTML too small ({content_len} bytes < "
                f"{self._MIN_CONTENT_BYTES} bytes minimum). "
                "Likely a CAPTCHA or block page."
            )

        # Check only the first 10KB for block signals (performance)
        head_slice = html[:10_240].lower()
        for signal in self._BLOCK_SIGNALS_PRE:
            if signal in head_slice:
                raise ValueError(
                    f"[CRIT-008] Block/CAPTCHA signal '{signal}' detected in HTML head. "
                    "Page is not a valid hotel page."
                )

    # ──────────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────────

    def extract_all(self) -> Dict[str, Any]:
        """
        Run all field extractors and return a unified dict.

        Returns:
            Dict[str, Any]: All extracted fields. Missing fields are None.

        Raises:
            Never — all extraction errors are isolated and logged.
        """
        extractors = [
            ("name",            self._extract_name),
            ("address",         self._extract_address),
            ("description",     self._extract_description),
            ("rating",          self._extract_rating),
            ("total_reviews",   self._extract_total_reviews),
            ("rating_category", self._extract_rating_category),
            ("review_scores",   self._extract_review_scores),
            ("services",        self._extract_services),
            ("facilities",      self._extract_facilities),
            ("house_rules",     self._extract_house_rules),
            ("important_info",  self._extract_important_info),
            ("rooms",           self._extract_rooms),
            ("images_urls",     self._extract_images),
        ]
        for field, fn in extractors:
            try:
                self._result[field] = fn()
            except Exception as exc:                # pragma: no cover
                logger.debug(f"[extractor] field='{field}' lang='{self._lang}' error={exc}")
                self._result[field] = None

        return self._result

    # ──────────────────────────────────────────────────────────────────────
    # Field extractors
    # ──────────────────────────────────────────────────────────────────────

    def _extract_name(self) -> Optional[str]:
        """Hotel name — multiple CSS / attribute strategies."""
        # Strategy 1: data-testid (stable across Booking.com redesigns)
        tag = self._soup.find(attrs={"data-testid": "property-name"})
        if tag:
            return self._clean_text(tag.get_text())

        # Strategy 2: h2 inside hotel page header
        tag = self._soup.select_one("#wrap-hotelpage-top h2")
        if tag:
            return self._clean_text(tag.get_text())

        # Strategy 3: OG meta title (always present, strip " - Booking.com" suffix)
        meta = self._soup.find("meta", property="og:title")
        if meta and meta.get("content"):
            name = meta["content"].split(" - ")[0].strip()
            return name or None

        # Strategy 4: <title> tag
        title_tag = self._soup.find("title")
        if title_tag:
            text = title_tag.get_text()
            name = text.split("|")[0].split("–")[0].split("-")[0].strip()
            return name or None

        return None

    def _extract_address(self) -> Optional[str]:
        """Full property address."""
        tag = self._soup.find(attrs={"data-testid": "property-address"})
        if tag:
            return self._clean_text(tag.get_text())

        tag = self._soup.select_one("span[data-node_tt_id='address']")
        if tag:
            return self._clean_text(tag.get_text())

        tag = self._soup.select_one("#wrap-hotelpage-top span.hp_address_subtitle")
        if tag:
            return self._clean_text(tag.get_text())

        return None

    def _extract_description(self) -> Optional[str]:
        """Property description (up to 5,000 chars)."""
        tag = self._soup.find("p", attrs={"data-testid": "property-description"})
        if tag:
            return self._clean_text(tag.get_text())[:5000]

        tag = self._soup.select_one("#property_description_content")
        if tag:
            return self._clean_text(tag.get_text())[:5000]

        tag = self._soup.select_one("div#summary > div.hotel_description_wrapper_exp")
        if tag:
            return self._clean_text(tag.get_text())[:5000]

        return None

    def _extract_rating(self) -> Optional[float]:
        """Overall review score (float, 0–10)."""
        # data-testid review score badge
        tag = self._soup.find(attrs={"data-testid": "review-score-badge"})
        if tag:
            return self._parse_float(tag.get_text())

        # aria-label on score component
        tag = self._soup.find(attrs={"data-testid": "review-score-component"})
        if tag:
            badge = tag.find(class_=re.compile(r"review-score|score", re.I))
            if badge:
                return self._parse_float(badge.get_text())

        # Microdata / JSON-LD fallback
        return self._extract_rating_from_jsonld()

    def _extract_total_reviews(self) -> Optional[int]:
        """Total number of reviews."""
        tag = self._soup.find(attrs={"data-testid": "review-score-component"})
        if tag:
            # look for "1,234 reviews" or "1.234 Bewertungen"
            text = tag.get_text(" ", strip=True)
            m = re.search(r"([\d,.\s]+)\s+\w+", text)
            if m:
                return self._parse_int(m.group(1))

        # Microdata
        meta = self._soup.find("meta", itemprop="reviewCount")
        if meta and meta.get("content"):
            return self._parse_int(meta["content"])

        return None

    def _extract_rating_category(self) -> Optional[str]:
        """Rating category label (e.g. 'Superb', 'Muy Bien')."""
        tag = self._soup.find(attrs={"data-testid": "review-score-component"})
        if tag:
            words = tag.get_text(" ", strip=True).lower()
            labels = _RATING_LABELS.get(self._lang, _RATING_LABELS["en"])
            for key, label in labels.items():
                if key in words:
                    return label

        return None

    def _extract_review_scores(self) -> Optional[Dict[str, float]]:
        """Per-category review subscores dict."""
        scores: Dict[str, float] = {}

        # ReviewSubscoresDesktop — most reliable selector
        container = self._soup.find(attrs={"data-testid": "ReviewSubscoresDesktop"})
        if container:
            # sibling div contains the actual score items
            sib = container.find_next_sibling("div")
            target = sib if sib else container

            for item in target.find_all(["div", "li"]):
                text = item.get_text(" ", strip=True)
                m = re.search(r"(.+?)\s+([\d]+[.,][\d]+)", text)
                if m:
                    key   = self._clean_text(m.group(1)).lower()
                    value = self._parse_float(m.group(2))
                    if key and value and len(key) < 50:
                        scores[key] = value

        return scores if scores else None

    def _extract_services(self) -> Optional[List[str]]:
        """List of property amenities / services."""
        services: List[str] = []

        # Most reliable: amenity list items
        for tag in self._soup.select(
            "div[data-testid='property-most-popular-facilities-wrapper'] "
            "span.bui-list__description"
        ):
            text = self._clean_text(tag.get_text())
            if text and len(text) < 100:
                services.append(text)

        if not services:
            for tag in self._soup.select("div.important_facility, span.hp_desc_important_facilities"):
                text = self._clean_text(tag.get_text())
                if text and len(text) < 100:
                    services.append(text)

        return list(dict.fromkeys(services)) if services else None  # preserve order, dedupe

    def _extract_facilities(self) -> Optional[Dict[str, List[str]]]:
        """Grouped facilities dict {category: [item, ...]}."""
        facilities: Dict[str, List[str]] = {}

        facility_box = self._soup.find(id="hp_facilities_box")
        if not facility_box:
            facility_box = self._soup.select_one("div[data-section-id='facilities']")
        if not facility_box:
            return None

        # Each category is a block with a header + list of items
        for block in facility_box.select("div.facilitiesChecklistSection"):
            header = block.select_one("h5, h4, .facilities-block--header")
            if not header:
                continue
            cat = self._clean_text(header.get_text())
            items = [
                self._clean_text(li.get_text())
                for li in block.select("li, .bui-list__item")
                if self._clean_text(li.get_text())
            ]
            if cat and items:
                facilities[cat] = items

        return facilities if facilities else None

    def _extract_house_rules(self) -> Optional[str]:
        """House rules section as plain text."""
        tag = self._soup.find(id="policies")
        if tag:
            return self._clean_text(tag.get_text())[:3000]

        tag = self._soup.find(id="policymain")
        if tag:
            return self._clean_text(tag.get_text())[:3000]

        return None

    def _extract_important_info(self) -> Optional[str]:
        """Important information section as plain text."""
        tag = self._soup.find(id="important_info")
        if tag:
            return self._clean_text(tag.get_text())[:3000]

        tag = self._soup.find(attrs={"data-testid": "important-information"})
        if tag:
            return self._clean_text(tag.get_text())[:3000]

        return None

    def _extract_rooms(self) -> Optional[List[Dict[str, str]]]:
        """List of room type dicts {name, description}."""
        rooms: List[Dict[str, str]] = []

        room_area = self._soup.find(id="maxotelRoomArea")
        if not room_area:
            room_area = self._soup.select_one("div[data-testid='rooms-section']")
        if not room_area:
            return None

        for row in room_area.select("tr.js-rt-block-row, div.roomInfo-desktop, div[data-testid='room-card']"):
            name_tag = row.select_one("span.hprt-roomtype-icon-link, h4[data-testid='room-name'], .room-card__name")
            desc_tag = row.select_one("div.hprt-facilities-facility, div[data-testid='room-description']")
            name = self._clean_text(name_tag.get_text()) if name_tag else None
            desc = self._clean_text(desc_tag.get_text()) if desc_tag else None
            if name:
                rooms.append({"name": name, "description": desc or ""})

        return rooms if rooms else None

    def _extract_images(self) -> Optional[List[str]]:
        """
        All hotel image URLs.

        Extraction order:
        1. Gallery modal images (data-testid='gallery-image')
        2. Main page photo grid
        3. OG image (single fallback)

        No artificial cap — all available URLs returned.
        """
        urls: List[str] = []

        # Strategy 1: gallery images (available after modal is opened by Selenium)
        for img in self._soup.select("img[data-testid='gallery-image']"):
            src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
            if src and src.startswith("http"):
                urls.append(self._normalise_image_url(src))

        # Strategy 2: main page photo strip
        if not urls:
            for img in self._soup.select(
                "div.hp-gallery-redesign img, "
                "div[data-testid='hp-gallery'] img, "
                "a.bh-photo-grid-item img"
            ):
                src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
                if src and src.startswith("http"):
                    urls.append(self._normalise_image_url(src))

        # Strategy 3: all page images with booking CDN domain
        if not urls:
            for img in self._soup.find_all("img"):
                src = img.get("src") or img.get("data-src") or ""
                if "bstatic.com" in src or "cf.bstatic.com" in src:
                    urls.append(self._normalise_image_url(src))

        # Strategy 4: OG image single fallback
        if not urls:
            og = self._soup.find("meta", property="og:image")
            if og and og.get("content"):
                urls.append(og["content"])

        # Deduplicate preserving order
        seen: set = set()
        unique: List[str] = []
        for u in urls:
            if u not in seen:
                seen.add(u)
                unique.append(u)

        return unique if unique else None

    # ──────────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────────

    @staticmethod
    def _clean_text(text: Optional[str]) -> str:
        """Strip whitespace and collapse internal runs."""
        if not text:
            return ""
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _parse_float(text: Optional[str]) -> Optional[float]:
        """Parse '8,5' or '8.5' → 8.5. Returns None on failure."""
        if not text:
            return None
        cleaned = re.sub(r"[^\d.,]", "", text).replace(",", ".")
        try:
            return float(cleaned)
        except ValueError:
            return None

    @staticmethod
    def _parse_int(text: Optional[str]) -> Optional[int]:
        """Parse '1,234' or '1.234' → 1234. Returns None on failure."""
        if not text:
            return None
        cleaned = re.sub(r"[^\d]", "", text)
        try:
            return int(cleaned)
        except ValueError:
            return None

    @staticmethod
    def _normalise_image_url(url: str) -> str:
        """
        Upgrade Booking.com image URLs to full resolution.

        Booking.com CDN serves thumbnails via max80/max300 path segments.
        Replacing these with 'max1024x768' returns a much larger image
        without an additional HTTP request.
        """
        url = re.sub(r"/max\d+x\d+/", "/max1024x768/", url)
        url = re.sub(r"/max\d+/", "/max1024x768/", url)
        return url

    def _extract_rating_from_jsonld(self) -> Optional[float]:
        """Fallback: extract rating from JSON-LD structured data."""
        import json
        for script in self._soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "")
                if isinstance(data, dict):
                    agg = data.get("aggregateRating") or {}
                    value = agg.get("ratingValue")
                    if value:
                        return self._parse_float(str(value))
            except (json.JSONDecodeError, AttributeError):
                continue
        return None
