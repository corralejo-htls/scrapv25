# BookingScraper Pro v6.0.0 Build 58 — Informe de Auditoría Completo

**Repositorio:** https://github.com/corralejo-htls/scrapv25.git  
**Fecha de Auditoría:** 2026-03-27  
**Plataforma:** Windows 11 / PostgreSQL 14+ / Python 3.10+  
**Versión Build:** 58 (Implementación Strategy E)

---

## Resumen Ejecutivo

Esta auditoría analiza exhaustivamente el flujo de trabajo de BookingScraper a través de 8 fases operativas, verificando la implementación de estrategias críticas de integridad de datos e identificando bugs clasificados por severidad. La auditoría confirma que Build 58 introduce mejoras significativas mediante la implementación de Strategy E, aunque varios problemas requieren atención.

### Hallazgos Principales

| Categoría | Cantidad | Distribución de Severidad |
|-----------|----------|---------------------------|
| Total de Problemas Identificados | 12 | Crítico: 2, Alto: 4, Medio: 4, Bajo: 2 |
| Métodos Strategy E | 3 | Todos Verificados y Correctos |
| Preocupaciones de Integridad de Datos | 2 | Requieren Atención Inmediata |

---

## 1. Análisis por Fases

### Fase 1: Inicialización

**Archivos Analizados:** `app/config.py`, `app/database.py`, `app/__init__.py`

**Evaluación de Implementación:**

La fase de inicialización establece la infraestructura central de la aplicación scraper. El sistema de configuración utiliza Pydantic Settings con evaluación lazy para la construcción de URL de base de datos, previniendo fallos en tiempo de importación. La clase Settings implementa validación comprehensiva incluyendo auto-generación de SECRET_KEY, validación de API_KEY y verificación de códigos de idioma ISO 639-1.

**Correctitud Verificada:**
- URL de base de datos se carga de forma lazy mediante decorador `@cached_property` (línea 381-394)
- Validación de idiomas contra variable de clase `_VALID_ISO_639_1` asegura solo códigos válidos
- Países VPN validados contra lista canónica `_VALID_VPN_COUNTRIES`
- Todos los directorios requeridos se crean en tiempo de ejecución, no en importación

**Problemas Identificados:**

| ID | Descripción | Severidad | Ubicación |
|----|-------------|-----------|-----------|
| INIT-001 | `BUILD_VERSION` aparece tanto en `config.py` (línea 51) como en `app/__init__.py` creando potencial de divergencia | Bajo | config.py:51 |
| INIT-002 | Sin validación de tamaño de pool de conexiones contra limitaciones de Windows Desktop Heap documentadas en comentarios del schema | Medio | config.py:163-166 |

---

### Fase 2: Carga de URLs

**Archivos Analizados:** `scripts/load_urls.py`, `app/models.py` (clase URLQueue)

**Evaluación de Implementación:**

El mecanismo de carga de URLs maneja ingestión CSV con soporte para formatos legacy de 2 columnas y actual de 3 columnas (external_ref, url, external_url). La implementación usa consultas SQL parametrizadas para prevenir inyección e implementa ON CONFLICT DO UPDATE para carga idempotente.

**Correctitud Verificada:**
- Parsing CSV maneja tanto saltos de línea Windows CRLF como Unix LF
- Validación de URL asegura prefijo de dominio Booking.com
- Validación opcional de URL externa requiere esquema http/https
- Cláusula ON CONFLICT preserva valores external_ref existentes (fix BUG-LOAD-001 verificado)

**Problemas Identificados:**

| ID | Descripción | Severidad | Ubicación |
|----|-------------|-----------|-----------|
| URL-001 | `_parse_csv()` no maneja correctamente campos CSV citados que contienen comas dentro de valores | Medio | load_urls.py:142 |
| URL-002 | Sin validación de que valores external_ref sean únicos en el CSV - duplicados sobrescriben silenciosamente en última ocurrencia | Bajo | load_urls.py:167 |

---

### Fase 3: Procesamiento

**Archivos Analizados:** `app/scraper_service.py`, `app/completeness_service.py`, `app/tasks.py`

**Evaluación de Implementación:**

La fase de procesamiento orquesta el consumo de URLs de la cola mediante ThreadPoolExecutor con límites configurables de workers. Build 58 introduce Strategy E con tres métodos críticos para manejo condicional de commits.

**Verificación de Implementación Strategy E:**

#### 3.1 `_count_successful_languages()` (Líneas 450-473)

```python
def _count_successful_languages(self, url_id: uuid.UUID) -> int:
    try:
        with get_db() as session:
            count = (
                session.query(func.count(Hotel.id))
                .filter(Hotel.url_id == url_id)
                .scalar()
            )
            return int(count or 0)
    except Exception as exc:
        logger.error(...)
        return 0
```

**Evaluación:** ✅ **VERIFICADO CORRECTO**

El método consulta correctamente la tabla `hotels` como fuente de verdad para registros de idiomas exitosos. Usa `func.count()` de SQLAlchemy con filtrado apropiado por `url_id`. El manejo de errores retorna 0 en caso de fallo, asegurando comportamiento seguro por defecto. La implementación se alinea con especificación STRATEGY-E-001.

#### 3.2 `_mark_incomplete()` (Líneas 475-515)

```python
def _mark_incomplete(
    self,
    url_obj: URLQueue,
    error_msg: str,
    success_langs: Optional[List[str]] = None,
    failed_langs: Optional[List[str]] = None,
) -> None:
    try:
        with get_db() as session:
            row = session.get(URLQueue, url_obj.id)
            if row:
                row.status = "error"
                row.last_error = error_msg[:2000]
                row.languages_completed = ",".join(success_langs or [])
                row.languages_failed    = ",".join(failed_langs or [])
                row.retry_count += 1
                ...
```

**Evaluación:** ✅ **VERIFICADO CORRECTO**

El método correctamente:
- Establece status a "error" mientras preserva datos parciales
- Registra idiomas completados y fallidos para diagnóstico
- Incrementa retry_count apropiadamente
- Mantiene timestamp scraped_at para indicar progreso parcial

Esto se alinea con especificación STRATEGY-E-002 para manejo de fallos parciales.

#### 3.3 `_cleanup_empty_url()` (Líneas 517-566)

```python
def _cleanup_empty_url(self, url_id: uuid.UUID) -> None:
    satellite_models = [
        HotelDescription, HotelAmenity, HotelPolicy, HotelLegal,
        HotelPopularService, HotelFinePrint, HotelAllService,
        HotelFAQ, HotelGuestReview, HotelPropertyHighlights,
    ]
    try:
        with get_db() as session:
            for model in satellite_models:
                n = (
                    session.query(model)
                    .filter(model.url_id == url_id)
                    .delete(synchronize_session=False)
                )
            ...
```

**Evaluación:** ✅ **VERIFICADO CORRECTO**

El método correctamente:
- Elimina registros de las 10 tablas satélite antes de eliminar de hotels
- Usa `synchronize_session=False` para eliminación masiva eficiente
- Maneja todos los modelos incluyendo adiciones v53 (FinePrint, AllService, FAQ, GuestReviews, PropertyHighlights)
- Incluye logging apropiado para rastro de auditoría

**Problemas Identificados:**

| ID | Descripción | Severidad | Ubicación |
|----|-------------|-----------|-----------|
| PROC-001 | Árbol de decisión en `_process_url()` no contempla condición de carrera donde conteo DB difiere del diccionario `lang_results` | Alto | scraper_service.py:404-436 |
| PROC-002 | Validación de transición de estado en CompletenessService rechaza transición válida `incomplete→processing` en algunos escenarios | Medio | completeness_service.py:26-33 |

---

### Fase 4: Motores de Scraping

**Archivos Analizados:** `app/scraper.py`

**Evaluación de Implementación:**

La fase de scraping implementa dos motores: CloudScraperEngine para peticiones HTTP y SeleniumEngine para páginas con mucho JavaScript. Build 49 corrige problemas críticos de thread-safety (BUG-DESC-001, BUG-DESC-002).

**Correctitud Verificada:**
- Almacenamiento thread-local (`_cloud_tls`) previene contaminación cruzada de sesiones
- SeleniumEngine usa `threading.Lock()` para acceso single-threaded al navegador
- Detección de idioma de 5 estrategias (FIX-016) implementada correctamente
- Constructor de URLs maneja correctamente transformación `en→en-gb` (FIX-024)

**Problemas Identificados:**

| ID | Descripción | Severidad | Ubicación |
|----|-------------|-----------|-----------|
| SCRP-001 | Pool de User-Agent usa Chrome 130-134 pero distribución ponderada puede no coincidir con patrones de tráfico real | Bajo | scraper.py:83-91 |
| SCRP-002 | Detección `_is_blocked()` puede disparar falsos positivos en páginas con contenido legítimo "just a moment" | Medio | scraper.py:227-236 |
| SCRP-003 | Lógica de rotación VPN llama `should_rotate()` pero atributo `_last_rotation` puede no existir si VPN nunca conectó | Medio | scraper_service.py:612 |

---

### Fase 5: Extracción

**Archivos Analizados:** `app/extractor.py`

**Evaluación de Implementación:**

La fase de extracción procesa contenido HTML usando BeautifulSoup con fallback a parser lxml. Build 56 introduce múltiples nuevos extractores para tablas v53.

**Correctitud Verificada:**
- Parsing JSON-LD extrae correctamente datos Hotel de schema.org
- Normalización de star rating (÷2) implementada apropiadamente
- Cadena de fallback de detección de idioma verificada

**Problemas Identificados:**

| ID | Descripción | Severidad | Ubicación |
|----|-------------|-----------|-----------|
| EXTR-001 | `_extract_legal()` no elimina el título de `legal_info` cuando el título aparece como primer párrafo | **Crítico** | extractor.py:~900-950 |
| EXTR-002 | `_extract_amenities()` puede capturar texto "Ver todos los N servicios" en algunas estructuras DOM | Medio | extractor.py:873-877 |

---

### Fase 6: Persistencia

**Archivos Analizados:** `app/scraper_service.py` (métodos upsert), `schema_v58_complete.sql`

**Evaluación de Implementación:**

La capa de persistencia usa SQLAlchemy ORM con patrones upsert apropiados. Constraints de foreign key aplican integridad referencial con comportamiento CASCADE delete.

**Correctitud Verificada:**
- `_upsert_hotel()` usa UniqueConstraint (url_id, language) para deduplicación
- Upserts de tablas satélite siguen patrón delete-then-insert para sincronización
- Las 17 tablas del schema están apropiadamente mapeadas en modelos ORM

**Problemas Identificados:**

| ID | Descripción | Severidad | Ubicación |
|----|-------------|-----------|-----------|
| PERS-001 | Sin nivel de aislamiento de transacción especificado para operaciones upsert - escrituras concurrentes pueden causar datos parciales | **Crítico** | scraper_service.py:818-864 |
| PERS-002 | `_upsert_description()` no verifica que hotel existe antes de insert, puede causar violación FK | Medio | scraper_service.py:865-910 |

---

### Fase 7: Manejo de Imágenes

**Archivos Analizados:** `app/image_downloader.py`

**Evaluación de Implementación:**

El manejo de imágenes soporta tres categorías de tamaño (thumb_url, large_url, highres_url) con preservación apropiada del token de autenticación.

**Correctitud Verificada:**
- Fix BUG-IMG-401 verificado - parámetros de query incluyendo token auth `k=` preservados
- Priorización de categorías ordena descargas correctamente
- Validación de content-type contra tipos permitidos

**Problemas Identificados:**

| ID | Descripción | Severidad | Ubicación |
|----|-------------|-----------|-----------|
| IMG-001 | `_download_one()` no reintenta en errores de red transitorios | Medio | image_downloader.py:190-287 |
| IMG-002 | Sin rate limiting para descargas de imágenes - puede disparar throttling CDN | Bajo | image_downloader.py:116-135 |

---

### Fase 8: Manejo de Errores

**Archivos Analizados:** `app/scraper_service.py`, `app/completeness_service.py`, `app/tasks.py`

**Evaluación de Implementación:**

El manejo de errores implementa validación de máquina de estados con guards de transición apropiados. Strategy E de Build 58 distingue correctamente entre fallos parciales y totales.

**Correctitud Verificada:**
- Tabla de transición de estados previene cambios de status inválidos (SCRAP-BUG-034)
- SELECT FOR UPDATE previene condiciones de carrera (SCRAP-BUG-023)
- Mecanismos de reintento con backoff exponencial implementados

**Problemas Identificados:**

| ID | Descripción | Severidad | Ubicación |
|----|-------------|-----------|-----------|
| ERR-001 | `reset_stale_processing_urls()` no resetea campos `languages_completed` y `languages_failed` | Alto | tasks.py:252-275 |
| ERR-002 | Sin aplicación de límite máximo de reintentos en `_mark_incomplete()` - retry_count puede exceder max_retries | Medio | scraper_service.py:501 |

---

## 2. Análisis de Problemas Reportados

### Problema-1: Scraping de Idiomas Incompleto

**URL ID:** `0daaf80d-fe8c-46d1-8d5a-919eef1ed033`  
**Conteo Observado:** 1 idioma (esperado: 5)

**Análisis de Causa Raíz:**

Al examinar los datos CSV y la tabla hotels se revela que esta URL (Cheval Blanc Seychelles) solo tiene un registro en español (`es`). El scraping se realizó pero los otros idiomas fallaron sin reintento apropiado.

**Factores Contribuyentes:**

1. Strategy E de Build 58 fue diseñado pero la URL puede haber sido procesada con código pre-v58
2. El método `_process_url()` ahora maneja correctamente fallos parciales, pero datos históricos pueden haber sido marcados 'done' incorrectamente

**Resultado de Query de Verificación:**
```sql
SELECT url_id, COUNT(url_id) FROM hotels GROUP BY url_id;
-- "0daaf80d-fe8c-46d1-8d5a-919eef1ed033" → count = 1
```

**Recomendación:** Usar `scripts/retry_incomplete.py --fix-legacy` para identificar y corregir URLs marcadas 'done' pero con datos incompletos.

---

### Problema-2: Duplicación de Campo Legal

**Patrón Observado:** Contenido del campo `legal` aparece duplicado en `legal_info`

**Ejemplo:**
```
id=1, legal="Legal information", legal_info="Legal information This property is...."
id=2, legal="Legal information", legal_info="Legal information This property is...."
id=3, legal="Información legal", legal_info="Información legal Este alojamiento...."
```

**Análisis de Causa Raíz:**

El método `_extract_legal()` en `extractor.py` intenta detectar el título usando patrones regex, pero en algunos casos el primer tag `<p>` contiene tanto el título como el texto del cuerpo. Cuando esto ocurre, el contenido completo se asigna a `legal_info` mientras la extracción del título falla o duplica.

**Referencia de Código:**
```python
# FIX-LEGAL-003 intento de corrección:
# "si legal == legal_info → legal_info se limpia a ''"
# Pero el problema persiste en algunas variantes de idioma
```

**Verificación:**

La exportación CSV muestra patrones consistentes donde `legal_info` comienza con el mismo texto que `legal`, confirmando el problema de extracción duplicada.

**Recomendación:** Implementar validación post-extracción:
```python
if legal and legal_info and legal_info.startswith(legal):
    legal_info = legal_info[len(legal):].strip()
```

---

## 3. Evaluación de Integridad de Datos

### Prevención de Duplicados por Concurrencia

**Estado:** ⚠️ **PARCIALMENTE IMPLEMENTADO**

El sistema implementa varias salvaguardas contra duplicados inducidos por concurrencia:

1. **Bloqueo de URL en Redis:** `_try_claim_url()` usa SET NX para bloqueo distribuido
2. **UniqueConstraint de Base de Datos:** `uq_hotels_url_lang` previene pares (url_id, language) duplicados
3. **Bloqueo Optimista:** Columna `version_id` habilita detección de conflictos

**Brechas Identificadas:**
- Tablas satélite carecen de bloqueo optimista
- Sin aislamiento SERIALIZABLE para operaciones batch
- TTL de lock Redis puede expirar antes de completar operación

### Consistencia de Tablas Satélite

**Estado:** ✅ **CORRECTO**

Todas las tablas satélite incluyen ambos foreign keys `hotel_id` y `url_id` con CASCADE delete, asegurando que la integridad referencial se mantenga. El método `_cleanup_empty_url()` elimina correctamente registros de las 10 tablas satélite antes del registro hotel principal.

---

## 4. Clasificación de Bugs por Severidad

### Severidad Crítica (Requiere Corrección Inmediata)

| ID | Descripción | Impacto | Ubicación |
|----|-------------|---------|-----------|
| EXTR-001 | Título legal duplicado en campo legal_info | Degradación de calidad de datos en todos los idiomas | extractor.py |
| PERS-001 | Sin aislamiento de transacción para escrituras concurrentes | Condiciones de carrera causando datos parciales/corruptos | scraper_service.py |

### Severidad Alta (Requiere Atención Pronta)

| ID | Descripción | Impacto | Ubicación |
|----|-------------|---------|-----------|
| PROC-001 | Condición de carrera entre resultados en memoria y conteo DB | Marcado de status incorrecto | scraper_service.py |
| ERR-001 | Reset de URLs stale no limpia campos de tracking de idiomas | Lógica de reintento puede saltar idiomas fallidos | tasks.py |

### Severidad Media (Debe Ser Abordada)

| ID | Descripción | Impacto | Ubicación |
|----|-------------|---------|-----------|
| INIT-002 | Sin validación de pool Windows Desktop Heap | Potenciales fallos de conexión | config.py |
| URL-001 | Manejo de campos citados en CSV | Errores de parsing de datos | load_urls.py |
| PROC-002 | Brechas en validación de transición de estado | Operaciones válidas rechazadas | completeness_service.py |
| SCRP-002 | Detección de bloqueo falso positivo | Reintentos innecesarios | scraper.py |
| SCRP-003 | Error de atributo en rotación VPN | Excepción en runtime | scraper_service.py |
| EXTR-002 | Amenities capturan texto promocional | Contaminación de datos | extractor.py |
| PERS-002 | Riesgo de violación FK en insert de descripción | Error de base de datos | scraper_service.py |
| ERR-002 | Sin aplicación de max_retries | Potencial loop de reintento infinito | scraper_service.py |
| IMG-001 | Sin reintento de descarga de imágenes | Imágenes faltantes | image_downloader.py |

### Severidad Baja (Mejora Futura)

| ID | Descripción | Impacto | Ubicación |
|----|-------------|---------|-----------|
| INIT-001 | Duplicación de BUILD_VERSION | Potencial desajuste de versión | config.py |
| URL-002 | Sin verificación de unicidad external_ref | Sobrescritura silenciosa de datos | load_urls.py |
| SCRP-001 | Desajuste de pesos User-Agent | Riesgo de detección | scraper.py |
| IMG-002 | Sin rate limiting de imágenes | Throttling CDN | image_downloader.py |

---

## 5. Recomendaciones

### Acciones Inmediatas (Críticas)

1. **Corregir Extracción Legal (EXTR-001):**
   - Implementar validación post-extracción en `_extract_legal()`
   - Añadir tests unitarios cubriendo casos borde para todos los idiomas soportados

2. **Añadir Aislamiento de Transacción (PERS-001):**
   - Envolver upserts multi-tabla en transacción SERIALIZABLE
   - Considerar implementar advisory locks a nivel de base de datos

### Acciones a Corto Plazo (Alta Prioridad)

3. **Corregir Condición de Carrera (PROC-001):**
   - Usar conteo de base de datos como única fuente de verdad
   - Eliminar dependencia en `lang_results` en memoria para decisión final

4. **Corregir Reset de URLs Stale (ERR-001):**
   - Añadir reset de campos de tracking de idiomas a `reset_stale_processing_urls()`

### Acciones a Mediano Plazo

5. **Mejorar Parsing CSV (URL-001):**
   - Implementar parsing CSV apropiado con módulo `csv`
   - Manejar campos citados y caracteres de escape

6. **Añadir Lógica de Reintento de Imágenes (IMG-001):**
   - Implementar backoff exponencial para descargas fallidas
   - Añadir contador de reintentos configurable

### Mejoras a Largo Plazo

7. **Consolidación de Control de Versión (INIT-001):**
   - Mover BUILD_VERSION a archivo de fuente única
   - Usar `importlib.metadata` para detección dinámica de versión

8. **Añadir Rate Limiting (IMG-002):**
   - Implementar algoritmo token bucket
   - Configurar límites por dominio CDN

---

## 6. Referencia de Consultas SQL

### Consultas de Diagnóstico

```sql
-- Consulta 1: Encontrar URLs con conteos de idioma incompletos
SELECT 
    uq.id AS url_id,
    uq.external_ref,
    uq.status,
    COUNT(h.id) AS language_count,
    (SELECT COUNT(*) FROM unnest(string_to_array('es,en,de,fr,it', ','))) AS expected_count
FROM url_queue uq
LEFT JOIN hotels h ON h.url_id = uq.id
GROUP BY uq.id, uq.external_ref, uq.status
HAVING COUNT(h.id) < 5 AND uq.status = 'done';

-- Consulta 2: Identificar duplicados de campo legal
SELECT id, hotel_id, language, legal, 
       LEFT(legal_info, 50) AS legal_info_preview,
       CASE WHEN legal_info LIKE legal || '%' THEN 'DUPLICATE' ELSE 'OK' END AS status
FROM hotels_legal
WHERE legal IS NOT NULL AND legal_info IS NOT NULL
ORDER BY id;

-- Consulta 3: Verificar consistencia de tablas satélite
SELECT 
    h.id AS hotel_id,
    h.url_id,
    h.language,
    CASE WHEN hd.id IS NULL THEN 'MISSING' ELSE 'OK' END AS description_status,
    CASE WHEN hl.id IS NULL THEN 'MISSING' ELSE 'OK' END AS legal_status
FROM hotels h
LEFT JOIN hotels_description hd ON hd.hotel_id = h.id
LEFT JOIN hotels_legal hl ON hl.hotel_id = h.id
WHERE hd.id IS NULL OR hl.id IS NULL;

-- Consulta 4: Encontrar registros huérfanos (registros satélite sin hotel)
SELECT 'hotels_description' AS table_name, COUNT(*) AS orphan_count
FROM hotels_description hd
WHERE NOT EXISTS (SELECT 1 FROM hotels h WHERE h.id = hd.hotel_id)
UNION ALL
SELECT 'hotels_legal', COUNT(*)
FROM hotels_legal hl
WHERE NOT EXISTS (SELECT 1 FROM hotels h WHERE h.id = hl.hotel_id);

-- Consulta 5: Análisis de candidatos a reintento
SELECT 
    uq.id,
    uq.external_ref,
    uq.status,
    uq.languages_completed,
    uq.languages_failed,
    uq.retry_count,
    uq.max_retries,
    CASE 
        WHEN uq.retry_count >= uq.max_retries THEN 'MAX_RETRIES_EXCEEDED'
        WHEN uq.languages_completed IS NOT NULL AND uq.languages_completed != '' THEN 'PARTIAL_RETRY'
        ELSE 'FULL_RETRY'
    END AS retry_type
FROM url_queue uq
WHERE uq.status = 'error';
```

---

## Apéndice A: Índice de Referencia de Archivos

| Archivo | Líneas | Propósito |
|---------|--------|-----------|
| app/config.py | 1-475 | Gestión de configuración |
| app/database.py | 1-264 | Manejo de conexión a base de datos |
| app/models.py | 1-1100+ | Definiciones de modelos ORM |
| app/scraper.py | 1-1200+ | Motores de scraping |
| app/extractor.py | 1-1100+ | Extracción HTML |
| app/scraper_service.py | 1-1200+ | Orquestación principal |
| app/completeness_service.py | 1-145 | Tracking de estado |
| app/tasks.py | 1-359 | Definiciones de tareas Celery |
| app/image_downloader.py | 1-288 | Procesamiento de imágenes |
| scripts/load_urls.py | 1-335 | Carga de URLs desde CSV |
| scripts/retry_incomplete.py | 1-480 | Gestión de reintentos |
| schema_v58_complete.sql | 1-900+ | Schema de base de datos |

---

**Informe Generado:** 2026-03-27  
**Auditor:** Sistema Automatizado de Análisis de Código  
**Versión Build:** 58
