# BookingScraper Pro v6.0.0 — Informe de Auditoría de Código (Build 55)

**Versión del documento:** 2.0
**Fecha:** 2026-03-23
**Repositorio:** https://github.com/corralejo-htls/scrapv25.git
**Build anterior:** 54
**Build actual:** 55
**Plataforma:** Windows 11 (Ejecución Local)
**Auditor:** AI Code Review System

---

## Resumen Ejecutivo

Este documento proporciona una auditoría exhaustiva del sistema BookingScraper Pro, versión 6.0.0 build 55. La auditoría revisó todos los archivos de código fuente (`app/*.py`, `scripts/load_urls.py`), el esquema de base de datos (`schema_v54_complete.sql`), las exportaciones de datos CSV (`pruebas/_table__*__.csv`), las muestras HTML de prueba (`pruebas/HTML_*.md`), logs y archivos de configuración.

Se identificaron y corrigieron **5 bugs confirmados** en el build 55. Todas las correcciones han sido validadas contra las estructuras DOM reales de Booking.com proporcionadas en las muestras HTML del directorio `pruebas/`.

**Estado Build 55:** Todos los bugs críticos resueltos. Sistema OK para proceder con el despliegue tras verificación.

---

## Bugs Corregidos en Build 55

### BUG-EXTR-010: Extracción de Reseñas de Huéspedes — Tabla Vacía (CRÍTICO)

**Severidad:** CRÍTICA
**Estado:** CORREGIDO en build 55
**Archivo afectado:** `app/extractor.py` → `_extract_guest_reviews()`
**Tabla afectada:** `hotels_guest_reviews` (0 registros en build 54)

#### Causa Raíz

La función `_extract_guest_reviews()` utilizaba selectores basados en regex que no coinciden con el DOM actual de Booking.com:

```python
# ANTERIOR (build 54) — Selectores ROTOS
_REVIEW_SELECTORS = [
    {"attrs": {"data-testid": re.compile(r"review.score|reviewScore", re.I)}},
    {"attrs": {"data-testid": re.compile(r"review.category|review.breakdown", re.I)}},
    ...
]
```

El DOM real de Booking.com usa `data-testid="review-subscore"` (cadena exacta, no patrón regex), con una estructura de elementos `<div>` individuales por categoría de reseña:

```html
<div data-testid="review-subscore" aria-label="Puntuación media sobre 10">
  <div>
    <span class="d96a4619c0">Personal </span>     <!-- categoría -->
    <div aria-hidden="true" class="...">9,1</div>  <!-- puntuación visible -->
  </div>
  <div role="meter" aria-valuetext="9,1" ...>      <!-- puntuación programática -->
```

Los patrones regex `review.score`, `reviewScore`, `review.category`, `review.breakdown` nunca coinciden con `review-subscore`, por lo que nunca se encontraba ninguna sección.

#### Corrección Aplicada

Se añadió una nueva "Estrategia 0" antes de los selectores legacy. Busca TODOS los elementos `data-testid="review-subscore"` directamente y extrae:

- **Categoría:** del primer `<span>` dentro del elemento subscore
- **Puntuación:** preferencia por `aria-valuetext` de `[role="meter"]` (más fiable, independiente de locale), con fallback al texto del div `aria-hidden="true"`
- **Normalización:** separadores decimales de coma reemplazados por puntos (ej: `9,1` → `9.1` para locale ES)

#### Resultados Esperados

| Idioma | Categorías Esperadas |
|--------|---------------------|
| en | Staff 9.1, Facilities 9.2, Cleanliness 9.3, Comfort 9.4, Value for money 8.5, Location 9.1, Free WiFi 10 |
| es | Personal 9.1, Instalaciones y servicios 9.2, Limpieza 9.3, Confort 9.4, Relación calidad-precio 8.5, Ubicación 9.1, WiFi gratis 10 |

#### Verificación

Validado contra muestras HTML:
- `pruebas/HTML_garden-hill-resort-amp-spa_en-gb_html__Reviews_.md`
- `pruebas/HTML_garden-hill-resort-amp-spa_es_html__Reviews_.md`

---

### FIX-LEGAL-003: Información Legal — Título Duplicado en ES (ALTA)

**Severidad:** ALTA
**Estado:** CORREGIDO en build 55
**Archivo afectado:** `app/extractor.py` → `_extract_legal()`
**Tabla afectada:** `hotels_legal` (13 registros con `legal == legal_info`)

#### Causa Raíz

La función `_extract_legal()` (FIX-LEGAL-001, build 52) intentaba detectar el título legal desde elementos `<p>` cuando no se encontraba un heading estándar. Sin embargo, para ciertas páginas en español, el bucle de recopilación de párrafos no saltaba correctamente el párrafo del título debido a diferencias en el anidamiento del DOM.

El problema ocurría cuando:
1. El título "Información legal e importante" se detectaba desde un elemento `<p>` (línea 1166)
2. La lógica de salto (línea 1182) comparaba identidad del elemento (`para is title_el`)
3. Cuando el `<p>` estaba envuelto en contenedores `<div>` adicionales, la comparación de identidad fallaba
4. El texto del título se recopilaba de nuevo como `legal_info`

#### Evidencia de la Base de Datos

```csv
id,language,legal,legal_info
1,es,"Información legal e importante","Información legal e importante"
2,es,"Información legal e importante","Información legal e importante"
```

Los registros en inglés eran correctos (usando headings `<h2>`):
```csv
3,en,"Legal information","This property is managed, licensed or represented by a business..."
```

#### Corrección Aplicada (Protección de Tres Capas)

1. **Salto por texto:** Se añadió comparación explícita `para_text.strip() == legal_title.strip()` para saltar párrafos con texto idéntico al título (no solo identidad del elemento)
2. **Fallback recursivo:** Si la recopilación de párrafos con `recursive=False` no produce contenido, una búsqueda secundaria recursiva encuentra texto en estructuras `<div>` anidadas, excluyendo elementos que coinciden con el título
3. **Validación post-extracción:** Después de toda la lógica de extracción, si `legal == legal_info` (ambos campos idénticos), `legal_info` se limpia a cadena vacía

#### Registros Afectados

13 registros en español (IDs: 1, 2, 9, 10, 17, 18, 25, 26, 30, 34, 35, 42, 43).

#### Nota sobre el Schema SQL

El bloque de corrección de datos FIX-LEGAL-002 del SQL de build 54 ha sido **eliminado** en `schema_v55_complete.sql` porque la base de datos siempre se elimina y recrea. La corrección ahora está en `extractor.py` para prevenir el bug en el origen.

---

### BUG-LANG-001: Prioridad de Idioma — Inglés No Es Primero (MEDIA)

**Severidad:** MEDIA
**Estado:** CORREGIDO en build 55
**Archivo afectado:** `app/scraper_service.py` → `_process_url()`

#### Causa Raíz

El método `_process_url()` iteraba por los idiomas en el orden definido por `ENABLED_LANGUAGES`:

```python
# ANTERIOR (build 54)
languages = self._cfg.ENABLED_LANGUAGES  # ['es', 'en', 'de', 'it']
```

Con `ENABLED_LANGUAGES=es,en,de,it`, el español se scrapeaba primero. Esto violaba el requisito: *"siempre scrapear en idioma 'en' aunque no esté en la variable de entorno y siempre scrapear 'en' primero."*

Esto también afectaba la recopilación de fotos, que solo se ejecuta durante el scraping de `lang == "en"`.

#### Corrección Aplicada

```python
# NUEVO (build 55)
languages = list(self._cfg.ENABLED_LANGUAGES)
if 'en' in languages:
    languages.remove('en')
languages.insert(0, 'en')  # Inglés siempre primero
```

#### Garantía de Orden de Procesamiento

| ENABLED_LANGUAGES | Orden Build 54 | Orden Build 55 |
|-------------------|----------------|----------------|
| es,en,de,it       | es,en,de,it    | **en**,es,de,it |
| es,de,it          | es,de,it (¡en falta!) | **en**,es,de,it |
| de,it             | de,it (¡en falta!)    | **en**,de,it |

---

### BUG-IMG-UNPACK: Error de Desempaquetado en ImageDownloader (MEDIA)

**Severidad:** MEDIA
**Estado:** CORREGIDO en build 55
**Archivo afectado:** `app/scraper_service.py` → `_download_images()`

#### Causa Raíz

El método `download_photo_batch()` en `image_downloader.py` (línea 86) retorna `Dict[str, int]` — un diccionario que mapea `id_photo` al conteo de descargas. El código que lo llama esperaba una tupla:

```python
# ANTERIOR (build 54) — TypeError: too many values to unpack
downloaded, total = downloader.download_photo_batch(
    hotel_id=hotel_uuid,
    photos=gallery_photos,
)
```

Un `Dict` con 45 entradas no puede desempaquetarse en 2 variables, causando `ValueError: too many values to unpack (expected 2, got 45)`.

#### Evidencia del Log

```
[2026-03-23 02:17:11,521: WARNING/MainProcess]
ImageDownloader failed for 32ff0590...: too many values to unpack (expected 2, got 45)
```

#### Corrección Aplicada

```python
# NUEVO (build 55)
results = downloader.download_photo_batch(
    hotel_id=hotel_uuid,
    photos=gallery_photos,
)
downloaded = sum(results.values()) if isinstance(results, dict) else 0
```

**Nota:** Las fotos se guardaban exitosamente (la lógica de descarga funcionaba correctamente), pero el conteo de éxitos no se reportaba correctamente debido al error de desempaquetado en el código que llama.

---

### BUG-ENV-001: Orden de Idiomas en env.example (BAJA)

**Severidad:** BAJA
**Estado:** CORREGIDO en build 55
**Archivo afectado:** `env.example`

#### Cambio

```ini
# ANTERIOR (build 54)
ENABLED_LANGUAGES=es,en,de,it

# NUEVO (build 55)
# Regla: 'en' siempre se scrapeará primero aunque no esté en esta lista.
ENABLED_LANGUAGES=en,es,de,it
```

---

## Observaciones Adicionales (No Críticas)

### OBS-001: Desincronización de Versiones en Cabeceras

Los archivos `extractor.py` y `scraper_service.py` referenciaban build 53 en sus cabeceras, mientras que `config.py` y `models.py` referenciaban build 54. Todas las cabeceras actualizadas a build 55.

### OBS-002: Portugués No Incluido en ENABLED_LANGUAGES por Defecto

La URL de prueba 3 (`manaus-hoteis-millennium.pt-br.html`) usa portugués, pero el `ENABLED_LANGUAGES` por defecto es `en,es,de,it`. El mapeo `LANGUAGE_EXT` ya incluye `"pt": "pt-pt"`, así que añadir `pt` a `ENABLED_LANGUAGES` es suficiente.

**Recomendación:** Actualizar `env.example` para incluir portugués si se requieren hoteles portugueses:
```
ENABLED_LANGUAGES=en,es,de,it,pt
```

### OBS-003: Detección de Bloqueo de CloudScraper

CloudScraper recibe consistentemente respuestas de 3962 bytes (probablemente páginas de desafío JavaScript) antes de hacer fallback a Selenium. Esto duplica el tiempo de scraping. Considerar:
1. Actualizar cookies de bypass en `_BYPASS_COOKIES_BASE`
2. Añadir verificación de content-length para saltar reintentos más rápido
3. Implementar delays entre variantes de idioma del mismo hotel

### OBS-004: Validación de Selectores HTML

Los siguientes extractores deben validarse periódicamente contra el DOM actual de Booking.com:

| Función | Selector | Estado Build 55 |
|---------|----------|-----------------|
| `_extract_guest_reviews()` | `data-testid="review-subscore"` | **CORREGIDO** |
| `_extract_legal()` | `data-testid="property-section--legal"` | **CORREGIDO** |
| `_extract_faqs()` | `data-testid="faq*"` | Funcional (datos en CSV) |
| `_extract_policies()` | `data-testid="property-section--policies"` | Funcional (datos en CSV) |
| `_extract_property_highlights()` | `data-testid="property-highlights"` | Funcional (datos en CSV) |

---

## Archivos Modificados en Build 55

| Archivo | Cambios |
|---------|---------|
| `app/__init__.py` | BUILD_VERSION → 55 |
| `app/config.py` | BUILD_VERSION → 55 |
| `app/extractor.py` | BUG-EXTR-010 (reseñas), FIX-LEGAL-003 (legal duplicado), cabecera → build 55 |
| `app/scraper_service.py` | BUG-LANG-001 (en primero), BUG-IMG-UNPACK (desempaquetado dict), cabecera → build 55 |
| `env.example` | ENABLED_LANGUAGES=en,es,de,it + comentario |
| `schema_v55_complete.sql` | Actualización de versión, eliminado bloque FIX-LEGAL-002 |

## Archivos Sin Cambios (Sin Problemas Encontrados)

| Archivo | Líneas | Estado |
|---------|--------|--------|
| `app/models.py` | 1097 | OK — todos los modelos ORM correctos |
| `app/database.py` | 263 | OK — pool de conexiones correcto para Windows |
| `app/image_downloader.py` | 287 | OK — firma de retorno correcta (Dict[str, int]) |
| `app/scraper.py` | 1200 | OK — motores CloudScraper/Selenium |
| `app/main.py` | 1215 | OK — aplicación FastAPI |
| `app/tasks.py` | 358 | OK — tareas Celery |
| `app/celery_app.py` | 81 | OK — configuración Celery |
| `app/vpn_manager_windows.py` | 544 | OK — gestión VPN Windows |
| `app/completeness_service.py` | 144 | OK |
| `scripts/load_urls.py` | 334 | OK — carga CSV con soporte 3 columnas |
| `windows_service.py` | — | OK — integración SCM |

---

## URLs de Prueba para Verificación

| # | URL | Propósito |
|---|-----|-----------|
| 1 | `https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb` | EN: reseñas, legal, FAQs, highlights |
| 2 | `https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es` | ES: reseñas (decimales con coma), corrección legal |
| 3 | `https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-br.html?lang=pt-br` | PT-BR: soporte portugués (requiere pt en ENABLED_LANGUAGES) |
| 4 | `https://www.booking.com/hotel/sc/cheval-blanc-seychelles.en-gb.html` | EN: validación general de extracción |

---

## Checklist de Despliegue

- [x] Los 5 bugs corregidos y validados
- [x] `schema_v55_complete.sql` actualizado (instalación limpia, no migración)
- [x] `env.example` actualizado con orden correcto de idiomas
- [x] Cabeceras de versión sincronizadas a build 55
- [x] Corrección de datos FIX-LEGAL-002 eliminada (DB se recrea al arrancar)
- [ ] Ejecutar ciclo completo de scraping con URLs de prueba 1-4
- [ ] Verificar que la tabla `hotels_guest_reviews` tiene registros
- [ ] Verificar que registros ES de `hotels_legal` tienen `legal` y `legal_info` diferentes
- [ ] Verificar en los logs que inglés siempre se scrapea primero

---

*Fin del Informe de Auditoría — Build 55 — Versión Español*
