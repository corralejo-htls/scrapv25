# BookingScraper Pro — SQL Diagnostic Queries (CORREGIDO v58)

**Versión:** Build 58 — Revisión de Auditoría  
**Base de datos:** PostgreSQL 14+  
**Fecha de revisión:** 2026-03-27  
**Cambios respecto a la versión original:**  

> ⚠️ **CORRECCIÓN CRÍTICA (BUG-NUEVO-001):** La versión original de este archivo
> hardcodeaba el número de idiomas esperados (`< 5`, `ARRAY['es','en','de','fr','it']`)
> siendo incompatible con cualquier configuración que difiera de exactamente 5 idiomas.
> El valor real de `ENABLED_LANGUAGES` en producción varía (4 idiomas en `env.example`,
> 7 en el default de `config.py`). Todas las queries han sido reescritas para ser
> dinámicas usando `url_language_status` como fuente de verdad de los idiomas configurados.

---

## 1. Queries de Verificación de Idiomas

### 1.1 Conteo de idiomas por URL — versión DINÁMICA

```sql
-- ✅ VERSIÓN CORREGIDA: sin hardcoding del número de idiomas esperados
-- La subquery calcula el expected_count desde url_language_status,
-- que refleja exactamente los idiomas configurados en ENABLED_LANGUAGES.
SELECT
    h.url_id,
    COUNT(h.id)                                                    AS scraped_count,
    (SELECT COUNT(*) FROM url_language_status uls
     WHERE uls.url_id = h.url_id)                                  AS configured_count,
    COUNT(h.id) = (SELECT COUNT(*) FROM url_language_status uls
                   WHERE uls.url_id = h.url_id)                    AS is_complete
FROM hotels h
GROUP BY h.url_id
ORDER BY scraped_count ASC;
```

**Resultado esperado:** Todas las filas con `is_complete = true`

### 1.2 URLs marcadas 'done' con idiomas incompletos — versión DINÁMICA

```sql
-- ✅ VERSIÓN CORREGIDA: HAVING dinámico sin < 5 hardcodeado
SELECT
    uq.id                                                           AS url_id,
    uq.external_ref,
    uq.status,
    uq.languages_completed,
    uq.languages_failed,
    COUNT(h.id)                                                     AS actual_lang_count,
    (SELECT COUNT(*) FROM url_language_status uls
     WHERE uls.url_id = uq.id)                                      AS expected_lang_count
FROM url_queue uq
LEFT JOIN hotels h ON h.url_id = uq.id
WHERE uq.status = 'done'
GROUP BY uq.id, uq.external_ref, uq.status,
         uq.languages_completed, uq.languages_failed
HAVING COUNT(h.id) < (
    SELECT COUNT(*) FROM url_language_status uls WHERE uls.url_id = uq.id
);
```

### 1.3 Desglose detallado de idiomas por URL

```sql
-- ✅ VERSIÓN CORREGIDA: usa url_language_status para calcular idiomas faltantes
SELECT
    uq.id                                                            AS url_id,
    uq.external_ref,
    uq.status,
    STRING_AGG(h.language, ', ' ORDER BY h.language)                AS present_languages,
    COUNT(h.id)                                                      AS scraped_count,
    (SELECT STRING_AGG(uls.language, ', ' ORDER BY uls.language)
     FROM url_language_status uls
     WHERE uls.url_id = uq.id
       AND uls.language NOT IN (
           SELECT language FROM hotels WHERE hotels.url_id = uq.id
       ))                                                            AS missing_languages,
    (SELECT COUNT(*) FROM url_language_status uls
     WHERE uls.url_id = uq.id)                                       AS expected_count
FROM url_queue uq
LEFT JOIN hotels h ON h.url_id = uq.id
GROUP BY uq.id, uq.external_ref, uq.status
ORDER BY scraped_count ASC;
```

---

## 2. Queries de Duplicación Legal (EXTR-001)

### 2.1 Identificar duplicaciones en campo legal_info

```sql
-- Caso A: legal_info IDÉNTICO al título (cubierto por FIX-LEGAL-003)
SELECT
    id, hotel_id, language,
    legal,
    LEFT(legal_info, 80)                                            AS legal_info_preview,
    'EXACT_DUPLICATE'                                               AS issue_type
FROM hotels_legal
WHERE legal IS NOT NULL
  AND legal_info IS NOT NULL
  AND LOWER(TRIM(legal_info)) = LOWER(TRIM(legal))

UNION ALL

-- Caso B: legal_info empieza por el título (FIX-LEGAL-004 — el caso no cubierto antes)
SELECT
    id, hotel_id, language,
    legal,
    LEFT(legal_info, 80)                                            AS legal_info_preview,
    'PREFIX_DUPLICATE'                                              AS issue_type
FROM hotels_legal
WHERE legal IS NOT NULL
  AND legal_info IS NOT NULL
  AND LOWER(TRIM(legal_info)) LIKE LOWER(TRIM(legal)) || '%'
  AND LOWER(TRIM(legal_info)) <> LOWER(TRIM(legal))   -- excluir caso A ya listado

ORDER BY issue_type, id;
```

### 2.2 Conteo por tipo de duplicación

```sql
SELECT
    SUM(CASE WHEN LOWER(TRIM(legal_info)) = LOWER(TRIM(legal))
             THEN 1 ELSE 0 END)                                     AS exact_duplicates,
    SUM(CASE WHEN LOWER(TRIM(legal_info)) LIKE LOWER(TRIM(legal)) || '%'
              AND LOWER(TRIM(legal_info)) <> LOWER(TRIM(legal))
             THEN 1 ELSE 0 END)                                     AS prefix_duplicates,
    COUNT(*)                                                         AS total_records,
    ROUND(100.0 * SUM(CASE WHEN LOWER(TRIM(legal_info)) LIKE LOWER(TRIM(legal)) || '%'
                           THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS pct_affected
FROM hotels_legal
WHERE legal IS NOT NULL AND legal_info IS NOT NULL;
```

### 2.3 Corrección de duplicación legal — ambos casos

```sql
-- PASO 1: Corregir Caso A — legal_info idéntico al título (limpiar)
UPDATE hotels_legal
SET legal_info = ''
WHERE legal IS NOT NULL
  AND legal_info IS NOT NULL
  AND LOWER(TRIM(legal_info)) = LOWER(TRIM(legal));

-- PASO 2: Corregir Caso B — legal_info con prefijo del título (recortar)
UPDATE hotels_legal
SET legal_info = TRIM(SUBSTRING(legal_info FROM LENGTH(TRIM(legal)) + 1))
WHERE legal IS NOT NULL
  AND legal_info IS NOT NULL
  AND LOWER(TRIM(legal_info)) LIKE LOWER(TRIM(legal)) || '%'
  AND LOWER(TRIM(legal_info)) <> LOWER(TRIM(legal));
```

---

## 3. Consistencia de Tablas Satélite

### 3.1 Verificación completa de huérfanos

```sql
-- ✅ Sin cambios — esta query era correcta en la versión original
SELECT
    'hotels_description'          AS table_name,
    COUNT(*)                      AS orphan_count
FROM hotels_description hd
WHERE NOT EXISTS (SELECT 1 FROM hotels h WHERE h.id = hd.hotel_id)
UNION ALL
SELECT 'hotels_amenities',        COUNT(*)
FROM hotels_amenities ha
WHERE NOT EXISTS (SELECT 1 FROM hotels h WHERE h.id = ha.hotel_id)
UNION ALL
SELECT 'hotels_policies',         COUNT(*)
FROM hotels_policies hp
WHERE NOT EXISTS (SELECT 1 FROM hotels h WHERE h.id = hp.hotel_id)
UNION ALL
SELECT 'hotels_legal',            COUNT(*)
FROM hotels_legal hl
WHERE NOT EXISTS (SELECT 1 FROM hotels h WHERE h.id = hl.hotel_id)
UNION ALL
SELECT 'hotels_popular_services', COUNT(*)
FROM hotels_popular_services hps
WHERE NOT EXISTS (SELECT 1 FROM hotels h WHERE h.id = hps.hotel_id)
UNION ALL
SELECT 'hotels_fine_print',       COUNT(*)
FROM hotels_fine_print hfp
WHERE NOT EXISTS (SELECT 1 FROM hotels h WHERE h.id = hfp.hotel_id)
UNION ALL
SELECT 'hotels_all_services',     COUNT(*)
FROM hotels_all_services has2
WHERE NOT EXISTS (SELECT 1 FROM hotels h WHERE h.id = has2.hotel_id)
UNION ALL
SELECT 'hotels_faqs',             COUNT(*)
FROM hotels_faqs hf
WHERE NOT EXISTS (SELECT 1 FROM hotels h WHERE h.id = hf.hotel_id)
UNION ALL
SELECT 'hotels_guest_reviews',    COUNT(*)
FROM hotels_guest_reviews hgr
WHERE NOT EXISTS (SELECT 1 FROM hotels h WHERE h.id = hgr.hotel_id)
UNION ALL
SELECT 'hotels_property_highlights', COUNT(*)
FROM hotels_property_highlights hph
WHERE NOT EXISTS (SELECT 1 FROM hotels h WHERE h.id = hph.hotel_id);
```

**Resultado esperado:** Todas las tablas con `orphan_count = 0`

---

## 4. Análisis de Reintentos

### 4.1 Candidatos a reintento parcial — versión DINÁMICA

```sql
-- ✅ VERSIÓN CORREGIDA: sin referencias hardcodeadas a idiomas específicos
SELECT
    uq.id,
    uq.external_ref,
    uq.url,
    uq.status,
    uq.languages_completed,
    uq.languages_failed,
    uq.retry_count,
    uq.max_retries,
    COUNT(h.id)                                                      AS hotels_in_db,
    (SELECT COUNT(*) FROM url_language_status uls
     WHERE uls.url_id = uq.id)                                       AS expected_langs,
    CASE
        WHEN uq.retry_count >= uq.max_retries  THEN 'MAX_RETRIES_EXCEEDED'
        WHEN COUNT(h.id) > 0
         AND COUNT(h.id) < (SELECT COUNT(*) FROM url_language_status uls
                            WHERE uls.url_id = uq.id) THEN 'PARTIAL_RETRY'
        WHEN COUNT(h.id) = 0                   THEN 'FULL_RETRY'
        ELSE 'UNKNOWN'
    END                                                              AS retry_type
FROM url_queue uq
LEFT JOIN hotels h ON h.url_id = uq.id
WHERE uq.status = 'error'
GROUP BY uq.id, uq.external_ref, uq.url, uq.status,
         uq.languages_completed, uq.languages_failed,
         uq.retry_count, uq.max_retries
ORDER BY retry_type, uq.retry_count DESC;
```

### 4.2 URLs atascadas en 'processing'

```sql
-- ✅ Sin cambios relevantes — correcta en versión original
SELECT
    id,
    external_ref,
    url,
    status,
    updated_at,
    NOW() - updated_at                                               AS stale_duration,
    EXTRACT(EPOCH FROM (NOW() - updated_at)) / 60                    AS stale_minutes
FROM url_queue
WHERE status = 'processing'
  AND updated_at < NOW() - INTERVAL '60 minutes'
ORDER BY updated_at;
```

---

## 5. Detección de Duplicados por Concurrencia

### 5.1 Duplicados en tabla hotels

```sql
-- ✅ Sin cambios — correcta en versión original
SELECT
    url_id,
    language,
    COUNT(*)                                                         AS duplicate_count
FROM hotels
GROUP BY url_id, language
HAVING COUNT(*) > 1;
```

**Resultado esperado:** Resultado vacío (sin duplicados)

---

## 6. Calidad de Datos

### 6.1 Distribución de idiomas

```sql
-- ✅ MEJORADA: muestra también idiomas configurados vs scraped
SELECT
    uls.language,
    COUNT(DISTINCT uls.url_id)                                       AS urls_configured,
    COUNT(DISTINCT h.url_id)                                         AS urls_scraped,
    COUNT(DISTINCT h.url_id) * 100.0
        / NULLIF(COUNT(DISTINCT uls.url_id), 0)                      AS completion_pct
FROM url_language_status uls
LEFT JOIN hotels h ON h.url_id = uls.url_id AND h.language = uls.language
GROUP BY uls.language
ORDER BY uls.language;
```

### 6.2 Resumen de estado de url_queue

```sql
-- ✅ Sin cambios — correcta en versión original
SELECT
    status,
    COUNT(*)                                                         AS url_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM url_queue), 2)   AS percentage
FROM url_queue
GROUP BY status
ORDER BY COUNT(*) DESC;
```

---

## 7. Monitoreo de Rendimiento

### 7.1 Actividad reciente de scraping

```sql
-- ✅ Sin cambios — correcta en versión original
SELECT
    DATE_TRUNC('hour', created_at)                                   AS hour,
    language,
    COUNT(*)                                                         AS hotels_scraped,
    ROUND(AVG(scrape_duration_s)::NUMERIC, 2)                        AS avg_duration_sec
FROM hotels
WHERE created_at > NOW() - INTERVAL '24 hours'
GROUP BY DATE_TRUNC('hour', created_at), language
ORDER BY hour DESC, language;
```

---

## 8. Queries Correctivas

### 8.1 Corregir URLs 'done' con datos incompletos — versión DINÁMICA

```sql
-- ✅ VERSIÓN CORREGIDA: sin ARRAY hardcodeado de idiomas
-- Calcula los idiomas faltantes comparando hotels con url_language_status
UPDATE url_queue uq
SET
    status = 'error',
    last_error = 'Legacy fix v58: incomplete language count',
    languages_completed = (
        SELECT STRING_AGG(h.language, ',' ORDER BY h.language)
        FROM hotels h
        WHERE h.url_id = uq.id
    ),
    languages_failed = (
        SELECT STRING_AGG(uls.language, ',' ORDER BY uls.language)
        FROM url_language_status uls
        WHERE uls.url_id = uq.id
          AND uls.language NOT IN (
              SELECT language FROM hotels WHERE hotels.url_id = uq.id
          )
    ),
    updated_at = NOW()
WHERE uq.status = 'done'
  AND (
      SELECT COUNT(*) FROM hotels h WHERE h.url_id = uq.id
  ) < (
      SELECT COUNT(*) FROM url_language_status uls WHERE uls.url_id = uq.id
  );
```

### 8.2 Resetear URLs atascadas en processing

```sql
-- ✅ VERSIÓN CORREGIDA: incluye limpieza de campos de tracking (FIX-ERR-001)
UPDATE url_queue
SET
    status              = 'pending',
    last_error          = 'Reset from stale processing after 60 minutes',
    languages_completed = '',          -- FIX-ERR-001: limpiar tracking parcial
    languages_failed    = '',          -- FIX-ERR-001: limpiar tracking parcial
    updated_at          = NOW()
WHERE status = 'processing'
  AND updated_at < NOW() - INTERVAL '60 minutes';
```

### 8.3 Limpiar registros satélite huérfanos

```sql
-- ✅ Sin cambios — correcta en versión original. Ejecutar en este orden.
DELETE FROM hotels_description
WHERE hotel_id NOT IN (SELECT id FROM hotels);

DELETE FROM hotels_amenities
WHERE hotel_id NOT IN (SELECT id FROM hotels);

DELETE FROM hotels_policies
WHERE hotel_id NOT IN (SELECT id FROM hotels);

DELETE FROM hotels_legal
WHERE hotel_id NOT IN (SELECT id FROM hotels);

DELETE FROM hotels_popular_services
WHERE hotel_id NOT IN (SELECT id FROM hotels);

DELETE FROM hotels_fine_print
WHERE hotel_id NOT IN (SELECT id FROM hotels);

DELETE FROM hotels_all_services
WHERE hotel_id NOT IN (SELECT id FROM hotels);

DELETE FROM hotels_faqs
WHERE hotel_id NOT IN (SELECT id FROM hotels);

DELETE FROM hotels_guest_reviews
WHERE hotel_id NOT IN (SELECT id FROM hotels);

DELETE FROM hotels_property_highlights
WHERE hotel_id NOT IN (SELECT id FROM hotels);
```

---

## 9. Query de Integridad Global (Nueva — Auditoría v58)

```sql
-- Dashboard de integridad completo — una sola query
-- Muestra el estado real del sistema sin asumir número de idiomas
SELECT
    uq.id                                                            AS url_id,
    uq.external_ref,
    uq.status                                                        AS queue_status,
    COUNT(DISTINCT h.language)                                       AS scraped_langs,
    COUNT(DISTINCT uls.language)                                     AS configured_langs,
    uq.languages_completed,
    uq.languages_failed,
    uq.retry_count,
    uq.max_retries,
    CASE
        WHEN COUNT(DISTINCT h.language) = COUNT(DISTINCT uls.language)
             AND uq.status = 'done'                THEN '✅ OK'
        WHEN COUNT(DISTINCT h.language) = COUNT(DISTINCT uls.language)
             AND uq.status <> 'done'               THEN '⚠️ COMPLETE_BUT_WRONG_STATUS'
        WHEN COUNT(DISTINCT h.language) > 0
             AND COUNT(DISTINCT h.language) < COUNT(DISTINCT uls.language)
             AND uq.status = 'done'                THEN '🔴 INCOMPLETE_MARKED_DONE'
        WHEN COUNT(DISTINCT h.language) > 0
             AND COUNT(DISTINCT h.language) < COUNT(DISTINCT uls.language)
             AND uq.status = 'error'               THEN '🟠 PARTIAL_AWAITING_RETRY'
        WHEN COUNT(DISTINCT h.language) = 0
             AND uq.status = 'error'               THEN '🔴 TOTAL_FAILURE'
        ELSE '❓ UNKNOWN'
    END                                                              AS integrity_status
FROM url_queue uq
LEFT JOIN hotels h              ON h.url_id   = uq.id
LEFT JOIN url_language_status uls ON uls.url_id = uq.id
GROUP BY uq.id, uq.external_ref, uq.status,
         uq.languages_completed, uq.languages_failed,
         uq.retry_count, uq.max_retries
ORDER BY
    CASE integrity_status
        WHEN '🔴 INCOMPLETE_MARKED_DONE' THEN 1
        WHEN '🔴 TOTAL_FAILURE'          THEN 2
        WHEN '🟠 PARTIAL_AWAITING_RETRY' THEN 3
        WHEN '⚠️ COMPLETE_BUT_WRONG_STATUS' THEN 4
        ELSE 5
    END;
```

---

**Documento generado:** 2026-03-27  
**Auditor:** Análisis de código — BookingScraper Pro v6.0.0 Build 58  
**Compatibilidad:** PostgreSQL 14+ / Windows 11  
**Versión schema:** v58
