"""
BookingScraper/app/extractor.py  v2.7
Extractor de datos HTML de Booking.com
Windows 11 + Python 3.14.3

CAMBIOS v2.1:  og:title como primer selector de nombre; fallbacks multiples.
CAMBIOS v2.2:  address JSON-LD, review_scores 4 estrategias, images bstatic CDN, rooms HPRT.
CAMBIOS v2.3:  extract_images filtro estricto: solo bstatic.com/xdata/images/hotel/
CAMBIOS v2.4:  extract_address JSON-LD primero + _clean_address() en todos los selectores DOM.
               _normalize_img_url() cubre /max500/, /max300/, /maxNNNxNNN/, /squareNN/.
CAMBIOS v2.5:  extract_address() JSON-LD: address duplicada eliminada.
               streetAddress ya contiene city y region; sub-campos solo se anaden
               si no estan ya presentes (comparacion lowercase).

CAMBIOS v2.7:
  [FIX] extract_name(): data-testid='title' movido a posición 1 (solo nombre, sin ciudad/país).
        Nuevo método _clean_hotel_name() elimina prefijo ★ y sufijo ", Ciudad, País" de og:title.
  [FIX] extract_rating_category(): diccionario de categorías completo para 8 idiomas.
        Nuevo método _infer_rating_category_from_score() deduce categoría del score numérico
        cuando el texto DOM no contiene la categoría esperada (idioma no coincide con página).

CAMBIOS v2.6:
  [FIX] extract_images(): eliminado limite artificial [:100].
        Se devuelven TODAS las fotos reales del hotel encontradas en el HTML,
        sin restriccion de cantidad. El filtro _is_hotel_photo() ya garantiza
        que solo pasan fotos del CDN bstatic.com/xdata/images/hotel/ —
        logos, banderas, avatares, iconos UI y tracking pixels son descartados.
        Las imagenes de habitaciones estan incluidas (mismo CDN, mismo path).
"""

import re
import json
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from loguru import logger


class BookingExtractor:
    """
    Extractor de datos de hoteles desde HTML de Booking.com.
    Soporta multi-idioma con múltiples selectores fallback.
    Estructura Booking.com 2025/2026.
    """

    def __init__(self, html_content: str, language: str = "en"):
        self.html_content = html_content
        self.language     = language
        self.tree         = None
        self.soup: Optional[BeautifulSoup] = None
        self._parse(html_content)

    def _parse(self, html_content: str):
        """Parsea el HTML."""
        try:
            from lxml import html as lhtml
            self.tree = lhtml.fromstring(html_content)
        except Exception:
            self.tree = None

        try:
            self.soup = BeautifulSoup(html_content, "lxml")
        except Exception:
            try:
                self.soup = BeautifulSoup(html_content, "html.parser")
            except Exception as e:
                logger.error(f"Error parseando HTML: {e}")
                self.soup = None

    # ── UTILIDADES ────────────────────────────────────────────────────────────

    @staticmethod
    def _clean_address(v: str) -> Optional[str]:
        """
        Elimina texto de puntuacion/valoracion que Booking.com pega en el
        mismo bloque DOM que la direccion fisica del hotel.

        Ejemplos de ruido capturado:
          '..., SeychellesUbicacionexcelente, puntuada con 9.1/10!'
          '..., BahamasDespues de reservar, encontraras todos los datos...'
          '..., ChurchDestacado por los clientes'
        """
        if not v:
            return None
        noise_triggers = [
            r'Ubicaci[oó]n', r'Excellent\s+location', r'Great\s+location',
            r'Location\b', r'[Vv]alorad', r'puntuada', r'basada\s+en\s*\d',
            r'comentarios', r'Ver\s+mapa', r'Show\s+on\s+map',
            r'\d+\s*/\s*10', r'[Pp]untuaci[oó]n', r'[Rr]ated\s+by',
            r'customers?', r'[Dd]estacado', r'[Dd]e\s+las\s+m[aá]s',
            r'[Vv]aloradas?', r'[Vv]alued\s+by', r'[Dd]espu[eé]s\s+de\s+reservar',
            r'encontrar[aá]s', r'n[uú]mero\s+de\s+tel[eé]fono',
        ]
        pattern = '|'.join(f'(?:{p})' for p in noise_triggers)
        m = re.search(pattern, v, re.IGNORECASE)
        if m:
            v = v[:m.start()].strip().rstrip('.,;– \n\t')
        return (v[:200] if len(v) > 200 else v).strip() or None

    @staticmethod
    def _normalize_img_url(url: str) -> str:
        """
        Normaliza URLs de imagenes de Booking.com a la resolucion maxima.
        Cubre TODOS los formatos del CDN bstatic.com:
          /max500/     -> /max1280x900/   (un solo numero)
          /max300/     -> /max1280x900/
          /max500x334/ -> /max1280x900/   (dos numeros)
          /square60/   -> /max1280x900/   (miniatura cuadrada)
        """
        url = re.sub(r'/max\d+x\d+x?\d*/', '/max1280x900/', url)
        url = re.sub(r'/max\d+/',          '/max1280x900/', url)
        url = re.sub(r'/square\d+/',       '/max1280x900/', url)
        return url

    def _xpath_text(self, xpath_expr: str) -> Optional[str]:
        if self.tree is None:
            return None
        try:
            elements = self.tree.xpath(xpath_expr)
            if elements:
                elem = elements[0]
                text = (elem if isinstance(elem, str) else elem.text_content()).strip()
                return text or None
        except Exception as e:
            logger.debug(f"XPath error ({xpath_expr[:60]}): {e}")
        return None

    def _xpath_list(self, xpath_expr: str) -> List[str]:
        if self.tree is None:
            return []
        try:
            return [
                (e if isinstance(e, str) else e.text_content()).strip()
                for e in self.tree.xpath(xpath_expr)
                if (e if isinstance(e, str) else e.text_content()).strip()
            ]
        except Exception:
            return []

    def _find_text(self, *args, **kwargs) -> Optional[str]:
        """BeautifulSoup find + get_text seguro."""
        if self.soup is None:
            return None
        try:
            elem = self.soup.find(*args, **kwargs)
            if elem:
                return elem.get_text(strip=True) or None
        except Exception:
            pass
        return None

    def _meta(self, prop: str = None, name: str = None) -> Optional[str]:
        """Extrae content de una meta tag."""
        if self.soup is None:
            return None
        try:
            if prop:
                tag = self.soup.find("meta", property=prop)
            else:
                tag = self.soup.find("meta", attrs={"name": name})
            if tag and tag.get("content"):
                return tag["content"].strip() or None
        except Exception:
            pass
        return None

    # ── DETECCIÓN DE PÁGINA REAL ──────────────────────────────────────────────

    def is_real_hotel_page(self) -> bool:
        """Devuelve True si parece una página real de hotel (no consentimiento)."""
        if self.soup is None:
            return False
        html_lower = self.html_content.lower()
        # Señales de página de hotel real
        has_hotel_signals = any(k in html_lower for k in [
            "property-description",
            "hp_facilities_box",
            "maxotelroomarea",
            "reviewscore",
            "review-score",
            "b2hotelpage",
            "hoteldetails",
        ])
        # Señales de consentimiento (página vacía)
        is_consent = any(k in html_lower for k in [
            "privacymanager",
            "optanon",
            "cookie-consent",
            "cookieconsentpopup",
        ]) and not has_hotel_signals
        return has_hotel_signals and not is_consent

    # ─────────────────────────────────────────────────────────────────────────
    # EXTRACCIÓN COMPLETA
    # ─────────────────────────────────────────────────────────────────────────

    def extract_all(self) -> Dict:
        result = {
            "name":            self.extract_name(),
            "address":         self.extract_address(),
            "description":     self.extract_description(),
            "rating":          self.extract_rating(),
            "rating_category": self.extract_rating_category(),
            "total_reviews":   self.extract_total_reviews(),
            "review_scores":   self.extract_review_scores(),
            "services":        self.extract_services(),
            "facilities":      self.extract_facilities(),
            "house_rules":     self.extract_house_rules(),
            "important_info":  self.extract_important_info(),
            "rooms":           self.extract_rooms(),
            "images_urls":     self.extract_images(),
            "language":        self.language,
        }
        # Diagnostico: mostrar que campos quedaron vacios
        empty = [k for k, v in result.items()
                 if v is None or v == [] or v == {} or v == ""]
        if empty:
            logger.debug(f"  [extractor] Campos vacios [{self.language}]: {empty}")
        imgs_count = len(result.get("images_urls") or [])
        if imgs_count:
            logger.debug(f"  [extractor] {imgs_count} imagenes extraidas [{self.language}]")
        return result

    # ─────────────────────────────────────────────────────────────────────────
    # NOMBRE (8 fallbacks progresivos)
    # ─────────────────────────────────────────────────────────────────────────

    @staticmethod
    def _clean_hotel_name(v: str) -> Optional[str]:
        """
        Limpia el nombre del hotel extraído de og:title o meta title.
        Booking.com añade:
          - Prefijo de estrellas:  "★★★★★ Hotel Name" → "Hotel Name"
          - Sufijo Booking.com:    "Hotel Name | Booking.com" → "Hotel Name"
          - Sufijo ciudad/país:    "Hotel Name, City, Country" → "Hotel Name"
            (solo si el sufijo coincide con patrón ciudad corta + país)
        """
        if not v:
            return None
        # Eliminar sufijo " | Booking.com" o " - Booking.com"
        v = re.sub(r'\s*[|\-–]\s*Booking\.com\s*$', '', v, flags=re.IGNORECASE).strip()
        # Eliminar prefijo de estrellas unicode ★☆ y espacios
        v = re.sub(r'^[★☆✦✩\s]+', '', v).strip()
        # Eliminar sufijo ", Ciudad, País" — Booking.com lo añade al og:title.
        # Patrón: ", Palabra(s), Palabra(s)" al final donde los segmentos
        # son relativamente cortos (≤30 chars cada uno) = ciudad + país.
        # NO eliminar si el nombre del hotel en sí contiene comas importantes.
        parts = v.split(',')
        if len(parts) >= 3:
            # Los últimos 2 segmentos son ciudad y país si son cortos
            last_two = parts[-2:]
            if all(len(p.strip()) <= 35 for p in last_two):
                v = ','.join(parts[:-2]).strip().rstrip(',').strip()
        elif len(parts) == 2:
            # Solo 1 sufijo: puede ser ciudad o país; eliminar si es corto
            if len(parts[-1].strip()) <= 35:
                v = parts[0].strip()
        return v if v and len(v) > 2 else None

    def extract_name(self) -> Optional[str]:
        """
        Extrae el nombre del hotel con 8 fallbacks.
        [v2.7] data-testid='title' es el MÁS FIABLE (solo nombre, sin ciudad/país).
        og:title se usa como fallback con limpieza de prefijo ★ y sufijo de ubicación.
        """
        # 1. data-testid="title" (estructura Booking.com 2024-2026 — solo el nombre)
        if self.soup:
            elem = self.soup.find(attrs={"data-testid": "title"})
            if elem:
                v = elem.get_text(strip=True)
                # Limpiar posible prefijo de estrellas
                v = re.sub(r'^[★☆✦✩\s]+', '', v).strip() if v else v
                if v and len(v) > 2:
                    logger.debug(f"  Nombre extraído vía: data-testid='title'")
                    return v

        # 2. data-testid="property-name"
        if self.soup:
            elem = self.soup.find(attrs={"data-testid": "property-name"})
            if elem:
                v = elem.get_text(strip=True)
                v = re.sub(r'^[★☆✦✩\s]+', '', v).strip() if v else v
                if v and len(v) > 2:
                    logger.debug(f"  Nombre extraído vía: data-testid='property-name'")
                    return v

        # 3. og:title (con limpieza de ★ y sufijo ciudad/país)
        v = self._meta(prop="og:title")
        if v:
            v = self._clean_hotel_name(v)
            if v:
                logger.debug(f"  Nombre extraído vía: og:title (limpiado)")
                return v

        # 4. meta name="title"
        v = self._meta(name="title")
        if v:
            v = self._clean_hotel_name(v)
            if v:
                logger.debug(f"  Nombre extraído vía: meta[name=title] (limpiado)")
                return v

        # 5. XPath clásico del proyecto
        v = self._xpath_text(
            '//div[@id="wrap-hotelpage-top"]/div[2]/div[1]/div[2]/h2[1]'
        )
        if v:
            logger.debug(f"  Nombre extraído vía: XPath wrap-hotelpage-top/h2")
            return v

        # 6. h2.pp-header__title
        if self.soup:
            h2 = self.soup.find("h2", class_="pp-header__title")
            if h2:
                v = h2.get_text(strip=True)
                if v:
                    logger.debug(f"  Nombre extraído vía: h2.pp-header__title")
                    return v

        # 7. h1 o h2 con "property" en clase o id
        if self.soup:
            for tag in self.soup.find_all(["h1", "h2"]):
                cls  = " ".join(tag.get("class", []))
                tid  = tag.get("id", "")
                if any(k in (cls + tid).lower() for k in ["property", "hotel", "title", "name"]):
                    v = tag.get_text(strip=True)
                    if v and len(v) > 3:
                        logger.debug(f"  Nombre extraído vía: h1/h2 con clase 'property/hotel/title'")
                        return v

        # 8. JSON-LD structured data
        if self.soup:
            for script in self.soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string or "")
                    if isinstance(data, dict) and data.get("name"):
                        v = data["name"]
                        if isinstance(v, str) and len(v) > 3:
                            logger.debug(f"  Nombre extraído vía: JSON-LD")
                            return v
                except Exception:
                    continue

        logger.warning(f"  ❌ Nombre NO extraído — ningún selector funcionó")
        return None

    # ─────────────────────────────────────────────────────────────────────────
    # DIRECCIÓN
    # ─────────────────────────────────────────────────────────────────────────

    def extract_address(self) -> Optional[str]:
        """
        [v2.4] JSON-LD siempre primero: datos estructurados, nunca contienen
        texto de rating/valoracion. Los selectores DOM usan _clean_address().
        """
        if self.soup is None:
            return None

        # 1. JSON-LD — FUENTE MAS LIMPIA (sin ruido de rating)
        for script in self.soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "")
                if isinstance(data, dict):
                    addr = data.get("address")
                    if isinstance(addr, dict):
                        street   = addr.get("streetAddress", "").strip()
                        locality = addr.get("addressLocality", "").strip()
                        region   = addr.get("addressRegion", "").strip()
                        postal   = addr.get("postalCode", "").strip()
                        country  = addr.get("addressCountry", "").strip()

                        # streetAddress a menudo YA contiene city y region.
                        # Solo anadir sub-campos si no estan ya en streetAddress.
                        street_lower = street.lower()
                        parts = [street] if street else []
                        for val in [locality, postal, country]:
                            if val and val.lower() not in street_lower:
                                parts.append(val)

                        full = ", ".join(p for p in parts if p)
                        if full and len(full) > 5:
                            return full
                    elif isinstance(addr, str) and len(addr.strip()) > 5:
                        return self._clean_address(addr.strip())
            except Exception:
                continue

        # 2 – 6. Selectores DOM, todos pasan por _clean_address()
        # 2. data-testid="address"
        elem = self.soup.find(attrs={"data-testid": "address"})
        if elem:
            v = self._clean_address(elem.get_text(strip=True))
            if v:
                return v

        # 3. PropertyHeaderAddressDesktop (Booking.com 2026)
        elem = self.soup.find(attrs={"data-testid": re.compile(r"PropertyHeaderAddress|address-line", re.I)})
        if elem:
            v = self._clean_address(elem.get_text(strip=True))
            if v:
                return v

        # 4. XPath clasico del proyecto
        v = self._xpath_text(
            '//*[@id="wrap-hotelpage-top"]/div[2]/div/div[3]/div/div/div/div/span[1]/button/div'
        )
        if v:
            return self._clean_address(v)

        # 5. Clases clasicas
        for cls in ["hp_address_subtitle", "address", "address-text"]:
            elem = self.soup.find(class_=cls)
            if elem:
                v = self._clean_address(elem.get_text(strip=True))
                if v:
                    return v

        # 6. itemprop="address"
        elem = self.soup.find(attrs={"itemprop": "address"})
        if elem:
            v = self._clean_address(elem.get_text(strip=True))
            if v:
                return v

        return None

    # ─────────────────────────────────────────────────────────────────────────
    # DESCRIPCIÓN
    # ─────────────────────────────────────────────────────────────────────────

    def extract_description(self) -> Optional[str]:
        # 1. data-testid="property-description" (p)
        if self.soup:
            elem = self.soup.find("p", attrs={"data-testid": "property-description"})
            if elem:
                return elem.get_text(strip=True) or None

        # 2. XPath
        v = self._xpath_text('//p[@data-testid="property-description"]')
        if v:
            return v

        # 3. div#property_description_content
        if self.soup:
            div = self.soup.find("div", id="property_description_content")
            if div:
                paragraphs = div.find_all("p")
                text = " ".join(p.get_text(strip=True) for p in paragraphs)
                return text or None

        # 4. div.hotel_desc_wrapper
        if self.soup:
            div = self.soup.find("div", class_="hotel_desc_wrapper")
            if div:
                return div.get_text(strip=True) or None

        # 5. og:description
        return self._meta(prop="og:description")

    # ─────────────────────────────────────────────────────────────────────────
    # RATING NUMÉRICO
    # ─────────────────────────────────────────────────────────────────────────

    def extract_rating(self) -> Optional[float]:
        # 1. data-testid="review-score-component"
        if self.soup:
            elem = self.soup.find(attrs={"data-testid": "review-score-component"})
            if elem:
                text = elem.get_text()
                m = re.search(r'(\d+[.,]\d+)', text)
                if m:
                    try:
                        return float(m.group(1).replace(",", "."))
                    except Exception:
                        pass

        # 2. XPath review-score
        v = self._xpath_text('//div[@data-testid="review-score-component"]')
        if v:
            m = re.search(r'(\d+[.,]\d+)', v)
            if m:
                try:
                    return float(m.group(1).replace(",", "."))
                except Exception:
                    pass

        # 3. aria-label con puntuación
        if self.soup:
            for elem in self.soup.find_all(attrs={"aria-label": True}):
                label = elem.get("aria-label", "")
                m = re.search(r'(\d+[.,]\d+)\s*(?:out\s*of|\/)', label)
                if m:
                    try:
                        return float(m.group(1).replace(",", "."))
                    except Exception:
                        pass

        # 4. itemprop ratingValue
        if self.soup:
            elem = self.soup.find(attrs={"itemprop": "ratingValue"})
            if elem:
                content = elem.get("content") or elem.get_text()
                m = re.search(r'(\d+[.,]\d+)', content)
                if m:
                    try:
                        return float(m.group(1).replace(",", "."))
                    except Exception:
                        pass

        # 5. JSON-LD
        if self.soup:
            for script in self.soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string or "")
                    if isinstance(data, dict):
                        agg = data.get("aggregateRating", {})
                        rv  = agg.get("ratingValue")
                        if rv:
                            return float(rv)
                except Exception:
                    continue

        return None

    # ─────────────────────────────────────────────────────────────────────────
    # CATEGORÍA DE RATING ("Excepcional", "Fabuloso", etc.)
    # ─────────────────────────────────────────────────────────────────────────

    def extract_rating_category(self) -> Optional[str]:
        """
        [v2.7] Categorías de rating completas para todos los idiomas soportados.
        Booking.com usa diferentes palabras según el rango de puntuación:
          9.0-10:  Exceptional / Excepcional / Hervorragend / Exceptionnel / Eccezionale
          8.0-8.9: Fabulous    / Fabuloso    / Fabelhaft    / Fabuleux     / Favoloso
                   Excellent   / Excelente   / Ausgezeichnet
          7.0-7.9: Very good   / Muy bien    / Sehr gut     / Très bien    / Molto buono
          6.0-6.9: Good        / Bien        / Gut          / Bien         / Buono
          5.0-5.9: Pleasant    / Agradable   / Angenehm     / Agréable     / Piacevole
        """
        CATEGORIES = {
            "en": [
                "Exceptional", "Superb", "Fabulous", "Excellent",
                "Very good", "Good", "Pleasant", "No rating",
            ],
            "es": [
                "Excepcional", "Fabuloso", "Espléndido", "Excelente",
                "Muy bien", "Bien", "Agradable",
            ],
            "de": [
                "Hervorragend", "Fantastisch", "Ausgezeichnet", "Fabelhaft",
                "Sehr gut", "Gut", "Angenehm",
            ],
            "fr": [
                "Exceptionnel", "Fabuleux", "Superbe", "Excellent",
                "Très bien", "Bien", "Agréable",
            ],
            "it": [
                "Eccezionale", "Favoloso", "Fantastico", "Eccellente",
                "Molto buono", "Buono", "Piacevole",
            ],
            "pt": [
                "Excepcional", "Fabuloso", "Soberbo", "Excelente",
                "Muito bom", "Bom", "Agradável",
            ],
            "nl": [
                "Uitzonderlijk", "Fantastisch", "Uitstekend",
                "Zeer goed", "Goed", "Aangenaam",
            ],
            "ru": [
                "Исключительно", "Великолепно", "Отлично",
                "Очень хорошо", "Хорошо",
            ],
        }
        # Buscar en idioma del documento + inglés como fallback universal
        search_cats = (
            CATEGORIES.get(self.language, []) +
            CATEGORIES.get("en", [])
        )
        # Eliminar duplicados manteniendo orden
        seen = set()
        search_cats = [c for c in search_cats if not (c in seen or seen.add(c))]

        if self.soup:
            # 1. Buscar en review-score component (fuente más fiable)
            elem = self.soup.find(attrs={"data-testid": "review-score-component"})
            if elem:
                text_content = elem.get_text()
                for cat in search_cats:
                    if cat.lower() in text_content.lower():
                        return cat

            # 2. aria-label en elementos del bloque de puntuación
            score_block = self.soup.find(attrs={"data-testid": re.compile(r"review-score|rating", re.I)})
            if score_block:
                for tag in score_block.find_all(attrs={"aria-label": True}):
                    label = tag.get("aria-label", "")
                    for cat in search_cats:
                        if cat.lower() in label.lower():
                            return cat

            # 3. Scan global de aria-label
            for tag in self.soup.find_all(attrs={"aria-label": True}):
                label = tag.get("aria-label", "")
                for cat in search_cats:
                    if cat.lower() in label.lower():
                        return cat

            # 4. Inferir desde rating numérico si no se encontró texto
            rating = self.extract_rating()
            if rating is not None:
                return self._infer_rating_category_from_score(rating)

        return None

    def _infer_rating_category_from_score(self, score: float) -> Optional[str]:
        """
        [v2.7] Infiere la categoría de rating a partir del score numérico
        cuando no se puede extraer el texto de categoría del DOM.
        """
        SCORE_MAP = {
            "en": [(9.0, "Exceptional"), (8.0, "Excellent"), (7.0, "Very good"), (6.0, "Good"), (0.0, "Pleasant")],
            "es": [(9.0, "Excepcional"), (8.0, "Fabuloso"),  (7.0, "Muy bien"), (6.0, "Bien"), (0.0, "Agradable")],
            "de": [(9.0, "Hervorragend"), (8.0, "Fabelhaft"), (7.0, "Sehr gut"), (6.0, "Gut"), (0.0, "Angenehm")],
            "fr": [(9.0, "Exceptionnel"), (8.0, "Fabuleux"), (7.0, "Très bien"), (6.0, "Bien"), (0.0, "Agréable")],
            "it": [(9.0, "Eccezionale"),  (8.0, "Favoloso"), (7.0, "Molto buono"), (6.0, "Buono"), (0.0, "Piacevole")],
            "pt": [(9.0, "Excepcional"),  (8.0, "Fabuloso"), (7.0, "Muito bom"), (6.0, "Bom"), (0.0, "Agradável")],
            "nl": [(9.0, "Uitzonderlijk"), (8.0, "Fantastisch"), (7.0, "Zeer goed"), (6.0, "Goed"), (0.0, "Aangenaam")],
            "ru": [(9.0, "Исключительно"), (8.0, "Великолепно"), (7.0, "Очень хорошо"), (6.0, "Хорошо"), (0.0, "Хорошо")],
        }
        scale = SCORE_MAP.get(self.language) or SCORE_MAP["en"]
        for threshold, label in scale:
            if score >= threshold:
                return label
        return None

    # ─────────────────────────────────────────────────────────────────────────
    # TOTAL REVIEWS
    # ─────────────────────────────────────────────────────────────────────────

    def extract_total_reviews(self) -> Optional[int]:
        if self.soup:
            # 1. data-testid="review-score-component"
            elem = self.soup.find(attrs={"data-testid": "review-score-component"})
            if elem:
                text = elem.get_text()
                m = re.search(r'([\d,\.]+)\s*(?:review|opinión|Bewertung|avis|recensioni|avaliações)', text, re.IGNORECASE)
                if m:
                    try:
                        return int(re.sub(r'[,\.]', '', m.group(1)))
                    except Exception:
                        pass

            # 2. itemprop reviewCount
            elem = self.soup.find(attrs={"itemprop": "reviewCount"})
            if elem:
                content = elem.get("content") or elem.get_text()
                m = re.search(r'(\d+)', content.replace(",", ""))
                if m:
                    return int(m.group(1))

        # 3. JSON-LD
        if self.soup:
            for script in self.soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string or "")
                    if isinstance(data, dict):
                        rc = data.get("aggregateRating", {}).get("reviewCount")
                        if rc:
                            return int(rc)
                except Exception:
                    continue

        return None

    # ─────────────────────────────────────────────────────────────────────────
    # REVIEW SCORES (puntuaciones por categoría)
    # ─────────────────────────────────────────────────────────────────────────

    def extract_review_scores(self) -> Dict:
        scores = {}
        if self.soup is None:
            return scores

        # 1. ReviewSubscoresDesktop (estructura clasica)
        container = self.soup.find(attrs={"data-testid": "ReviewSubscoresDesktop"})
        if container:
            for item in container.find_all(class_=re.compile(r"subscores|score|category", re.I)):
                text = item.get_text(separator=" ").strip()
                m = re.search(r'^(.+?)\s+(\d+[.,]\d+)\s*$', text)
                if m:
                    try:
                        scores[m.group(1).strip()] = float(m.group(2).replace(",", "."))
                    except Exception:
                        pass
            if scores:
                return scores

        # 2. review-score-category items (Booking.com 2024-2026)
        for elem in self.soup.find_all(attrs={"data-testid": re.compile(r"review.?score.?category|ReviewScore", re.I)}):
            text = elem.get_text(separator=" ").strip()
            m = re.search(r'([A-Za-z\u00C0-\u024F\s]{2,40})\s+(\d+[.,]\d+)', text)
            if m:
                try:
                    score_val = float(m.group(2).replace(",", "."))
                    if 1.0 <= score_val <= 10.0:
                        scores[m.group(1).strip()] = score_val
                except Exception:
                    pass
        if scores:
            return scores

        # 3. JSON-LD aggregateRating con subratings
        for script in self.soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "")
                if isinstance(data, dict):
                    agg = data.get("aggregateRating", {})
                    if isinstance(agg, dict) and agg.get("ratingValue"):
                        scores["overall"] = float(str(agg["ratingValue"]).replace(",", "."))
                    # reviewAspects
                    for aspect in data.get("reviewAspects", []):
                        name = aspect.get("name") or aspect.get("@type", "")
                        val  = aspect.get("ratingValue")
                        if name and val:
                            try:
                                scores[name] = float(str(val).replace(",", "."))
                            except Exception:
                                pass
                if scores:
                    return scores
            except Exception:
                continue

        # 4. Scan general: pares de texto+puntuacion en el area de reviews
        review_section = self.soup.find(attrs={"data-testid": re.compile(r"review", re.I)})
        if review_section:
            text = review_section.get_text(separator="\n")
            for m in re.finditer(r'([A-Za-z\u00C0-\u024F][A-Za-z\u00C0-\u024F\s]{1,30})\s*\n\s*(\d+[.,]\d+)', text):
                try:
                    score_val = float(m.group(2).replace(",", "."))
                    if 1.0 <= score_val <= 10.0:
                        scores[m.group(1).strip()] = score_val
                except Exception:
                    pass

        return scores

    # ─────────────────────────────────────────────────────────────────────────
    # SERVICIOS
    # ─────────────────────────────────────────────────────────────────────────

    def extract_services(self) -> List[str]:
        services = []
        if self.soup is None:
            return services

        # 1. hp_facilities_box
        box = self.soup.find(id="hp_facilities_box")
        if box:
            for li in box.find_all(["li", "span"]):
                text = li.get_text(strip=True)
                if text and len(text) > 2 and text not in services:
                    services.append(text)
            if services:
                return services[:50]

        # 2. data-testid con "facilities" o "amenities"
        for container in self.soup.find_all(attrs={"data-testid": re.compile(r"facilities|amenities|services", re.I)}):
            for li in container.find_all(["li", "span", "div"]):
                text = li.get_text(strip=True)
                if text and 2 < len(text) < 100 and text not in services:
                    services.append(text)

        return services[:50]

    # ─────────────────────────────────────────────────────────────────────────
    # FACILITIES (instalaciones por categoría)
    # ─────────────────────────────────────────────────────────────────────────

    def extract_facilities(self) -> Dict:
        facilities = {}
        if self.soup is None:
            return facilities

        box = self.soup.find(id="hp_facilities_box")
        if not box:
            # intentar con data-testid
            box = self.soup.find(attrs={"data-testid": re.compile(r"facilities", re.I)})

        if box:
            # Buscar secciones/categorías
            for section in box.find_all(["div", "section"], recursive=False):
                header = section.find(["h3", "h4", "p"])
                if header:
                    cat   = header.get_text(strip=True)
                    items = [li.get_text(strip=True) for li in section.find_all("li") if li.get_text(strip=True)]
                    if items:
                        facilities[cat] = items

        return facilities

    # ─────────────────────────────────────────────────────────────────────────
    # HOUSE RULES / POLÍTICAS
    # ─────────────────────────────────────────────────────────────────────────

    def extract_house_rules(self) -> Optional[str]:
        if self.soup:
            # 1. id="policies"
            sec = self.soup.find(id="policies")
            if sec:
                return sec.get_text(separator="\n", strip=True) or None

            # 2. data-testid="property-policies"
            sec = self.soup.find(attrs={"data-testid": re.compile(r"policies|rules", re.I)})
            if sec:
                return sec.get_text(separator="\n", strip=True) or None

        return None

    # ─────────────────────────────────────────────────────────────────────────
    # IMPORTANT INFO
    # ─────────────────────────────────────────────────────────────────────────

    def extract_important_info(self) -> Optional[str]:
        if self.soup:
            sec = self.soup.find(id="important_info")
            if sec:
                return sec.get_text(separator="\n", strip=True) or None

            sec = self.soup.find(attrs={"data-testid": "important-info"})
            if sec:
                return sec.get_text(separator="\n", strip=True) or None

        return None

    # ─────────────────────────────────────────────────────────────────────────
    # HABITACIONES
    # ─────────────────────────────────────────────────────────────────────────

    def extract_rooms(self) -> List[Dict]:
        rooms = []
        seen_names = set()
        if self.soup is None:
            return rooms

        def _add_room(name, price=None, capacity=None, beds=None):
            name = name.strip() if name else None
            if not name or name in seen_names or len(name) < 3:
                return
            seen_names.add(name)
            room = {"name": name}
            if price:
                room["price"] = price.strip()
            if capacity:
                room["capacity"] = capacity.strip()
            if beds:
                room["beds"] = beds.strip()
            rooms.append(room)

        # 1. id="maxotelRoomArea" (estructura clasica)
        area = self.soup.find(id="maxotelRoomArea")
        if area:
            for row in area.find_all(["tr", "div"], class_=re.compile(r"room|hprt")):
                name_e  = row.find(class_=re.compile(r"room.?name|room.?title", re.I))
                price_e = row.find(class_=re.compile(r"price|rate", re.I))
                if name_e:
                    _add_room(name_e.get_text(strip=True),
                              price_e.get_text(strip=True) if price_e else None)

        # 2. data-testid con "roomType" o "room" (estructura 2024-2026)
        if not rooms:
            for container in self.soup.find_all(attrs={"data-testid": re.compile(r"roomType|room.?block|room.?row", re.I)}):
                name_e = (
                    container.find(attrs={"data-testid": re.compile(r"room.?name|room.?type.?name", re.I)})
                    or container.find(["h3", "h4", "strong"])
                )
                price_e = container.find(attrs={"data-testid": re.compile(r"price", re.I)})
                if name_e:
                    _add_room(name_e.get_text(strip=True),
                              price_e.get_text(strip=True) if price_e else None)

        # 3. Tabla HPRT (tabla de habitaciones clasica)
        if not rooms:
            for row in self.soup.find_all(class_=re.compile(r"hprt-table-room|roomtype", re.I)):
                name_e = row.find(class_=re.compile(r"room.?type|room.?name", re.I))
                if name_e:
                    _add_room(name_e.get_text(strip=True))

        # 4. JSON-LD con containsPlace o roomAmenities
        if not rooms:
            for script in self.soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string or "")
                    if isinstance(data, dict):
                        for room_data in data.get("containsPlace", []):
                            name = room_data.get("name")
                            if name:
                                _add_room(name)
                except Exception:
                    continue

        return rooms[:20]

    # ─────────────────────────────────────────────────────────────────────────
    # IMÁGENES
    # ─────────────────────────────────────────────────────────────────────────

    def extract_images(self) -> List[str]:
        """
        [v2.6] Extrae TODAS las fotos reales del hotel y sus habitaciones, SIN LIMITE.

        Patron valido (unico aceptado):
          cf.bstatic.com/xdata/images/hotel/  — fotos de hotel Y habitaciones

        Descartado automaticamente por _is_hotel_photo():
          - t-cf.bstatic.com/design-assets/   (logos, banderas, iconos UI Booking.com)
          - xx.bstatic.com/static/img/review/  (avatares de resenadores)
          - r-xx.bstatic.com/images/user/      (fotos de perfil de usuarios)
          - bstatic.com/xdata/images/xphoto/   (fotos de destino, no del hotel)
          - tracking pixels, GIFs, 1×1

        No hay limite de cantidad: se devuelven todas las URLs encontradas.
        El filtro de dimensiones minimas (200×150 px) en ImageDownloader descarta
        cualquier residuo pequeno que pudiera escapar.
        """
        images = []
        seen   = set()

        def _is_hotel_photo(url: str) -> bool:
            """Acepta solo fotos reales del hotel del CDN de Booking.com."""
            if not url or not url.startswith("http"):
                return False
            # UNICO patron valido: CDN principal de fotos de hotel
            return "bstatic.com/xdata/images/hotel/" in url

        def _add(url: str):
            if not _is_hotel_photo(url):
                return
            # Normalizar a resolucion maxima — usa _normalize_img_url para cubrir
            # /max500/, /max300/, /max1280x900/, /square60/, etc.
            url = self._normalize_img_url(url)
            # Deduplicacion por path base (sin query params de firma)
            base = url.split("?")[0] if "?" in url else url
            if base not in seen:
                seen.add(base)
                images.append(url)

        if self.soup is None:
            return images

        # 1. GalleryGridViewModal (galeria interactiva si esta abierta)
        gallery = self.soup.find(attrs={"data-testid": "GalleryGridViewModal-wrapper"})
        if gallery:
            for img in gallery.find_all("img"):
                _add(img.get("src") or img.get("data-src") or "")

        # 2. b2hotelPage - bloque principal de la ficha del hotel
        b2page = self.soup.find(id="b2hotelPage")
        if not b2page:
            b2page = self.soup.find(attrs={"data-testid": "b2hotelPage"})
        if b2page:
            for img in b2page.find_all("img"):
                _add(img.get("src") or img.get("data-src") or img.get("data-lazy-src") or "")
            for source in b2page.find_all("source"):
                for part in (source.get("srcset", "") or "").split(","):
                    _add(part.strip().split(" ")[0])

        # 3. Scan global por fotos de hotel (captura lo que no este en b2hotelPage)
        for img in self.soup.find_all("img"):
            _add(img.get("src") or img.get("data-src") or img.get("data-lazy-src") or "")
            for part in (img.get("srcset", "") or "").split(","):
                _add(part.strip().split(" ")[0])

        # 4. og:image — fallback si no se encontro nada (debe ser foto del hotel)
        if not images:
            og_img = self._meta(prop="og:image")
            if og_img and _is_hotel_photo(og_img):
                _add(og_img)

        # 5. data-photos JSON embebido en algun elemento
        for tag in self.soup.find_all(attrs={"data-photos": True}):
            try:
                photos = json.loads(tag.get("data-photos", "[]"))
                for p in photos:
                    if isinstance(p, dict):
                        _add(p.get("url") or p.get("src") or "")
                    elif isinstance(p, str):
                        _add(p)
            except Exception:
                pass

        count = len(images)
        if count:
            logger.debug(f"  [extractor] {count} fotos de hotel extraidas [{self.language}]")
        else:
            logger.warning(f"  [extractor] Sin fotos de hotel en [{self.language}]")

        # [v2.6] Sin limite: se devuelven TODAS las fotos reales del hotel.
        # El filtro _is_hotel_photo() ya elimina logos, banderas y avatares.
        return images
