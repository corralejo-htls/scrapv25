"""
extractor.py — BookingScraper Pro v6.0.0 Build 83
==================================================
Cambios v83 — validados contra HTML real en pruebas/:

  BUG-NEARBY-001-FIX : _extract_nearby_places() reescrito.
    Root cause: el extractor llamaba get_text() en div.d1bc97eb82 que incluye
    el sub-type label ("Restaurant") en un span.f0595bb7c6 hijo, concatenando
    label+nombre. El filtro anterior buscaba parent_span en el div de distancia
    (incorrecto). Fix: localizar div.d1bc97eb82 (nombre), extraer y eliminar
    span.f0595bb7c6 antes de get_text(). Localizar div.cbf0753d0c (distancia).
    Fallback: regex de distancia en el texto restante si div.cbf0753d0c ausente.

  BUG-LEGAL-001-FIX  : _extract_legal() corregido.
    Root cause: el cuerpo de legal_info se extraía de find_next_siblings() sobre
    el elemento h2, pero ese método retornaba el texto ya sin el título. Sin
    embargo en el flujo fallback (párrafos recursivos) el título se incluía en
    el primer párrafo. Fix: usar find_next_siblings() directamente sobre el h2/h4
    del bloque k2-hp--cpc_regulation como fuente primaria del cuerpo.

  BUG-POLICY-001-FIX : _extract_policies() reescrito.
    Root cause: selector 'property-section--policies' no existe en el DOM real.
    La sección real es section#policies (id="policies") > div[data-testid=
    property-section--content] > div.b0400e5749 (row) con hijos div.a776c0ae8b
    (label) y div.c92998be48 (value). Fix: añadir strategy 0 que parsea esta
    estructura de clases verificada. Las strategies 1-3 legacy se conservan.

  BUG-STAR-001-FIX   : _extract_star_rating() corregido.
    Root cause: Strategy 1 contaba todos los SVG dentro del span data-testid=
    "rating-stars" (incluye duplicados React), obteniendo 8-10 en lugar de 1-5.
    Fix: leer el atributo aria-label del span ("X out of 5 stars") y parsear
    el número directamente. Fallback a conteo de SVG solo si aria-label ausente.

Cambios v82:

  GAP-API-001-FIX: _extract_all_services() actualizada.
    Ahora devuelve List[Dict[str, str]] con claves {service, service_category}
    en lugar de List[str].  La categoría se extrae del heading (div/h3) del
    bloque facility-group de Booking.com (Strategy 1.5).  Estrategias que no
    proporcionan contexto de grupo (Apollo JSON, popular-wrapper) usan
    service_category="" para evitar rotura del pipeline.
    scraper_service._upsert_hotel_all_services() actualizado en consecuencia.

  GAP-SCHEMA-003-FIX: _extract_nearby_places() actualizada.
    Añade clave category_code (int | None) a cada dict de lugar.
    El código se obtiene del mapa _NEARBY_CATEGORY_CODE_MAP aplicado al
    valor text ya existente en 'category'.
    Códigos: 1=airport 2=restaurant 3=beach 4=transport 5=nature 6=attraction
    scraper_service._upsert_hotel_nearby_places() actualizado en consecuencia.

Cambios v81:

  GAP-SCHEMA-001-FIX: _extract_individual_reviews() implementada.
    Extrae reseñas textuales individuales de huéspedes desde el DOM de
    Booking.com (data-testid="review-card"). Cada reseña incluye:
    reviewer_name, score, title, positive_comment, negative_comment,
    reviewer_country, booking_id.
    extract_all() ahora incluye la clave 'individual_reviews'.
    Deduplicación por (reviewer_name, title, positive_comment).
    WARNING log cuando review-card existe pero no extrae datos.
    Nota: Booking.com solo renderiza reseñas individuales en el HTML
    estático cuando la página las incluye en el initial DOM — en hoteles
    con pocas reseñas o con paginación JS puede retornar lista vacía.

Cambios v80:

  GAP-SCHEMA-002-FIX: _extract_room_types() actualizado.
    Ahora retorna adults (conteo SVG adultos en columna occupancy),
    children (conteo SVG ninos), images [] e info None en cada dict
    de habitacion para conformar con el payload _API_.md rooms[].
    adults/children son None cuando la pagina se carga sin parametros
    de disponibilidad (tabla de habitaciones no renderizada).

Cambios v78:

  BUILD-SYNC-003: Encabezado sincronizado a Build 78.
                  Sin cambios funcionales en extractor.py para este build.
                  El fix BUG-PERSIST-003 es responsabilidad exclusiva de
                  scraper_service._upsert_hotel_extra_info() — el método
                  estaba definido pero nunca era invocado desde
                  _persist_hotel_data(), dejando hotels_extra_info siempre
                  vacía aunque _extract_extra_info() extrajera datos
                  correctamente.

  NOTA-ROOMS-001: hotels_room_types vacía es ESPERADO cuando las URLs no
                  incluyen parámetros de disponibilidad (?checkin/checkout).
                  Booking.com no renderiza la tabla de habitaciones
                  (data-testid="rt-name-link") sin fechas en la URL.
                  El extractor (_extract_room_types) es correcto — la
                  limitación es arquitectónica: se necesitan fechas reales.

Cambios v60:

  BUILD-SYNC-002: Encabezado sincronizado a build 60.
                  Sin cambios funcionales en extractor.py para este build.
                  El fix BUG-DB-002 es responsabilidad exclusiva de
                  scraper_service._upsert_legal() y models.HotelLegal.

Cambios v59:

  BUG-EXTR-010 : _extract_guest_reviews() corregido — selectores actualizados
                 para coincidir con el DOM actual de Booking.com React.
                 data-testid="review-subscore" es el selector correcto.
                 Puntuación extraída de aria-valuetext del [role="meter"].
                 Categoría extraída del span.d96a4619c0 dentro del subscore.
                 Tabla hotels_guest_reviews ahora se puebla correctamente.

  FIX-LEGAL-003: _extract_legal() reforzado — validación post-extracción para
                 detectar y corregir el caso donde legal == legal_info.
                 Si ambos campos son idénticos, legal_info se limpia a ''.
                 Párrafos recopilados recursivamente (no solo recursive=False)
                 para capturar contenido en DOMs con divs anidados.

Cambios v53:

  STRUCT-013 : _extract_fine_print() nueva — extrae el bloque "Fine Print" /
               "Letra pequeña" de Booking.com como HTML sanitizado.
               Preserva etiquetas <p> para saltos de línea.
               SVG, <img>, <picture>, <source> eliminados completamente.
               Atributos HTML eliminados de todas las etiquetas restantes.
               extract_all() devuelve clave 'fine_print'.

  STRUCT-014 : _extract_all_services() nueva — extrae la lista COMPLETA
               de servicios/instalaciones del hotel desde el bloque de
               instalaciones de Booking.com.
               Una entrada por servicio (texto de cada <li>).
               extract_all() devuelve clave 'all_services'.

  STRUCT-015 : _extract_faqs() nueva — extrae las preguntas frecuentes
               del bloque FAQ de la página del hotel.
               Solo se extrae el texto de la pregunta (campo ask).
               extract_all() devuelve clave 'faqs'.

  STRUCT-016 : _extract_guest_reviews() nueva — extrae las categorías de
               valoración de huéspedes con sus puntuaciones.
               Lista de dicts {reviews_categories, reviews_score}.
               extract_all() devuelve clave 'guest_reviews'.

  STRUCT-017 : _extract_property_highlights() nueva — extrae el bloque
               "Property Highlights" como HTML sanitizado.
               SVG e imágenes eliminados. Atributos HTML eliminados.
               extract_all() devuelve clave 'property_highlights'.

  HELPER     : _sanitize_html_fragment() nuevo — función helper de instancia
               para sanitizar fragmentos HTML (eliminar SVG/img, quitar atributos).
               Usada por _extract_fine_print() y _extract_property_highlights().

Cambios v52:

  STRUCT-005 : _extract_amenities() — ELIMINADA en build 65 (hotels_amenities suprimida).
               (property-section--facilities). El bloque popular-facilities-wrapper
               ahora es fuente exclusiva de _extract_popular_services().
               extract_all() devuelve clave 'amenities' (lista completa normalizada).

  STRUCT-006 : _extract_policies() nueva — parsea el bloque de reglas del alojamiento
               (data-testid="property-section--policies") y devuelve lista de dicts
               {policy_name, policy_details}. extract_all() devuelve clave 'policies'.

  STRUCT-007 : _extract_legal() nueva — parsea el bloque de información legal
               y devuelve dict {legal, legal_info, legal_details}.
               extract_all() devuelve clave 'legal'.

  STRUCT-008 : _extract_popular_services() nueva — extrae el bloque curado
               'Most popular facilities' (property-most-popular-facilities-wrapper).
               (build 65: _extract_amenities() eliminada — popular_services es fuente única.)
               extract_all() devuelve clave 'popular_services'.

Cambios v52:

  STRUCT-011 : extract_all() — clave 'city' RENOMBRADA a 'address_city'.
               Alineación con la convención address_* del modelo Hotel.
               _extract_city() sin cambios internos.

  STRUCT-012 : extract_all() — clave 'country' ELIMINADA.
               hotels.country eliminado (duplicado de address_country).
               _extract_country() eliminado — su lógica era redundante con
               address_country ya presente en el merge JSON-LD de extract_all().
               _extract_json_ld() — asignación result["country"] eliminada.

  FIX-LEGAL-001 : _extract_legal() corregido para detectar el título del
               bloque legal en múltiples idiomas (ES, JA, AR, FR, PT, etc.).
               Raíz del problema: Booking.com a veces emite el título como <p>
               en lugar de <h2>/<h3>/<h4>/<strong>, causando que el título
               se asignara a legal_info y el texto real quedara sin guardar.
               Solución: si no se encuentra heading estándar, se analiza el
               primer <p> contra _LEGAL_TITLE_RE (regex multiidioma). Si
               coincide, se extrae como legal_title y se excluye del cuerpo.

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

        v53 — cambios en el dict retornado:
          - 'fine_print'           : HTML sanitizado del bloque Fine Print (→ hotels_fine_print)
          - 'all_services'         : lista de todos los servicios (→ hotels_all_services)
          - 'faqs'                 : lista de preguntas frecuentes (→ hotels_faqs)
          - 'guest_reviews'        : lista de dicts {reviews_categories, reviews_score}
                                     (→ hotels_guest_reviews)
          - 'property_highlights'  : HTML sanitizado del bloque Property Highlights
                                     (→ hotels_property_highlights)

        v52 — cambios en el dict retornado:
          - 'address_city'     : RENOMBRADO desde 'city' (STRUCT-011)
          - 'country'          : ELIMINADO — usar 'address_country' del merge JSON-LD (STRUCT-012)

        v51 — cambios en el dict retornado:
          - 'popular_services' : bloque curado popular-facilities (→ hotels_popular_services)
          - 'policies'         : lista de dicts {policy_name, policy_details} (→ hotels_policies)
          - 'legal'            : dict {legal, legal_info, legal_details} (→ hotels_legal)

        v50 — cambios en el dict retornado:
          - 'description'      : incluido (se persiste en hotels_description)
          - 'photos'           : ELIMINADO (gestionado solo por image_downloads)
          - 'review_count'     : renombrado desde 'review_count_schema' (JSON-LD)
          - 'review_score'     : corregido (antes siempre None)
          - 'star_rating'      : normalizado 0-5 (antes ×2 sin normalizar)
          - 'hotel_id_booking' : intenta extraer del HTML
        """
        # Parsear JSON-LD una sola vez — varios métodos lo usan
        jsonld = self._get_jsonld()

        data: Dict[str, Any] = {
            "url": self.url,
            "language": self.language,
            "hotel_name": self._extract_name(),
            "description": self._extract_description(),              # → hotels_description
            "review_score": self._extract_review_score(jsonld),      # BUG-EXTR-001
            "review_count": self._extract_review_count(jsonld),      # BUG-EXTR-003
            "star_rating": self._extract_star_rating(),              # BUG-EXTR-007
            # STRUCT-011 (v52): clave renombrada 'city' → 'address_city'
            "address_city": self._extract_city(jsonld),              # BUG-EXTR-006
            # STRUCT-012 (v52): clave 'country' ELIMINADA — address_country viene del merge JSON-LD
            "latitude": self._extract_latitude(),
            "longitude": self._extract_longitude(),
            "popular_services": self._extract_popular_services(),    # STRUCT-008: curated subset
            "policies": self._extract_policies(),                    # STRUCT-006: políticas
            "legal": self._extract_legal(),                          # STRUCT-007: texto legal
            "hotel_id_booking": self._extract_hotel_id(jsonld),      # BUG-EXTR-005
            # STRUCT-013 (v53): Fine Print HTML sanitizado
            "fine_print": self._extract_fine_print(),
            # STRUCT-014 (v53): todos los servicios/instalaciones
            "all_services": self._extract_all_services(),
            # STRUCT-015 (v53): preguntas frecuentes
            "faqs": self._extract_faqs(),
            # STRUCT-016 (v53): categorías de valoración de huéspedes
            "guest_reviews": self._extract_guest_reviews(),
            # STRUCT-017 (v53): Property Highlights HTML sanitizado
            "property_highlights": self._extract_property_highlights(),
            # GAP-EXTRACT-001-FIX: tipo de alojamiento del JSON-LD @type
            "accommodation_type": None,          # populated via JSON-LD merge below
            # STRUCT-018 (Audit-HTML-001): tipos de habitación → hotels.room_types JSONB
            # scraper_service persiste data.get("room_types") — antes siempre NULL
            # porque extractor nunca generaba esta clave.
            "room_types": self._extract_room_types(),
            # STRUCT-019/020 (v76): precio de disponibilidad y cantidad de tipos de habitación
            "price_range":    self._extract_price_range(),
            "rooms_quantity": self._extract_rooms_quantity(),
            # STRUCT-021 (v76): información importante del alojamiento
            "extra_info":     self._extract_extra_info(),
            # STRUCT-022 (v76): lugares cercanos
            "nearby_places":  self._extract_nearby_places(),
            # STRUCT-024 (v76): meta tags SEO
            "seo":            self._extract_seo(),
            # GAP-SCHEMA-001-FIX (v81): reseñas textuales individuales
            "individual_reviews": self._extract_individual_reviews(),
        }

        # Merge campos schema.org / JSON-LD (excluye review_count — ya mapeado)
        if jsonld:
            for key in (
                "main_image_url", "short_description", "rating_value", "best_rating",
                "street_address", "address_locality", "address_country", "postal_code",
                "accommodation_type",  # GAP-EXTRACT-001-FIX
            ):
                if jsonld.get(key) is not None:
                    data[key] = jsonld[key]

        # Limpiar None para no sobreescribir campos existentes con NULL en upsert
        # Nota: listas vacías [] se preservan para detectar ausencia de datos
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
                    # GAP-EXTRACT-001-FIX (v76 patch): capture JSON-LD @type
                    ld_type = item.get("@type")
                    if ld_type and isinstance(ld_type, str):
                        result["accommodation_type"] = ld_type.strip()

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

        BUG-STAR-001-FIX (Build 83):
        Strategy 1 anterior contaba TODOS los SVGs dentro de rating-stars,
        obteniendo 8-10 (React duplica SVGs internamente). El span contiene
        aria-label="X out of 5 stars" que es la fuente canónica y fiable.
        Fix: parsear aria-label directamente. Fallback a conteo de SVG solo
        cuando aria-label está ausente.

        Estrategias (en orden de prioridad):
        1. aria-label del span data-testid="rating-stars" → parse "X out of Y"
        2. data-property-rating attr (raw ×2 si > 5 → ÷2)
        3. aria-label pattern genérico en cualquier elemento rating
        """
        # Estrategia 1: aria-label "X out of 5 stars" — FUENTE CANÓNICA
        try:
            el = self.soup.find(attrs={"data-testid": "rating-stars"})
            if el:
                aria = el.get("aria-label", "")
                if aria:
                    m = re.search(r"(\d+(?:[.,]\d+)?)\s+out\s+of\s+(\d+)", aria, re.I)
                    if m:
                        star_val = float(m.group(1).replace(",", "."))
                        max_val  = float(m.group(2))
                        # Normalise to 0-5 scale
                        if max_val > 0:
                            normalised = star_val * 5.0 / max_val
                            if 0.0 <= normalised <= 5.0:
                                return round(normalised, 1)
                # Fallback within strategy 1: count only first-level star SVGs
                # (direct children of the span, not React duplicates)
                star_containers = el.find_all(
                    "span",
                    attrs={"aria-hidden": "true"},
                    recursive=False,
                )
                # Each visible star is wrapped in an aria-hidden span
                count = len(star_containers)
                if 1 <= count <= 5:
                    return float(count)
                logger.debug(
                    "star_rating strategy-1 aria-hidden spans=%d out of range [1-5] lang=%s",
                    count, self.language,
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

        # Estrategia 3: aria-label pattern genérico
        try:
            for el in self.soup.find_all(
                True, attrs={"aria-label": re.compile(r"out\s+of\s+\d+\s+star", re.I)}
            ):
                aria = el.get("aria-label", "")
                m = re.search(r"(\d+(?:[.,]\d+)?)\s+out\s+of\s+(\d+)", aria, re.I)
                if m:
                    star_val = float(m.group(1).replace(",", "."))
                    max_val  = float(m.group(2))
                    if max_val > 0:
                        normalised = star_val * 5.0 / max_val
                        if 0.0 <= normalised <= 5.0:
                            return round(normalised, 1)
        except Exception:
            pass

        return None

    def _extract_city(self, jsonld: Dict[str, Any]) -> Optional[str]:
        """
        BUG-EXTR-006 / STRUCT-011 (v52): ciudad desde JSON-LD addressRegion o breadcrumb.

        Fuente de datos para hotels.address_city (renombrado desde hotels.city en v52).
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

    # STRUCT-012 (v52): _extract_country ELIMINADO.
    # El campo hotels.country fue eliminado por ser duplicado de address_country.
    # address_country se sigue poblando via merge JSON-LD en extract_all():
    #   data["address_country"] = jsonld["address_country"]

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

    def _extract_popular_services(self) -> List[str]:
        """
        STRUCT-008: Extrae el bloque curado 'Most popular facilities'.

        Fuente: data-testid="property-most-popular-facilities-wrapper" → <ul> → <li> → <span>
        Este bloque contiene 8-12 servicios seleccionados editorialmente por Booking.com.
        Se almacena en hotels_popular_services.

        (build 65: _extract_amenities() eliminada — _extract_popular_services() es fuente única.)
        """
        popular: List[str] = []
        try:
            wrapper = self.soup.find(
                attrs={"data-testid": "property-most-popular-facilities-wrapper"}
            )
            if wrapper:
                for li in wrapper.find_all("li"):
                    spans = li.find_all("span")
                    for span in spans:
                        text = span.get_text(strip=True)
                        # Excluir links "Ver todos los X servicios" / "See all N facilities"
                        if text and len(text) > 2 and not re.match(
                            r"(Ver |See |Alle |Voir |Ver )(los |all |les |alle |\d)", text, re.I
                        ):
                            popular.append(text)
                            break  # un texto por <li>
                if popular:
                    logger.debug(
                        "Popular services extracted via popular-facilities-wrapper: %d", len(popular)
                    )
        except Exception as exc:
            logger.debug("popular-services popular-wrapper extraction failed: %s", exc)

        return popular

    def _extract_policies(self) -> List[Dict[str, str]]:
        """
        STRUCT-006: Extrae las políticas del alojamiento.

        BUG-POLICY-001-FIX (Build 83):
        Root cause: el selector 'data-testid=property-section--policies' NO existe
        en el DOM real de Booking.com 2025. La sección real es section#policies
        (o div[data-testid="HouseRules-wrapper"]) con esta estructura verificada:

          section#policies  (o data-testid="HouseRules-wrapper")
            div[data-testid="property-section--content"]
              div.b0400e5749              ← una fila por política
                div.a776c0ae8b           ← nombre de la política
                div.c92998be48           ← detalle de la política (puede estar vacío)
                h3.ff410f42e9            ← sub-heading (e.g. "Child policies")
                p                        ← texto de sub-detalle
                span.f323fd7e96          ← método de pago aceptado

        Estrategias:
          0 (nueva/prioritaria): section#policies / HouseRules-wrapper + clases verificadas
          1-3: selectores legacy conservados como fallback
        """
        policies: List[Dict[str, str]] = []

        # ── Estrategia 0: DOM real 2025 — clases verificadas en pruebas/ ────
        try:
            pol_section = (
                self.soup.find("section", id="policies")
                or self.soup.find(attrs={"data-testid": "HouseRules-wrapper"})
            )
            if pol_section:
                content = pol_section.find(
                    attrs={"data-testid": "property-section--content"}
                )
                if content:
                    seen_names: set = set()
                    for row in content.find_all("div", class_="b0400e5749"):
                        label_el = row.find("div", class_="a776c0ae8b")
                        if not label_el:
                            continue
                        name = label_el.get_text(strip=True)
                        if not name or len(name) >= 256 or name in seen_names:
                            continue
                        seen_names.add(name)

                        detail_parts: List[str] = []
                        # Value div (may be absent for some rows)
                        val_el = row.find("div", class_="c92998be48")
                        if val_el:
                            v = val_el.get_text(" ", strip=True)
                            if v:
                                detail_parts.append(v)
                        # Sub-headings (e.g. "Child policies", "Cot and extra bed policies")
                        for sub_h in row.find_all("h3", class_="ff410f42e9"):
                            st = sub_h.get_text(strip=True)
                            if st:
                                detail_parts.append(st)
                        # Paragraph content
                        for sub_p in row.find_all("p"):
                            pt = sub_p.get_text(" ", strip=True)
                            if pt and pt not in detail_parts:
                                detail_parts.append(pt)
                        # Card / payment method spans
                        for span in row.find_all("span", class_="f323fd7e96"):
                            st = span.get_text(strip=True)
                            if st and st not in detail_parts:
                                detail_parts.append(st)

                        detail = " ".join(detail_parts).strip()
                        policies.append({"policy_name": name, "policy_details": detail})

                    if policies:
                        logger.debug(
                            "Policies strategy0 (section#policies): %d pairs lang=%s",
                            len(policies), self.language,
                        )
                        return policies
        except Exception as exc:
            logger.debug("Policies strategy0 failed lang=%s: %s", self.language, exc)

        # ── Estrategia 1: data-testid legacy ────────────────────────────────
        try:
            section = self.soup.find(
                attrs={"data-testid": "property-section--policies"}
            )
            if section:
                policies = self._parse_policy_section(section)
                if policies:
                    logger.debug(
                        "Policies via property-section--policies: %d lang=%s",
                        len(policies), self.language,
                    )
                    return policies
        except Exception as exc:
            logger.debug("policies section extraction failed: %s", exc)

        # ── Estrategia 2: id/class legacy ────────────────────────────────────
        try:
            for selector in [
                {"id": "hp_desc_the_property_rules"},
                {"class_": re.compile(r"hp_desc_the_property_rules", re.I)},
                {"class_": re.compile(r"policies|property-rules|house-rules", re.I)},
            ]:
                section = self.soup.find(True, **selector)  # type: ignore[arg-type]
                if section:
                    policies = self._parse_policy_section(section)
                    if policies:
                        logger.debug(
                            "Policies via legacy selector: %d lang=%s",
                            len(policies), self.language,
                        )
                        return policies
        except Exception as exc:
            logger.debug("policies legacy extraction failed: %s", exc)

        # ── Estrategia 3: pares label/value genéricos ────────────────────────
        try:
            for block in self.soup.find_all(
                "div",
                attrs={"data-testid": re.compile(r"policy|check.in|check.out|cancell", re.I)},
            ):
                label = block.find(["h3", "h4", "strong", "b"])
                detail = block.find(["p", "div", "span"], recursive=False)
                if label and detail:
                    name = label.get_text(strip=True)
                    details = detail.get_text(" ", strip=True)
                    if name and len(name) < 120:
                        policies.append({"policy_name": name, "policy_details": details})
            if policies:
                logger.debug(
                    "Policies via generic data-testid: %d lang=%s",
                    len(policies), self.language,
                )
        except Exception as exc:
            logger.debug("policies generic extraction failed: %s", exc)

        return policies

    def _parse_policy_section(self, section: Any) -> List[Dict[str, str]]:
        """
        Helper: parsea una sección de políticas en pares nombre/detalle.

        Detecta automáticamente la estructura del DOM (tables, divs, definition lists).
        """
        policies: List[Dict[str, str]] = []
        seen_names: set = set()

        # Patrón 1: tabla de políticas (th=nombre, td=detalle)
        for row in section.find_all("tr"):
            cells = row.find_all(["th", "td"])
            if len(cells) >= 2:
                name = cells[0].get_text(strip=True)
                details = cells[1].get_text(" ", strip=True)
                if name and name not in seen_names and len(name) < 256:
                    seen_names.add(name)
                    policies.append({"policy_name": name, "policy_details": details})

        if policies:
            return policies

        # Patrón 2: definition list (dt=nombre, dd=detalle)
        dts = section.find_all("dt")
        dds = section.find_all("dd")
        if dts and dds:
            for dt, dd in zip(dts, dds):
                name = dt.get_text(strip=True)
                details = dd.get_text(" ", strip=True)
                if name and name not in seen_names and len(name) < 256:
                    seen_names.add(name)
                    policies.append({"policy_name": name, "policy_details": details})
            if policies:
                return policies

        # Patrón 3: divs con título (h2/h3/h4/strong) seguidos de texto
        for block in section.find_all(["div", "section"], recursive=False):
            title_el = block.find(["h2", "h3", "h4", "strong", "b"])
            if not title_el:
                continue
            name = title_el.get_text(strip=True)
            if not name or len(name) >= 256 or name in seen_names:
                continue
            # Extraer el texto del bloque excluyendo el título
            title_el.extract()
            details = block.get_text(" ", strip=True)
            seen_names.add(name)
            policies.append({"policy_name": name, "policy_details": details})

        return policies

    def _extract_legal(self) -> Optional[Dict[str, str]]:
        """
        STRUCT-007: Extrae el bloque de información legal del pie de página de Booking.com.

        Booking.com incluye un bloque de texto legal bajo el título 'Información legal' (ES)
        o 'Legal information' (EN). Contiene quién gestiona o representa el alojamiento.

        Estructura DOM típica:
          <div data-testid="property-section--legal" | class="legal-info...">
            <h3>Información legal</h3>
            <p>Este alojamiento lo gestiona...</p>
          </div>

        Estructura DOM problemática (causa del bug ES ids 1-22):
          <div data-testid="property-section--legal">
            <p>Información legal</p>          ← título en <p>, no en <h3>
            <p>Este alojamiento lo gestiona...</p>
          </div>

        FIX-LEGAL-001 (v52):
          Si section.find(["h2","h3","h4","strong"]) no encuentra heading,
          se analiza el primer <p> contra _LEGAL_TITLE_RE (regex multiidioma).
          Si coincide, ese <p> es el título legal y se excluye del cuerpo.

        Idiomas cubiertos por la detección de título:
          EN, ES, DE, FR, IT, NL, PT, RU, ZH, JA, AR, KO, PL, CS, HU, TR, ID

        Retorna: dict {legal, legal_info, legal_details} o None si no se encuentra.
        """
        # ---------------------------------------------------------------------------
        # FIX-LEGAL-001: Regex multiidioma para detectar títulos en cualquier elemento
        # Cubre: EN/ES/IT/DE/FR/NL/PT/RU/ZH/JA/AR/KO/PL/CS/HU/TR/ID y variantes
        # ---------------------------------------------------------------------------
        _LEGAL_TITLE_RE = re.compile(
            r"""
            legal\s+information          # EN
            | legal\s+info               # EN abrev
            | informaci[oó]n\s+legal     # ES
            | info\s+legal               # ES abrev
            | informazioni\s+legali      # IT
            | rechtliche\s+(?:informationen|hinweise)  # DE
            | informations?\s+l[eé]gales?  # FR
            | juridische\s+informatie    # NL
            | informa[cç][aã]o\s+legal   # PT/PT-BR
            | (?:правовая|юридическая)\s+информация  # RU
            | 法律情報                   # ZH/JA
            | 法的情報                   # JA
            | 法律资讯                   # ZH-HANS
            | 法律資訊                   # ZH-HANT
            | معلومات\s*قانون[يی]ة?      # AR
            | 법적\s*정보                # KO
            | informacje\s+prawne        # PL
            | právní\s+informace         # CS
            | jogi\s+(?:információ|tájékoztató)  # HU
            | yasal\s+bilg(?:i|iler)     # TR
            | informasi\s+hukum          # ID
            """,
            re.IGNORECASE | re.VERBOSE | re.UNICODE,
        )

        # Selectores en orden de prioridad
        # BUG-LEGAL-SELECTOR / BUG-LEGAL-CLASS (v56):
        #   La sección legal real usa la clase k2-hp--cpc_regulation (CPC Regulation).
        #   Los selectores anteriores no la detectaban. Se añade como primera prioridad.
        #   BUG-LEGAL-WRONG-TITLE (v56): el fallback encontraba el nav-bar "Información
        #   legal e importante" en lugar de la sección <div class="k2-hp--cpc_regulation">.
        selectors = [
            # Prioridad 1: clase CPC regulation — fuente confirmada en HTML real
            {"attrs": {"class": re.compile(r"k2-hp--cpc.regulation", re.I)}},
            # Prioridad 2: data-testid estándar (versiones antiguas de Booking.com)
            {"attrs": {"data-testid": "property-section--legal"}},
            {"attrs": {"data-testid": re.compile(r"cpc.regulation|legal", re.I)}},
            # Prioridad 3: clases genéricas (fallback)
            {"attrs": {"class": re.compile(r"legal.info|legal.text|legalinfo|cpc.regulation", re.I)}},
            {"attrs": {"id": re.compile(r"legal", re.I)}},
        ]

        # Palabras clave para localizar el bloque sin selector específico
        _LEGAL_KEYWORDS = {
            "en": ["legal information", "legal info"],
            "es": ["información legal", "info legal"],
            "de": ["rechtliche informationen", "rechtliche hinweise"],
            "fr": ["informations légales"],
            "it": ["informazioni legali"],
            "nl": ["juridische informatie"],
            "pt": ["informações legais"],
            "ja": ["法的情報", "法律情報"],
            "zh": ["法律信息", "法律資訊"],
            "ar": ["معلومات قانونية"],
            "ko": ["법적 정보"],
            "ru": ["правовая информация", "юридическая информация"],
        }

        section = None

        # Intento 1: selectores específicos
        for sel in selectors:
            try:
                section = self.soup.find(True, **sel)  # type: ignore[arg-type]
                if section:
                    break
            except Exception:
                continue

        # Intento 2: buscar por texto del título en elementos heading o párrafo
        if not section:
            try:
                keywords = _LEGAL_KEYWORDS.get(self.language, []) + _LEGAL_KEYWORDS.get("en", [])
                for kw in keywords:
                    el = self.soup.find(
                        ["h2", "h3", "h4", "p", "div"],
                        string=re.compile(re.escape(kw), re.I | re.UNICODE),
                    )
                    if el:
                        # Subir al contenedor padre
                        section = el.parent
                        break
            except Exception:
                pass

        if not section:
            logger.debug("Legal section not found for lang=%s", self.language)
            return None

        try:
            # ── Paso 1: buscar título en heading estándar ─────────────────────────
            title_el = section.find(["h2", "h3", "h4", "strong"])
            legal_title = title_el.get_text(strip=True) if title_el else ""

            # FIX-LEGAL-001 (v52): si no hay heading estándar, inspeccionar el
            # primer elemento <p> o <span> del bloque contra el regex multiidioma.
            # Booking.com a veces emite el título como <p> en lugar de <h3>,
            # lo que causaba que el título quedara en legal_info en lugar de legal.
            title_from_paragraph = False
            if not legal_title:
                first_text_el = None
                for candidate in section.find_all(["p", "span", "b"], recursive=True):
                    candidate_text = candidate.get_text(strip=True)
                    if candidate_text and len(candidate_text) >= 4:
                        first_text_el = candidate
                        break

                if first_text_el is not None:
                    candidate_text = first_text_el.get_text(strip=True)
                    # Sólo asignamos como título si: longitud razonable Y coincide regex
                    if len(candidate_text) <= 120 and _LEGAL_TITLE_RE.search(candidate_text):
                        legal_title = candidate_text
                        title_from_paragraph = True
                        title_el = first_text_el  # lo excluiremos del cuerpo


            # BUG-LEGAL-001-FIX (Build 83):
            # Root cause: el flujo "Paso 2" (recursive=False paragraphs) capturaba el
            # contenedor externo del bloque k2-hp--cpc_regulation como primer párrafo,
            # que incluye el título h2. Esto hacía que legal_info = "Legal information
            # This property is managed..." (título + cuerpo en el mismo campo).
            # Fix: si title_el existe (siempre en el DOM real), usar find_next_siblings
            # sobre el h2 DIRECTAMENTE como fuente primaria del cuerpo. Esto garantiza
            # que el título queda en 'legal' y el cuerpo queda en 'legal_info'.
            # El fallback de paragraphs recursive=False se conserva solo si sibling
            # strategy no produce texto.
            body_started = False
            legal_info = ""
            legal_details = ""

            # ── Paso 2a (prioritario): siblings del heading ──────────────────────
            if title_el:
                try:
                    for sibling in title_el.find_next_siblings(["div", "p", "span"]):
                        sib_text = sibling.get_text(" ", strip=True)
                        if not sib_text or len(sib_text) < 5:
                            continue
                        if legal_title and sib_text.strip() == legal_title.strip():
                            continue
                        if not body_started:
                            legal_info = sib_text
                            body_started = True
                        elif not legal_details:
                            legal_details = sib_text
                        else:
                            legal_details += " " + sib_text
                except Exception:
                    pass

            # ── Paso 2b: paragraphs fallback (recursive=False) ──────────────────
            # Used only when step 2a produced nothing (title_el absent or no siblings)
            if not legal_info:
                paragraphs = section.find_all(["p", "div"], recursive=False)
                for para in paragraphs:
                    if title_from_paragraph and title_el is not None:
                        if para is title_el or para == title_el:
                            continue
                        if title_el in para.descendants:
                            continue
                    para_text = para.get_text(" ", strip=True)
                    if not para_text or len(para_text) < 5:
                        continue
                    if legal_title and para_text.strip() == legal_title.strip():
                        continue
                    if not body_started:
                        legal_info = para_text
                        body_started = True
                    elif not legal_details:
                        legal_details = para_text
                    else:
                        legal_details += " " + para_text

            # ── Paso 2c: recursive fallback ──────────────────────────────────────
            if not legal_info:
                all_text_els = section.find_all(["p", "div", "span"], recursive=True)
                for el in all_text_els:
                    el_text = el.get_text(" ", strip=True)
                    if not el_text or len(el_text) < 10:
                        continue
                    if legal_title and el_text.strip() == legal_title.strip():
                        continue
                    if el.find(["p", "div"]):
                        continue
                    legal_info = el_text
                    break

            # ── Paso 2d: full-section fallback ────────────────────────────────────
            if not legal_info:
                if title_el:
                    import copy as _copy
                    section_copy = _copy.copy(section)
                    for t in section_copy.find_all(
                        ["h2", "h3", "h4", "strong", "p"] if title_from_paragraph
                        else ["h2", "h3", "h4", "strong"]
                    ):
                        if t.get_text(strip=True) == legal_title:
                            t.extract()
                            break
                    legal_info = section_copy.get_text(" ", strip=True).strip()
                else:
                    legal_info = section.get_text(" ", strip=True).strip()

            if not legal_title and not legal_info:
                return None

            # FIX-LEGAL-003 (v55): Validación post-extracción — detectar y corregir
            # el caso donde legal == legal_info (ambos campos contienen el título).
            # Si son idénticos, legal_info no contiene texto real del cuerpo.
            if (
                legal_title
                and legal_info
                and legal_title.strip() == legal_info.strip()
            ):
                logger.debug(
                    "Legal section: legal == legal_info detected for lang=%s — clearing legal_info",
                    self.language,
                )
                legal_info = ""
                legal_details = ""

            result = {
                "legal": legal_title or "",
                "legal_info": legal_info or "",
                "legal_details": legal_details or "",
            }
            logger.debug(
                "Legal section extracted for lang=%s: title=%r info_len=%d",
                self.language, legal_title, len(legal_info),
            )
            return result

        except Exception as exc:
            logger.debug("Legal section parse error for lang=%s: %s", self.language, exc)
            return None


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

    # =========================================================================
    # STRUCT-013/017 (v53): HTML SANITIZER HELPER
    # =========================================================================

    def _sanitize_html_fragment(
        self,
        html_str: str,
        remove_tags: Tuple[str, ...] = ("svg", "img", "picture", "source", "canvas", "video"),
    ) -> Optional[str]:
        """
        Sanitiza un fragmento HTML para almacenamiento seguro en base de datos.

        Proceso (STRUCT-013 / STRUCT-017, v53):
          1. Elimina completamente las etiquetas de imagen/vector (svg, img, etc.)
             junto con TODO su contenido interno.
          2. Elimina TODOS los atributos de las etiquetas HTML restantes:
             class, id, height, width, aria-hidden, focusable, data-*, style,
             role, tabindex, etc.
          3. Preserva la estructura HTML y el texto: <div>, <p>, <ul>, <li>,
             <span>, <h1>-<h6>, <strong>, <em>, <br>, <a>, etc.

        Args:
            html_str   : Fragmento HTML a sanitizar.
            remove_tags: Tupla de nombres de etiqueta a eliminar completamente.
                         Por defecto elimina: svg, img, picture, source, canvas, video.

        Returns:
            HTML sanitizado como string, o None si el resultado está vacío
            después del saneamiento.

        Platform note (Windows 11):
            BeautifulSoup no depende de señales POSIX — compatible con Windows.
            Usa html.parser (stdlib) o lxml si está disponible.
        """
        if not html_str or not html_str.strip():
            return None

        import copy as _copy

        try:
            fragment_soup = _make_soup(html_str)

            # Paso 1: eliminar completamente las etiquetas de imagen/vector
            for tag_name in remove_tags:
                for tag in fragment_soup.find_all(tag_name):
                    tag.decompose()

            # Paso 2: eliminar TODOS los atributos de las etiquetas restantes
            for tag in fragment_soup.find_all(True):
                tag.attrs = {}

            # Paso 3: obtener el HTML resultante
            result = str(fragment_soup)

            # Limpieza de artefactos del parser (etiquetas html/body/head añadidas)
            result = re.sub(r'^<html[^>]*><head[^>]*></head><body[^>]*>', '', result, flags=re.I)
            result = re.sub(r'</body></html>$', '', result, flags=re.I)
            result = result.strip()

            if not result:
                return None

            logger.debug(
                "_sanitize_html_fragment: output_len=%d lang=%s",
                len(result), self.language,
            )
            return result

        except Exception as exc:
            logger.debug("_sanitize_html_fragment failed for lang=%s: %s", self.language, exc)
            return None

    # =========================================================================
    # STRUCT-013 (v53): FINE PRINT EXTRACTOR
    # =========================================================================

    def _extract_fine_print(self) -> Optional[str]:
        """
        STRUCT-013 (v53): Extrae el bloque "Fine Print" / "Letra pequeña" de Booking.com.

        El contenido se almacena como HTML sanitizado:
          - Etiquetas <p> preservadas para mantener saltos de línea del texto.
          - SVG, <img>, <picture>, <source> eliminados completamente.
          - Atributos HTML (class, id, style, data-*, etc.) eliminados de todas
            las etiquetas restantes.

        Estructura DOM típica (Booking.com React):
          <div data-testid="property-section--fine-print">
            <div>
              <h3>Fine print</h3>
              <p>You must show a valid photo ID and credit card upon check-in.</p>
              <p>Special requests are subject to availability...</p>
            </div>
          </div>

        Estrategias de localización (en orden de prioridad):
          1. data-testid="property-section--fine-print"
          2. class pattern: fine-print, fineprint, fine_print
          3. id pattern: fine-print, fineprint
          4. heading/párrafo con keyword en el idioma del scrape
          5. Texto en section con "fine print" / idioma-equivalente

        Retorna: HTML sanitizado con <p> preservados, o None si no se encuentra.
        """
        # ── Selectores específicos por data-testid y class/id ─────────────────
        # BUG-FP-SELECTOR-001 FIX (v56): Selectores actualizados para DOM real de
        # Booking.com, validados contra HTML descargado en pruebas/*.md.
        # Estructura real confirmada:
        #   <div data-testid="PropertyFinePrintDesktop-wrapper">
        #     <section id="important_info" class="cbdacf5131">
        #       <div data-testid="property-section--content" class="b99b6ef58f">
        #         <div class="c3bdfd4ac2 ...">
        #           <div class="c85a1d1c49">
        #             <p>The property can be reached by seaplanes...</p>
        #           </div>
        #         </div>
        #       </div>
        #     </section>
        #   </div>
        _SELECTORS = [
            # Prioridad 1: wrapper semántico externo (más estable)
            {"attrs": {"data-testid": "PropertyFinePrintDesktop-wrapper"}},
            # Prioridad 2: section por id semántico HTML (muy estable)
            {"attrs": {"id": "important_info"}},
            # Prioridad 3: legacy data-testid (por si Booking lo reactiva)
            {"attrs": {"data-testid": "property-section--fine-print"}},
            {"attrs": {"data-testid": re.compile(r"fine.?print", re.I)}},
            # Prioridad 4: class/id pattern (fallback robusto)
            {"attrs": {"class": re.compile(r"fine.?print|fineprint|fine_print", re.I)}},
            {"attrs": {"id":    re.compile(r"fine.?print|fineprint", re.I)}},
        ]

        # ── Keywords por idioma para localización por texto ───────────────────
        _FP_KEYWORDS: Dict[str, List[str]] = {
            "en": ["fine print", "important information", "know before you go"],
            "es": ["letra pequeña", "información importante", "lo que debe saber"],
            "de": ["kleingedruckte", "wichtige informationen", "das kleingedruckte"],
            "fr": ["bon à savoir", "informations importantes", "petits caractères"],
            "it": ["note importanti", "informazioni importanti", "da sapere"],
            "nl": ["kleine lettertjes", "belangrijke informatie"],
            "pt": ["informações importantes", "letras pequenas"],
            "ja": ["ご注意", "重要なお知らせ"],
            "zh": ["注意事项", "重要信息"],
            "ar": ["معلومات مهمة", "ملاحظة"],
            "ko": ["중요 정보", "참고 사항"],
            "ru": ["важная информация", "примечание"],
            "pl": ["ważne informacje", "drobny druk"],
            "tr": ["önemli bilgiler", "notlar"],
        }

        section = None

        # Intento 1: selectores específicos
        for sel in _SELECTORS:
            try:
                section = self.soup.find(True, **sel)  # type: ignore[arg-type]
                if section:
                    logger.debug("FinePrint: found via selector %s lang=%s", sel, self.language)
                    break
            except Exception:
                continue

        # Intento 2: buscar por keyword de heading/párrafo
        if not section:
            keywords = (
                _FP_KEYWORDS.get(self.language, []) +
                _FP_KEYWORDS.get(self.language[:2], []) +
                _FP_KEYWORDS.get("en", [])
            )
            for kw in keywords:
                try:
                    el = self.soup.find(
                        ["h2", "h3", "h4", "p", "div", "span"],
                        string=re.compile(re.escape(kw), re.I | re.UNICODE),
                    )
                    if el:
                        # Subir al contenedor padre relevante
                        parent = el.parent
                        # Verificar que el padre contiene párrafos de contenido
                        if parent and parent.find("p"):
                            section = parent
                            logger.debug(
                                "FinePrint: found via keyword %r lang=%s", kw, self.language
                            )
                            break
                        elif parent and parent.parent and parent.parent.find("p"):
                            section = parent.parent
                            logger.debug(
                                "FinePrint: found via keyword %r (grandparent) lang=%s",
                                kw, self.language,
                            )
                            break
                except Exception:
                    continue

        if not section:
            logger.debug("FinePrint: section not found for lang=%s", self.language)
            return None

        try:
            # FIX-FP-CONTENT-001 (v59): extraer SOLO el contenido <p>, no el HTML
            # envolvente (wrappers React/div/section que Booking.com genera).
            #
            # Estructura real confirmada en HTML de prueba (Build 58):
            #   <section id="important_info">
            #     <div data-testid="property-section--content" class="b99b6ef58f">
            #       <div class="c3bdfd4ac2 ...">
            #         <div class="c85a1d1c49">   ← contenedor directo de <p>
            #           <p>The property can be reached...</p>
            #           <p>Seaplane transfer takes...</p>
            #         </div>
            #       </div>
            #     </div>
            #   </section>
            #
            # Estrategia: buscar el contenedor interno con clase c85a1d1c49.
            # Fallback 1: cualquier div que tenga <p> como hijos directos.
            # Fallback 2: usar la sección completa y extraer todos los <p>.

            inner = section.find(attrs={"class": lambda c: c and "c85a1d1c49" in c})

            if not inner:
                # Fallback 1: buscar contenedor con <p> hijos directos
                for candidate in section.find_all("div"):
                    if candidate.find("p", recursive=False):
                        inner = candidate
                        logger.debug(
                            "FinePrint: inner container via p-direct-child fallback lang=%s",
                            self.language,
                        )
                        break

            if not inner:
                # Fallback 2: usar la sección completa
                inner = section
                logger.debug(
                    "FinePrint: using full section as fallback lang=%s", self.language
                )

            paragraphs = inner.find_all("p")
            if not paragraphs:
                logger.debug("FinePrint: no <p> elements found for lang=%s", self.language)
                return None

            # Concatenar solo <p> con contenido real (umbral bajo para no perder
            # ítems de precio cortos como "- Adult: USD 550")
            content_parts: List[str] = []
            for para in paragraphs:
                text = para.get_text(strip=True)
                if len(text) >= 3:
                    content_parts.append(str(para))

            if not content_parts:
                logger.debug(
                    "FinePrint: all <p> elements were empty for lang=%s", self.language
                )
                return None

            result = "".join(content_parts)

            logger.debug(
                "FinePrint extracted for lang=%s: %d <p> elements, %d chars",
                self.language, len(content_parts), len(result),
            )
            return result

        except Exception as exc:
            logger.debug("FinePrint parse error for lang=%s: %s", self.language, exc)
            return None

    # =========================================================================
    # STRUCT-014 (v57): ALL SERVICES EXTRACTOR
    # BUG-ALL-SERVICES-001: Fix extracción idiomas no-EN (ES/DE/IT).
    # Cambios:
    #   - Strategy 0 (nueva): Apollo JSON cache — fuente idioma-independiente.
    #   - Strategy 1: sin cambios (selector legacy, nunca presente en DOM actual).
    #   - Strategy 2 fix: regex "facilit" en lugar de "facility" para capturar
    #     "facilities-wrapper" y derivados con substring correcto.
    #   - _SEE_ALL_PATTERN: regex multi-idioma extendido (ES/DE/IT/FR/PT).
    # =========================================================================

    # Patrón multi-idioma para filtrar links "Ver todos los servicios"
    # Validado contra: EN/ES/DE/IT/FR/PT.

    # BUG-SVC-CAT-001-FIX (Build 87):
    # Mapa estático groupId → nombre de categoría por idioma.
    # Derivado de análisis empírico de BaseFacility.groupId en HTMLs de prueba.
    # groupIds verificados: 1,3,7,11,12,13,15,16,21,23,25,26.
    # Fuente: Booking.com Apollo/GraphQL normalized cache en <script type="application/json">.
    _FACILITY_GROUP_MAP: Dict[int, Dict[str, str]] = {
        1:  {"en": "General",          "es": "General",             "de": "Allgemein",
             "fr": "Général",          "it": "Generale",            "pt": "Geral"},
        3:  {"en": "Services",         "es": "Servicios",           "de": "Dienstleistungen",
             "fr": "Services",         "it": "Servizi",             "pt": "Serviços"},
        7:  {"en": "Food & Drink",     "es": "Alimentos y bebidas", "de": "Speisen & Getränke",
             "fr": "Alimentation",     "it": "Cibo e bevande",      "pt": "Comida e bebidas"},
        11: {"en": "Internet",         "es": "Internet",            "de": "Internet",
             "fr": "Internet",         "it": "Internet",            "pt": "Internet"},
        12: {"en": "Kitchen",          "es": "Cocina",              "de": "Küche",
             "fr": "Cuisine",          "it": "Cucina",              "pt": "Cozinha"},
        13: {"en": "Outdoors & View",  "es": "Exteriores y vistas", "de": "Außenbereich",
             "fr": "Extérieur",        "it": "Spazi esterni",       "pt": "Exterior"},
        15: {"en": "Room Amenities",   "es": "Comodidades",         "de": "Zimmerausstattung",
             "fr": "Équipements",      "it": "Dotazioni camera",    "pt": "Comodidades"},
        16: {"en": "Parking",          "es": "Aparcamiento",        "de": "Parken",
             "fr": "Parking",          "it": "Parcheggio",          "pt": "Estacionamento"},
        21: {"en": "Pool & Wellness",  "es": "Piscina y bienestar", "de": "Pool & Wellness",
             "fr": "Piscine & bien-être", "it": "Piscina & benessere", "pt": "Piscina e bem-estar"},
        23: {"en": "Reception",        "es": "Recepción",           "de": "Rezeption",
             "fr": "Réception",        "it": "Ricevimento",         "pt": "Recepção"},
        25: {"en": "Family & Kids",    "es": "Familia e hijos",     "de": "Familie & Kinder",
             "fr": "Famille & Enfants","it": "Famiglia e bambini",  "pt": "Família e crianças"},
        26: {"en": "Cleaning Services","es": "Limpieza",            "de": "Reinigung",
             "fr": "Nettoyage",        "it": "Pulizia",             "pt": "Limpeza"},
    }

    _SEE_ALL_PATTERN: re.Pattern = re.compile(
        r"""
        ^(
            See\s+all                       # EN: "See all 101 facilities"
          | Ver\s+(los\s+)?\d              # ES: "Ver los 101 servicios" / "Ver 101"
          | Ver\s+todos                    # ES: "Ver todos"
          | \d+\s+Einrichtungen            # DE: "101 Einrichtungen anzeigen"
          | Alle\s+\d+\s+Einrichtungen     # DE alt
          | Alle\s+anzeigen               # DE alt 2
          | Voir\s+(les\s+)?\d+           # FR: "Voir les 101"
          | Vedi\s+tutti                  # IT: "Vedi tutti e 101 i servizi"
          | Mostra\s+tutti                # IT alt
          | Ver\s+todas                   # PT
          | Toon\s+alle                   # NL
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    def _extract_all_services(self) -> List[Dict[str, str]]:
        """
        STRUCT-014 (v57 — BUG-ALL-SERVICES-001):
        Extrae la lista COMPLETA de servicios/instalaciones del hotel.

        BUILD-82-FIX (GAP-API-001):
        Tipo de retorno cambiado: List[str] → List[Dict[str, str]].
        Cada dict tiene:
          service          : str — texto del servicio
          service_category : str — nombre del grupo (e.g. "Internet", "Parking")
                                   Cadena vacía "" si la estrategia no aporta categoría.

        Estrategias (en orden de prioridad):
          0. Apollo/GraphQL JSON cache — devuelve {service, service_category=""} (sin grupo).
          1. DOM selector 'property-section--facilities' (legacy).
          1.5. data-testid="facility-group" — PROPORCIONA CATEGORÍA desde el heading del grupo.
          2. facilit* groups (regex).
          3. Fallback: popular-wrapper (~10 items, sin categoría).

        Retorna: lista de dicts deduplicados por 'service'.
        """
        services: List[Dict[str, str]] = []
        seen: set = set()

        def _add(text: str, category: str = "") -> None:
            t = re.sub(r"\s+", " ", text).strip()
            if (
                t
                and len(t) > 2
                and len(t) < 300
                and t not in seen
                and not self._SEE_ALL_PATTERN.match(t)
            ):
                seen.add(t)
                services.append({
                    "service": t,
                    "service_category": (category or "").strip()[:128],
                })

        # ── Estrategia 0: Apollo JSON cache ─────────────────────────────────
        # BUG-SVC-CAT-001-FIX (Build 87):
        #   - _extract_services_from_json() ahora retorna List[Dict] con
        #     {service, service_category} en lugar de List[str].
        #   - El umbral >=5 reemplaza >=30: el Apollo JSON solo incluye las
        #     instalaciones del hotel (BaseFacility), que son 5-25 items.
        #     El umbral anterior >=30 hacía que esta estrategia fallase siempre
        #     para hoteles con <30 instalaciones (la mayoría), cayendo al fallback
        #     popular-wrapper sin categoría.
        try:
            json_services = self._extract_services_from_json()
            if json_services and len(json_services) >= 5:
                logger.debug(
                    "AllServices: strategy0 (JSON cache+category): %d items lang=%s",
                    len(json_services), self.language,
                )
                for item in json_services:
                    _add(item.get("service", ""), category=item.get("service_category", ""))
                return services
        except Exception as exc:
            logger.debug(
                "AllServices strategy 0 (JSON) failed lang=%s: %s",
                self.language, exc,
            )

        # ── Estrategia 1: sección facilities completa (DOM post-expansión) ──
        # BUG-SVC-CAT-001-FIX (Build 87): cuando property-section--facilities existe
        # (post-expansión Selenium), intentar extraer categorías de facility-group
        # hijos antes de hacer el flat-extract de <li> sin categoría.
        try:
            section = self.soup.find(
                attrs={"data-testid": "property-section--facilities"}
            )
            if section:
                # Primero intentar con facility-group hijos (tienen categoría)
                fac_groups_in_section = section.find_all(
                    attrs={"data-testid": "facility-group"}
                )
                if fac_groups_in_section:
                    for group in fac_groups_in_section:
                        icon_el = group.find(attrs={"data-testid": "facility-icon"})
                        if icon_el:
                            icon_el.extract()
                        for svg in group.find_all("svg"):
                            svg.extract()
                        group_category = ""
                        content_div = group.find("div")
                        if content_div:
                            for child in content_div.find_all(
                                ["div", "span", "h3", "h4", "p"], recursive=False
                            ):
                                candidate = child.get_text(strip=True)
                                if candidate and not child.find(["ul", "li", "ol"]):
                                    group_category = candidate[:128]
                                    break
                        for li in group.find_all("li"):
                            _add(li.get_text(" ", strip=True), category=group_category)
                    if services:
                        logger.debug(
                            "AllServices: strategy1+group (section+category): %d items lang=%s",
                            len(services), self.language,
                        )
                        return services
                # Fallback: flat list sin categoría si no hay facility-group
                for li in section.find_all("li"):
                    _add(li.get_text(" ", strip=True))
                if services:
                    logger.debug(
                        "AllServices: strategy1 (section flat): %d items lang=%s",
                        len(services), self.language,
                    )
                    return services
        except Exception as exc:
            logger.debug("AllServices strategy 1 failed lang=%s: %s", self.language, exc)

        # ── Estrategia 1.5: facility-group — FUENTE CON CATEGORÍA ───────────
        # BUG-SVC-CAT-001-FIX (Build 87): Correcciones en esta estrategia:
        #
        #   BUG-SVC-CAT-001-C: El código buscaba data-testid="facility-group-icon"
        #     para eliminar el icono antes de extraer el heading. Este testid NO
        #     existe en el DOM de Booking.com — el testid real es "facility-icon"
        #     (verificado en todos los HTMLs de pruebas/). Como el icono no se
        #     eliminaba, el texto del SVG contaminaba la búsqueda de categoría.
        #     FIX: buscar "facility-icon" (sin "group-").
        #
        #   BUG-SVC-CAT-001-D: La búsqueda de heading usaba find_all(["div","span",
        #     "h3","h4"], recursive=False). El heading real de categoría en el DOM
        #     expandido de Booking.com puede estar en <p>, no solo en <div>/<h3>.
        #     FIX: añadir "p" a la lista de tags de heading.
        #
        # Estructura DOM real (post-expansión Selenium):
        #   <div data-testid="facility-group">
        #     <span data-testid="facility-icon" aria-hidden="true"><svg/></span>
        #     <div>
        #       <p class="...">Internet</p>    ← categoría en <p> o <div>
        #       <ul><li>Free WiFi</li>...</ul>
        #     </div>
        #   </div>
        try:
            fac_groups = self.soup.find_all(
                attrs={"data-testid": "facility-group"}
            )
            if fac_groups:
                for group in fac_groups:
                    # BUG-SVC-CAT-001-C-FIX: testid correcto es "facility-icon"
                    icon_el = group.find(attrs={"data-testid": "facility-icon"})
                    if icon_el:
                        icon_el.extract()
                    # También eliminar SVG huérfano si quedara
                    for svg in group.find_all("svg"):
                        svg.extract()

                    # BUG-SVC-CAT-001-D-FIX: buscar heading en <div>/<span>/<h3>/<h4>/<p>
                    group_category = ""
                    content_div = group.find("div")
                    if content_div:
                        for child in content_div.find_all(
                            ["div", "span", "h3", "h4", "p"], recursive=False
                        ):
                            candidate = child.get_text(strip=True)
                            if candidate and not child.find(["ul", "li", "ol"]):
                                group_category = candidate[:128]
                                break

                    for li in group.find_all("li"):
                        _add(li.get_text(" ", strip=True), category=group_category)

                if services:
                    logger.debug(
                        "AllServices: strategy1.5 (facility-group): %d items lang=%s",
                        len(services), self.language,
                    )
                    return services
        except Exception as exc:
            logger.debug("AllServices strategy 1.5 failed lang=%s: %s", self.language, exc)

        # ── Estrategia 2: facilit* groups (FIX: "facilit" no "facility") ────
        try:
            groups = self.soup.find_all(
                attrs={"data-testid": re.compile(r"facilit", re.I)}
            )
            for group in groups:
                for li in group.find_all("li"):
                    _add(li.get_text(" ", strip=True))
            if services:
                logger.debug(
                    "AllServices: strategy2 (facilit groups): %d items lang=%s",
                    len(services), self.language,
                )
                return services
        except Exception as exc:
            logger.debug("AllServices strategy 2 failed lang=%s: %s", self.language, exc)

        # ── Estrategia 3: fallback popular-wrapper ───────────────────────────
        try:
            wrapper = self.soup.find(
                attrs={"data-testid": "property-most-popular-facilities-wrapper"}
            )
            if wrapper:
                for li in wrapper.find_all("li"):
                    _add(li.get_text(" ", strip=True))
                if services:
                    logger.debug(
                        "AllServices: strategy3 (popular fallback): %d items lang=%s",
                        len(services), self.language,
                    )
        except Exception as exc:
            logger.debug("AllServices strategy 3 failed lang=%s: %s", self.language, exc)

        return services

    def _extract_services_from_json(self) -> List[Dict[str, str]]:
        """
        BUG-SVC-CAT-001-FIX / BUG-SVC-NAME-001-FIX (Build 87):
        Extrae servicios del Apollo/GraphQL cache con nombre correcto Y categoría.

        Bugs corregidos vs versión anterior:
          BUG-SVC-NAME-001: El método anterior cruzaba BaseFacility.id (valores como
            433, 158, 89) con hotelfacility/name.items (IDs de visualización 1-372).
            Estos son espacios de IDs DISTINTOS — la coincidencia era parcial y
            producía nombres incorrectos (id=89→"Ticket service" en lugar de
            "Kitchenware"; id=433→"Swimming pool" en lugar de "Indoor swimming pool").
            FIX: usar BaseFacility.instances[0].__ref.title, que contiene el nombre
            real traducido al idioma del request (ya language-aware).

          BUG-SVC-CAT-001-A: Retornaba List[str], el caller asignaba category="".
            FIX: retorna List[Dict[str,str]] con claves {service, service_category}.

          BUG-SVC-CAT-001-B: No extraía groupId de cada BaseFacility.
            FIX: extrae groupId y lo mapea a nombre de categoría mediante
            _FACILITY_GROUP_MAP[groupId][language], con fallback a inglés.

        Estructura Apollo JSON verificada en HTML real (EN/ES/DE/IT/FR/PT):
          BaseFacility:{...} → {id, groupId, slug, icon, instances:[{__ref:...}]}
          instances[0].__ref = 'Instance:{"id":N,"title":"<nombre traducido>"}'
          groupId → _FACILITY_GROUP_MAP → categoría traducida

        Retorna: List[Dict] con {service, service_category}. Lista vacía si no hay
        datos suficientes (sin BaseFacility objects en el JSON del hotel).
        """
        import re as _re

        # BaseFacility objects: {fid: {groupId, title_from_instance}}
        base_facilities: List[Dict[str, Any]] = []
        seen_ids: set = set()

        lang_key: str = self.language[:2].lower()

        for script in self.soup.find_all("script", type="application/json"):
            raw = script.get_text()
            if not raw.strip().startswith("{"):
                continue
            try:
                data = json.loads(raw)
            except (json.JSONDecodeError, ValueError):
                continue

            # BaseFacility objects del hotel (Apollo normalized cache)
            for key, val in data.items():
                if not key.startswith("BaseFacility:") or not isinstance(val, dict):
                    continue
                fid = val.get("id")
                if fid is None or fid in seen_ids:
                    continue
                seen_ids.add(fid)

                gid = val.get("groupId")

                # BUG-SVC-NAME-001-FIX: extraer nombre del título de instances[0].__ref
                # en lugar de usar el mapa hotelfacility/name (espacio de IDs distinto).
                title = ""
                instances = val.get("instances", [])
                for inst in instances:
                    ref = inst.get("__ref", "") if isinstance(inst, dict) else ""
                    m = _re.search(r'"title"\s*:\s*"([^"]+)"', ref)
                    if m:
                        title = m.group(1).strip()
                        break

                if not title:
                    # Fallback: slug humanizado si instances vacío
                    slug = val.get("slug", "")
                    if slug:
                        title = slug.replace("_", " ").strip().capitalize()

                if title:
                    base_facilities.append({"id": fid, "groupId": gid, "title": title})

        if not base_facilities:
            logger.debug(
                "AllServices JSON: no BaseFacility objects found lang=%s",
                self.language,
            )
            return []

        # BUG-SVC-CAT-001-FIX: resolver categoría desde groupId → _FACILITY_GROUP_MAP
        result: List[Dict[str, str]] = []
        seen_titles: set = set()

        for fac in base_facilities:
            title = fac["title"]
            if title in seen_titles:
                continue
            seen_titles.add(title)

            gid = fac.get("groupId")
            category = ""
            if gid is not None:
                group_langs = self._FACILITY_GROUP_MAP.get(int(gid), {})
                category = (
                    group_langs.get(lang_key)
                    or group_langs.get("en")
                    or ""
                )

            result.append({"service": title, "service_category": category})

        logger.debug(
            "AllServices JSON: resolved %d/%d facilities with category lang=%s",
            len(result), len(base_facilities), self.language,
        )
        return result

    # =========================================================================
    # STRUCT-018 (Audit): ROOM TYPES EXTRACTOR
    # AUDIT-HTML-001: hotels.room_types (JSONB) existe en schema y
    # scraper_service.py persiste data.get("room_types"), pero extractor.py
    # nunca generaba esa clave → el campo quedaba siempre NULL.
    # Fix: nuevo método _extract_room_types() que popula la clave "room_types"
    # en extract_all() con una lista de dicts [{name, description, facilities}].
    #
    # Selectores: data-testid React (estables).  BUI clases (.bui-list__item,
    # .bui-title__text) descartadas — no presentes en DOM actual de Booking.com.
    # =========================================================================

    def _extract_room_types(self) -> List[Dict[str, Any]]:
        """
        STRUCT-018 (Audit-HTML-001) — BUG-SELECTOR-ROOMS-001 FIX (Build 77):
        Extrae los tipos de habitación disponibles del hotel.

        DOM REAL verificado contra archivos HTML en pruebas/ (Booking.com 2025):

          <table class="cdd0659f86">
            <thead>
              <tr><th>Room type</th><th>Number of guests</th><th>&nbsp;</th></tr>
            </thead>
            <tbody>
              <tr>
                <th scope="row">
                  <div>
                    <a data-testid="rt-name-link" href="#RD...">
                      <span><div>Deluxe Room with Garden View</div></span>
                    </a>
                  </div>
                  <div>
                    <!-- bed info: spans d7a50099f7 -->
                    <div><span class="d7a50099f7">1 extra-large double bed</span></div>
                    <div class="ee6184f499">and</div>
                    <div><span class="d7a50099f7">1 sofa bed</span></div>
                  </div>
                </th>
                <td><!-- occupancy icons --></td>
                <td><!-- price button --></td>
              </tr>
            </tbody>
          </table>

        NOTA: el selector anterior "room-block" y "room-type-title" NO existen en
        el DOM actual. La tabla de habitaciones usa data-testid="rt-name-link"
        dentro de elementos <th scope="row">.

        Estrategia de extracción:
          1. Strategy 1 (DOM 2025): data-testid="rt-name-link" dentro de <th scope="row">
          2. Strategy 2 (legacy fallback): data-testid="room-block" / "room-type-title"

                Retorna: List[Dict] con claves:
          - name        : str  — nombre del tipo de habitación
          - description : str  — info de camas (puede ser vacía)
          - facilities  : []   — siempre vacío (requiere clic en cada fila)
          - adults      : None — OMITIDO: requiere parámetros de fecha en URL
          - children    : None — OMITIDO: requiere parámetros de fecha en URL
          - images      : []   — OMITIDO: requiere navegación de galería separada
          - info        : None — OMITIDO: no disponible en DOM estático

        CONSTRAINT (Build 80): adults/children/price_range/rooms_quantity
          NO se extraen en esta versión. Requieren ?checkin=&checkout= en URL.
          Las columnas existen en el schema para compatibilidad con el ORM.
        """
        rooms: List[Dict[str, Any]] = []
        seen_names: set = set()

        try:
            # ── Strategy 1: rt-name-link dentro de <th scope="row"> (DOM 2025) ──
            name_links = self.soup.find_all(attrs={"data-testid": "rt-name-link"})

            if name_links:
                for link_el in name_links:
                    name = link_el.get_text(" ", strip=True)
                    if not name or len(name) > 256 or name in seen_names:
                        continue
                    seen_names.add(name)

                    # Bed description: <th scope="row"> parent → span.d7a50099f7
                    description = ""
                    th_el = link_el.find_parent("th", attrs={"scope": "row"})
                    if th_el:
                        bed_spans = th_el.find_all("span", class_=re.compile(r"d7a50099f7"))
                        if bed_spans:
                            bed_parts: List[str] = []
                            for s in bed_spans:
                                t = s.get_text(" ", strip=True)
                                if t and len(t) < 256:
                                    bed_parts.append(t)
                            # Join: "1 extra-large double bed and 1 sofa bed"
                            if bed_parts:
                                # Read connector words ("and", "oder", "e", "et", "y")
                                connectors = th_el.find_all(
                                    class_=re.compile(r"ee6184f499")
                                )
                                conn_texts = [c.get_text(strip=True) for c in connectors
                                              if c.get_text(strip=True)]
                                if conn_texts and len(bed_parts) > 1:
                                    parts_joined: List[str] = [bed_parts[0]]
                                    for idx, conn in enumerate(conn_texts):
                                        if idx + 1 < len(bed_parts):
                                            parts_joined.append(conn)
                                            parts_joined.append(bed_parts[idx + 1])
                                    description = " ".join(parts_joined)
                                else:
                                    description = ", ".join(bed_parts)

                    # CONSTRAINT (Build 80): adults/children/images/info are NULL/[]
                    # because these fields require date params in URL to render.
                    # The schema columns exist (GAP-SCHEMA-002-FIX) to prevent
                    # UndefinedColumn, but values are intentionally omitted here.
                    rooms.append({
                        "name":        name,
                        "description": description[:512] if description else "",
                        "facilities":  [],
                        "adults":      None,
                        "children":    None,
                        "images":      [],
                        "info":        None,
                    })

                logger.debug(
                    "RoomTypes (strategy1/rt-name-link): extracted %d lang=%s",
                    len(rooms), self.language
                )

            else:
                # ── Strategy 2: legacy room-block / room-type-title fallback ──
                blocks = self.soup.find_all(attrs={"data-testid": "room-block"})
                if not blocks:
                    logger.warning(
                        "RoomTypes: no rt-name-link nor room-block elements found "
                        "lang=%s — DOM may have changed", self.language
                    )
                    return rooms

                for block in blocks:
                    name_el = block.find(attrs={"data-testid": "room-type-title"})
                    if not name_el:
                        continue
                    name = name_el.get_text(" ", strip=True)
                    if not name or len(name) > 256 or name in seen_names:
                        continue
                    seen_names.add(name)

                    desc_el = block.find(attrs={"data-testid": "room-description"})
                    description = desc_el.get_text(" ", strip=True) if desc_el else ""

                    fac_container = block.find(attrs={"data-testid": "room-facilities"})
                    facilities: List[str] = []
                    if fac_container:
                        for span in fac_container.find_all("span"):
                            fac_text = span.get_text(" ", strip=True)
                            if fac_text and len(fac_text) < 256:
                                facilities.append(fac_text)

                    # GAP-SCHEMA-002-FIX (Build 80): include adults/children/images/info
                    rooms.append({
                        "name":        name,
                        "description": description,
                        "facilities":  facilities,
                        "adults":      None,
                        "children":    None,
                        "images":      [],
                        "info":        None,
                    })

                logger.debug(
                    "RoomTypes (strategy2/room-block): extracted %d lang=%s",
                    len(rooms), self.language
                )

        except Exception as exc:
            logger.warning("RoomTypes extraction failed lang=%s: %s", self.language, exc)

        return rooms

    # =========================================================================
    # STRUCT-015 (v53): FAQs EXTRACTOR
    # =========================================================================

    def _extract_faqs(self) -> List[Dict[str, str]]:
        """
        STRUCT-015 (v53): Extrae las preguntas frecuentes (FAQ) del hotel.

        BUG-FAQ-ANSWERS (v56): ahora retorna List[Dict[str, str]] con claves
        'ask' (pregunta) y 'answer' (respuesta del accordion).

        Estructura DOM típica (Booking.com React, accordion):
          <div data-testid="faq-section">
            <div>
              <h3>Frequently asked questions</h3>
              <div>
                <button aria-expanded="false">
                  What are the check-in and check-out times at Garden Hill Resort?
                </button>
                <div>Check-in is from 3:00 PM...</div>  <!-- respuesta — ahora capturada -->
              </div>
              <div>
                <button>Is there a swimming pool at Garden Hill Resort?</button>
              </div>
            </div>
          </div>

        Estrategias de localización:
          1. data-testid con "faq"
          2. class pattern: faq, frequently-asked
          3. Heading con keyword FAQ por idioma
          4. Botones de accordion con texto de pregunta (contienen "?")

        Retorna: lista de dicts {'ask': str, 'answer': str}, deduplicados por ask.
        """
        faqs: List[Dict[str, str]] = []
        seen: set = set()

        def _add_question(text: str, answer_text: str = "") -> None:
            # BUG-FAQ-ANSWERS (v56): captura también la respuesta del accordion
            t = text.strip()
            if t and len(t) > 5 and len(t) < 1000 and t not in seen:
                seen.add(t)
                faqs.append({"ask": t, "answer": answer_text.strip()})

        # ── Keywords de heading FAQ por idioma ────────────────────────────────
        _FAQ_KEYWORDS: Dict[str, List[str]] = {
            "en": ["frequently asked questions", "faqs", "faq"],
            "es": ["preguntas frecuentes", "preguntas más frecuentes"],
            "de": ["häufig gestellte fragen", "faq"],
            "fr": ["questions fréquentes", "foire aux questions", "faq"],
            "it": ["domande frequenti", "faq"],
            "nl": ["veelgestelde vragen", "faq"],
            "pt": ["perguntas frequentes", "faq"],
            "ja": ["よくあるご質問", "faq"],
            "zh": ["常见问题", "faq"],
            "ar": ["الأسئلة الشائعة", "faq"],
            "ko": ["자주 묻는 질문", "faq"],
            "ru": ["часто задаваемые вопросы", "faq"],
        }

        section = None

        # Intento 1: data-testid con "faq"
        try:
            section = self.soup.find(
                attrs={"data-testid": re.compile(r"faq", re.I)}
            )
        except Exception:
            pass

        # Intento 2: class con "faq"
        if not section:
            try:
                section = self.soup.find(
                    attrs={"class": re.compile(r"faq|frequently.asked", re.I)}
                )
            except Exception:
                pass

        # Intento 3: buscar por keyword de heading
        if not section:
            lang_key = self.language[:2].lower()
            keywords = (
                _FAQ_KEYWORDS.get(lang_key, []) +
                _FAQ_KEYWORDS.get("en", [])
            )
            for kw in keywords:
                try:
                    el = self.soup.find(
                        ["h2", "h3", "h4", "div", "span"],
                        string=re.compile(re.escape(kw), re.I | re.UNICODE),
                    )
                    if el:
                        # Subir al contenedor padre que contiene preguntas
                        parent = el.parent
                        if parent:
                            buttons = parent.find_all(["button", "dt", "summary"])
                            if buttons:
                                section = parent
                                break
                            elif parent.parent:
                                buttons = parent.parent.find_all(["button", "dt", "summary"])
                                if buttons:
                                    section = parent.parent
                                    break
                except Exception:
                    continue

        if section:
            # Extraer preguntas de botones de accordion, <dt>, <summary>
            try:
                # Patrón 1: botones de accordion (pregunta) + div hermano (respuesta)
                # BUG-FAQ-ANSWERS (v56): extrae el div siguiente al botón como respuesta
                for btn in section.find_all(["button", "dt", "summary"]):
                    text = btn.get_text(" ", strip=True)
                    text = re.sub(r'\s+', ' ', text).strip()
                    # Criterio: texto razonable (tiene contenido mínimo)
                    if text and len(text) > 5 and len(text) < 1000:
                        # Buscar respuesta en el siguiente sibling div/dd/p
                        answer_text = ""
                        try:
                            next_sib = btn.find_next_sibling(["div", "dd", "p"])
                            if next_sib:
                                answer_text = re.sub(r'\s+', ' ', next_sib.get_text(" ", strip=True)).strip()
                                # Sanity check: descartamos respuestas que parezcan otra pregunta
                                if len(answer_text) > 2000:
                                    answer_text = answer_text[:2000]
                        except Exception:
                            answer_text = ""
                        _add_question(text, answer_text)

                if faqs:
                    logger.debug(
                        "FAQs: extracted %d questions via accordion buttons lang=%s",
                        len(faqs), self.language,
                    )
                    return faqs

                # Patrón 2: headings dentro de la sección FAQ
                for hdr in section.find_all(["h3", "h4", "h5", "strong"]):
                    text = hdr.get_text(strip=True)
                    # Filtrar: no incluir el título de la sección FAQ
                    lang_key = self.language[:2].lower()
                    faq_title_words = {"faq", "frequently", "preguntas", "domande",
                                       "häufig", "questions", "veelgestelde",
                                       "perguntas", "よくある", "常见"}
                    is_section_title = any(
                        w in text.lower() for w in faq_title_words
                    )
                    if text and len(text) > 5 and not is_section_title:
                        _add_question(text, "")  # answer not available from headings

                if faqs:
                    logger.debug(
                        "FAQs: extracted %d questions via headings lang=%s",
                        len(faqs), self.language,
                    )

            except Exception as exc:
                logger.debug("FAQs section parse error lang=%s: %s", self.language, exc)

        # Estrategia global: buscar botones accordion con preguntas en toda la página
        if not faqs:
            try:
                # Buscar divs con patrón accordion (aria-controls o aria-expanded)
                accordion_triggers = self.soup.find_all(
                    True,
                    attrs={
                        "aria-expanded": True,
                    },
                )
                for trigger in accordion_triggers:
                    text = trigger.get_text(" ", strip=True)
                    text = re.sub(r'\s+', ' ', text).strip()
                    # Heurística: preguntas frecuentes suelen ser frases relativamente largas
                    if text and 10 < len(text) < 500:
                        _add_question(text, "")  # answer not available from global scan

                if faqs:
                    logger.debug(
                        "FAQs: extracted %d questions via aria-expanded global scan lang=%s",
                        len(faqs), self.language,
                    )
            except Exception as exc:
                logger.debug("FAQs global scan failed lang=%s: %s", self.language, exc)

        return faqs

    # =========================================================================
    # STRUCT-016 (v53): GUEST REVIEWS EXTRACTOR
    # =========================================================================

    def _extract_guest_reviews(self) -> List[Dict[str, str]]:
        """
        STRUCT-016 (v53): Extrae las categorías de valoración de huéspedes.

        Booking.com muestra puntuaciones por categorías en el bloque de reseñas:
          - Cleanliness / Limpieza
          - Comfort / Confort
          - Location / Ubicación
          - Facilities / Instalaciones
          - Staff / Personal
          - Value for money / Relación calidad-precio
          - WiFi / Free WiFi
          (el número y nombre de categorías varía según el idioma)

        Estructura DOM típica:
          <div data-testid="review-score-badge">
            <div>
              <span class="...">Cleanliness</span>
              <span class="...">9.5</span>
            </div>
            <div>
              <span>Comfort</span>
              <span>9.2</span>
            </div>
          </div>

        Retorna: lista de dicts [{reviews_categories: str, reviews_score: str}, ...]
                 Una entrada por categoría, deduplicada.
        """
        reviews: List[Dict[str, str]] = []
        seen_cats: set = set()

        def _add_review(category: str, score: str) -> None:
            cat = category.strip()
            sc = score.strip()
            if cat and len(cat) < 256 and cat not in seen_cats:
                seen_cats.add(cat)
                reviews.append({
                    "reviews_categories": cat,
                    "reviews_score": sc or None,  # type: ignore[dict-item]
                })

        # ── Selectores para el bloque de review categories ────────────────────
        # BUG-EXTR-010 (v55): Booking.com React usa data-testid="review-subscore"
        # para cada categoría de reseña. El DOM contiene:
        #   <div data-testid="review-subscore" aria-label="Average rating out of 10">
        #     <div>
        #       <span class="d96a4619c0">Staff </span>       ← categoría
        #       <div aria-hidden="true" class="... f87e152973">9.1</div>  ← score visible
        #     </div>
        #     <div role="meter" aria-valuetext="9.1" ...>     ← score programático
        #   </div>
        _REVIEW_SELECTORS = [
            # v55: selector correcto basado en DOM real de Booking.com
            {"attrs": {"data-testid": "review-subscore"}},
            # Fallbacks legacy
            {"attrs": {"data-testid": re.compile(r"review.score|reviewScore", re.I)}},
            {"attrs": {"data-testid": re.compile(r"review.category|review.breakdown", re.I)}},
            {"attrs": {"class": re.compile(r"review.score.widget|reviewScoreWidget", re.I)}},
            {"attrs": {"class": re.compile(r"review.breakdown|reviewBreakdown", re.I)}},
            {"attrs": {"id": re.compile(r"review.score|review.breakdown", re.I)}},
        ]

        # ── Estrategia 0 (v55): data-testid="review-subscore" directo ────────
        # Busca TODOS los elementos con data-testid="review-subscore" en la página.
        # Cada uno es una categoría individual (Staff, Cleanliness, Comfort, etc.)
        try:
            subscore_items = self.soup.find_all(
                attrs={"data-testid": "review-subscore"}
            )
            if subscore_items:
                for item in subscore_items:
                    cat_text = ""
                    score_text = ""

                    # Extraer categoría: span dentro del subscore con texto de categoría
                    cat_span = item.find("span")
                    if cat_span:
                        cat_text = cat_span.get_text(strip=True)

                    # Extraer score: preferir aria-valuetext del meter (más fiable)
                    meter = item.find(attrs={"role": "meter"})
                    if meter:
                        score_text = meter.get("aria-valuetext", "")

                    # Fallback score: div con aria-hidden="true" que contiene el número
                    if not score_text:
                        score_div = item.find(attrs={"aria-hidden": "true"})
                        if score_div:
                            score_text = score_div.get_text(strip=True)

                    # Fallback score: buscar texto numérico en cualquier hijo
                    if not score_text:
                        for child in item.find_all(True, recursive=True):
                            child_text = child.get_text(strip=True)
                            if child_text and re.match(r'^\d+[.,]?\d*$', child_text.replace(',', '.')):
                                score_text = child_text
                                break

                    if cat_text and len(cat_text) < 128:
                        # Normalizar score: reemplazar coma decimal por punto
                        if score_text:
                            score_text = score_text.replace(",", ".")
                        _add_review(cat_text, score_text)

                if reviews:
                    logger.debug(
                        "GuestReviews: extracted %d via review-subscore data-testid lang=%s",
                        len(reviews), self.language,
                    )
                    return reviews

        except Exception as exc:
            logger.debug("GuestReviews review-subscore extraction failed lang=%s: %s", self.language, exc)

        section = None
        for sel in _REVIEW_SELECTORS[1:]:  # Skip first (already tried above)
            try:
                section = self.soup.find(True, **sel)  # type: ignore[arg-type]
                if section:
                    break
            except Exception:
                continue

        if section:
            try:
                # Patrón 1: pares de spans adyacentes (categoría + puntuación)
                # Buscar divs/li que contengan exactamente 2 spans relevantes
                for container in section.find_all(["div", "li", "p"], recursive=True):
                    spans = container.find_all("span", recursive=False)
                    if len(spans) >= 2:
                        cat_text = spans[0].get_text(strip=True)
                        score_text = spans[1].get_text(strip=True)
                        # Validar: categoría es texto alfanumérico, score es numérico
                        if (
                            cat_text
                            and score_text
                            and len(cat_text) < 128
                            and re.match(r'^\d+[.,]?\d*$', score_text.replace(',', '.'))
                        ):
                            _add_review(cat_text, score_text)

                if reviews:
                    logger.debug(
                        "GuestReviews: extracted %d categories via span pairs lang=%s",
                        len(reviews), self.language,
                    )
                    return reviews

                # Patrón 2: elementos con data-testid="review-score-right-component"
                # o similar, buscar label + valor
                for item in section.find_all(True, recursive=True):
                    testid = item.get("data-testid", "")
                    if re.search(r"review.score.component|score.component", str(testid), re.I):
                        children = [c for c in item.children if hasattr(c, 'get_text')]
                        texts = [c.get_text(strip=True) for c in children if c.get_text(strip=True)]
                        if len(texts) >= 2:
                            cat_text = texts[0]
                            score_text = texts[-1]
                            if cat_text and len(cat_text) < 128:
                                _add_review(cat_text, score_text)

                if reviews:
                    logger.debug(
                        "GuestReviews: extracted %d via score component data-testid lang=%s",
                        len(reviews), self.language,
                    )

            except Exception as exc:
                logger.debug("GuestReviews section parse error lang=%s: %s", self.language, exc)

        # Estrategia fallback: buscar en toda la página con data-testid de review
        if not reviews:
            try:
                items = self.soup.find_all(
                    True,
                    attrs={"data-testid": re.compile(r"review.score.category|score.bar", re.I)},
                )
                for item in items:
                    all_spans = item.find_all("span")
                    texts = [s.get_text(strip=True) for s in all_spans if s.get_text(strip=True)]
                    if len(texts) >= 2:
                        cat_text = texts[0]
                        score_text = texts[-1]
                        if cat_text and len(cat_text) < 128:
                            _add_review(cat_text, score_text)

                if reviews:
                    logger.debug(
                        "GuestReviews: extracted %d via fallback data-testid scan lang=%s",
                        len(reviews), self.language,
                    )
            except Exception as exc:
                logger.debug("GuestReviews fallback scan failed lang=%s: %s", self.language, exc)

        return reviews

    # =========================================================================
    # STRUCT-017 (v53): PROPERTY HIGHLIGHTS EXTRACTOR
    # =========================================================================

    def _extract_property_highlights(self) -> Optional[List[Dict[str, str]]]:
        """
        STRUCT-017 (v59 — FIX-PH-SELECTOR-001 + FIX-PH-STRUCTURE-001):
        Extrae los highlights de propiedad con estructura categoría/detalle.

        CAMBIOS v59 respecto a v58:
          - Tipo de retorno cambiado: str (HTML blob) → List[Dict[str, str]]
            Cada dict tiene 'category' (nombre del grupo) y 'detail' (ítem individual).
          - Estrategia 0 (nueva, PRIORITARIA): selector real del DOM validado contra
            HTML de prueba del hotel Manaus Millennium (Build 58).
            Ruta: #hp_facilities_box > div > section > div >
                  div[data-testid=property-section--content] > div.e43cb5a00e
          - Estrategias 1-3: selectores data-testid y class como fallback.
          - Estrategia 4 (nueva): keyword por idioma en heading.
          - Parser normalizado: extrae categorías (h3/h4/div.categoria) con sus
            ítems de lista (<li>) para generar pares category/detail.

        Estructura retornada:
          [
            {"category": "Ideal para tu estancia", "detail": "Baño privado"},
            {"category": "Ideal para tu estancia", "detail": "Parking"},
            {"category": "Baño",                   "detail": "Secador de pelo"},
            ...
          ]

        Retorna: lista de dicts o None si no se encontró la sección / estaba vacía.
        """
        # ── Selectores por prioridad ──────────────────────────────────────────
        # Estrategia 0: ruta real del DOM confirmada en HTML de prueba Build 58.
        # #hp_facilities_box → section → div[data-testid=property-section--content]
        # → div.e43cb5a00e  (contenedor de highlights con grupos categoría/ítem)
        section = None

        # ── LEGACY: div.property-highlights (estructura server-rendered) ─────
        # FIX-PH-LEGACY-001 (Build 63-fix):
        #   El HTML real de Booking.com usa la estructura server-rendered legacy:
        #     <div class="property-highlights ph-icon-fill-color">
        #       <h3>Property highlights</h3>
        #       <div class="ph-sections">
        #         <div class="ph-section">
        #           <h4 class="ph-item-header">Breakfast info</h4>
        #           <p class="ph-item">Buffet</p>
        #         </div>
        #   Las estrategias 0-3 buscan la estructura React (e43cb5a00e /
        #   data-testid="property-highlights") que está vacía en estas páginas.
        #   Validado contra: _HTML-view-source__manaus-hoteis-millennium_en-gb.
        ph_legacy = self.soup.find(
            attrs={"class": lambda c: c and "property-highlights" in c}
        )
        if ph_legacy:
            ph_sections = ph_legacy.find_all(class_="ph-section")
            if ph_sections:
                logger.debug(
                    "PropertyHighlights: found via legacy div.property-highlights "
                    "with %d ph-section(s) lang=%s",
                    len(ph_sections), self.language,
                )
                _results_leg: List[Dict[str, str]] = []
                _seen_leg: set = set()
                for _sec in ph_sections:
                    _header_el = _sec.find(class_="ph-item-header")
                    if _header_el:
                        _category = _header_el.get_text(strip=True)
                    else:
                        _copy_el = _sec.find(
                            attrs={"class": lambda c: c and
                                   any("ph-item-copy-" in _cls
                                       for _cls in (c if isinstance(c, list) else [c]))}
                        )
                        if _copy_el:
                            _cls_name = next(
                                (_cls for _cls in (_copy_el.get("class") or [])
                                 if "ph-item-copy-" in _cls), ""
                            )
                            _category = _cls_name.replace(
                                "ph-item-copy-", "").replace("-", " ").title()
                        else:
                            _category = "Property Highlights"
                    _item_p = _sec.find("p", class_="ph-item")
                    _detail = (_item_p.get_text(strip=True)
                               if _item_p else _sec.get_text(strip=True))
                    if _category and _detail and _category != _detail:
                        _key = (_category, _detail)
                        if _key not in _seen_leg and len(_detail) <= 512:
                            _seen_leg.add(_key)
                            _results_leg.append({"category": _category, "detail": _detail})
                    elif _detail:
                        _key = ("", _detail)
                        if _key not in _seen_leg and len(_detail) <= 512:
                            _seen_leg.add(_key)
                            _results_leg.append({"category": "", "detail": _detail})
                if _results_leg:
                    logger.debug(
                        "PropertyHighlights LEGACY extracted for lang=%s: %d items",
                        self.language, len(_results_leg),
                    )
                    return _results_leg


        facilities_box = self.soup.find(id="hp_facilities_box")
        if facilities_box:
            section_content = facilities_box.find(
                attrs={"data-testid": "property-section--content"}
            )
            if section_content:
                hl_container = section_content.find(
                    attrs={"class": lambda c: c and "e43cb5a00e" in c}
                )
                if hl_container:
                    section = hl_container
                    logger.debug(
                        "PropertyHighlights: found via hp_facilities_box path lang=%s",
                        self.language,
                    )

        # Estrategia 1: data-testid variants (legacy / futuras versiones DOM)
        if not section:
            _HIGHLIGHT_SELECTORS = [
                {"attrs": {"data-testid": "property-highlights"}},
                {"attrs": {"data-testid": re.compile(r"property.highlight|highlights", re.I)}},
                {"attrs": {"class": re.compile(r"property.highlight|propertyHighlight", re.I)}},
                {"attrs": {"id": re.compile(r"property.highlight|highlights", re.I)}},
            ]
            for sel in _HIGHLIGHT_SELECTORS:
                try:
                    section = self.soup.find(True, **sel)  # type: ignore[arg-type]
                    if section:
                        logger.debug(
                            "PropertyHighlights: found via selector %s lang=%s", sel, self.language
                        )
                        break
                except Exception:
                    continue

        # Estrategia 2: keyword en heading por idioma
        if not section:
            _HL_KEYWORDS: Dict[str, List[str]] = {
                "en": ["property highlights", "highlights", "top features"],
                "es": ["aspectos destacados", "destacados del alojamiento", "puntos fuertes"],
                "de": ["highlights", "besonderheiten", "höhepunkte"],
                "fr": ["points forts", "atouts", "points forts du logement"],
                "it": ["punti di forza", "highlights", "caratteristiche principali"],
                "nl": ["hoogtepunten", "highlights", "troeven"],
                "pt": ["destaques", "pontos fortes"],
                "ja": ["ハイライト", "特徴"],
                "zh": ["亮点", "特色"],
                "ar": ["أبرز الميزات", "المميزات"],
                "ko": ["하이라이트", "특징"],
                "ru": ["особенности", "highlights"],
            }
            lang_key = self.language[:2].lower()
            keywords = (
                _HL_KEYWORDS.get(lang_key, []) +
                _HL_KEYWORDS.get("en", [])
            )
            for kw in keywords:
                try:
                    el = self.soup.find(
                        ["h2", "h3", "h4", "div", "span"],
                        string=re.compile(re.escape(kw), re.I | re.UNICODE),
                    )
                    if el:
                        parent = el.parent
                        if parent and parent.find(["ul", "li"]):
                            section = parent
                            logger.debug(
                                "PropertyHighlights: found via keyword %r lang=%s", kw, self.language
                            )
                            break
                        elif parent and parent.parent and parent.parent.find(["ul", "li"]):
                            section = parent.parent
                            logger.debug(
                                "PropertyHighlights: found via keyword %r (grandparent) lang=%s",
                                kw, self.language,
                            )
                            break
                except Exception:
                    continue

        if not section:
            logger.debug("PropertyHighlights: section not found for lang=%s", self.language)
            return None

        # ── Parser categoría / detalle ────────────────────────────────────────
        try:
            results: List[Dict[str, str]] = []
            seen: set = set()

            # Buscar grupos de categoría: elementos que contengan una etiqueta
            # de título y una lista de ítems subordinados.
            # Estructura típica de Booking.com:
            #   <div>                          ← grupo de categoría
            #     <div>Ideal para tu estancia</div>  ← nombre de categoría
            #     <ul><li>Baño privado</li>...</ul>  ← ítems
            #   </div>
            groups = section.find_all(recursive=False)
            if not groups:
                # Si no hay hijos directos con esa estructura, intentar un nivel más
                groups = section.find_all(["div", "section", "article"])

            for group in groups:
                # Determinar nombre de categoría: primer texto de heading o div
                category_text = ""
                category_el = group.find(["h3", "h4", "h5"])
                if not category_el:
                    # Buscar el primer div/span que solo contenga texto (sin <ul>/<li>)
                    for el in group.find_all(["div", "span"], recursive=False):
                        candidate = el.get_text(strip=True)
                        if candidate and not el.find(["ul", "li", "ol"]):
                            category_text = candidate
                            break
                else:
                    category_text = category_el.get_text(strip=True)

                if not category_text:
                    continue

                # Extraer ítems de lista
                items_found = False
                for li in group.find_all("li"):
                    detail = li.get_text(strip=True)
                    if not detail or detail == category_text:
                        continue
                    key = (category_text, detail)
                    if key not in seen and len(detail) <= 512:
                        seen.add(key)
                        results.append({"category": category_text, "detail": detail})
                        items_found = True

                # Fallback: si no hay <li>, tratar los div/p hijos como ítems
                if not items_found:
                    for child in group.find_all(["div", "p"], recursive=False):
                        detail = child.get_text(strip=True)
                        if (not detail or detail == category_text
                                or child.find(["ul", "li"])):
                            continue
                        key = (category_text, detail)
                        if key not in seen and len(detail) <= 512:
                            seen.add(key)
                            results.append({"category": category_text, "detail": detail})

            if not results:
                # Último fallback: extraer todos los <li> sin categoría
                for li in section.find_all("li"):
                    detail = li.get_text(strip=True)
                    if detail and len(detail) <= 512:
                        key = ("", detail)
                        if key not in seen:
                            seen.add(key)
                            results.append({"category": "", "detail": detail})

            if not results:
                logger.debug(
                    "PropertyHighlights: no items extracted for lang=%s", self.language
                )
                return None

            logger.debug(
                "PropertyHighlights extracted for lang=%s: %d items",
                self.language, len(results),
            )
            return results

        except Exception as exc:
            logger.debug(
                "PropertyHighlights parse error for lang=%s: %s", self.language, exc
            )
            return None


    # =========================================================================
    # STRUCT-019 (v76): PRICE RANGE EXTRACTOR
    # =========================================================================

    def _extract_price_range(self) -> Optional[str]:
        """
        STRUCT-019 (v76): Extrae el precio visible en la sección de disponibilidad.

        ⚠ LIMITACIÓN ARQUITECTÓNICA:
        Booking.com solo muestra precios cuando la URL incluye parámetros de
        selección de fechas (?checkin=YYYY-MM-DD&checkout=YYYY-MM-DD). En el
        scraping estático de páginas de hotel sin fechas, este campo será NULL.
        El valor, cuando existe, puede ser el precio mínimo de la primera noche.

        Selectores en orden de prioridad:
          1. data-testid="price-and-discounted-price" — precio React actual
          2. data-testid="availability-rate-information" — bloque de disponibilidad
          3. Clases BUI legacy (bui-price-display__value, prco-valign-middle-helper)
             — pueden no estar presentes en DOM React actual.

        Retorna: str con el texto del precio (e.g. "€ 89", "USD 120"), o None.
        """
        # Strategy 1: React primary selector
        try:
            el = self.soup.find(attrs={"data-testid": "price-and-discounted-price"})
            if el:
                text = el.get_text(" ", strip=True)
                if text and len(text) < 64:
                    logger.debug("PriceRange: strategy1 lang=%s: %r", self.language, text)
                    return text
        except Exception as exc:
            logger.debug("PriceRange strategy1 failed lang=%s: %s", self.language, exc)

        # Strategy 2: availability rate block
        try:
            el = self.soup.find(attrs={"data-testid": "availability-rate-information"})
            if el:
                span = el.find("span")
                if span:
                    text = span.get_text(" ", strip=True)
                    if text and len(text) < 64:
                        logger.debug("PriceRange: strategy2 lang=%s: %r", self.language, text)
                        return text
        except Exception as exc:
            logger.debug("PriceRange strategy2 failed lang=%s: %s", self.language, exc)

        # Strategy 3: BUI class fallbacks (legacy)
        for class_name in ["bui-price-display__value", "prco-valign-middle-helper"]:
            try:
                el = self.soup.find(class_=class_name)
                if el:
                    text = el.get_text(" ", strip=True)
                    if text and len(text) < 64:
                        logger.debug("PriceRange: BUI fallback %s lang=%s: %r",
                                     class_name, self.language, text)
                        return text
            except Exception:
                pass

        logger.debug("PriceRange: not found lang=%s (expected if no date params in URL)",
                     self.language)
        return None

    # =========================================================================
    # STRUCT-020 (v76): ROOMS QUANTITY EXTRACTOR
    # =========================================================================

    def _extract_rooms_quantity(self) -> Optional[int]:
        """
        STRUCT-020 (v76): Extrae el número de tipos de habitación visibles.

        ⚠ NOTA SEMÁNTICA:
        Este campo cuenta los TIPOS de habitación que Booking.com muestra
        en la sección de disponibilidad, NO el total de habitaciones físicas
        del hotel. Para el número físico de habitaciones, consultar JSON-LD
        numberOfRooms cuando esté disponible.

        Estrategias:
          1. JSON-LD numberOfRooms (más preciso — número físico real)
          2. Conteo de data-testid="room-block" (número de tipos en DOM)
          3. Última opción del select[name="nr_rooms"] (max seleccionable)

        Retorna: int >= 0 o None si no disponible.
        """
        # Strategy 1: JSON-LD numberOfRooms
        try:
            jsonld = self._get_jsonld()
            if jsonld:
                n = jsonld.get("numberOfRooms")
                if n is not None:
                    val = int(n)
                    if val > 0:
                        logger.debug("RoomsQuantity: JSON-LD numberOfRooms=%d lang=%s",
                                     val, self.language)
                        return val
        except Exception as exc:
            logger.debug("RoomsQuantity strategy1 (JSON-LD) failed lang=%s: %s",
                         self.language, exc)

        # Strategy 2: count room-block elements
        try:
            blocks = self.soup.find_all(attrs={"data-testid": "room-block"})
            if blocks:
                count = len(blocks)
                logger.debug("RoomsQuantity: %d room-block elements lang=%s",
                             count, self.language)
                return count
        except Exception as exc:
            logger.debug("RoomsQuantity strategy2 (room-block) failed lang=%s: %s",
                         self.language, exc)

        # Strategy 3: select[name="nr_rooms"] — max value option
        try:
            sel = self.soup.find("select", {"name": "nr_rooms"})
            if sel:
                options = sel.find_all("option")
                if options:
                    last_val = options[-1].get("value", "0")
                    val = int(last_val)
                    if val > 0:
                        logger.debug("RoomsQuantity: nr_rooms select max=%d lang=%s",
                                     val, self.language)
                        return val
        except Exception as exc:
            logger.debug("RoomsQuantity strategy3 (select) failed lang=%s: %s",
                         self.language, exc)

        return None

    # =========================================================================
    # STRUCT-021 (v76): EXTRA INFO EXTRACTOR
    # =========================================================================

    def _extract_extra_info(self) -> Optional[str]:
        """
        STRUCT-021 (v76): Extrae el bloque "Good to know" / "Información importante".

        ⚠ DIFERENCIA CON FINE PRINT:
        Fine Print (hotels_fine_print) extrae la sección "Fine Print" / "Letra pequeña".
        Extra info extrae "property-important-info" — sección distinta que aparece
        antes del Fine Print y contiene información práctica del alojamiento.

        Selectores en orden de prioridad:
          1. data-testid="property-important-info" — bloque React principal
          2. data-testid="house-rules" — reglas de la casa (alternativo)
          3. id="hotelPoliciesInc" — legacy
          4. class regex "hp--important_info" — legacy

        Retorna: str con el texto plano del bloque, o None.
        """
        # Strategy 1: property-important-info React block
        try:
            el = self.soup.find(attrs={"data-testid": "property-important-info"})
            if el:
                text = el.get_text(" ", strip=True)
                if text and len(text) > 10:
                    logger.debug("ExtraInfo: strategy1 (property-important-info) "
                                 "len=%d lang=%s", len(text), self.language)
                    return text
        except Exception as exc:
            logger.debug("ExtraInfo strategy1 failed lang=%s: %s", self.language, exc)

        # Strategy 2: house-rules block
        try:
            el = self.soup.find(attrs={"data-testid": "house-rules"})
            if el:
                text = el.get_text(" ", strip=True)
                if text and len(text) > 10:
                    logger.debug("ExtraInfo: strategy2 (house-rules) "
                                 "len=%d lang=%s", len(text), self.language)
                    return text
        except Exception as exc:
            logger.debug("ExtraInfo strategy2 failed lang=%s: %s", self.language, exc)

        # Strategy 3: legacy id
        try:
            el = self.soup.find(id="hotelPoliciesInc")
            if el:
                text = el.get_text(" ", strip=True)
                if text and len(text) > 10:
                    logger.debug("ExtraInfo: strategy3 (hotelPoliciesInc) lang=%s", self.language)
                    return text
        except Exception as exc:
            logger.debug("ExtraInfo strategy3 failed lang=%s: %s", self.language, exc)

        # Strategy 4: legacy class
        try:
            el = self.soup.find(True, class_=re.compile(r"hp--important_info", re.I))
            if el:
                text = el.get_text(" ", strip=True)
                if text and len(text) > 10:
                    logger.debug("ExtraInfo: strategy4 (hp--important_info) lang=%s", self.language)
                    return text
        except Exception as exc:
            logger.debug("ExtraInfo strategy4 failed lang=%s: %s", self.language, exc)

        logger.debug("ExtraInfo: not found lang=%s", self.language)
        return None

    # =========================================================================
    # STRUCT-022 (v76): NEARBY PLACES EXTRACTOR
    # =========================================================================

    def _extract_nearby_places(self) -> List[Dict[str, Any]]:
        """
        STRUCT-022 (v76) — BUG-SELECTOR-NEARBY-001 FIX (Build 77):
        Extrae los lugares de interés cercanos al hotel.

        BUILD-82-FIX (GAP-SCHEMA-003): añade clave 'category_code' (int|None)
        a cada dict. El código se obtiene aplicando _NEARBY_CATEGORY_CODE_MAP
        al valor de 'category' ya inferido del h3 del bloque.
        Códigos: 1=airport 2=restaurant 3=beach 4=transport 5=nature 6=attraction

        DOM REAL verificado contra archivos HTML en pruebas/ (Booking.com React 2025):

          <section id="surroundings_block">
            <div data-testid="poi-block">
              <h3>Top attractions</h3>
              <ul data-testid="poi-block-list">
                <li>
                  <span role="listitem">
                    <div>
                      <div class="...d1bc97eb82">Victoria Clock Tower</div>
                      <div><div class="...cbf0753d0c">3.6 km</div></div>
                    </div>
                  </span>
                </li>
              </ul>
            </div>
          </section>

        Retorna: List[Dict] con claves:
          place_name    : nombre del lugar
          distance      : distancia textual (e.g. "2.1 km")
          category      : categoría texto (e.g. "airport", "attraction")
          category_code : código numérico API (int | None)
        """
        places: List[Dict[str, Any]] = []
        seen: set = set()

        # Mapeo de keywords del h3 → categoría texto normalizada
        _CATEGORY_MAP: List[tuple] = [
            (re.compile(r"airport|aeropuerto|flughafen|aéroport|aeroporto", re.I), "airport"),
            (re.compile(r"restaurant|cafe|bar|food|essen|restaur", re.I),          "restaurant"),
            (re.compile(r"beach|playa|strand|plage|praia|spiaggia", re.I),         "beach"),
            (re.compile(r"transport|transit|bus|metro|tram|train|bahn", re.I),     "transport"),
            (re.compile(r"natural|nature|park|lake|lago|see|montagne|berg", re.I), "nature"),
        ]

        # BUILD-82-FIX (GAP-SCHEMA-003): mapa categoría texto → código numérico API
        _NEARBY_CATEGORY_CODE_MAP: Dict[str, int] = {
            "airport":    1,
            "restaurant": 2,
            "beach":      3,
            "transport":  4,
            "nature":     5,
            "attraction": 6,
        }

        def _infer_category(heading_text: str) -> str:
            for pattern, cat in _CATEGORY_MAP:
                if pattern.search(heading_text):
                    return cat
            return "attraction"

        def _category_code(category_text: str) -> Optional[int]:
            """Convierte categoría texto a código numérico API."""
            return _NEARBY_CATEGORY_CODE_MAP.get(category_text)

        try:
            # Strategy 1: data-testid="poi-block" blocks (real DOM 2025)
            poi_blocks = self.soup.find_all(attrs={"data-testid": "poi-block"})

            if poi_blocks:
                for block in poi_blocks:
                    h_el = block.find(["h3", "h4"])
                    category = _infer_category(h_el.get_text(strip=True) if h_el else "")

                    list_el = block.find(attrs={"data-testid": "poi-block-list"})
                    if not list_el:
                        continue

                    for item in list_el.find_all(lambda t: t.name == "span" and
                                                  t.get("role") == "listitem"):

                        # BUG-NEARBY-001-FIX (Build 83):
                        # DOM real confirmado en pruebas/ HTML:
                        #   <div class="d1bc97eb82">          <- nombre container
                        #     <span class="f0595bb7c6">Restaurant</span>  <- sub-type label
                        #     Ilaafathi Restaurant            <- texto real (text node)
                        #   </div>
                        #   <div class="cbf0753d0c">8 km*</div>  <- distancia
                        #
                        # Fix: localizar div.d1bc97eb82, eliminar span.f0595bb7c6
                        # antes de get_text(). Localizar div.cbf0753d0c para distancia.
                        import copy as _nearby_copy

                        name = ""
                        name_div = item.find("div", class_=re.compile(r"d1bc97eb82"))
                        if name_div:
                            name_div_copy = _nearby_copy.copy(name_div)
                            subtype_span = name_div_copy.find(
                                "span", class_=re.compile(r"f0595bb7c6")
                            )
                            if subtype_span:
                                subtype_span.extract()
                            name = name_div_copy.get_text(strip=True)
                        else:
                            # Fallback: iterate leaf divs, skip distance and containers
                            for div in item.find_all("div", recursive=True):
                                if div.find("div"):  # container, skip
                                    continue
                                text = div.get_text(strip=True)
                                if not text or len(text) <= 2 or len(text) > 256:
                                    continue
                                if re.search(r"^\d+[.,]?\d*\s*(km|m|mi|miles|ft)", text, re.I):
                                    continue
                                name = text
                                break

                        # Distance: div.cbf0753d0c (confirmed class)
                        distance = ""
                        dist_div = item.find("div", class_=re.compile(r"cbf0753d0c"))
                        if dist_div:
                            distance = dist_div.get_text(strip=True)
                        else:
                            for el in item.find_all(
                                string=re.compile(r"\d+[.,]?\d*\s*(km|m|mi|miles|ft)", re.I)
                            ):
                                t = el.strip()
                                if re.search(r"^\d+[.,]?\d*\s*(km|m|mi|miles|ft)\*?$", t, re.I):
                                    distance = t
                                    break

                        if not name or name in seen:
                            continue
                        seen.add(name)

                        places.append({
                            "place_name":    name[:256],
                            "distance":      distance[:64] if distance else "",
                            "category":      category,
                            "category_code": _category_code(category),
                        })

            else:
                # Strategy 2: legacy fallback — location-highlight
                highlights = self.soup.find_all(attrs={"data-testid": "location-highlight"})
                if not highlights:
                    logger.warning(
                        "NearbyPlaces: no poi-block nor location-highlight elements "
                        "found lang=%s — DOM may have changed again", self.language
                    )
                    return places

                for item in highlights:
                    name_el = item.find(["h2", "h3", "h4", "strong"])
                    name = name_el.get_text(strip=True) if name_el else ""
                    if not name or len(name) > 256 or name in seen:
                        continue
                    seen.add(name)

                    distance = ""
                    dist_el = item.find("span", class_=re.compile(r"distance", re.I))
                    if not dist_el:
                        for span in item.find_all("span"):
                            t = span.get_text(strip=True)
                            if re.search(r"\d+[.,]?\d*\s*(km|m|mi|miles|min)", t, re.I):
                                dist_el = span
                                break
                    if dist_el:
                        distance = dist_el.get_text(strip=True)

                    category = ""
                    svg_el = item.find("svg")
                    if svg_el:
                        cat_raw = svg_el.get("data-testid", "")
                        if cat_raw:
                            category = re.sub(r"^icon-", "", cat_raw, flags=re.I)

                    # Normalise legacy text category for code mapping
                    cat_normalised = _infer_category(category) if category else "attraction"

                    places.append({
                        "place_name":    name,
                        "distance":      distance[:64] if distance else "",
                        "category":      category[:128] if category else "",
                        "category_code": _category_code(cat_normalised),  # BUILD-82-FIX
                    })

            if not places:
                logger.warning(
                    "NearbyPlaces: extraction returned 0 places lang=%s", self.language
                )
            else:
                logger.debug(
                    "NearbyPlaces: extracted %d places lang=%s", len(places), self.language
                )

        except Exception as exc:
            logger.warning("NearbyPlaces extraction failed lang=%s: %s", self.language, exc)

        return places
        # BUG-DEAD-CODE-001-FIX (Build 86): Duplicate unreachable implementation
        # of _extract_nearby_places() removed. The block below was an old version
        # of this method (without category_code support) accidentally left after
        # a merge. Python ignores string literals and unreachable code after return,
        # but the 170-line duplicate caused confusion and maintenance risk.

    # =========================================================================
    # STRUCT-024 (v76): SEO META TAGS EXTRACTOR
    # =========================================================================

    def _extract_seo(self) -> Optional[Dict[str, str]]:
        """
        STRUCT-024 (v76): Extrae los meta tags SEO del <head> de la página.

        Campos extraídos:
          seo_description — <meta name="description"> o <meta property="og:description">
          keywords        — <meta name="keywords"> o <meta property="og:keywords">

        Los valores están localizados: cada idioma tiene su propia descripción y
        keywords según el parámetro ?lang= de la URL.

        Retorna: dict con 'seo_description' y/o 'keywords', o None si ambos están vacíos.
        """
        result: Dict[str, str] = {}

        # SEO description
        try:
            desc_el = self.soup.find("meta", {"name": "description"})
            if desc_el and desc_el.get("content"):
                result["seo_description"] = desc_el["content"].strip()
            else:
                og_desc = self.soup.find("meta", {"property": "og:description"})
                if og_desc and og_desc.get("content"):
                    result["seo_description"] = og_desc["content"].strip()
        except Exception as exc:
            logger.debug("SEO description extraction failed lang=%s: %s", self.language, exc)

        # Keywords
        try:
            kw_el = self.soup.find("meta", {"name": "keywords"})
            if kw_el and kw_el.get("content"):
                result["keywords"] = kw_el["content"].strip()
            else:
                og_kw = self.soup.find("meta", {"property": "og:keywords"})
                if og_kw and og_kw.get("content"):
                    result["keywords"] = og_kw["content"].strip()
        except Exception as exc:
            logger.debug("SEO keywords extraction failed lang=%s: %s", self.language, exc)

        if result:
            logger.debug("SEO: extracted fields=%s lang=%s", list(result.keys()), self.language)
            return result

        logger.debug("SEO: no meta tags found lang=%s", self.language)
        return None

    # =========================================================================
    # GAP-SCHEMA-001-FIX (Build 81): INDIVIDUAL GUEST REVIEWS EXTRACTOR
    # =========================================================================

    def _extract_individual_reviews(self) -> List[Dict[str, Any]]:
        """
        GAP-SCHEMA-001-FIX (Build 81): Extrae reseñas textuales individuales
        de huéspedes desde la página de hotel de Booking.com.

        DIFERENCIA CON _extract_guest_reviews():
          _extract_guest_reviews()      → puntuaciones por categoría (Limpieza: 9.3)
          _extract_individual_reviews() → reseñas textuales (nombre + comentario)

        DOM típico de Booking.com (React 2025):
          <div data-testid="review-card">
            <span data-testid="review-author">John D.</span>
            <div data-testid="review-score">9.0</div>
            <div data-testid="review-title">Amazing stay</div>
            <div data-testid="review-positive-text">Clean rooms, friendly staff</div>
            <div data-testid="review-negative-text">Small bathroom</div>
            <div data-testid="review-author-country">United Kingdom</div>
          </div>

        NOTA ARQUITECTÓNICA:
          Booking.com renderiza reseñas individuales en el DOM estático solo
          cuando forman parte del initial payload React. En hoteles con pocas
          reseñas o con paginación JS puede retornar lista vacía — esto es
          comportamiento esperado, no un error del extractor.

        Deduplicación: por (reviewer_name, title, positive_comment).

        Retorna: List[Dict] con claves:
          reviewer_name    : str   | None
          score            : float | None  — 0-10
          title            : str   | None
          positive_comment : str   | None
          negative_comment : str   | None
          reviewer_country : str   | None
          booking_id       : str   | None
        """
        reviews: List[Dict[str, Any]] = []
        seen: set = set()

        try:
            cards = self.soup.find_all(attrs={"data-testid": "review-card"})

            if not cards:
                logger.debug(
                    "IndividualReviews: no review-card elements found lang=%s",
                    self.language,
                )
                return reviews

            for card in cards:
                # ── Reviewer name ─────────────────────────────────────────────
                reviewer_name: Optional[str] = None
                name_el = card.find(attrs={"data-testid": "review-author"})
                if not name_el:
                    name_el = card.find(
                        attrs={"class": re.compile(
                            r"reviewer.*name|author.*name|guest.*name", re.I
                        )}
                    )
                if name_el:
                    reviewer_name = name_el.get_text(strip=True) or None

                # ── Score ─────────────────────────────────────────────────────
                score: Optional[float] = None
                # Primary: aria-label on score badge (e.g. "Scored 9.0")
                score_el = card.find(
                    attrs={"aria-label": re.compile(
                        r"scored|score|rating|puntuaci|bewertet|noté|valutato", re.I
                    )}
                )
                if not score_el:
                    score_el = card.find(
                        attrs={"data-testid": re.compile(r"review.*score|score.*badge", re.I)}
                    )
                if score_el:
                    raw_score = (
                        score_el.get("aria-label", "")
                        or score_el.get_text(strip=True)
                    )
                    m = re.search(r"(\d+[.,]\d+|\d+)", str(raw_score))
                    if m:
                        try:
                            val = float(m.group(1).replace(",", "."))
                            # Normalise: Booking.com scores are 0-10
                            score = val if val <= 10.0 else val / 10.0
                        except ValueError:
                            pass

                # ── Title ─────────────────────────────────────────────────────
                title: Optional[str] = None
                title_el = card.find(attrs={"data-testid": "review-title"})
                if title_el:
                    title = title_el.get_text(strip=True) or None

                # ── Positive comment ──────────────────────────────────────────
                positive_comment: Optional[str] = None
                pos_el = card.find(attrs={"data-testid": "review-positive-text"})
                if not pos_el:
                    pos_el = card.find(
                        attrs={"class": re.compile(r"positive|liked|pos_rev", re.I)}
                    )
                if pos_el:
                    positive_comment = pos_el.get_text(" ", strip=True) or None

                # ── Negative comment ──────────────────────────────────────────
                negative_comment: Optional[str] = None
                neg_el = card.find(attrs={"data-testid": "review-negative-text"})
                if not neg_el:
                    neg_el = card.find(
                        attrs={"class": re.compile(r"negative|disliked|neg_rev", re.I)}
                    )
                if neg_el:
                    negative_comment = neg_el.get_text(" ", strip=True) or None

                # ── Reviewer country ──────────────────────────────────────────
                reviewer_country: Optional[str] = None
                country_el = card.find(attrs={"data-testid": "review-author-country"})
                if not country_el:
                    country_el = card.find(
                        attrs={"class": re.compile(
                            r"reviewer.*country|country.*flag|traveler.*type", re.I
                        )}
                    )
                if country_el:
                    reviewer_country = country_el.get_text(strip=True) or None

                # ── Booking ID ────────────────────────────────────────────────
                booking_id: Optional[str] = None
                bid_el = card.find(
                    attrs={"data-testid": re.compile(r"booking.*id|review.*id", re.I)}
                )
                if bid_el:
                    booking_id = bid_el.get_text(strip=True) or None
                # Fallback: data-review-id HTML attribute
                if not booking_id:
                    rid_el = card.find(attrs={"data-review-id": True})
                    if rid_el:
                        booking_id = str(rid_el.get("data-review-id", "")).strip() or None

                # ── Deduplication ─────────────────────────────────────────────
                key = (reviewer_name, title, positive_comment)
                if key in seen:
                    continue
                seen.add(key)

                reviews.append({
                    "reviewer_name":    reviewer_name,
                    "score":            score,
                    "title":            title,
                    "positive_comment": positive_comment,
                    "negative_comment": negative_comment,
                    "reviewer_country": reviewer_country,
                    "booking_id":       booking_id,
                })

            if reviews:
                logger.debug(
                    "IndividualReviews: extracted %d reviews lang=%s",
                    len(reviews), self.language,
                )
            else:
                # review-card found but yielded no usable data → DOM may differ
                logger.warning(
                    "IndividualReviews: %d review-card elements present but 0 reviews "
                    "extracted lang=%s — DOM selectors may need updating",
                    len(cards), self.language,
                )

        except Exception as exc:
            logger.warning(
                "IndividualReviews extraction failed lang=%s: %s",
                self.language, exc,
            )

        return reviews


# ---------------------------------------------------------------------------
# Compatibility aliases
# ---------------------------------------------------------------------------
# BUG-IMPORT-002 (Build 63-fix):
#   scraper_service.py:44 imports 'BookingExtractor'.
#   The ORM class is defined as 'HotelExtractor'.
#   This alias resolves the ImportError without renaming the class or altering
#   any extraction logic.  Both names reference the same class.
#
# NOTE: This alias was present in the previous delivery and was accidentally
#   dropped when extractor.py was rebuilt from the repo base for FIX-PH-LEGACY-001.
#   Restored here — must always be present at the end of this file.
BookingExtractor = HotelExtractor
