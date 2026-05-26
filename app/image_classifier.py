"""
app/image_classifier.py — BookingScraper Pro v6.0.0 Build 109
==============================================================

OBJETIVO (sesión Build 109)
---------------------------
Clasificar TODA foto extraída en dos clases, sin descartar el excedente:

  • gallery_visible = True   → subconjunto que Booking.com renderiza en el
                               modal de galería (rejilla "Ver todas las fotos").
                               Es el ÚNICO conjunto que debe exportarse a la API
                               externa (campo ``images`` de _API_.md).
  • gallery_visible = False  → resto del inventario interno (fotos de
                               habitación, instalaciones, exterior, etc.).
                               Se conserva con ``subcategory`` para uso futuro.

POR QUÉ ESTE MÓDULO (hallazgos de auditoría verificados contra el repositorio)
------------------------------------------------------------------------------
1. El pipeline de producción (``extractor.extract_hotel_photos_from_html``)
   captura un SUPERCONJUNTO: cada ``id_photo`` con token ``k=`` presente en
   cualquier parte del HTML. Para Villa Dvor (external_ref 1001) eso son 106
   fotos únicas, exactamente el ``count_large_url`` de la BD.

2. El script validado por el usuario (``pruebas/extraer_imagenes.py``) cuenta
   SOLO los botones ``button[data-testid^="gallery-grid-photo-action-"]`` que
   viven dentro de ``[data-testid="GalleryGridViewModal-wrapper"]``. Para
   Villa Dvor eso son 59 fotos — el conjunto público real.

3. VERIFICADO: el HTML estático/renderizado que devuelve ``scraper.scrape()``
   NO contiene la rejilla del modal (0 ocurrencias de
   ``gallery-grid-photo-action`` y de ``GalleryGridViewModal`` en los snapshots
   completos de ``pruebas/``). El modal solo se materializa tras hacer clic en
   el abridor de galería. Conclusión: la IDENTIDAD de las fotos de galería NO
   es derivable del page source; debe capturarse abriendo el modal en vivo
   (mismo método que ``extraer_imagenes.py``).

4. El badge "+N photos" del hero SÍ permite derivar el CONTEO de galería sin
   abrir el modal: gallery_count = previsualizaciones_visibles + N.
   Verificado exacto contra ground truth: Villa Dvor 8+51=59; wild&bolz
   8+14=22. Útil como validación/*fallback* de conteo, pero NO da identidad,
   por lo que no sustituye al modal para clasificar.

LIMITACIÓN HONESTA DE LA SUBCATEGORIZACIÓN
------------------------------------------
El ``alt`` del array ``hotelPhotos`` JS es genérico ("Gallery image of <hotel>
in <city>") para casi todas las fotos, por lo que la heurística por alt-text
rinde poco en la práctica. La señal MÁS fiable es el cruce por ``id_photo``
contra ``hotels_room_types.images`` (JSONB) ya persistido: si la foto pertenece
a una habitación, es ``room`` con certeza. El resto cae a ``unknown`` salvo que
el alt o las dimensiones aporten evidencia. No se sobrevende la heurística.

NOTA DE ARQUITECTURA (single-node Windows 11)
---------------------------------------------
La extracción del modal usa el driver Selenium VIVO del pase EN (las fotos son
language-independent). No abre un segundo navegador ni rota VPN aparte; reutiliza
la sesión existente, evitando coste y fingerprinting adicionales. Todo el bloque
es tolerante a fallos: cualquier excepción degrada con elegancia a "sin galería"
y deja que el *fallback* de conteo y la persistencia continúen.
"""

from __future__ import annotations

import logging
import re
import time
from typing import Any, Dict, Iterable, List, Optional, Set

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Selectores (idénticos a pruebas/extraer_imagenes.py — fuente validada)
# ---------------------------------------------------------------------------
GALLERY_BUTTON_SELECTOR = 'button[data-testid^="gallery-grid-photo-action-"]'

GALLERY_MODAL_SELECTORS = [
    '[data-testid="GalleryGridViewModal-wrapper"]',
    '[data-testid="gallery-modal-grid"]',
]

GALLERY_OPENER_SELECTORS = [
    'button[data-testid="property-hero-gallery-desktop"]',
    'a[data-testid="property-hero-photos-gallery"]',
    '[data-testid="property-hero-photos"]',
    '[data-testid="property-hero-gallery"]',
    '.js-bh-photo-modal-trigger',
]

# ---------------------------------------------------------------------------
# Subcategorías permitidas (deben coincidir con el CHECK de image_data en
# schema_v77_complete.sql y con el CheckConstraint del ORM ImageData).
# ---------------------------------------------------------------------------
SUBCATEGORY_GALLERY = "gallery"
SUBCATEGORY_ROOM = "room"
SUBCATEGORY_FACILITY = "facility"
SUBCATEGORY_EXTERIOR = "exterior"
SUBCATEGORY_THUMBNAIL = "thumbnail"
SUBCATEGORY_REVIEW = "review_photo"
SUBCATEGORY_UNKNOWN = "unknown"

VALID_SUBCATEGORIES = frozenset({
    SUBCATEGORY_GALLERY, SUBCATEGORY_ROOM, SUBCATEGORY_FACILITY,
    SUBCATEGORY_EXTERIOR, SUBCATEGORY_THUMBNAIL, SUBCATEGORY_REVIEW,
    SUBCATEGORY_UNKNOWN,
})

# Fuentes permitidas (deben coincidir con el CHECK de image_data.source).
SOURCE_GALLERY_MODAL = "gallery_modal"
SOURCE_JS_ARRAY = "js_array"
SOURCE_DOM_SCAN = "dom_scan"
SOURCE_UNKNOWN = "unknown"

VALID_SOURCES = frozenset({
    SOURCE_GALLERY_MODAL, SOURCE_JS_ARRAY, SOURCE_DOM_SCAN, SOURCE_UNKNOWN,
})

# ---------------------------------------------------------------------------
# Derivación de URLs por talla (regla VERIFICADA: mismo id_photo y mismo token
# k= en las 3 tallas; solo cambia el segmento de tamaño). Reutiliza la misma
# convención que app/extractor.py para mantener coherencia.
# ---------------------------------------------------------------------------
_SIZE_SEGMENTS = {
    "thumb_url": "max200",
    "large_url": "max1024x768",
    "highres_url": "max1280x900",
}

# id_photo desde el basename de la URL: .../hotel/<size>/<id>.jpg?k=<token>
_ID_FROM_URL = re.compile(r"/hotel/[^/]+/(\d+)\.(?:jpg|jpeg|png|webp)", re.IGNORECASE)
_TOKEN_FROM_URL = re.compile(r"[?&]k=([^\"'&\\\s]+)")

# Heurística alt-text (segunda señal, débil para el array JS genérico).
_ALT_ROOM = re.compile(r"\b(room|suite|bedroom|double|twin|apartment|studio|chalet|villa|dormitory|family)\b", re.IGNORECASE)
_ALT_FACILITY = re.compile(r"\b(bathroom|spa|pool|gym|fitness|restaurant|bar|sauna|jacuzzi|wellness|breakfast|lobby|reception|kitchen)\b", re.IGNORECASE)
_ALT_EXTERIOR = re.compile(r"\b(exterior|building|facade|garden|view|mountain|lake|beach|terrace|balcony|property\s+building|aerial|surrounding)\b", re.IGNORECASE)
_ALT_REVIEW = re.compile(r"\b(review|guest\s+photo|uploaded|traveller\s+photo|visitor)\b", re.IGNORECASE)


def id_photo_from_src(src: Optional[str]) -> Optional[str]:
    """Extrae el id_photo de Booking.com desde una URL de imagen, o None."""
    if not src:
        return None
    m = _ID_FROM_URL.search(src)
    return m.group(1) if m else None


def _token_from_src(src: Optional[str]) -> Optional[str]:
    if not src:
        return None
    m = _TOKEN_FROM_URL.search(src)
    return m.group(1) if m else None


def _build_sizes_from_src(src: str) -> Dict[str, str]:
    """Deriva las 3 tallas (thumb/large/highres) desde cualquier URL autenticada."""
    pid = id_photo_from_src(src)
    token = _token_from_src(src)
    if not pid or not token:
        return {}
    base = "https://cf.bstatic.com/xdata/images/hotel"
    return {
        cat: f"{base}/{seg}/{pid}.jpg?k={token}"
        for cat, seg in _SIZE_SEGMENTS.items()
    }


# ===========================================================================
# Fallback de CONTEO por badge "+N photos" (NO da identidad; solo valida)
# ===========================================================================
_BADGE_PATTERN = re.compile(r"\+\s*(\d+)\s*photos?", re.IGNORECASE)
_HERO_IMG_PATTERN = re.compile(
    r"<img[^>]*bstatic\.com/xdata/images/hotel[^>]*>", re.IGNORECASE
)


def gallery_count_from_html(html: Optional[str]) -> Optional[int]:
    """
    Estima el conteo de fotos de galería desde el HTML del hero, sin abrir el
    modal:  gallery_count = previsualizaciones_visibles + N (badge "+N photos").

    Verificado exacto contra ground truth (Villa Dvor 8+51=59; wild&bolz
    8+14=22). Devuelve None si no hay señales suficientes. SOLO sirve como
    validación o *fallback* de conteo: no identifica qué fotos son de galería.
    """
    if not html:
        return None
    previews = len(_HERO_IMG_PATTERN.findall(html))
    badges = [int(n) for n in _BADGE_PATTERN.findall(html)]
    if not previews and not badges:
        return None
    badge_n = max(badges) if badges else 0
    return previews + badge_n


# ===========================================================================
# GalleryModalExtractor — extracción EN VIVO del modal de galería
# ===========================================================================
class GalleryModalExtractor:
    """
    Abre la rejilla del modal de galería con el driver Selenium vivo y devuelve
    la lista ORDENADA de fotos visibles (mismo algoritmo que extraer_imagenes.py).

    Se asume que el driver ya está en la página del hotel (caso producción). Si
    se pasa ``url``, navega primero (uso autónomo/pruebas).
    """

    def __init__(self, driver: Any, cfg: Any = None) -> None:
        self.driver = driver
        self.cfg = cfg
        self.scroll_iterations = int(getattr(cfg, "GALLERY_MODAL_SCROLL_ITERATIONS", 8))
        self.scroll_pause_s = float(getattr(cfg, "GALLERY_MODAL_SCROLL_PAUSE_S", 1.5))
        self.modal_timeout_s = float(getattr(cfg, "GALLERY_MODAL_TIMEOUT_S", 25.0))

    # -- internals ----------------------------------------------------------
    def _open_modal(self) -> bool:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        for sel in GALLERY_OPENER_SELECTORS:
            try:
                opener = WebDriverWait(self.driver, 4).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                )
                opener.click()
                logger.debug("GalleryModalExtractor: opener clicked (%s)", sel)
                time.sleep(3)
                return True
            except Exception:
                continue
        # Fallback: clic en la imagen hero
        try:
            hero = self.driver.find_element(
                By.CSS_SELECTOR,
                '[data-testid="property-hero"] img, .k2-hp--gallery-header img',
            )
            hero.click()
            time.sleep(3)
            logger.debug("GalleryModalExtractor: hero image fallback clicked")
            return True
        except Exception:
            return False

    def _wait_modal(self) -> bool:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        try:
            WebDriverWait(self.driver, self.modal_timeout_s).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ", ".join(GALLERY_MODAL_SELECTORS))
                )
            )
            return True
        except Exception:
            return False

    def _scroll_modal(self) -> None:
        from selenium.webdriver.common.by import By
        try:
            modal = self.driver.find_element(
                By.CSS_SELECTOR, '[data-testid="GalleryGridViewModal-wrapper"]'
            )
            for _ in range(self.scroll_iterations):
                self.driver.execute_script("arguments[0].scrollBy(0, 1000);", modal)
                time.sleep(self.scroll_pause_s)
        except Exception:
            # Sin contenedor desplazable → desplaza la ventana
            for i in range(5):
                self.driver.execute_script(f"window.scrollBy(0, {800 + i * 200});")
                time.sleep(self.scroll_pause_s)

    # -- public -------------------------------------------------------------
    def extract(self, url: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Devuelve lista ordenada de dicts:
          {id_photo, thumb_url, large_url, highres_url, alt, gallery_order, source}
        Lista vacía si el modal no se abre (degradación elegante).
        """
        from selenium.webdriver.common.by import By

        if self.driver is None:
            return []
        if url:
            try:
                self.driver.get(url)
                time.sleep(10)
            except Exception as exc:
                logger.warning("GalleryModalExtractor: navigation failed: %s", exc)
                return []

        if not self._open_modal():
            logger.info("GalleryModalExtractor: gallery opener not found/clickable")
            return []
        if not self._wait_modal():
            logger.info("GalleryModalExtractor: modal did not render in DOM")
            return []

        self._scroll_modal()
        time.sleep(1)

        try:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, GALLERY_BUTTON_SELECTOR)
        except Exception as exc:
            logger.warning("GalleryModalExtractor: button query failed: %s", exc)
            return []

        photos: List[Dict[str, Any]] = []
        seen: Set[str] = set()
        for order, btn in enumerate(buttons):
            try:
                aria = btn.get_attribute("aria-label") or ""
                src = ""
                try:
                    img = btn.find_element(By.TAG_NAME, "img")
                    src = img.get_attribute("src") or ""
                    if not aria:
                        aria = img.get_attribute("aria-label") or ""
                except Exception:
                    pass
                pid = id_photo_from_src(src)
                if not pid or pid in seen:
                    continue
                seen.add(pid)
                photo: Dict[str, Any] = {
                    "id_photo": pid,
                    "alt": (aria or "").strip() or None,
                    "gallery_order": order,
                    "source": SOURCE_GALLERY_MODAL,
                }
                photo.update(_build_sizes_from_src(src))
                photos.append(photo)
            except Exception as exc:
                logger.debug("GalleryModalExtractor: button %d skipped: %s", order, exc)

        logger.info("GalleryModalExtractor: %d gallery photos captured", len(photos))
        return photos


# ===========================================================================
# NonGallerySubcategorizer — heurística honesta para fotos no-galería
# ===========================================================================
class NonGallerySubcategorizer:
    """
    Clasifica una foto NO presente en la galería. Orden de precedencia:

      1. Cruce por id_photo contra hotels_room_types.images  → 'room' (fiable)
      2. alt-text regir (room/facility/exterior/review)       → subcategoría
      3. dimensiones (max lado < 300 px)                       → 'thumbnail'
      4. fallback                                              → 'unknown'

    ``room_image_ids`` es el conjunto de id_photo que ya aparecen en las URLs
    de imágenes de habitación persistidas (hotels_room_types.images JSONB).
    """

    def __init__(self, room_image_ids: Optional[Iterable[str]] = None) -> None:
        self.room_image_ids: Set[str] = {str(x) for x in (room_image_ids or [])}

    def classify(self, photo: Dict[str, Any]) -> str:
        pid = str(photo.get("id_photo", "")).strip()

        # 1) Señal fuerte: la foto pertenece a una habitación.
        if pid and pid in self.room_image_ids:
            return SUBCATEGORY_ROOM

        # 2) alt-text (débil para el array JS genérico, pero útil cuando existe).
        alt = (photo.get("alt") or "")
        if alt:
            if _ALT_REVIEW.search(alt):
                return SUBCATEGORY_REVIEW
            if _ALT_ROOM.search(alt):
                return SUBCATEGORY_ROOM
            if _ALT_FACILITY.search(alt):
                return SUBCATEGORY_FACILITY
            if _ALT_EXTERIOR.search(alt):
                return SUBCATEGORY_EXTERIOR

        # 3) Miniaturas decorativas por dimensión.
        w = photo.get("photo_width")
        h = photo.get("photo_height")
        try:
            if w and h and max(int(w), int(h)) < 300:
                return SUBCATEGORY_THUMBNAIL
        except (TypeError, ValueError):
            pass

        # 4) Sin evidencia.
        return SUBCATEGORY_UNKNOWN


# ===========================================================================
# PhotoClassifier — orquestador
# ===========================================================================
class PhotoClassifier:
    """
    Fusiona el conjunto de galería (modal) con el superconjunto dual-source y
    etiqueta cada foto con gallery_visible / source / subcategory / gallery_order.
    """

    def __init__(self, driver: Any = None, cfg: Any = None) -> None:
        self.driver = driver
        self.cfg = cfg
        self.enabled = bool(getattr(cfg, "IMAGE_CLASSIFICATION_ENABLED", True))

    def classify_all(
        self,
        all_photos: List[Dict[str, Any]],
        html: Optional[str] = None,
        url: Optional[str] = None,
        room_image_ids: Optional[Iterable[str]] = None,
        gallery_photos: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Devuelve la lista enriquecida. ``all_photos`` es el superconjunto
        producido por extractor.extract_hotel_photos_from_html(). Si no se
        proveen ``gallery_photos`` y hay driver + clasificación activada, abre
        el modal en vivo.
        """
        all_photos = all_photos or []

        # 1) Conjunto de galería (identidad).
        if gallery_photos is None:
            if self.enabled and self.driver is not None:
                try:
                    gallery_photos = GalleryModalExtractor(self.driver, self.cfg).extract(url)
                except Exception as exc:
                    logger.warning("PhotoClassifier: gallery extraction failed: %s", exc)
                    gallery_photos = []
            else:
                gallery_photos = []

        gallery_by_id: Dict[str, Dict[str, Any]] = {
            str(p["id_photo"]): p for p in gallery_photos if p.get("id_photo")
        }

        # 2) Validación/fallback de conteo por badge (solo informativo si el
        #    modal no devolvió nada).
        if not gallery_by_id and html:
            est = gallery_count_from_html(html)
            if est is not None:
                logger.info(
                    "PhotoClassifier: modal empty; '+N photos' badge estimates "
                    "%d gallery photos (count-only, no identity available)", est,
                )

        subcat = NonGallerySubcategorizer(room_image_ids)

        # 3) Etiqueta cada foto del superconjunto.
        for photo in all_photos:
            pid = str(photo.get("id_photo", "")).strip()
            if pid and pid in gallery_by_id:
                g = gallery_by_id[pid]
                photo["gallery_visible"] = True
                photo["source"] = SOURCE_GALLERY_MODAL
                photo["subcategory"] = SUBCATEGORY_GALLERY
                photo["gallery_order"] = g.get("gallery_order")
                if not photo.get("alt") and g.get("alt"):
                    photo["alt"] = g["alt"]
            else:
                photo["gallery_visible"] = False
                photo.setdefault("source", SOURCE_JS_ARRAY)
                photo["subcategory"] = subcat.classify(photo)
                photo["gallery_order"] = None

        # 4) Añade fotos que SOLO aparecieron en el modal y que el dual-source
        #    no capturó (raro, pero garantiza completitud de la galería).
        known_ids = {str(p.get("id_photo", "")).strip() for p in all_photos}
        for pid, g in gallery_by_id.items():
            if pid in known_ids:
                continue
            extra: Dict[str, Any] = {
                "id_photo": pid,
                "alt": g.get("alt"),
                "gallery_visible": True,
                "source": SOURCE_GALLERY_MODAL,
                "subcategory": SUBCATEGORY_GALLERY,
                "gallery_order": g.get("gallery_order"),
            }
            for cat in _SIZE_SEGMENTS:
                if g.get(cat):
                    extra[cat] = g[cat]
            all_photos.append(extra)

        n_gallery = sum(1 for p in all_photos if p.get("gallery_visible"))
        logger.info(
            "PhotoClassifier: %d total photos (%d gallery_visible, %d non-gallery)",
            len(all_photos), n_gallery, len(all_photos) - n_gallery,
        )
        return all_photos
