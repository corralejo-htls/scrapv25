# BookingScraper Pro — Resumen de Build 58
## Estrategia E: Estado Mejorado con Commit Condicional

**Versión:** v6.0.0 Build 58  
**Fecha:** 2026-03-26  
**Repositorio:** https://github.com/corralejo-htls/scrapv25.git  
**Plataforma:** Windows 11 Professional / PostgreSQL 14+ / Python 3.10+

---

## Bug Crítico Corregido — BUG-INTEGRITY-001

### Causa Raíz

En `scraper_service.py`, el método `_process_url()` tenía un parámetro `True` **hardcodeado** que hacía que cada URL se marcara como `done` independientemente de cuántos idiomas se hubieran scrapeado exitosamente:

```python
# BUILD 57 — CÓDIGO DEFECTUOSO
all_ok = True
for lang in languages:
    ok = self._scrape_language(url_obj, lang)
    if not ok:
        all_ok = False      # variable actualizada, pero NUNCA usada

self._mark_done(url_obj, all_ok=True)   # ← TRUE HARDCODEADO — BUG
```

### Impacto en Producción

| Efecto | Tabla afectada |
|--------|---------------|
| URLs marcadas `done` con sólo 1 de 4 idiomas scrapeados | `url_queue` |
| 75% de los datos multilingües faltantes por URL afectada | `hotels` |
| Cascada de datos incompletos en amenidades, políticas, FAQs, reseñas | tablas satellite |
| Descarga de imágenes omitida (el trigger de inglés nunca ejecutó) | `image_downloads` |
| Reportes mostraban 100% de completitud con sólo 25% de integridad real | dashboards |

### Evidencia Confirmada (datos de pruebas/)

```
url_id: bc5d8b35-1a5f-4ab6-b778-3a7ba516bc0b
  → url_queue.status = 'done'    ← INCORRECTO
  → hotels: 1 registro (sólo es) ← debería ser 4
  → en: error | de: error | it: error | es: done
```

---

## Estrategia E — Arquitectura de la Solución

### Árbol de Decisión (3 casos)

```
_count_successful_languages(url_id)  →  actual_count
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         │                                    │                                    │
actual == expected               0 < actual < expected                     actual == 0
         │                                    │                                    │
  Caso 1: DONE                    Caso 2: ERROR                        Caso 3: ERROR
_mark_done(all_ok=True)       _mark_incomplete()                  _cleanup_empty_url()
                               DATOS PRESERVADOS                       + _mark_error()
                               PARTIAL RETRY OK                     RETRY COMPLETO
```

### Principio Clave
**"Preservar lo que tuvo éxito. Reintentar sólo lo que falló."**

---

## Archivos Modificados

| Archivo | Cambio | Tipo |
|---------|--------|------|
| `app/scraper_service.py` | Estrategia E — 3 métodos nuevos + bug corregido | MODIFICADO |
| `app/models.py` | Columnas `languages_completed`, `languages_failed` + `'incomplete'` en CHECK | MODIFICADO |
| `app/config.py` | BUILD_VERSION 56 → 58 | MODIFICADO |
| `app/__init__.py` | BUILD_VERSION 56 → 58 | MODIFICADO |
| `schema_v58_complete.sql` | Schema `url_queue` — nuevas columnas + CHECK actualizado | NUEVO |
| `scripts/retry_incomplete.py` | Herramienta CLI de reintento parcial | NUEVO |
| `tests/test_strategy_e.py` | 22 tests unitarios cubriendo los 5 casos | NUEVO |

---

## Nuevos Métodos — `scraper_service.py`

### `_count_successful_languages(url_id) → int`
Consulta la tabla `hotels` (fuente de verdad) para contar los registros de idioma confirmados en DB.

```python
# Reemplaza la variable all_ok no confiable
actual_count = session.query(func.count(Hotel.id))
               .filter(Hotel.url_id == url_id).scalar()
```

### `_mark_incomplete(url_obj, error_msg, success_langs, failed_langs)`
Marca la URL como `error` **sin eliminar** los datos parciales.
Habilita el reintento dirigido. Actualiza `languages_completed` y `languages_failed`.

### `_cleanup_empty_url(url_id)`
Se llama **SÓLO en fallo total** (actual_count == 0). Elimina todos los registros de:
`hotels`, `hotels_description`, `hotels_amenities`, `hotels_policies`, `hotels_legal`,
`hotels_popular_services`, `hotels_fine_print`, `hotels_all_services`,
`hotels_faqs`, `hotels_guest_reviews`, `hotels_property_highlights`, `url_language_status`

---

## Cambios en el Schema — `schema_v58_complete.sql`

### Nuevas columnas en `url_queue`
```sql
languages_completed  VARCHAR(64)  NULL DEFAULT ''   -- e.g. 'es,it'
languages_failed     VARCHAR(64)  NULL DEFAULT ''   -- e.g. 'en,de'
```

### Restricción CHECK actualizada
```sql
-- ANTES (v57)
status IN ('pending','processing','done','error','skipped')

-- AHORA (v58)
status IN ('pending','processing','done','error','skipped','incomplete')
```

---

## Nueva Herramienta — `scripts/retry_incomplete.py`

```powershell
# Uso en Windows 11 PowerShell desde el directorio raíz del proyecto:

python scripts/retry_incomplete.py --summary
    # Muestra estado de integridad de todos los datos de URLs.

python scripts/retry_incomplete.py --dry-run
    # Previsualiza qué se reintentaría sin hacer cambios.

python scripts/retry_incomplete.py --limit 10
    # Re-encola hasta 10 URLs con fallo parcial para reintento.

python scripts/retry_incomplete.py --reset-total-failures
    # Resetea URLs con fallo total a 'pending' para re-scraping completo.

python scripts/retry_incomplete.py --fix-legacy
    # Corrige URLs pre-v58 marcadas 'done' con datos incompletos.

python scripts/retry_incomplete.py --url-id <UUID>
    # Reintenta una URL específica por su UUID.
```

---

## Cobertura de Tests — `tests/test_strategy_e.py`

| Clase de Test | Casos | Descripción |
|---|---|---|
| `TestCase1CompleteSuccess` | 3 | 4/4 idiomas OK → `done` |
| `TestCase2PartialFailure` | 4 | Algunos OK → `error` + datos preservados |
| `TestCase3TotalFailure` | 3 | Todos fallan → cleanup + `error` |
| `TestCase4OriginalBugScenario` | 3 | Reproducción exacta del bug: 1/4 (sólo es) |
| `TestCase5ExceptionHandling` | 2 | Excepción en idioma contada como fallo |
| `TestCountSuccessfulLanguages` | 3 | Tests unitarios del método de conteo en DB |
| `TestMarkIncomplete` | 4 | Tests del método de preservación parcial |

**Total: 22 casos de prueba**

```powershell
# Ejecutar desde el directorio raíz (Windows 11)
python -m pytest tests/test_strategy_e.py -v
```

---

## Procedimiento de Despliegue (Windows 11)

### Paso 1 — Actualizar Archivos
Reemplazar los archivos del proyecto con los archivos de este build:
```
app/__init__.py          ← BUILD 58
app/config.py            ← BUILD 58
app/models.py            ← nuevas columnas
app/scraper_service.py   ← Strategy E
```

### Paso 2 — Recrear la Base de Datos
```batch
REM La DB se elimina y recrea en cada arranque (comportamiento normal del sistema)
psql -U postgres -c "DROP DATABASE IF EXISTS bookingscraper;"
psql -U postgres -c "CREATE DATABASE bookingscraper OWNER bookingscraper_user;"
psql -U bookingscraper_user -d bookingscraper -f schema_v58_complete.sql
```

### Paso 3 — Cargar URLs y Ejecutar
```batch
python scripts/load_urls.py
python -m app.main
```

### Paso 4 — Verificar Integridad
```batch
REM Diagnóstico de estado
python scripts/retry_incomplete.py --summary

REM Corregir datos legacy si existen (runs anteriores)
python scripts/retry_incomplete.py --fix-legacy --dry-run
python scripts/retry_incomplete.py --fix-legacy
```

### Paso 5 — Ejecutar Tests
```batch
python -m pytest tests/test_strategy_e.py -v
python -m pytest tests/ -v
```

---

## Consulta de Auditoría de Integridad

Ejecutar después del despliegue para verificar que no hay URLs incorrectamente marcadas como `done`:

```sql
-- URLs 'done' con datos de idiomas incompletos
SELECT
    uq.id,
    uq.url,
    uq.status,
    COUNT(h.id)             AS idiomas_scrapeados,
    uq.languages_completed  AS completados,
    uq.languages_failed     AS fallidos
FROM url_queue uq
LEFT JOIN hotels h ON h.url_id = uq.id
WHERE uq.status = 'done'
GROUP BY uq.id, uq.url, uq.status, uq.languages_completed, uq.languages_failed
HAVING COUNT(h.id) < 4
ORDER BY uq.id;
-- Resultado esperado: 0 filas después del despliegue de Build 58
```

---

## Notas de Arquitectura Windows 11

| Aspecto | Implementación |
|---------|---------------|
| Concurrencia | `ThreadPoolExecutor` (no `ProcessPoolExecutor`) — compatible con Windows |
| Rutas de archivo | `pathlib.Path` — manejo correcto de letras de unidad Windows |
| Señales | Sin POSIX signals — compatible con Windows 11 |
| Pool de conexiones | `max_connections ≤ 100` — límite Desktop Heap respetado |
| Event Loop | `ProactorEventLoop` (defecto en Windows para asyncio) |
| Logging | `RotatingFileHandler` + `NTEventLogHandler` (sin `logrotate`) |

---

*BookingScraper Pro v6.0.0 Build 58 — Implementación Estrategia E*  
*Generado: 2026-03-26*
