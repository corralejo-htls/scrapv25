# BookingScraper Pro — Bug Report Build 87
**Fecha / Date:** 2026-04-10  
**Versión / Version:** 6.0.0  
**Build anterior / Previous build:** 86 → **Build corregido / Fixed build:** 87  
**Plataforma / Platform:** Windows 11 Pro + Python 3.14.x + PostgreSQL 14+

---

## 🇪🇸 INFORME EN ESPAÑOL

### Identificador
**BUG-COMMIT-STATUS-001**

### Síntoma observado
- 14 URLs cargadas vía `/urls/load-csv` permanecen en `status = 'pending'` de forma indefinida.
- La tabla `hotels` permanece vacía tras varios ciclos de Celery Beat (cada 30 s).
- El sistema parecía procesar (el lock Redis se adquiría cada 280 s) pero ningún dato era raspado.
- La interfaz `http://localhost:8000/docs` podía aparecer inaccesible si el Worker de Celery consumía el lock Redis sin liberar progreso real.

### Archivo afectado
`app/scraper_service.py` — método `dispatch_batch()`

### Causa raíz

El **Build 86** introdujo `BUG-DOUBLE-COMMIT-002-FIX`, que eliminó commits explícitos en varios métodos confiando en que el gestor de contexto `get_db()` realizara el `session.commit()` al salir del bloque `with`. Esta lógica es **correcta** cuando los objetos modificados fueron cargados dentro de esa misma sesión.

En `dispatch_batch()` el flujo era:

```python
# BLOQUE 1 — sesión A: carga objetos y cierra sesión
with get_db() as session:          # session A abierta
    pending = session.query(URLQueue).filter(...).all()
# session A.close() ← objetos url_obj ahora DETACHED

# ... código VPN ...

# BLOQUE 2 — sesión B: intenta modificar objetos DETACHED
with get_db() as session:          # session B abierta (diferente)
    for url_obj in pending:
        url_obj.status = "processing"  # ← modificación sobre objeto detached
        url_obj.updated_at = _now()    #   session B NO rastrea estos objetos
# session B.commit() ← no hay nada en la transacción → url_queue NO se actualiza
```

SQLAlchemy con `expire_on_commit=False` permite leer atributos de objetos detached (no lanza `DetachedInstanceError`), pero las modificaciones sobre ellos **no se propagan** a ninguna sesión activa. El `commit()` de la segunda sesión confirma una transacción vacía. Las URLs quedan permanentemente en `'pending'`.

### Consecuencia en producción
| Capa | Efecto |
|------|--------|
| `url_queue` | 100% filas en `pending`; ninguna pasa a `processing` |
| `hotels` (y todas las satélites) | Vacías — ningún scraping ejecutado |
| Celery Beat | Adquiere Redis lock cada 280 s; lo libera al terminar sin datos |
| Redis lock | TTL de 280 s bloquea la siguiente ejecución automática |

### Corrección aplicada

Se extrae la lista de PKs de los objetos detached (posible porque `expire_on_commit=False` preserva los atributos cargados) y se ejecuta un `UPDATE` masivo con una sesión fresca que posee las filas desde el inicio:

```python
# Build 87 — CORRECTO:
url_ids = [u.id for u in pending]
with get_db() as session:
    session.query(URLQueue).filter(
        URLQueue.id.in_(url_ids)
    ).update(
        {"status": "processing", "updated_at": _now()},
        synchronize_session=False,
    )
```

`synchronize_session=False` es seguro aquí porque los objetos `url_obj` ya están detached y no se vuelven a usar en este contexto de sesión.

### Archivos modificados en Build 87

| Archivo | Cambio |
|---------|--------|
| `app/scraper_service.py` | Bloque de marcado `processing` reemplazado por bulk UPDATE con PKs |
| `app/__init__.py` | `BUILD_VERSION` actualizado a `87`; changelog añadido |

### Verificación sintáctica
```
OK: app/scraper_service.py
OK: app/__init__.py
```

---

### 📋 Protocolo de arranque correcto (Windows 11)

```
1. create_db.bat         ← elimina BD y aplica schema_v77_complete.sql
2. inicio_rapido.bat     ← lanza API (uvicorn) + Celery Worker + Celery Beat
3. POST /urls/load-csv   ← carga las 14 URLs (status = pending)
4. Esperar 30 s          ← Celery Beat dispara scrape_pending_urls automáticamente
5. GET /scraping/status  ← verificar que URLs pasan a processing / done
```

---

---

## 🇬🇧 REPORT IN ENGLISH

### Identifier
**BUG-COMMIT-STATUS-001**

### Observed symptom
- 14 URLs loaded via `/urls/load-csv` remain stuck at `status = 'pending'` indefinitely.
- The `hotels` table remains empty across multiple Celery Beat cycles (every 30 s).
- The system appeared to be processing (Redis lock was acquired every 280 s) but no data was scraped.

### Affected file
`app/scraper_service.py` — `dispatch_batch()` method

### Root cause

**Build 86** introduced `BUG-DOUBLE-COMMIT-002-FIX`, removing explicit `session.commit()` calls across several methods in favour of relying on the `get_db()` context manager's `__exit__` commit. That logic is **correct** when modified objects were loaded within the same session.

In `dispatch_batch()` there are two distinct `get_db()` blocks:

```
Block 1 → loads pending URLQueue objects, session closes → objects become DETACHED
Block 2 → attempts to set status="processing" on DETACHED objects
```

With `expire_on_commit=False` SQLAlchemy does not raise `DetachedInstanceError` when reading attributes of detached objects, but **attribute mutations are not tracked** by any active session. The `commit()` on Block 2's session flushes an empty transaction — `url_queue` is never updated.

### Impact
All URLs remain `pending`; no hotel data is scraped; Redis lock creates a false "busy" signal every 280 s.

### Fix applied
PKs are extracted from the (readable but detached) objects and a single bulk `UPDATE` is issued through a fresh session that actually owns the rows:

```python
url_ids = [u.id for u in pending]
with get_db() as session:
    session.query(URLQueue).filter(
        URLQueue.id.in_(url_ids)
    ).update(
        {"status": "processing", "updated_at": _now()},
        synchronize_session=False,
    )
```

### Files changed
| File | Change |
|------|--------|
| `app/scraper_service.py` | Processing-status block replaced with bulk UPDATE by PKs |
| `app/__init__.py` | `BUILD_VERSION` bumped to `87`; changelog entry added |

### Syntax validation
```
OK: app/scraper_service.py
OK: app/__init__.py
```
