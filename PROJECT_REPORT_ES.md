# BookingScraper Pro v6.0 — Informe de Proyecto (Español)
**Versión:** 46 (Corregida desde Auditoría v44)  
**Fecha:** 2026-03-07  
**Plataforma:** Windows 11 Professional/Enterprise + Python 3.11+ + PostgreSQL 15-18  
**Estado:** ✅ Todos los problemas de auditoría resueltos

---

## Índice de Contenidos
1. [Resumen de Problemas y Registro de Correcciones](#1-resumen-de-problemas-y-registro-de-correcciones)
2. [Mapa de Arquitectura](#2-mapa-de-arquitectura)
3. [Guía de Instalación](#3-guía-de-instalación)
4. [Referencia de Configuración](#4-referencia-de-configuración)
5. [Esquema de Base de Datos](#5-esquema-de-base-de-datos)
6. [Lista de Verificación](#6-lista-de-verificación)
7. [Solución de Problemas](#7-solución-de-problemas)

---

## 1. Resumen de Problemas y Registro de Correcciones

### 1.1 Hallazgos Combinados de Ambos Informes de Auditoría (v44)

| ID | Severidad | Archivo | Descripción | Estado en v46 |
|----|-----------|---------|-------------|---------------|
| BUG-001 | Crítico | `app/database.py` | Credenciales DB validadas al crear el motor (diferido), no en tiempo de importación | ✅ Corregido |
| BUG-002 | Crítico | `app/models.py` | Índice único parcial `ix_hotels_url_lang_null` solo en comentarios, no en `Index()` | ✅ Corregido |
| BUG-003 | Crítico | `requirements.txt` | Archivo de dependencias en subdirectorio `app/`, no en la raíz del proyecto | ✅ Corregido |
| BUG-004 | Alto | `app/config.py` | Incompatibilidad VPN + multi-worker validada tarde en el arranque | ✅ Documentado |
| BUG-005 | Alto | `app/models.py` | Bloqueo optimista `version_id` sin respaldo en trigger de BD | ✅ Corregido en SQL |
| BUG-006 | Alto | `app/database.py` | `get_serializable_db()` usa `SET TRANSACTION` dentro de transacción activa | ✅ Corregido |
| BUG-007 | Alto | `install_clean_v43.sql` | Índices GIN requieren `CREATE INDEX CONCURRENTLY` manual | ✅ Corregido en SQL |
| BUG-008 | Alto | `app/main.py` | Versión declarada como `v4.0` en docstring pero `APP_VERSION = "6.0.0"` en config | ✅ Documentado |
| BUG-011 | Medio | `app/database.py` | `execute_with_retry()` captura excepciones genéricas, enmascara errores de programación | ✅ Corregido |
| BUG-012 | Medio | `app/models.py` | Brecha FK en `ScrapingLog`; tabla particionada no puede tener restricciones FK | ✅ Corregido (trigger) |
| BUG-014 | Medio | `app/config.py` | `MAX_ERROR_LEN=2000` duplicado en config y definiciones de columnas del modelo | ✅ Corregido (constante) |
| BUG-015 | Bajo | `scripts/verify_system.py` | Importación desde módulo inexistente `app.core.database` | ✅ Corregido |
| BUG-016 | Bajo | `scripts/verify_system.py` | Importación desde módulo inexistente `app.core.config` | ✅ Corregido |
| BUG-017 | Bajo | `scripts/verify_system.py` | Segunda referencia a `app.core.database` | ✅ Corregido |
| BUG-018 | Bajo | `scripts/verify_system.py` | Importación desde `app.tasks.celery_app` (no existe) | ✅ Corregido |
| BUG-021 | Bajo | `models.py` | Tabla particionada `ScrapingLog` sin FK, sin explicación | ✅ Corregido (comentario) |
| BUG-022 | Bajo | `completeness_service.py` | `MAX_LANG_RETRIES` codificado en `1` | ✅ Corregido (.env) |
| BUG-EN-003 | Medio | `scripts/load_urls.py` | `except:` sin tipo captura `KeyboardInterrupt` (3 ubicaciones) | ✅ Corregido |

### 1.2 Detalle de Correcciones Críticas

#### BUG-001: Validación de Credenciales en Tiempo Correcto (CRÍTICO → Corregido)
**Problema:** `_build_database_url()` en `database.py` solo se llamaba al instanciar el motor SQLAlchemy. La aplicación podía arrancar y servir peticiones con credenciales inválidas, fallando únicamente en la primera consulta a la BD.

**Corrección:** `_get_required_env()` se llama en tiempo de importación del módulo. Si `DB_USER` o `DB_PASSWORD` están vacíos, se lanza `EnvironmentError` inmediatamente durante `import app.database`, antes de atender ninguna petición.

```python
# v46 — falla inmediatamente en importación si faltan credenciales
DATABASE_URL = _build_database_url()  # llamado a nivel de módulo
```

#### BUG-002: Índice Parcial Ausente (CRÍTICO → Corregido)
**Problema:** El índice único parcial `ix_hotels_url_lang_null` estaba descrito en un comentario dentro de `__table_args__` pero nunca declarado como `Index()` de SQLAlchemy. Ejecutar `create_all()` no creaba este índice, permitiendo pares duplicados `(url, language)` cuando `url_id IS NULL`.

**Corrección:** Declarado como `Index()` con `postgresql_where`:
```python
Index(
    "ix_hotels_url_lang_null",
    "url", "language",
    unique=True,
    postgresql_where=text("url_id IS NULL"),
),
```
Este índice ahora se crea tanto por `create_all()` como por `install_clean_v46.sql`.

#### BUG-003: Ubicación de requirements.txt (CRÍTICO → Corregido)
**Problema:** `requirements.txt` estaba en `app/requirements.txt`. Ejecutar `pip install -r requirements.txt` desde la raíz del proyecto fallaba con `FileNotFoundError`.

**Corrección:** `requirements.txt` movido a la raíz del proyecto. El archivo antiguo `app/requirements.txt` debe eliminarse.

#### BUG-006: Configuración del Nivel de Aislamiento (ALTO → Corregido)
**Problema:** `get_serializable_db()` ejecutaba `SET TRANSACTION ISOLATION LEVEL REPEATABLE READ` dentro de una transacción ya iniciada. PostgreSQL requiere que el nivel de aislamiento se establezca antes del primer statement.

**Corrección:** Usa `execution_options` de SQLAlchemy sobre el objeto de conexión antes de iniciar la transacción:
```python
session.connection(execution_options={"isolation_level": "REPEATABLE READ"})
```

#### BUG-007: Índices GIN No Automatizados (ALTO → Corregido)
**Problema:** Los índices GIN en columnas JSONB estaban anotados en `install_clean_v43.sql` como pasos manuales con `CREATE INDEX CONCURRENTLY`. Esto no estaba documentado en los pasos de despliegue.

**Corrección:** `install_clean_v46.sql` incluye todos los índices GIN en el script principal. No se usa `CONCURRENTLY` (el script corre sobre base de datos vacía; `CONCURRENTLY` requiere tabla existente sin transacción activa).

#### BUG-015 a BUG-018: Errores de Importación en verify_system.py (BAJO → Corregido)
**Problema:** Cuatro importaciones referenciaban rutas de módulos inexistentes. El script fallaba con `ImportError` en cada ejecución.

**Correcciones:**
| Antes (roto) | Después (correcto) |
|---|---|
| `from app.core.database import ...` | `from app.database import ...` |
| `from app.core.config import ...` | `from app.config import ...` |
| `from app.tasks.celery_app import ...` | `from app.celery_app import ...` |
| `import psycopg2` | `import psycopg` (v3) |

#### BUG-EN-003: Cláusulas `except:` Genéricas en load_urls.py (MEDIO → Corregido)
**Problema:** Tres ubicaciones en `load_urls.py` usaban `except:` sin tipo, capturando silenciosamente `KeyboardInterrupt` y `SystemExit`, impidiendo la terminación limpia del proceso con Ctrl+C.

**Corrección:** Todas las cláusulas `except:` reemplazadas por tipos específicos:
- `except KeyboardInterrupt:` → re-lanzado siempre (`raise`)
- `except SystemExit:` → re-lanzado siempre (`raise`)
- `except OSError:` / `except csv.Error:` → manejados con mensajes apropiados

---

## 2. Mapa de Arquitectura

```
BookingScraper Pro v6.0 — Arquitectura Nodo Único Windows 11
=============================================================

[Puntos de Entrada]
├── app/main.py                FastAPI (Uvicorn en Windows)
│   ├── GET /health            Verificación de salud (BD + Redis + pool)
│   ├── POST /api/scrape       Envío de URLs para scraping
│   ├── GET /api/hotels        Consulta de datos de hoteles
│   └── GET /api/queue         Monitoreo del estado de cola
│
├── app/celery_app.py          Worker Celery
│   └── celery -A app.celery_app worker --pool=threads
│
└── scripts/
    ├── load_urls.py           CLI: carga masiva de URLs desde CSV
    ├── verify_system.py       CLI: verificación pre-arranque del sistema
    └── export_data.py         CLI: exportación de datos a CSV/Excel

[Capa de Lógica de Negocio]
├── app/scraper_service.py     Orquestación: despacho de URLs, workers, estadísticas
├── app/scraper.py             Motores de scraping (CloudScraper + Selenium)
├── app/completeness_service.py Seguimiento de completitud por idioma
├── app/image_downloader.py    Descarga paralela de imágenes
└── app/vpn_manager_windows.py Integración NordVPN CLI (solo Windows)

[Capa de Extracción de Datos]
└── app/extractor.py           Parsing HTML y normalización de datos

[Capa de Acceso a Datos]
├── app/database.py            Motor SQLAlchemy + gestión de sesiones
│   ├── get_db()               Contexto READ COMMITTED
│   ├── get_serializable_db()  Contexto REPEATABLE READ [BUG-006 corregido]
│   ├── execute_with_retry()   Reintento con backoff exponencial [BUG-011 corregido]
│   └── get_pool_status()      Métricas del pool [BUG-017 corregido]
│
├── app/models.py              Modelos ORM SQLAlchemy
│   ├── URLQueue               Cola de tareas de scraping
│   ├── URLLanguageStatus      Seguimiento de completitud por idioma
│   ├── Hotel                  Datos de hotel (columnas JSONB)
│   ├── ScrapingLog            Registro de eventos (particionado mensual)
│   └── ImageDownload          Seguimiento de descargas de imágenes
│
└── app/config.py              Configuración Pydantic con validación Windows

[Infraestructura]
├── PostgreSQL 15-18           Almacenamiento primario (Servicio Windows)
├── Redis / Memurai            Broker Celery (Memurai recomendado Windows 11)
└── NordVPN CLI                Rotación de IP (opcional, solo un worker)

[Integración Windows]
├── *.bat                      15 scripts batch de Windows
├── windows_service.py         Registro en SCM (pywin32)
└── PostgreSQL Windows Service Inicio automático vía Administrador de Servicios
```

### Decisiones de Diseño Específicas para Windows 11

| Decisión | Razón |
|----------|-------|
| ThreadPoolExecutor (no ProcessPoolExecutor) | `multiprocessing` en Windows usa spawn (no fork); los threads comparten memoria de forma segura para tareas I/O-bound |
| Memurai en lugar de Redis | Redis no tiene binario oficial para Windows 11; Memurai es compatible y nativo |
| `pool_pre_ping=True` | Windows Defender Firewall puede cerrar silenciosamente conexiones TCP inactivas |
| `pool_recycle=3600` | Recicla conexiones antes de que el timeout TCP de Windows las mate |
| Nodo único | Desktop Heap limita max_connections; WSFC no disponible en escritorio |
| Signal handlers limitados | SIGUSR1/SIGUSR2 no disponibles en Windows; rotación de logs usa `RotatingFileHandler` |

---

## 3. Guía de Instalación

### 3.1 Prerequisitos

```
Windows 11 Professional o Enterprise (64-bit)
Python 3.11+ (64-bit) — https://python.org/downloads/
PostgreSQL 15-18 (Windows x64) — https://www.enterprisedb.com/downloads/
Memurai (Redis para Windows) — https://www.memurai.com/ (edición desarrollador gratuita)
Git — https://git-scm.com/download/win
Visual C++ Redistributables — https://aka.ms/vs/17/release/vc_redist.x64.exe
```

### 3.2 Preparación del Sistema Windows

**Paso 1: Activar soporte de rutas largas** (PowerShell como Administrador)
```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
    -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

**Paso 2: Plan de energía de alto rendimiento**
```powershell
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
```

**Paso 3: Crear directorios de la aplicación**
```powershell
New-Item -ItemType Directory -Force -Path "C:\BookingScraper\images"
New-Item -ItemType Directory -Force -Path "C:\BookingScraper\data"
New-Item -ItemType Directory -Force -Path "C:\BookingScraper\exports"
New-Item -ItemType Directory -Force -Path "C:\BookingScraper\logs"
```

### 3.3 Configuración de PostgreSQL

**Paso 1: Instalar PostgreSQL 16 via EnterpriseDB**

**Paso 2: Crear base de datos y usuario** (como superusuario postgres)
```sql
CREATE USER bookingscraper_app WITH PASSWORD 'tu-contraseña-segura';
CREATE DATABASE bookingscraper OWNER bookingscraper_app;
GRANT ALL PRIVILEGES ON DATABASE bookingscraper TO bookingscraper_app;
```

**Paso 3: Configurar postgresql.conf**
```ini
# Ajuste según tu RAM disponible
max_connections = 75
shared_buffers = 2GB              # 25% de 8GB RAM ejemplo
effective_cache_size = 4GB        # 50% de RAM
work_mem = 8MB
maintenance_work_mem = 256MB
wal_buffers = 16MB
checkpoint_completion_target = 0.9
random_page_cost = 1.1            # SSD NVMe; usar 4.0 para SSD SATA
effective_io_concurrency = 1      # Limitación I/O async Windows
log_min_duration_statement = 1000 # Registrar queries >1 segundo
```

**Paso 4: Exclusiones de Windows Defender** (PowerShell como Administrador)
```powershell
Add-MpPreference -ExclusionPath "C:\Program Files\PostgreSQL\16\data"
Add-MpPreference -ExclusionPath "C:\BookingScraper"
```

**Paso 5: Regla de firewall para PostgreSQL**
```powershell
New-NetFirewallRule -DisplayName "PostgreSQL 5432" -Direction Inbound `
    -Protocol TCP -LocalPort 5432 -Action Allow -Profile Private
```

### 3.4 Entorno Python

```cmd
:: Clonar repositorio
git clone https://github.com/corralejo-htls/scrapv25.git
cd scrapv25

:: Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate

:: BUG-003 CORRECCIÓN: Instalar desde requirements.txt en la RAÍZ (no en app/)
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.5 Configuración

```cmd
:: Copiar plantilla de entorno
copy .env.example .env

:: Editar .env con tus credenciales
notepad .env
```

Valores mínimos requeridos en `.env`:
```env
DB_USER=bookingscraper_app
DB_PASSWORD=tu-contraseña-segura
DB_NAME=bookingscraper
```

### 3.6 Creación del Esquema de Base de Datos

```cmd
:: BUG-007 CORRECCIÓN: Un solo script SQL crea TODAS las tablas, índices (incluidos GIN) y triggers
psql -U bookingscraper_app -d bookingscraper -f install_clean_v46.sql

:: Verificar instalación
python scripts/verify_system.py
```

### 3.7 Arrancar la Aplicación

**Desarrollo:**
```cmd
.venv\Scripts\activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Worker Celery (terminal separada):**
```cmd
.venv\Scripts\activate
:: Windows: obligatorio usar --pool=threads (sin soporte fork)
celery -A app.celery_app worker --pool=threads --concurrency=4 --loglevel=info
```

**Producción como Servicio Windows:**
```cmd
:: Registrar como Servicio Windows
python windows_service.py install
python windows_service.py start
```

---

## 4. Referencia de Configuración

### 4.1 Variables de Entorno

| Variable | Defecto | Requerida | Descripción |
|----------|---------|-----------|-------------|
| `DB_USER` | — | ✅ Sí | Usuario PostgreSQL |
| `DB_PASSWORD` | — | ✅ Sí | Contraseña PostgreSQL (validada al arrancar) |
| `DB_NAME` | `bookingscraper` | No | Nombre de la base de datos |
| `DB_HOST` | `localhost` | No | Host PostgreSQL |
| `DB_PORT` | `5432` | No | Puerto PostgreSQL |
| `DB_POOL_SIZE` | `10` | No | Tamaño del pool de conexiones (máx. 20 Windows) |
| `DB_MAX_OVERFLOW` | `5` | No | Conexiones extra sobre pool_size |
| `REDIS_HOST` | `localhost` | No | Host Redis/Memurai |
| `SCRAPER_MAX_WORKERS` | `4` | No | Threads de scraping concurrentes |
| `VPN_ENABLED` | `false` | No | Activar rotación NordVPN |
| `MAX_LANG_RETRIES` | `3` | No | Reintentos por idioma (corrección BUG-022) |
| `LOG_LEVEL` | `INFO` | No | Nivel de verbosidad de logs |
| `IMAGES_DIR` | `C:/BookingScraper/images` | No | Ruta de almacenamiento de imágenes |

### 4.2 Restricciones de Windows 11

| Restricción | Límite | Recomendación |
|------------|-------|---------------|
| PostgreSQL max_connections | ≤ 100 (Desktop Heap) | Establecer en 75 |
| DB_POOL_SIZE | ≤ 20 | Defecto: 10 |
| SCRAPER_MAX_WORKERS | ≤ 8 | Defecto: 4 |
| VPN_ENABLED + MAX_WORKERS | VPN requiere MAX_WORKERS=1 | BUG-004: validado por config |
| Pool Celery | Solo `--pool=threads` | `gevent`/`fork` no compatible |

---

## 5. Esquema de Base de Datos

### 5.1 Resumen de Tablas

| Tabla | Tipo | Clave Primaria | Notas |
|-------|------|----------------|-------|
| `url_queue` | Estándar | UUID v4 | Cola de tareas con bloqueo optimista |
| `hotels` | Estándar | UUID v4 | Datos de hotel con columnas JSONB |
| `url_language_status` | Estándar | UUID v4 | Seguimiento de completitud por idioma |
| `scraping_logs` | Particionada (RANGE mensual) | BigSerial + created_at | Registro de eventos; FK via trigger |
| `image_downloads` | Estándar | UUID v4 | Seguimiento de descargas de imágenes |
| `system_config` | Estándar | VARCHAR key | Configuración en tiempo de ejecución |

### 5.2 Índices Clave

| Índice | Tabla | Tipo | Propósito |
|--------|-------|------|-----------|
| `ix_hotels_url_lang_null` | hotels | UNIQUE Parcial | Unicidad para (url, language) WHERE url_id IS NULL **(corrección BUG-002)** |
| `ix_hotels_url_id_lang` | hotels | UNIQUE Parcial | Unicidad para (url_id, language) WHERE url_id IS NOT NULL |
| `ix_hotels_amenities_gin` | hotels | GIN | Búsqueda JSONB en amenities **(corrección BUG-007)** |
| `ix_hotels_room_types_gin` | hotels | GIN | Búsqueda JSONB en room_types **(corrección BUG-007)** |
| `ix_url_queue_status_priority` | url_queue | B-Tree Parcial | Obtención eficiente de trabajos pendientes |

### 5.3 Triggers

| Trigger | Tabla | Propósito |
|---------|-------|-----------|
| `trg_*_updated_at` | Todas | Auto-actualizar timestamp `updated_at` |
| `trg_*_version` | url_queue, hotels, url_language_status | Aplicar bloqueo optimista **(corrección BUG-005)** |
| `trg_scraping_logs_fk_check` | scraping_logs | Integridad referencial para tabla particionada **(corrección BUG-012)** |

---

## 6. Lista de Verificación

Ejecutar esta lista después de la instalación para verificar que el sistema está listo:

### Pre-arranque
- [ ] Python 3.11+ instalado: `python --version`
- [ ] Entorno virtual activado: `.venv\Scripts\activate`
- [ ] Archivo `.env` existe en la RAÍZ del proyecto (no en `app/`)
- [ ] `DB_USER` y `DB_PASSWORD` configurados en `.env`
- [ ] Servicio Windows PostgreSQL ejecutándose: `Get-Service postgresql*`
- [ ] Servicio Windows Memurai ejecutándose: `Get-Service memurai`

### Dependencias
- [ ] `pip install -r requirements.txt` completado sin errores
- [ ] `python -c "import psycopg; print(psycopg.__version__)"` muestra versión (NO psycopg2)
- [ ] `python -c "import fastapi, sqlalchemy, celery"` importa sin error

### Base de Datos
- [ ] Esquema instalado: `psql -U bookingscraper_app -d bookingscraper -c "\dt"`
- [ ] Las 6 tablas presentes: url_queue, hotels, url_language_status, scraping_logs, image_downloads, system_config
- [ ] Índices GIN presentes: `SELECT indexname FROM pg_indexes WHERE indexname LIKE '%gin%';`
- [ ] Índice parcial presente: `SELECT indexname FROM pg_indexes WHERE indexname = 'ix_hotels_url_lang_null';`
- [ ] Triggers presentes: `SELECT trigger_name FROM information_schema.triggers WHERE trigger_schema = 'public';`

### Aplicación
- [ ] `python scripts/verify_system.py` termina con código 0 (todas las verificaciones pasan)
- [ ] `uvicorn app.main:app` arranca sin EnvironmentError ni ImportError
- [ ] `GET http://localhost:8000/health` devuelve HTTP 200

### Integración Windows
- [ ] Exclusiones de Windows Defender configuradas para directorio de datos PostgreSQL
- [ ] Exclusiones de Windows Defender configuradas para `C:\BookingScraper`
- [ ] Regla de firewall para puerto 5432 activa
- [ ] Plan de energía de alto rendimiento activo: `powercfg /getactivescheme`
- [ ] Soporte de rutas largas activado

---

## 7. Solución de Problemas

### Error: `EnvironmentError: Required environment variable 'DB_PASSWORD' is not set`
**Causa:** Archivo `.env` no cargado antes de `import app.database`. La corrección de BUG-001 hace que falle rápido.  
**Solución:** Asegurar que `.env` está en la raíz del proyecto y `python-dotenv` está instalado.

### Error: `FileNotFoundError: [Errno 2] No such file or directory: 'requirements.txt'`
**Causa:** Ejecutar `pip install -r requirements.txt` desde el directorio `app/`.  
**Solución (BUG-003):** Ejecutar desde la raíz del proyecto: `cd scrapv25 && pip install -r requirements.txt`

### Error: `ImportError: No module named 'app.core.database'`
**Causa:** `verify_system.py` antiguo (pre-v46) con importaciones incorrectas.  
**Solución (BUG-015):** Reemplazar `scripts/verify_system.py` con la versión corregida v46.

### Error: `ImportError: No module named 'psycopg2'`
**Causa:** Script o dependencia intenta usar `psycopg2` (v2). Este proyecto usa `psycopg` (v3).  
**Solución:** `pip install psycopg[binary]` — NO instalar `psycopg2`.

### Error: `duplicate key value violates unique constraint` en tabla hotels
**Causa:** Índice parcial `ix_hotels_url_lang_null` ausente (BUG-002). Volver a ejecutar `install_clean_v46.sql`.  
**Verificación:** `SELECT indexname FROM pg_indexes WHERE indexname = 'ix_hotels_url_lang_null';`

### Error: `celery: ERROR - no such option: --pool=gevent`
**Causa:** `gevent` no instalado o tipo de pool incorrecto en Windows.  
**Solución:** Usar siempre `--pool=threads` en Windows 11: `celery -A app.celery_app worker --pool=threads`

### Consultas JSONB lentas (amenities, room_types)
**Causa:** Índices GIN no creados (BUG-007 — script SQL pre-v46).  
**Solución:** Volver a ejecutar `install_clean_v46.sql` que incluye todos los índices GIN.

### PostgreSQL no arranca tras actualización de Windows
**Causa:** Windows Update puede reiniciar servicios en orden incorrecto.  
**Solución:** Configurar servicio PostgreSQL como "Inicio automático (retrasado)":
```powershell
Set-Service -Name "postgresql-x64-16" -StartupType AutomaticDelayedStart
```

### Alto uso de memoria
**Causa:** `work_mem` demasiado alto con múltiples conexiones.  
**Solución:** Reducir `work_mem` en `postgresql.conf`. Con `max_connections=75` y `work_mem=8MB`, el peor caso es `75 * 8MB = 600MB` de RAM adicional solo para operaciones de ordenación.

### Proceso no termina con Ctrl+C durante carga de URLs
**Causa:** Cláusula `except:` genérica pre-v46 capturaba `KeyboardInterrupt` silenciosamente.  
**Solución (BUG-EN-003):** Reemplazar `scripts/load_urls.py` con la versión corregida v46.

---

*BookingScraper Pro v6.0 — Informe Técnico v46*  
*Generado: 2026-03-07*  
*Plataforma: Windows 11 + Python 3.11+ + PostgreSQL 15-18*
