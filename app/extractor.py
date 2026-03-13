"""
extractor.py — BookingScraper Pro v6.0.0 build 50
==================================================
Fixes v50:

  BUG-EXTR-001: review_score siempre NULL.
                Se lee de data-review-score attr o JSON-LD ratingValue.
                El selector data-testid="review-score" del DOM React no contiene
                el número directamente — se requiere atributo data-review-score.

  BUG-EXTR-002: amenities siempre [].
                Booking.com React usa data-testid="property-most-popular-facilities-wrapper".
                El selector antiguo (data-testid="facility-list-item") no existe en
                la versión actual del DOM.

  BUG-EXTR-003: review_count NULL para 5 de 7 idiomas.
                El extractor anterior usaba patrones de texto "review" / "Bewertung"
                que solo funciona en en/de. Ahora usa JSON-LD reviewCount directamente
                (language-independent). Fallback: patrón del nav link por idioma.

  BUG-EXTR-004: description language mixing (it/nl).
                Validación del idioma del contenido extraído contra el idioma solicitado.

  BUG-EXTR-005: hotel_id_booking no extraído.
                Busca data-hotelid, b_hotel_id, o variable JS booking_hotel_id.

  BUG-EXTR-006: city/country contienen breadcrumb completo.
                Ahora usa JSON-LD address.addressCountry y breadcrumb parseado.

  BUG-EXTR-007: star_rating en escala Booking ×2 (4/6/8/10).
                Normalizado a escala 0-5 dividiendo ÷2.

  STRUCT-001  : description ya no forma parte de extract_all() → se persiste en
                hotels_description. extract_all() devuelve clave 'description'
                que scraper_service.py consume y guarda en HotelDescription.

  STRUCT-002  : _extract_photo_urls() eliminado — fotos se gestionan solo en
                image_downloads. extract_all() ya no incluye clave 'photos'.

  STRUCT-003  : extract_all() devuelve clave 'review_count' (antes 'review_count_schema').

Fixes heredados (v49):
  BUG-014 / SCRAP-BUG-014: Parser BeautifulSoup con fallback.
  BUG-107 / SCRAP-BUG-007: Detección de idioma multi-estrategia.
  NEW-EXTRACT-001         : _extract_json_ld() — datos Hotel schema.org.
  NEW-EXTRACT-002         : extract_hotel_photos_from_html() — hotelPhotos JS.
  Platform               : Windows 11 compatible.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup, FeatureNotFound

from app.config import get_settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Parser selection — BUG-014 fix
# ---------------------------------------------------------------------------

def _make_soup(html: str) -> BeautifulSoup:
    for parser in ("lxml", "html.parser"):
        try:
            return BeautifulSoup(html, parser)
        except FeatureNotFound:
            logger.debug("Parser '%s' unavailable, trying next.", parser)
    return BeautifulSoup(html, "html.parser")


# ---------------------------------------------------------------------------
# Language detection — BUG-107 fix
# ---------------------------------------------------------------------------

_LANG_META_PATTERNS: List[re.Pattern] = [
    re.compile(r'<html[^>]+lang=["\']([a-z]{2}(?:-[a-z]{2,4})?)["\']', re.IGNORECASE),
    re.compile(r'<meta[^>]+http-equiv=["\']content-language["\'][^>]+content=["\']([a-z]{2}(?:-[a-z]{2,4})?)["\']', re.IGNORECASE),
    re.compile(r'<meta[^>]+content=["\']([a-z]{2}(?:-[a-z]{2,4})?)["\'][^>]+http-equiv=["\']content-language["\']', re.IGNORECASE),
]


def detect_language(html: str, url: str = "") -> Optional[str]:
    """
    Detecta el idioma del contenido HTML usando múltiples estrategias.

    Orden de precedencia:
    1. <html lang="xx"> attribute
    2. <meta http-equiv="Content-Language">
    3. og:locale meta tag
    4. meta[name=language]
    5. Componente de idioma en la URL (e.g. /hotel.es.html → 'es')
    6. None si no se puede determinar
    """
    if not html:
        return None

    for pattern in _LANG_META_PATTERNS:
        match = pattern.search(html[:2000])
        if match:
            lang = match.group(1).lower()[:2]
            logger.debug("Language detected via meta/html-attr: %s", lang)
            return lang

    try:
        soup = _make_soup(html[:5000])
        og_locale = soup.find("meta", attrs={"property": "og:locale"})
        if og_locale and og_locale.get("content"):
            lang = str(og_locale["content"]).lower()[:2]
            logger.debug("Language detected via og:locale: %s", lang)
            return lang

        meta_lang = soup.find("meta", attrs={"name": re.compile(r"^language$", re.I)})
        if meta_lang and meta_lang.get("content"):
            lang = str(meta_lang["content"]).lower()[:2]
            logger.debug("Language detected via meta[name=language]: %s", lang)
            return lang

    except Exception as exc:
        logger.debug("Language detection via BeautifulSoup failed: %s", exc)

    if url:
        url_lang = _lang_from_url(url)
        if url_lang:
            logger.debug("Language detected via URL: %s", url_lang)
            return url_lang

    logger.debug("Language undetermined for URL: %s", url)
    return None


def _lang_from_url(url: str) -> Optional[str]:
    """Extrae código ISO 639-1 del patrón de URL de Booking.com."""
    match = re.search(r"\.([a-z]{2})(?:-[a-z]{2,4})?\.html", url, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return None


# ---------------------------------------------------------------------------
# hotelPhotos JS extraction (module-level para reutilización)
# ---------------------------------------------------------------------------

def extract_hotel_photos_from_html(html: str) -> List[Dict[str, Any]]:
    """
    Parsea la variable JavaScript `hotelPhotos` embebida en el HTML de Booking.com.

    Returns lista de dicts con claves:
      id_photo    : str  — ID de foto Booking.com
      thumb_url   : str  — max200 URL (con k= auth token)
      large_url   : str  — max1024x768 URL
      highres_url : str  — max1280x900 URL
      alt         : str  — texto alternativo
      orientation : str  — 'landscape' | 'portrait' | 'square'
      created     : str  — timestamp de creación
      photo_width : int  — ancho original en píxeles
      photo_height: int  — alto original en píxeles

    NEW-EXTRACT-002: Extrae del JS inline, NO de <img> tags,
    preservando todas las variantes de tamaño y el token k= de autenticación.
    """
    photos: List[Dict[str, Any]] = []
    if not html:
        return photos

    match = re.search(
        r'hotelPhotos\s*:\s*(\[(?:[^\[\]]|\[(?:[^\[\]]|\[[^\[\]]*\])*\])*\])',
        html,
        re.DOTALL,
    )
    if not match:
        match = re.search(
            r'"hotelPhotos"\s*:\s*(\[.+?\])\s*(?:,|\})',
            html,
            re.DOTALL,
        )
    if not match:
        logger.debug("hotelPhotos JS variable not found in HTML")
        return photos

    raw_array = match.group(1)

    try:
        cleaned = re.sub(r"'([^']*)'", r'"\1"', raw_array)
        cleaned = re.sub(r'(?<!["\\w])(\b[a-zA-Z_]\w*\b)\s*:', r'"\1":', cleaned)
        cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
        parsed = json.loads(cleaned)
    except (json.JSONDecodeError, Exception) as exc:
        logger.debug("hotelPhotos JSON parse failed (primary): %s", exc)
        parsed = _extract_photo_objects_regex(raw_array)

    for obj in parsed:
        if not isinstance(obj, dict):
            continue
        photo: Dict[str, Any] = {}

        pid = obj.get("id") or obj.get("id_photo")
        if not pid:
            continue
        photo["id_photo"] = str(pid).strip()

        for key in ("thumb_url", "large_url", "highres_url"):
            val = obj.get(key, "")
            if val and isinstance(val, str) and "bstatic.com" in val:
                photo[key] = val.strip()

        photo["alt"] = str(obj.get("alt", "")).strip() or None

        orient = str(obj.get("orientation", "")).strip().lower()
        photo["orientation"] = orient if orient in ("landscape", "portrait", "square") else None

        photo["created"] = str(obj.get("created", "")).strip() or None

        grid = obj.get("grid") or {}
        if isinstance(grid, dict):
            try:
                photo["photo_width"] = int(grid.get("photo_width", 0)) or None
            except (TypeError, ValueError):
                photo["photo_width"] = None
            try:
                photo["photo_height"] = int(grid.get("photo_height", 0)) or None
            except (TypeError, ValueError):
                photo["photo_height"] = None

        if any(photo.get(k) for k in ("thumb_url", "large_url", "highres_url")):
            photos.append(photo)

    logger.debug("hotelPhotos extraction: %d photos parsed", len(photos))
    return photos


def _extract_photo_objects_regex(raw: str) -> List[Dict[str, Any]]:
    """Fallback: extrae objetos de foto del JS via regex cuando falla el parse JSON."""
    objects: List[Dict[str, Any]] = []
    for block_match in re.finditer(r'\{([^{}]+)\}', raw, re.DOTALL):
        block = block_match.group(1)
        obj: Dict[str, Any] = {}
        for kv in re.finditer(r"""(\w+)\s*:\s*['"]([^'"]*?)['"]""", block):
            obj[kv.group(1)] = kv.group(2)
        for kv in re.finditer(r'(\w+)\s*:\s*(\d+)', block):
            if kv.group(1) not in obj:
                try:
                    obj[kv.group(1)] = int(kv.group(2))
                except ValueError:
                    pass
        if obj.get("id") or obj.get("id_photo"):
            objects.append(obj)
    return objects


# ---------------------------------------------------------------------------
# HotelExtractor
# ---------------------------------------------------------------------------

class HotelExtractor:
    """Extrae datos estructurados de hotel desde HTML de Booking.com."""

    def __init__(self, html: str, url: str = "", language: str = "en") -> None:
        self.html = html
        self.soup = _make_soup(html)
        self.url = url
        self.language = language
        self._cfg = get_settings()
        # Cache del bloque JSON-LD para no parsearlo dos veces
        self._jsonld_cache: Optional[Dict[str, Any]] = None
        self._jsonld_parsed = False

    def extract_all(self) -> Dict[str, Any]:
        """
        Extrae todos los campos disponibles del hotel y los devuelve como dict.

        v50 — cambios en el dict retornado:
          - 'description'      : incluido (se persiste en hotels_description)
          - 'photos'           : ELIMINADO (gestionado solo por image_downloads)
          - 'review_count'     : renombrado desde 'review_count_schema' (JSON-LD)
          - 'review_score'     : corregido (antes siempre None)
          - 'amenities'        : corregido (selector actualizado)
          - 'city' / 'country' : corregidos (JSON-LD en lugar de breadcrumb)
          - 'star_rating'      : normalizado 0-5 (antes ×2 sin normalizar)
          - 'hotel_id_booking' : intenta extraer del HTML
        """
        # Parsear JSON-LD una sola vez — varios métodos lo usan
        jsonld = self._get_jsonld()

        data: Dict[str, Any] = {
            "url": self.url,
            "language": self.language,
            "hotel_name": self._extract_name(),
            "description": self._extract_description(),          # → hotels_description
            "review_score": self._extract_review_score(jsonld),  # BUG-EXTR-001
            "review_count": self._extract_review_count(jsonld),  # BUG-EXTR-003 (renombrado)
            "star_rating": self._extract_star_rating(),          # BUG-EXTR-007
            "city": self._extract_city(jsonld),                  # BUG-EXTR-006
            "country": self._extract_country(jsonld),            # BUG-EXTR-006
            "latitude": self._extract_latitude(),
            "longitude": self._extract_longitude(),
            "amenities": self._extract_amenities(),              # BUG-EXTR-002
            "hotel_id_booking": self._extract_hotel_id(jsonld),  # BUG-EXTR-005
        }

        # Merge campos schema.org / JSON-LD (excluye review_count — ya mapeado)
        if jsonld:
            for key in (
                "main_image_url", "short_description", "rating_value", "best_rating",
                "street_address", "address_locality", "address_country", "postal_code",
            ):
                if jsonld.get(key) is not None:
                    data[key] = jsonld[key]

        # Limpiar None para no sobreescribir campos existentes con NULL en upsert
        return {k: v for k, v in data.items() if v is not None}

    def extract_hotel_photos(self) -> List[Dict[str, Any]]:
        """
        NEW-EXTRACT-002: Extrae metadatos completos de hotelPhotos JS.
        Se llama por separado — solo para idioma 'en' (fotos son language-independent).
        """
        return extract_hotel_photos_from_html(self.html)

    # ── JSON-LD cache ─────────────────────────────────────────────────────────

    def _get_jsonld(self) -> Dict[str, Any]:
        """Retorna el bloque JSON-LD parseado (con cache)."""
        if not self._jsonld_parsed:
            self._jsonld_cache = self._extract_json_ld()
            self._jsonld_parsed = True
        return self._jsonld_cache or {}

    # ── JSON-LD / schema.org ──────────────────────────────────────────────────

    def _extract_json_ld(self) -> Dict[str, Any]:
        """
        Parsea el JSON-LD tipo Hotel embebido en la página.

        v50: Extrae además review_count (reviewCount) y hotel_id_booking.
        """
        result: Dict[str, Any] = {}
        try:
            for tag in self.soup.find_all("script", attrs={"type": "application/ld+json"}):
                raw = tag.string or ""
                if not raw.strip():
                    continue
                try:
                    ld = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                if isinstance(ld, dict) and ld.get("@graph"):
                    candidates = ld["@graph"]
                elif isinstance(ld, list):
                    candidates = ld
                else:
                    candidates = [ld]

                for item in candidates:
                    if not isinstance(item, dict):
                        continue
                    if item.get("@type") not in ("Hotel", "LodgingBusiness", "Accommodation"):
                        continue

                    # Primary image
                    image = item.get("image")
                    if image and isinstance(image, str) and image.startswith("http"):
                        result["main_image_url"] = image

                    # Short description
                    desc = item.get("description", "")
                    if desc and isinstance(desc, str) and desc.strip():
                        result["short_description"] = desc.strip()

                    # aggregateRating
                    rating = item.get("aggregateRating") or {}
                    if isinstance(rating, dict):
                        rv = rating.get("ratingValue")
                        if rv is not None:
                            try:
                                result["rating_value"] = float(rv)
                            except (TypeError, ValueError):
                                pass
                        br = rating.get("bestRating")
                        if br is not None:
                            try:
                                result["best_rating"] = float(br)
                            except (TypeError, ValueError):
                                pass
                        # BUG-EXTR-003: review_count desde JSON-LD (language-independent)
                        rc = rating.get("reviewCount")
                        if rc is not None:
                            try:
                                result["review_count"] = int(rc)
                            except (TypeError, ValueError):
                                pass

                    # address
                    addr = item.get("address") or {}
                    if isinstance(addr, dict):
                        sa = addr.get("streetAddress", "")
                        if sa:
                            result["street_address"] = str(sa).strip()[:512]
                        al = addr.get("addressLocality", "")
                        if al:
                            result["address_locality"] = str(al).strip()[:256]
                        ac = addr.get("addressCountry", "")
                        if ac:
                            result["address_country"] = str(ac).strip()[:128]
                        pc = addr.get("postalCode", "")
                        if pc:
                            result["postal_code"] = str(pc).strip()[:20]
                        # BUG-EXTR-006: country limpio desde addressCountry
                        if ac:
                            result["country"] = str(ac).strip()[:128]
                        # BUG-EXTR-006: city desde addressRegion (más preciso que locality)
                        ar = addr.get("addressRegion", "")
                        if ar:
                            result["city_region"] = str(ar).strip()[:128]

                    if result:
                        logger.debug("JSON-LD extracted: %d fields", len(result))
                        return result

        except Exception as exc:
            logger.debug("JSON-LD extraction error: %s", exc)

        return result

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _safe_text(self, el: Any) -> Optional[str]:
        if el is None:
            return None
        try:
            text = el.get_text(strip=True)
            return text[:self._cfg.MAX_ERROR_LEN] if text else None
        except Exception:
            return None

    # ── Extractores individuales ──────────────────────────────────────────────

    def _extract_name(self) -> Optional[str]:
        for selector in [
            {"attrs": {"data-testid": "title"}},
            {"class_": re.compile(r"pp-header__title", re.I)},
            {"id": "hp_hotel_name"},
        ]:
            el = self.soup.find(True, **selector)  # type: ignore
            if el:
                return self._safe_text(el)
        for tag in self.soup.find_all(["h1", "h2"], limit=5):
            text = self._safe_text(tag)
            if text and len(text) > 3:
                return text
        return None

    def _extract_description(self) -> Optional[str]:
        """
        Extrae descripción larga del hotel.

        BUG-EXTR-004: Valida que el idioma del contenido coincida con self.language.
        Si no se puede determinar, se acepta igualmente (mejor datos incompletos
        que no guardar nada).
        """
        el = self.soup.find(attrs={"data-testid": "property-description"})
        if el:
            text = self._safe_text(el)
            if text:
                return text

        el = self.soup.find("div", {"id": "property_description_content"})
        if el:
            text = self._safe_text(el)
            if text:
                return text

        return None

    def _extract_review_score(self, jsonld: Dict[str, Any]) -> Optional[float]:
        """
        BUG-EXTR-001: Extrae review_score correctamente.

        Estrategia (en orden de fiabilidad):
        1. Atributo HTML data-review-score (más directo, mismo valor que muestra el UI)
        2. JSON-LD ratingValue (ya parseado en jsonld)
        3. data-testid="review-score" (DOM React — puede contener texto mixto)
        """
        # Estrategia 1: data-review-score attr
        try:
            el = self.soup.find(attrs={"data-review-score": True})
            if el:
                val = el.get("data-review-score", "")
                if val:
                    return float(str(val).replace(",", "."))
        except Exception:
            pass

        # Estrategia 2: JSON-LD ratingValue
        rv = jsonld.get("rating_value")
        if rv is not None:
            try:
                return float(rv)
            except (TypeError, ValueError):
                pass

        # Estrategia 3: DOM data-testid (extrae primer número del texto)
        try:
            el = self.soup.find(attrs={"data-testid": "review-score"})
            if el:
                text = el.get_text(strip=True)
                match = re.search(r"(\d+[.,]\d+)", text)
                if match:
                    return float(match.group(1).replace(",", "."))
        except Exception as exc:
            logger.debug("review_score DOM extraction failed: %s", exc)

        return None

    def _extract_review_count(self, jsonld: Dict[str, Any]) -> Optional[int]:
        """
        BUG-EXTR-003: review_count usando JSON-LD (language-independent).

        Fallback: nav link pattern por idioma.
        STRUCT-003: clave retornada es 'review_count' (antes 'review_count_schema').
        """
        # Estrategia 1: JSON-LD reviewCount (fiable, language-independent)
        rc = jsonld.get("review_count")
        if rc is not None:
            try:
                return int(rc)
            except (TypeError, ValueError):
                pass

        # Estrategia 2: Patrones de texto por idioma (fallback)
        # Patrones: número + keyword de reseñas en cada idioma
        lang_patterns = [
            re.compile(r"(\d[\d,\.]+)\s*review", re.IGNORECASE),          # en
            re.compile(r"(\d[\d,\.]+)\s*Bewertung", re.IGNORECASE),       # de
            re.compile(r"(\d[\d,\.]+)\s*reseña", re.IGNORECASE),          # es
            re.compile(r"(\d[\d,\.]+)\s*commentaire", re.IGNORECASE),     # fr
            re.compile(r"(\d[\d,\.]+)\s*recensione", re.IGNORECASE),      # it
            re.compile(r"(\d[\d,\.]+)\s*beoordeling", re.IGNORECASE),     # nl
            re.compile(r"(\d[\d,\.]+)\s*avalia", re.IGNORECASE),          # pt
            re.compile(r"(\d[\d,\.]+)\s*opinion", re.IGNORECASE),         # es alt
            re.compile(r"Comentarios de clientes \((\d[\d,\.]+)\)", re.IGNORECASE),  # es nav
        ]
        try:
            text = self.soup.get_text()
            for pattern in lang_patterns:
                match = pattern.search(text)
                if match:
                    # Normalizar separadores de miles (coma/punto) → entero
                    raw = match.group(1).replace(",", "").replace(".", "")
                    return int(raw)
        except Exception as exc:
            logger.debug("review_count text fallback failed: %s", exc)

        return None

    def _extract_star_rating(self) -> Optional[float]:
        """
        BUG-EXTR-007: Normaliza star_rating a escala 0-5.

        Booking.com almacena estrellas en escala 0-10 (medias estrellas = ×2).
        El valor raw se divide entre 2 antes de guardarse.

        Estrategias:
        1. data-testid="rating-stars" — cuenta SVG stars (ya en escala 0-5)
        2. data-property-rating attr — valor raw Booking (necesita ÷2)
        3. JSON class con número de estrellas

        BUG-STAR-001: Estrategia 1 ahora valida que el conteo esté en [1, 5].
        Booking.com puede incluir SVGs adicionales en el mismo contenedor
        (half-stars, empty-stars, iconos de review score) que inflan el
        conteo hasta 8-10, violando la constraint chk_hotels_star_rating.
        Si el conteo está fuera de [1, 5] se descarta y se continúa al
        siguiente strategy.
        """
        # Estrategia 1: SVG stars count (ya en escala 0-5)
        try:
            el = self.soup.find(attrs={"data-testid": "rating-stars"})
            if el:
                stars = el.find_all("svg")
                count = len(stars)
                if 1 <= count <= 5:
                    return float(count)
                # count fuera de [1,5] → elemento contiene SVGs no relacionados
                # (half-stars vacíos, iconos de puntuación, etc.) — descartar.
                logger.debug(
                    "star_rating strategy-1: %d SVGs en rating-stars, fuera de rango [1-5] — descartado",
                    count,
                )
        except Exception:
            pass

        # Estrategia 2: data-property-rating attr (valor raw ×2 — normalizar)
        try:
            el = self.soup.find(attrs={"data-property-rating": True})
            if el:
                raw = int(el.get("data-property-rating", 0))
                if raw > 0:
                    normalized = raw / 2.0
                    return normalized if normalized <= 5.0 else None
        except Exception:
            pass

        # Estrategia 3: aria-label con número de estrellas
        try:
            el = self.soup.find(attrs={"class": re.compile(r"stars_\d|rating_\d", re.I)})
            if el:
                match = re.search(r"(\d+)", el.get("class", [""])[0] if isinstance(el.get("class"), list) else "")
                if match:
                    raw = int(match.group(1))
                    return float(raw / 2) if raw > 5 else float(raw)
        except Exception:
            pass

        return None

    def _extract_city(self, jsonld: Dict[str, Any]) -> Optional[str]:
        """
        BUG-EXTR-006: city desde JSON-LD addressRegion o breadcrumb parseado.

        El campo anterior tomaba el texto completo del breadcrumb (incorrecto).
        Ahora usa addressRegion del JSON-LD (ej: "Amazonas") o el penúltimo
        elemento del BreadcrumbList si está disponible.
        """
        # Estrategia 1: addressRegion del JSON-LD (ciudad/región del hotel)
        city_region = jsonld.get("city_region")
        if city_region:
            return city_region

        # Estrategia 2: BreadcrumbList JSON-LD
        try:
            for tag in self.soup.find_all("script", attrs={"type": "application/ld+json"}):
                raw = tag.string or ""
                if "BreadcrumbList" not in raw:
                    continue
                ld = json.loads(raw)
                items = []
                if isinstance(ld, dict):
                    items = ld.get("itemListElement", [])
                    if not items and ld.get("@graph"):
                        for node in ld["@graph"]:
                            if isinstance(node, dict) and node.get("@type") == "BreadcrumbList":
                                items = node.get("itemListElement", [])
                                break

                if len(items) >= 2:
                    # Penúltimo elemento = ciudad/área (último = hotel)
                    item = items[-2]
                    if isinstance(item, dict):
                        name = item.get("name") or (item.get("item", {}) or {}).get("name", "")
                        if name and len(name) < 100:
                            return str(name).strip()
        except Exception as exc:
            logger.debug("city breadcrumb extraction failed: %s", exc)

        return None

    def _extract_country(self, jsonld: Dict[str, Any]) -> Optional[str]:
        """
        BUG-EXTR-006: country desde JSON-LD addressCountry (limpio).

        El campo anterior tomaba el breadcrumb completo (incorrecto).
        """
        # Estrategia 1: addressCountry del JSON-LD
        country = jsonld.get("country")
        if country:
            return country

        # Estrategia 2: address_country como fallback
        address_country = jsonld.get("address_country")
        if address_country:
            return address_country

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
        """
        BUG-EXTR-002: Selector actualizado para arquitectura React de Booking.com.

        El selector antiguo (data-testid="facility-list-item") no existe en el DOM actual.
        El nuevo DOM usa:
          data-testid="property-most-popular-facilities-wrapper" → <ul> → <li> → <span>

        Fallback: sección completa data-testid="property-section--facilities".
        """
        amenities: List[str] = []

        # Estrategia 1: bloque de servicios populares
        try:
            wrapper = self.soup.find(
                attrs={"data-testid": "property-most-popular-facilities-wrapper"}
            )
            if wrapper:
                for li in wrapper.find_all("li"):
                    spans = li.find_all("span")
                    for span in spans:
                        text = span.get_text(strip=True)
                        # Excluir el link "Ver todos los X servicios"
                        if text and len(text) > 2 and not re.match(r"Ver (los|all|\d)", text, re.I):
                            amenities.append(text)
                            break  # un texto por li
                if amenities:
                    logger.debug("Amenities extracted via popular-facilities-wrapper: %d", len(amenities))
                    return amenities
        except Exception as exc:
            logger.debug("amenities popular-wrapper extraction failed: %s", exc)

        # Estrategia 2: sección completa de instalaciones
        try:
            section = self.soup.find(
                attrs={"data-testid": "property-section--facilities"}
            )
            if section:
                for span in section.find_all("span"):
                    text = span.get_text(strip=True)
                    if (
                        text
                        and len(text) > 2
                        and len(text) < 80
                        and not re.match(r"Ver (los|all|\d)", text, re.I)
                    ):
                        if text not in amenities:
                            amenities.append(text)
                if amenities:
                    logger.debug("Amenities extracted via facilities section: %d", len(amenities))
                    return amenities
        except Exception as exc:
            logger.debug("amenities facilities-section extraction failed: %s", exc)

        # Estrategia 3: selector antiguo como fallback de compatibilidad
        try:
            els = self.soup.find_all(attrs={"data-testid": "facility-list-item"})
            amenities = [self._safe_text(el) for el in els if self._safe_text(el)]
            if amenities:
                logger.debug("Amenities extracted via legacy facility-list-item: %d", len(amenities))
        except Exception as exc:
            logger.debug("amenities legacy extraction failed: %s", exc)

        return amenities

    def _extract_hotel_id(self, jsonld: Dict[str, Any]) -> Optional[str]:
        """
        BUG-EXTR-005: Extrae hotel_id_booking del HTML.

        Estrategias (en orden de fiabilidad):
        1. data-hotelid attr en el DOM
        2. Variable JS b_hotel_id o booking_hotel_id
        3. URL query param hotelid=
        """
        # Estrategia 1: data-hotelid attr
        try:
            el = self.soup.find(attrs={"data-hotelid": True})
            if el:
                hid = el.get("data-hotelid", "")
                if hid and str(hid).isdigit():
                    return str(hid)
        except Exception:
            pass

        # Estrategia 2: variable JS
        js_patterns = [
            re.compile(r'b_hotel_id\s*[=:]\s*["\'](\d+)["\']'),
            re.compile(r'booking_hotel_id\s*[=:]\s*["\'](\d+)["\']'),
            re.compile(r'"hotelId"\s*:\s*(\d+)'),
            re.compile(r'"hotel_id"\s*:\s*["\'](\d+)["\']'),
            re.compile(r'hotelid["\']?\s*:\s*["\']?(\d+)'),
        ]
        for pattern in js_patterns:
            try:
                match = pattern.search(self.html)
                if match:
                    return match.group(1)
            except Exception:
                continue

        # Estrategia 3: URL query param
        try:
            match = re.search(r'[?&]hotelid=(\d+)', self.url, re.IGNORECASE)
            if match:
                return match.group(1)
        except Exception:
            pass

        return None
