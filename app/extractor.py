"""
BookingScraper Pro v6.0 - HTML Data Extractor
=============================================
Extracts structured hotel data from raw Booking.com HTML.

Corrections Applied (v46):
- BUG-009 : _extract_images() complexity 23 refactored into helper methods.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup, Tag

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class HotelData:
    hotel_name  : Optional[str]         = None
    hotel_id_ext: Optional[str]         = None
    star_rating : Optional[float]       = None
    review_score: Optional[float]       = None
    review_count: Optional[int]         = None
    address     : Optional[str]         = None
    city        : Optional[str]         = None
    country     : Optional[str]         = None
    latitude    : Optional[float]       = None
    longitude   : Optional[float]       = None
    amenities   : list[str]             = field(default_factory=list)
    room_types  : list[dict[str,Any]]   = field(default_factory=list)
    policies    : dict[str, Any]        = field(default_factory=dict)
    photos      : list[str]             = field(default_factory=list)
    raw_data    : dict[str, Any]        = field(default_factory=dict)


# ─────────────────────────────────────────────────────────────────────────────
class HotelExtractor:
    """Extract structured hotel data from a Booking.com HTML page."""

    BASE_URL = "https://www.booking.com"

    def __init__(self, html: str, url: str = "") -> None:
        self._soup = BeautifulSoup(html, "lxml")
        self._url  = url

    # ── Public API ──────────────────────────────────────────────────────────

    def extract(self) -> HotelData:
        """Run all extractors and return a populated HotelData."""
        data = HotelData()
        try:
            data.hotel_name   = self._extract_name()
            data.hotel_id_ext = self._extract_hotel_id()
            data.star_rating  = self._extract_stars()
            data.review_score = self._extract_review_score()
            data.review_count = self._extract_review_count()
            data.address      = self._extract_address()
            data.city, data.country = self._extract_location()
            data.latitude, data.longitude = self._extract_coordinates()
            data.amenities    = self._extract_amenities()
            data.room_types   = self._extract_room_types()
            data.policies     = self._extract_policies()
            data.photos       = self._extract_images()  # BUG-009 refactored
            data.raw_data     = self._extract_raw_meta()
        except Exception as exc:
            logger.error("Extraction error for %s: %s", self._url, exc, exc_info=True)
        return data

    # ── Name / Identity ─────────────────────────────────────────────────────

    def _extract_name(self) -> Optional[str]:
        for sel in ["h2.pp-header__title", "h1.pp-header__title", "[data-testid='property-name']"]:
            el = self._soup.select_one(sel)
            if el:
                return el.get_text(strip=True)
        return None

    def _extract_hotel_id(self) -> Optional[str]:
        # Booking.com embeds hotel ID in various locations
        match = re.search(r"hotel_id=(\d+)", self._url)
        if match:
            return match.group(1)
        el = self._soup.select_one("input[name='hotel_id']")
        if el:
            return el.get("value")
        return None

    # ── Ratings ─────────────────────────────────────────────────────────────

    def _extract_stars(self) -> Optional[float]:
        el = self._soup.select_one("[data-testid='rating-stars'] [aria-label]")
        if el:
            txt = el.get("aria-label", "")
            m = re.search(r"([\d.]+)", txt)
            if m:
                return float(m.group(1))
        return None

    def _extract_review_score(self) -> Optional[float]:
        for sel in [
            "[data-testid='review-score-right-component'] .b5cd09854e",
            ".review-score-badge",
            "[aria-label*='Scored']",
        ]:
            el = self._soup.select_one(sel)
            if el:
                txt = el.get_text(strip=True).replace(",", ".")
                m = re.search(r"[\d.]+", txt)
                if m:
                    return float(m.group(0))
        return None

    def _extract_review_count(self) -> Optional[int]:
        el = self._soup.select_one("[data-testid='review-score-right-component'] .b193604e51")
        if el:
            txt = el.get_text(strip=True)
            m = re.search(r"[\d,]+", txt)
            if m:
                return int(m.group(0).replace(",", ""))
        return None

    # ── Location ────────────────────────────────────────────────────────────

    def _extract_address(self) -> Optional[str]:
        el = self._soup.select_one("[data-testid='property-sidebar'] address")
        if el:
            return el.get_text(separator=", ", strip=True)
        return None

    def _extract_location(self) -> tuple[Optional[str], Optional[str]]:
        breadcrumbs = self._soup.select("nav[aria-label='breadcrumb'] li a")
        city = country = None
        if len(breadcrumbs) >= 3:
            city    = breadcrumbs[-2].get_text(strip=True)
            country = breadcrumbs[1].get_text(strip=True)
        return city, country

    def _extract_coordinates(self) -> tuple[Optional[float], Optional[float]]:
        el = self._soup.select_one("#hotel_sidebar_static_map")
        if el:
            try:
                lat = float(el.get("data-lat", 0) or 0)
                lng = float(el.get("data-lng", 0) or 0)
                if lat and lng:
                    return lat, lng
            except (ValueError, TypeError):
                pass
        # Try JSON-LD schema
        for script in self._soup.find_all("script", type="application/ld+json"):
            try:
                import json
                data = json.loads(script.string or "{}")
                geo = data.get("geo", {})
                if geo.get("latitude") and geo.get("longitude"):
                    return float(geo["latitude"]), float(geo["longitude"])
            except (json.JSONDecodeError, ValueError, TypeError):
                pass
        return None, None

    # ── Amenities ───────────────────────────────────────────────────────────

    def _extract_amenities(self) -> list[str]:
        amenities: list[str] = []
        for el in self._soup.select("[data-testid='property-most-popular-facilities-wrapper'] li"):
            txt = el.get_text(strip=True)
            if txt:
                amenities.append(txt)
        if not amenities:
            for el in self._soup.select(".facilitiesChecklistSection li"):
                txt = el.get_text(strip=True)
                if txt:
                    amenities.append(txt)
        return amenities

    # ── Room types ──────────────────────────────────────────────────────────

    def _extract_room_types(self) -> list[dict[str, Any]]:
        rooms: list[dict] = []
        for row in self._soup.select("table#rooms-table tbody tr.js-rt-block"):
            name_el = row.select_one(".hprt-roomtype-icon-link")
            price_el = row.select_one(".hprt-price-price .prco-valign-middle-helper")
            rooms.append({
                "name" : name_el.get_text(strip=True) if name_el else "",
                "price": price_el.get_text(strip=True) if price_el else "",
            })
        return rooms

    # ── Policies ────────────────────────────────────────────────────────────

    def _extract_policies(self) -> dict[str, Any]:
        policies: dict[str, Any] = {}
        checkin_el  = self._soup.select_one(".bui-timeline--check-in  .bui-timeline__bullet-secondary")
        checkout_el = self._soup.select_one(".bui-timeline--check-out .bui-timeline__bullet-secondary")
        if checkin_el:
            policies["checkin"]  = checkin_el.get_text(strip=True)
        if checkout_el:
            policies["checkout"] = checkout_el.get_text(strip=True)
        for item in self._soup.select(".bc-hlbooking-conditions li"):
            policies.setdefault("conditions", []).append(item.get_text(strip=True))
        return policies

    # ── Images (BUG-009 FIX: refactored from complexity 23 into helpers) ────

    def _extract_images(self) -> list[str]:
        """
        BUG-009 FIX: Was a single 51-line function with cyclomatic complexity 23.
        Refactored into four targeted helpers; each handles one source of images.
        """
        seen: set[str] = set()
        photos: list[str] = []

        for url in (
            self._images_from_gallery()
            + self._images_from_thumbnails()
            + self._images_from_og_tags()
            + self._images_from_srcset()
        ):
            clean = self._clean_image_url(url)
            if clean and clean not in seen:
                seen.add(clean)
                photos.append(clean)

        return photos

    def _images_from_gallery(self) -> list[str]:
        urls: list[str] = []
        for el in self._soup.select("[data-testid='property-gallery'] img"):
            src = el.get("src") or el.get("data-src") or ""
            if src:
                urls.append(src)
        return urls

    def _images_from_thumbnails(self) -> list[str]:
        urls: list[str] = []
        for el in self._soup.select(".photo-grid a[href*='max']"):
            href = el.get("href", "")
            if href:
                urls.append(href)
        return urls

    def _images_from_og_tags(self) -> list[str]:
        urls: list[str] = []
        for el in self._soup.find_all("meta", property="og:image"):
            content = el.get("content", "")
            if content:
                urls.append(content)
        return urls

    def _images_from_srcset(self) -> list[str]:
        urls: list[str] = []
        for el in self._soup.select("img[srcset]"):
            srcset = el.get("srcset", "")
            for part in srcset.split(","):
                src = part.strip().split(" ")[0]
                if src and "booking" in src.lower():
                    urls.append(src)
        return urls

    @staticmethod
    def _clean_image_url(url: str) -> Optional[str]:
        """Normalise a raw image URL; return None if not useful."""
        if not url or not isinstance(url, str):
            return None
        url = url.strip()
        if url.startswith("//"):
            url = "https:" + url
        if not url.startswith("http"):
            return None
        # Upgrade to highest available resolution (Booking.com pattern)
        url = re.sub(r"square\d+", "max", url)
        url = re.sub(r"square", "max", url)
        return url if len(url) < 2048 else None

    # ── Raw meta ────────────────────────────────────────────────────────────

    def _extract_raw_meta(self) -> dict[str, Any]:
        meta: dict[str, Any] = {}
        for tag in self._soup.find_all("meta"):
            name = tag.get("name") or tag.get("property", "")
            if name:
                meta[name] = tag.get("content", "")
        return meta
