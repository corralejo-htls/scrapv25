"""
api_payload_builder.py — BookingScraper Pro v6.0.0 Build 97
============================================================

BUG-HTML-FP-001-FIX (Build 97):
    _build_to_consider(): fine_print.fp almacena HTML crudo (<p> tags,
    &amp; entidades). La API espera texto plano con saltos \n, no HTML.
    Se añade _html_to_plaintext() que convierte <p>/<br> a \n y limpia
    entidades HTML antes de concatenar los fragmentos.
    Confirmado en payload_villa_dvor_1001.json y _table__hotels_fine_print__.csv:
    toConsider contenía "<p>Guests are required...</p><p>..." en lugar de
    "Guests are required...\nPlease inform...".

BUG-CATMAP-001-FIX (Build 97):
    _CATEGORY_KEY_MAP: 5 variantes reales de Booking.com no estaban mapeadas
    y se descartaban silenciosamente (warning en log, datos perdidos en payload):
      - "kostenfreies wlan"    (DE) → hotel_wifi    (mapa tenía "kostenloses wlan")
      - "relación calidad-precio" (ES) → hotel_value (mapa tenía "precio calidad")
      - "rapporto qualità-prezzo" (IT) → hotel_value (mapa tenía "qualità/prezzo")
      - "situation géographique"  (FR) → hotel_location (mapa tenía "emplacement")
      - "wifi gratuito"           (IT) → hotel_wifi (mapa tenía "wi-fi gratuito")
    Verificado en _table__hotels_guest_reviews__.csv con datos reales de producción.

BUG-LOCALES-EN-001-FIX (Build 97):
    build_payload(): hotel_rows se ordenaban por Hotel.language alfabéticamente
    ('de' < 'en'), produciendo langs = ['de', 'en', ...] con 'de' primero.
    El contrato _API_.md exige 'en' siempre en primer lugar en args.locales
    y en la inserción de los dicts multilingüe. Fix: reordenamiento explícito
    después de la query para garantizar 'en' primero.
    Impacto: GET /hotels/url/{url_id}/api-payload devolvía locales incorrectos;
    api_export_system.py ya tenía en-first pero build_payload() no.

GAP-API-001-FIX (Build 85):
    Implementa ApiPayloadBuilder — servicio que agrega datos de todas las
    tablas de la base de datos por URL y los transforma al formato exacto
    requerido por _API_.md.

    El endpoint GET /hotels/url/{url_id}/api-payload invoca este servicio
    y devuelve un payload JSON listo para consumo externo.

Tablas fuente:
    hotels                     → name, rating, address, geoPosition, scoreReview,
                                  scoreReviewBasedOn, roomsQuantity, accommodationType,
                                  priceRange
    hotels_description         → longDescription
    hotels_all_services        → services (agrupados por service_category)
    hotels_policies            → conditions
    hotels_fine_print          → toConsider (parte 1)
    hotels_legal               → toConsider (parte 2, concatenado)
    image_downloads            → images (URLs de fotos max1280x900)
    hotels_guest_reviews       → categoryScoreReview
    hotels_individual_reviews  → reviews
    hotels_room_types          → rooms
    hotels_nearby_places       → nearbyPlaces
    hotels_faqs                → guestValues
    hotels_seo                 → seoDescription, keywords
    hotels_extra_info          → extraInfo

Mapeo de claves para categoryScoreReview:
    La tabla hotels_guest_reviews almacena la categoría como texto libre en
    el idioma del scraping (e.g. "Cleanliness", "Limpieza", "Sauberkeit").
    El mapa _CATEGORY_KEY_MAP normaliza estos valores al conjunto de claves
    estándar del API: hotel_services, hotel_clean, hotel_comfort, hotel_value,
    hotel_location, hotel_wifi, total.

Platform: Windows 11 / Python 3.14 / PostgreSQL 14+
"""

from __future__ import annotations

import html
import logging
import re
from collections import defaultdict
from typing import Any, Dict, List, Optional
from uuid import UUID

from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.models import (
    Hotel,
    HotelAllService,
    HotelDescription,
    HotelExtraInfo,
    HotelFAQ,
    HotelFinePrint,
    HotelGuestReview,
    HotelIndividualReview,
    HotelLegal,
    HotelNearbyPlace,
    HotelPolicy,
    HotelRoomType,
    HotelSEO,
    ImageDownload,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

# Idiomas soportados por el sistema (orden canónico)
SUPPORTED_LANGUAGES: List[str] = ["en", "es", "de", "fr", "it", "pt"]

# Mapa de normalización: texto libre de categoría → clave API estándar.
# Cubre los 6 idiomas de scraping para cada categoría.
_CATEGORY_KEY_MAP: Dict[str, str] = {
    # Facilities / Instalaciones
    "facilities":       "hotel_services",
    "instalaciones":    "hotel_services",
    "ausstattung":      "hotel_services",
    "équipements":      "hotel_services",
    "servizi":          "hotel_services",
    "instalações":      "hotel_services",
    # Cleanliness / Limpieza
    "cleanliness":      "hotel_clean",
    "limpieza":         "hotel_clean",
    "sauberkeit":       "hotel_clean",
    "propreté":         "hotel_clean",
    "pulizia":          "hotel_clean",
    "limpeza":          "hotel_clean",
    # Comfort / Comodidad
    "comfort":          "hotel_comfort",
    "comodidad":        "hotel_comfort",
    "komfort":          "hotel_comfort",
    "confort":          "hotel_comfort",
    "comfort_it":       "hotel_comfort",    # italiano usa "comfort" (alias legacy)
    "conforto":         "hotel_comfort",    # BUG-CATMAP-001-FIX: PT usa "Conforto"
    # Value for money / Precio-calidad
    "value for money":  "hotel_value",
    "precio calidad":   "hotel_value",
    "relación calidad-precio": "hotel_value",   # BUG-CATMAP-001-FIX: ES variante
    "preis-leistung":   "hotel_value",
    "rapport qualité/prix": "hotel_value",
    "qualità/prezzo":   "hotel_value",
    "rapporto qualità-prezzo": "hotel_value",   # BUG-CATMAP-001-FIX: IT variante
    "custo-benefício":  "hotel_value",
    "relação qualidade/preço": "hotel_value",
    # Location / Ubicación
    "location":         "hotel_location",
    "ubicación":        "hotel_location",
    "lage":             "hotel_location",
    "emplacement":      "hotel_location",
    "situation géographique": "hotel_location",  # BUG-CATMAP-001-FIX: FR variante
    "posizione":        "hotel_location",
    "localização":      "hotel_location",
    # Free Wifi
    "free wifi":        "hotel_wifi",
    "wifi gratis":      "hotel_wifi",
    "kostenloses wlan": "hotel_wifi",
    "kostenfreies wlan": "hotel_wifi",    # BUG-CATMAP-001-FIX: DE variante
    "wi-fi gratuit":    "hotel_wifi",
    "wi-fi gratuito":   "hotel_wifi",
    "wifi gratuito":    "hotel_wifi",     # BUG-CATMAP-001-FIX: IT sin guión
    "wi-fi grátis":     "hotel_wifi",
    # Total / Score global
    "total":            "total",
}

# Etiquetas canónicas de categoría por clave de API y por idioma.
# Se usan cuando la clave API ya está resuelta y queremos la etiqueta humana.
_CATEGORY_LABELS: Dict[str, Dict[str, str]] = {
    "hotel_services": {
        "en": "Facilities", "es": "Instalaciones", "de": "Ausstattung",
        "fr": "Équipements", "it": "Servizi", "pt": "Instalações",
    },
    "hotel_clean": {
        "en": "Cleanliness", "es": "Limpieza", "de": "Sauberkeit",
        "fr": "Propreté", "it": "Pulizia", "pt": "Limpeza",
    },
    "hotel_comfort": {
        "en": "Comfort", "es": "Comodidad", "de": "Komfort",
        "fr": "Confort", "it": "Comfort", "pt": "Conforto",
    },
    "hotel_value": {
        "en": "Value for money", "es": "Precio calidad", "de": "Preis-Leistung",
        "fr": "Rapport qualité/prix", "it": "Qualità/prezzo", "pt": "Custo-benefício",
    },
    "hotel_location": {
        "en": "Location", "es": "Ubicación", "de": "Lage",
        "fr": "Emplacement", "it": "Posizione", "pt": "Localização",
    },
    "hotel_wifi": {
        "en": "Free Wifi", "es": "Wifi gratis", "de": "Kostenloses WLAN",
        "fr": "Wi-Fi gratuit", "it": "Wi-Fi gratuito", "pt": "Wi-Fi grátis",
    },
    "total": {
        "en": "Total", "es": "Total", "de": "Gesamt",
        "fr": "Total", "it": "Totale", "pt": "Total",
    },
}

# Categorías de imagen preferidas para el array images[], en orden de prioridad
_IMAGE_CATEGORY_PRIORITY: List[str] = ["highres_url", "large_url", "thumb_url"]


# ---------------------------------------------------------------------------
# ApiPayloadBuilder
# ---------------------------------------------------------------------------

class ApiPayloadBuilder:
    """
    Transforma los registros de la base de datos de un hotel (identificado
    por url_id) al formato JSON requerido por _API_.md.

    Uso:
        builder = ApiPayloadBuilder(session)
        payload = builder.build_payload(url_id)

    El payload resultante tiene la forma:
        {
            "data": {
                "name":   {"en": "...", "es": "..."},
                "rating": 4,
                ...
                "services": {"en": [...], "es": [...]},
                ...
            },
            "args": { ... }
        }
    """

    def __init__(self, session: Session) -> None:
        self.db = session

    # ------------------------------------------------------------------
    # Punto de entrada público
    # ------------------------------------------------------------------

    def build_payload(self, url_id: UUID) -> Dict[str, Any]:
        """
        Construye el payload completo para la URL indicada.

        Raises:
            ValueError: si no existe ningún registro hotels para este url_id.
        """
        # ── 1. Cargar todos los registros hotels (uno por idioma) ──────────
        hotel_rows: List[Hotel] = (
            self.db.query(Hotel)
            .filter(Hotel.url_id == url_id)
            .order_by(Hotel.language)
            .all()
        )

        if not hotel_rows:
            raise ValueError(f"No hotel records found for url_id={url_id}")

        # BUG-LOCALES-EN-001-FIX (Build 97): order_by(Hotel.language) produce orden
        # alfabético ('de' < 'en'), violando el contrato _API_.md que exige 'en'
        # siempre primero en args.locales y en los dicts multilingüe del payload.
        # Reordenamos explícitamente: 'en' al inicio, resto en orden original.
        raw_langs: List[str] = [h.language for h in hotel_rows]
        if "en" in raw_langs and raw_langs[0] != "en":
            langs = ["en"] + [ln for ln in raw_langs if ln != "en"]
        else:
            langs = raw_langs

        hotel_by_lang: Dict[str, Hotel] = {h.language: h for h in hotel_rows}

        # Para tablas language-independent usamos el registro 'en' si existe,
        # si no el primero (para mayor consistencia con idioma canónico).
        primary: Hotel = hotel_by_lang.get("en", hotel_rows[0])
        hotel_id: UUID = primary.id

        logger.info(
            "ApiPayloadBuilder: url_id=%s | hotel_id=%s | langs=%s (en-first enforced)",
            url_id, hotel_id, langs,
        )

        # ── 2. Cargar datos de tablas satélite ────────────────────────────
        desc_by_lang       = self._load_desc(url_id)
        services_by_lang   = self._load_services(url_id)
        policies_by_lang   = self._load_policies(url_id)
        legal_by_lang      = self._load_legal(url_id)
        fine_print_by_lang = self._load_fine_print(url_id)
        guest_rev_by_lang  = self._load_guest_reviews(url_id)
        ind_rev_by_lang    = self._load_individual_reviews(url_id)
        rooms_by_lang      = self._load_rooms(url_id)
        nearby_by_lang     = self._load_nearby(url_id)
        faqs_by_lang       = self._load_faqs(url_id)
        seo_by_lang        = self._load_seo(url_id)
        extra_by_lang      = self._load_extra_info(url_id)

        # image_downloads: language-independent (keyed by hotel_id)
        image_urls = self._load_image_urls(hotel_id)

        # ── 3. Construir sección "data" ───────────────────────────────────
        data: Dict[str, Any] = {}

        # --- Campos language-independent (tomados del primer registro) ---
        data["rating"]              = primary.star_rating  # BUG-PAYLOAD-002-FIX (Build 96): None si no hay clasificación, no 0
        data["geoPosition"]         = {
            "latitude":  primary.latitude,
            "longitude": primary.longitude,
        }
        data["scoreReview"]         = primary.review_score
        data["scoreReviewBasedOn"]  = primary.review_count
        data["roomsQuantity"]       = primary.rooms_quantity  # BUG-PAYLOAD-003-FIX (Build 96): None si date-dependent NULL, no 0
        # BUG-ENV-REGEX-001-FIX / STRUCT-CITY-002 (Build 89):
        # atnm_en (Booking.com specific, e.g. "hotel", "resort", "guest_house")
        # is now populated correctly. Use it as primary; fall back to
        # accommodation_type (JSON-LD @type, e.g. "Hotel", "LodgingBusiness").
        data["accommodationType"]   = primary.atnm_en or primary.accommodation_type or "Hotel"
        data["priceRange"]          = primary.price_range
        data["images"]              = image_urls

        # --- Campos multilingüe ---
        data["name"]            = {}
        data["address"]         = {}
        data["services"]        = {}
        data["conditions"]      = {}
        data["toConsider"]      = {}
        data["longDescription"] = {}
        data["reviews"]         = {}
        data["categoryScoreReview"] = {}
        data["rooms"]           = {}
        data["nearbyPlaces"]    = {}
        data["guestValues"]     = {}
        data["seoDescription"]  = {}
        data["keywords"]        = {}
        data["extraInfo"]       = {}

        for lang in langs:
            h = hotel_by_lang[lang]

            # name
            data["name"][lang] = h.hotel_name or ""

            # address
            data["address"][lang] = self._build_address(h)

            # services
            data["services"][lang] = services_by_lang.get(lang, [])

            # conditions (policies)
            data["conditions"][lang] = policies_by_lang.get(lang, [])

            # toConsider = fine_print + legal concatenados
            data["toConsider"][lang] = self._build_to_consider(
                fine_print_by_lang.get(lang),
                legal_by_lang.get(lang),
            )

            # longDescription
            desc = desc_by_lang.get(lang)
            data["longDescription"][lang] = desc.description if desc else ""

            # reviews (individual)
            data["reviews"][lang] = self._build_individual_reviews(
                ind_rev_by_lang.get(lang, [])
            )

            # categoryScoreReview
            data["categoryScoreReview"][lang] = self._build_category_scores(
                guest_rev_by_lang.get(lang, []), lang
            )

            # rooms
            data["rooms"][lang] = self._build_rooms(rooms_by_lang.get(lang, []))

            # nearbyPlaces
            data["nearbyPlaces"][lang] = self._build_nearby(
                nearby_by_lang.get(lang, [])
            )

            # guestValues (FAQs)
            data["guestValues"][lang] = self._build_faqs(
                faqs_by_lang.get(lang, [])
            )

            # seoDescription / keywords
            seo = seo_by_lang.get(lang)
            data["seoDescription"][lang] = seo.seo_description if seo else ""
            data["keywords"][lang]       = seo.keywords if seo else ""

            # extraInfo
            extra = extra_by_lang.get(lang)
            data["extraInfo"][lang] = extra.extra_info if extra else None

        # ── 4. Construir sección "args" ───────────────────────────────────
        args: Dict[str, Any] = {
            "seoFormatKey":  "",
            "onlyTitle":     True,
            "regenerateSeo": True,
            "append":        False,
            "cache":         True,
            "locales":       langs,
        }

        return {"data": data, "args": args}

    # ------------------------------------------------------------------
    # Loaders (tablas satélite)
    # ------------------------------------------------------------------

    def _load_desc(self, url_id: UUID) -> Dict[str, Any]:
        rows = self.db.query(HotelDescription).filter_by(url_id=url_id).all()
        return {r.language: r for r in rows}

    def _load_services(self, url_id: UUID) -> Dict[str, List[Dict]]:
        """
        Carga hotels_all_services y agrupa por idioma y categoría.
        Formato de salida por idioma: [ { "Categoría": ["item1", "item2"] } ]
        """
        rows = (
            self.db.query(HotelAllService)
            .filter_by(url_id=url_id)
            .order_by(HotelAllService.service_category, HotelAllService.id)
            .all()
        )
        by_lang: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
        for r in rows:
            cat = r.service_category or "Other"
            by_lang[r.language][cat].append(r.service)

        result: Dict[str, List[Dict]] = {}
        for lang, cat_map in by_lang.items():
            result[lang] = [dict(cat_map)]
        return result

    def _load_policies(self, url_id: UUID) -> Dict[str, List[Dict]]:
        rows = (
            self.db.query(HotelPolicy)
            .filter_by(url_id=url_id)
            .order_by(HotelPolicy.id)
            .all()
        )
        by_lang: Dict[str, List[Dict]] = defaultdict(list)
        for r in rows:
            by_lang[r.language].append({
                "condition": r.policy_name,
                "detail":    r.policy_details,
            })
        return dict(by_lang)

    def _load_legal(self, url_id: UUID) -> Dict[str, Any]:
        rows = self.db.query(HotelLegal).filter_by(url_id=url_id).all()
        return {r.language: r for r in rows}

    def _load_fine_print(self, url_id: UUID) -> Dict[str, Any]:
        rows = self.db.query(HotelFinePrint).filter_by(url_id=url_id).all()
        return {r.language: r for r in rows}

    def _load_guest_reviews(self, url_id: UUID) -> Dict[str, List[Any]]:
        rows = (
            self.db.query(HotelGuestReview)
            .filter_by(url_id=url_id)
            .order_by(HotelGuestReview.id)
            .all()
        )
        by_lang: Dict[str, List] = defaultdict(list)
        for r in rows:
            by_lang[r.language].append(r)
        return dict(by_lang)

    def _load_individual_reviews(self, url_id: UUID) -> Dict[str, List[Any]]:
        rows = (
            self.db.query(HotelIndividualReview)
            .filter_by(url_id=url_id)
            .order_by(HotelIndividualReview.id)
            .all()
        )
        by_lang: Dict[str, List] = defaultdict(list)
        for r in rows:
            by_lang[r.language].append(r)
        return dict(by_lang)

    def _load_rooms(self, url_id: UUID) -> Dict[str, List[Any]]:
        rows = (
            self.db.query(HotelRoomType)
            .filter_by(url_id=url_id)
            .order_by(HotelRoomType.id)
            .all()
        )
        by_lang: Dict[str, List] = defaultdict(list)
        for r in rows:
            by_lang[r.language].append(r)
        return dict(by_lang)

    def _load_nearby(self, url_id: UUID) -> Dict[str, List[Any]]:
        rows = (
            self.db.query(HotelNearbyPlace)
            .filter_by(url_id=url_id)
            .order_by(HotelNearbyPlace.id)
            .all()
        )
        by_lang: Dict[str, List] = defaultdict(list)
        for r in rows:
            by_lang[r.language].append(r)
        return dict(by_lang)

    def _load_faqs(self, url_id: UUID) -> Dict[str, List[Any]]:
        rows = (
            self.db.query(HotelFAQ)
            .filter_by(url_id=url_id)
            .order_by(HotelFAQ.id)
            .all()
        )
        by_lang: Dict[str, List] = defaultdict(list)
        for r in rows:
            by_lang[r.language].append(r)
        return dict(by_lang)

    def _load_seo(self, url_id: UUID) -> Dict[str, Any]:
        rows = self.db.query(HotelSEO).filter_by(url_id=url_id).all()
        return {r.language: r for r in rows}

    def _load_extra_info(self, url_id: UUID) -> Dict[str, Any]:
        rows = self.db.query(HotelExtraInfo).filter_by(url_id=url_id).all()
        return {r.language: r for r in rows}

    def _load_image_urls(self, hotel_id: UUID) -> List[str]:
        """
        Carga URLs de imágenes desde image_downloads.
        Prioriza highres_url > large_url > thumb_url.
        Devuelve lista de URLs únicas (deduplicada) para el payload images[].
        """
        for category in _IMAGE_CATEGORY_PRIORITY:
            rows = (
                self.db.query(ImageDownload)
                .filter(
                    ImageDownload.hotel_id == hotel_id,
                    ImageDownload.category == category,
                    ImageDownload.status == "done",
                )
                .order_by(ImageDownload.created_at)
                .all()
            )
            if rows:
                seen: set = set()
                urls: List[str] = []
                for r in rows:
                    if r.url not in seen:
                        seen.add(r.url)
                        urls.append(r.url)
                logger.debug(
                    "ApiPayloadBuilder: %d image URLs loaded (category=%s) for hotel_id=%s",
                    len(urls), category, hotel_id,
                )
                return urls

        # Fallback: cualquier categoría con status done
        rows = (
            self.db.query(ImageDownload)
            .filter(
                ImageDownload.hotel_id == hotel_id,
                ImageDownload.status == "done",
            )
            .order_by(ImageDownload.created_at)
            .all()
        )
        seen = set()
        urls = []
        for r in rows:
            if r.url not in seen:
                seen.add(r.url)
                urls.append(r.url)

        if not urls:
            logger.warning(
                "ApiPayloadBuilder: No image URLs with status='done' for hotel_id=%s — "
                "returning empty list. Check image_downloads population.",
                hotel_id,
            )
        return urls

    # ------------------------------------------------------------------
    # Transformadores
    # ------------------------------------------------------------------

    def _build_address(self, h: Hotel) -> str:
        """
        Construye la dirección formateada para el campo address del payload.
        Formato: "street_address, postal_code address_city, address_country"
        """
        parts = []
        if h.street_address:
            parts.append(h.street_address)
        # STRUCT-CITY-001 (Build 88): city_name (booking.env) es más limpio
        # que address_city (addressRegion JSON-LD que puede ser región/estado).
        # Prioridad: city_name → address_city → address_locality
        city_resolved = h.city_name or h.address_city or h.address_locality
        city_part = " ".join(filter(None, [
            h.postal_code,
            city_resolved,
        ]))
        if city_part:
            parts.append(city_part)
        if h.address_country:
            parts.append(h.address_country)
        return ", ".join(parts) if parts else ""

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------

    @staticmethod
    def _html_to_plaintext(raw: str) -> str:
        """
        BUG-HTML-FP-001-FIX (Build 97):
        Convierte HTML (con <p>, <br>, &amp; etc.) a texto plano con saltos
        de línea \\n, como exige el contrato _API_.md para el campo toConsider.

        Transformaciones:
          - <p>...</p> → texto + \\n
          - <br> / <br/> → \\n
          - Entidades HTML (&amp; &lt; &gt; &nbsp;) → caracteres UTF-8
          - Tags HTML residuales → eliminados
          - Espacios múltiples y líneas vacías → normalizados

        Ejemplo:
          Input : "<p>Show a photo ID.</p><p>Check-in from 3 PM.</p>"
          Output: "Show a photo ID.\\nCheck-in from 3 PM."
        """
        if not raw:
            return ""
        try:
            soup = BeautifulSoup(raw, "html.parser")
            # Insertar marcador \n después de cada <p> y <br>
            for tag in soup.find_all(["p", "br"]):
                tag.insert_after("\n")
            text = soup.get_text(separator="")
            # Normalizar líneas: strip por línea, colapsar múltiples blank lines
            lines = [line.strip() for line in text.splitlines()]
            # Eliminar líneas completamente vacías duplicadas consecutivas
            normalized: List[str] = []
            prev_blank = False
            for line in lines:
                is_blank = (line == "")
                if is_blank and prev_blank:
                    continue
                normalized.append(line)
                prev_blank = is_blank
            return "\n".join(normalized).strip()
        except Exception:
            # Fallback: strip de tags básicos con regex si BeautifulSoup falla
            text = re.sub(r"<br\s*/?>", "\n", raw, flags=re.IGNORECASE)
            text = re.sub(r"<p[^>]*>", "", text, flags=re.IGNORECASE)
            text = re.sub(r"</p>", "\n", text, flags=re.IGNORECASE)
            text = re.sub(r"<[^>]+>", "", text)
            text = html.unescape(text)
            return text.strip()

    def _build_to_consider(
        self,
        fine_print: Optional[Any],
        legal: Optional[Any],
    ) -> str:
        """
        Concatena fine_print.fp y legal.legal_info (separados por \\n\\n)
        para construir el campo toConsider del payload.
        """
        fragments: List[str] = []
        if fine_print and fine_print.fp:
            # BUG-HTML-FP-001-FIX (Build 97): fp almacena HTML con <p> tags.
            # La API exige texto plano con \n. Convertir antes de concatenar.
            fp_text = self._html_to_plaintext(fine_print.fp.strip())
            if fp_text:
                fragments.append(fp_text)
        # BUG-PAYLOAD-004-FIX (Build 96): elif -> if+if para incluir AMBOS
        # legal_info y legal_details cuando ambos tienen contenido.
        # El elif previo descartaba legal_details silenciosamente cuando
        # legal_info ya existía. Ambos campos son complementarios.
        if legal:
            if legal.legal_info:
                fragments.append(legal.legal_info.strip())
            if legal.legal_details:
                fragments.append(legal.legal_details.strip())
        return "\n\n".join(fragments)

    # BUG-PAYLOAD-005-FIX (Build 96): Literales nulos en negative_comment
    # El extractor almacena "None", "Nada", "No", "" cuando Booking.com no
    # incluye comentario negativo. La API debe recibir null, no estos strings.
    _NULL_COMMENT_LITERALS: frozenset = frozenset({
        "none", "nada", "no", "n/a", "nothing", "niente",
        "rien", "nichts", "nenhum", "ninguno", "",
    })

    def _build_individual_reviews(
        self,
        rows: List[Any],
    ) -> List[Dict[str, Any]]:
        result = []
        for r in rows:
            # BUG-PAYLOAD-005-FIX: normaliza literales "None","Nada","No" a None
            neg = r.negative_comment
            if neg is not None and neg.strip().lower() in self._NULL_COMMENT_LITERALS:
                neg = None
            result.append({
                "name":    r.reviewer_name,
                "score":   float(r.score) if r.score is not None else None,
                "title":   r.title,
                "comments": {
                    "negative": neg,
                    "positive": r.positive_comment,
                },
                "country":   r.reviewer_country,
                "bookingId": r.booking_id,
            })
        return result

    def _build_category_scores(
        self,
        rows: List[Any],
        lang: str,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Transforma filas de hotels_guest_reviews al objeto categoryScoreReview.
        Mapea el texto libre de categoría al conjunto de claves estándar
        del API usando _CATEGORY_KEY_MAP.
        """
        result: Dict[str, Dict[str, Any]] = {}
        for r in rows:
            raw_cat = (r.reviews_categories or "").strip().lower()
            api_key = _CATEGORY_KEY_MAP.get(raw_cat)

            if api_key is None:
                # Intentar coincidencia parcial como último recurso
                for keyword, key in _CATEGORY_KEY_MAP.items():
                    if keyword in raw_cat:
                        api_key = key
                        break

            if api_key is None:
                logger.warning(
                    "ApiPayloadBuilder: unmapped guest review category %r (lang=%s) — skipped",
                    r.reviews_categories, lang,
                )
                continue

            label = _CATEGORY_LABELS.get(api_key, {}).get(lang, r.reviews_categories)

            try:
                score_val = float(r.reviews_score) if r.reviews_score else None
            except (ValueError, TypeError):
                score_val = None

            result[api_key] = {
                "category": label,
                "score":    score_val,
            }
        return result

    def _build_rooms(self, rows: List[Any]) -> List[Dict[str, Any]]:
        result = []
        for r in rows:
            result.append({
                "name":        r.room_name,
                "adults":      r.adults,
                "children":    r.children,
                "description": r.description,
                "images":      r.images or [],
                "info":        r.info,
                "facilities":  r.facilities or [],
            })
        return result

    def _build_nearby(self, rows: List[Any]) -> List[Dict[str, Any]]:
        result = []
        for r in rows:
            result.append({
                "name":     r.place_name,
                "distance": r.distance,
                "category": r.category_code,
            })
        return result

    def _build_faqs(self, rows: List[Any]) -> List[Dict[str, Any]]:
        result = []
        for r in rows:
            result.append({
                "topic":         r.ask,
                "topicComments": r.answer,
            })
        return result
