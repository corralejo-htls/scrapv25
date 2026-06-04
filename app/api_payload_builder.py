"""
api_payload_builder.py — BookingScraper Pro v6.0.0 Build 112
============================================================

BUG-ONLYTITLE-001-FIX (Build 112):
    build_payload() construía la sección "args" con "onlyTitle": True fijo.
    La API externa interpreta onlyTitle=True como "solo actualizar el campo
    name/title", silenciando todos los demás campos de data[] aunque estén
    presentes. Fix: "onlyTitle" ahora lee el toggle API_EXPORT_ONLY_TITLE
    del objeto config (default False = exportación completa).

BUG-SVC-DOC-001-FIX (Build 112):
    El docstring del módulo describía _ROOM_LEVEL_CATEGORIES y un filtro de
    amenidades de habitación en _load_services() (BUG-SVC-002-FIX Build 98).
    Ese filtro fue eliminado en Build 103 junto con room_level_category_labels,
    pero el docstring permanecía activo. Docstring actualizado para reflejar el
    estado post-Build 103: service_category verbatim del DOM, sin filtrado por
    categoría de habitación.

BUG-GALLERY-MODAL-001 (Build 110):
    _load_image_urls(): nuevo modo API_IMAGES_STRICT_GALLERY. Cuando un hotel
    no tiene fotos gallery_visible (el modal no se capturó), en modo estricto
    se exporta images[] VACÍO en vez del superconjunto; el default conserva la
    red de seguridad histórica con una advertencia más diagnóstica.

Build 109 (BUG-IMG-CLASS-001):
    images[] solo incluye fotos gallery_visible=TRUE, ordenadas por gallery_order.
    Red de seguridad: si no hay galería para el hotel, recae en el conjunto
    histórico (todas las descargas 'done').

Build 97 (BUG-HTML-FP-001-FIX):
    _build_to_consider(): _html_to_plaintext() convierte HTML a texto plano con
    \\n, como exige el contrato _API_.md para el campo toConsider.

Build 97 (BUG-CATMAP-001-FIX):
    _build_category_scores(): 5 variantes de categoría no estaban en
    _CATEGORY_KEY_MAP y se descartaban silenciosamente.

Build 97 (BUG-LOCALES-EN-001-FIX):
    build_payload(): 'en' siempre en primer lugar de args.locales y de los
    dicts multilingüe del payload.

Build 97 (BUG-PRIMARY-EN-001-FIX):
    primary hotel row tomado del registro 'en', no del primero alfabético ('de').
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

from app.language_config import get_language_config
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
    ImageData,
    ImageDownload,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes no dependientes de idioma
# ---------------------------------------------------------------------------

# Categorías de imagen preferidas para el array images[], en orden de prioridad
_IMAGE_CATEGORY_PRIORITY: List[str] = ["highres_url", "large_url", "thumb_url"]

# Literales de comentario negativo nulo (independientes de idioma en la BD)
_NULL_COMMENT_LITERALS: frozenset = frozenset({
    "none", "nada", "no", "n/a", "nothing", "niente",
    "rien", "nichts", "nenhum", "ninguno", "",
})

# ---------------------------------------------------------------------------
# Accesores de LanguageConfig (todas las constantes dependientes de idioma
# provienen de languages.json via language_config.py)
# ---------------------------------------------------------------------------

def _lc():
    """Acceso seguro al singleton LanguageConfig."""
    return get_language_config()


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
        # Build 109: toggle de exportación solo-galería (BUG-IMG-CLASS-001).
        from app.config import get_settings
        self._cfg = get_settings()

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
        # BUG-ONLYTITLE-001-FIX (Build 112): onlyTitle era True hardcodeado.
        # La API externa con onlyTitle=True solo procesa el campo name/title,
        # ignorando todos los demás campos de data[]. Ahora se lee el toggle
        # API_EXPORT_ONLY_TITLE (default False = exportación completa).
        only_title: bool = bool(getattr(self._cfg, "API_EXPORT_ONLY_TITLE", False))
        args: Dict[str, Any] = {
            "seoFormatKey":  "",
            "onlyTitle":     only_title,
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

        Build 103 (BUG-SVC-EXTRAER4-001 v4.5): service_category es texto verbatim
        del DOM — no hay inferencia ni traducción. Los filtros de amenidades de
        habitación (_ROOM_LEVEL_CATEGORIES) y category_key_map que existían en
        Build 98 fueron eliminados en Build 103 junto con room_level_category_labels
        de languages.json. Todos los servicios se incluyen en el payload tal y como
        están en hotels_all_services. NULL/vacío en service_category → "Other".

        BUG-SVC-DOC-001-FIX (Build 112): docstring anterior describía el filtro
        _ROOM_LEVEL_CATEGORIES como activo (BUG-SVC-002-FIX Build 98). Ese filtro
        fue eliminado en Build 103 y el docstring era incorrecto.
        """
        rows = (
            self.db.query(HotelAllService)
            .filter_by(url_id=url_id)
            .order_by(HotelAllService.service_category, HotelAllService.id)
            .all()
        )
        by_lang: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
        # BUILD-103: room_level_category_labels removed from languages.json.
        # service_category is verbatim DOM text — no language-dependent filtering.
        # All extracted services are included in the API payload as-is.
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

        Build 109 (BUG-IMG-CLASS-001):
          Si API_IMAGES_GALLERY_ONLY=True (por defecto), restringe el array a
          las fotos visibles en galería (image_data.gallery_visible=TRUE),
          ordenadas por image_data.gallery_order. Esto alinea el conteo con el
          modal público de Booking.com (validado por extraer_imagenes.py) en
          lugar de exportar el superconjunto interno.

          Red de seguridad: si el modo galería está activo pero NO hay fotos
          de galería para el hotel (p. ej. el modal no se abrió en ese run),
          registra una advertencia y recae en el conjunto histórico (todas las
          descargas 'done'), para no enviar un array vacío.
        """
        gallery_only = bool(getattr(self._cfg, "API_IMAGES_GALLERY_ONLY", True))

        if gallery_only:
            gallery_urls = self._load_gallery_image_urls(hotel_id)
            if gallery_urls:
                logger.debug(
                    "ApiPayloadBuilder: %d gallery image URLs loaded for hotel_id=%s",
                    len(gallery_urls), hotel_id,
                )
                return gallery_urls

            # Build 110 (BUG-GALLERY-MODAL-001): el hotel no tiene fotos
            # gallery_visible (el modal no se capturó en ese run). En modo
            # estricto NO exportamos el superconjunto — el objetivo es enviar
            # SOLO lo que se ve en la galería pública. Default (no estricto)
            # conserva la red de seguridad histórica para no enviar [].
            strict = bool(getattr(self._cfg, "API_IMAGES_STRICT_GALLERY", False))
            if strict:
                logger.warning(
                    "ApiPayloadBuilder: API_IMAGES_STRICT_GALLERY=True and no "
                    "gallery_visible photos for hotel_id=%s — returning EMPTY "
                    "images[] (gallery modal capture likely failed; re-scrape "
                    "this hotel to populate gallery_visible).",
                    hotel_id,
                )
                return []
            logger.warning(
                "ApiPayloadBuilder: API_IMAGES_GALLERY_ONLY=True but no "
                "gallery_visible photos for hotel_id=%s — falling back to all "
                "downloaded images (SUPERSET; will NOT match the public gallery "
                "count). Re-scrape to populate gallery_visible, or enable "
                "API_IMAGES_STRICT_GALLERY to suppress the fallback.",
                hotel_id,
            )

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

    def _load_gallery_image_urls(self, hotel_id: UUID) -> List[str]:
        """
        Build 109: carga SOLO las URLs de fotos visibles en galería
        (image_data.gallery_visible=TRUE), ordenadas por gallery_order, una URL
        por foto según prioridad de talla highres > large > thumb.

        Une image_data (clasificación + orden) con image_downloads (URLs
        descargadas) por id_photo + hotel_id. Devuelve [] si no hay galería.
        """
        rows = (
            self.db.query(
                ImageData.id_photo,
                ImageData.gallery_order,
                ImageDownload.category,
                ImageDownload.url,
            )
            .join(
                ImageDownload,
                (ImageDownload.id_photo == ImageData.id_photo)
                & (ImageDownload.hotel_id == ImageData.hotel_id),
            )
            .filter(
                ImageData.hotel_id == hotel_id,
                ImageData.gallery_visible.is_(True),
                ImageDownload.status == "done",
            )
            .all()
        )
        if not rows:
            return []

        # Selecciona una URL por id_photo según prioridad de talla.
        priority = {cat: i for i, cat in enumerate(_IMAGE_CATEGORY_PRIORITY)}
        best: dict = {}  # id_photo -> (gallery_order, priority_idx, url)
        for pid, order, category, url in rows:
            pidx = priority.get(category, len(_IMAGE_CATEGORY_PRIORITY))
            ord_key = order if order is not None else 1_000_000
            cur = best.get(pid)
            if cur is None or pidx < cur[1]:
                best[pid] = (ord_key, pidx, url)

        ordered = sorted(best.values(), key=lambda t: (t[0], t[1]))
        return [url for _, _, url in ordered]

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
    # (Movido a módulo-level _NULL_COMMENT_LITERALS para evitar duplicación)

    def _build_individual_reviews(
        self,
        rows: List[Any],
    ) -> List[Dict[str, Any]]:
        result = []
        for r in rows:
            # BUG-PAYLOAD-005-FIX: normaliza literales "None","Nada","No" a None
            neg = r.negative_comment
            if neg is not None and neg.strip().lower() in _NULL_COMMENT_LITERALS:
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
        del API usando category_key_map de languages.json (via LanguageConfig).
        """
        lc = _lc()
        # BUILD-103: category_key_map removed from languages.json.
        # Review category normalization uses raw DOM text as api_key.
        # category_labels still provides API labels when a known api_key matches.
        result: Dict[str, Dict[str, Any]] = {}
        for r in rows:
            raw_cat = (r.reviews_categories or "").strip()
            if not raw_cat:
                continue
            # Use lowercased raw text as api_key (best-effort normalization)
            api_key = raw_cat.lower().replace(" ", "_")
            # Attempt label lookup; fall back to raw category text
            label = lc.get_category_label(api_key, lang) or raw_cat

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
