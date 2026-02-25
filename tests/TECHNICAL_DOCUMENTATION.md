# BookingScraper Pro — Documentación Técnica

> **Versión del sistema:** v2.5 (extractor) / v2.4 (scraper)  
> **Plataforma:** Windows 11 nativo — sin Docker, sin WSL2  
> **Runtime:** Python 3.14.3  
> **Repositorio1:** https://github.com/Aprendiz73/scrvIIpro26
> **Repositorio2:** https://drive.google.com/drive/folders/1BBci8z1T-FWJj4GBeHptIeU1gPmoAgb6?usp=sharing 

---

## Índice

1. [Objetivo del sistema](#1-objetivo-del-sistema)
2. [Stack tecnológico](#2-stack-tecnológico)
3. [Estructura del proyecto](#3-estructura-del-proyecto)
4. [Arquitectura y componentes](#4-arquitectura-y-componentes)
5. [Esquema de base de datos](#5-esquema-de-base-de-datos)
6. [Flujo de scraping](#6-flujo-de-scraping)
7. [Extracción de datos](#7-extracción-de-datos)
8. [Gestión de imágenes](#8-gestión-de-imágenes)
9. [Gestión de VPN](#9-gestión-de-vpn)
10. [API REST](#10-api-rest)
11. [Configuración](#11-configuración)
12. [Scripts de operación](#12-scripts-de-operación)
13. [Versiones y historial de cambios](#13-versiones-y-historial-de-cambios)

---

## 1. Objetivo del sistema

BookingScraper Pro es un sistema de extracción de datos de fichas de hoteles en Booking.com. Para cada URL de hotel en cola, el sistema descarga y persiste:

- Nombre, dirección, descripción, rating y puntuaciones por categoría
- Servicios e instalaciones
- Normas de la casa e información importante
- Tipos de habitaciones
- Hasta 8 fotografías del hotel en resolución máxima (`max1280x900`)

La extracción se realiza en **múltiples idiomas** (hasta 19) por hotel, generando una fila por combinación `url_id × language` en la tabla `hotels`.

El sistema opera bajo NordVPN con rotación automática de servidor para evitar bloqueos por IP, usando Brave como browser principal con Selenium WebDriver para eludir las protecciones JavaScript de Booking.com.

---

## 2. Stack tecnológico

| Capa | Componente | Versión |
|------|-----------|---------|
| API / Servidor | FastAPI + Uvicorn | 0.115.12 / 0.34.3 |
| ORM | SQLAlchemy 2.0 | 2.0.36 |
| Driver PostgreSQL | psycopg3 (binary) | ≥ 3.2.10 |
| Base de datos | PostgreSQL | 15+ |
| Cola de tareas | Celery + Redis/Memurai | 5.4.0 / 5.2.0 |
| Browser automation | Selenium WebDriver | ≥ 4.41.0 |
| Browser | Brave (fallback: Chrome, Edge) | sistema |
| HTTP scraping | cloudscraper + httpx | — |
| HTML parsing | BeautifulSoup4 + lxml | 4.12.3 / ≥ 6.0 |
| Imágenes | Pillow | ≥ 12.1.1 |
| VPN | NordVPN (CLI o app Windows) | sistema |
| Logging | Loguru | 0.7.3 |
| Validación config | Pydantic Settings v2 | 2.7.1 |

---

## 3. Estructura del proyecto

```
C:\BookingScraper\
│
├── app/                          # Código fuente principal
│   ├── __init__.py
│   ├── config.py                 # Configuración centralizada (Pydantic Settings)
│   ├── database.py               # Motor SQLAlchemy, pool de conexiones, utils DB
│   ├── models.py                 # Modelos ORM (URLQueue, Hotel, ScrapingLog, ...)
│   ├── main.py                   # FastAPI app, lifespan, todos los endpoints
│   ├── scraper.py                # Descarga HTML via cloudscraper o Selenium
│   ├── scraper_service.py        # Orquestador: despacha, ejecuta y persiste
│   ├── extractor.py              # Parsea HTML → diccionario de campos
│   ├── image_downloader.py       # Descarga y valida imágenes desde CDN bstatic
│   ├── celery_app.py             # Instancia y configuración de Celery
│   ├── tasks.py                  # Tareas Celery (scrape_hotel_task, beat tasks)
│   ├── vpn_manager.py            # Interfaz abstracta VPN (no Windows-specific)
│   └── vpn_manager_windows.py    # Implementación NordVPN para Windows 11
│
├── scripts/
│   ├── load_urls.py              # Carga masiva de URLs (CSV/TXT) a url_queue
│   ├── export_data.py            # Exporta hotels a CSV / Excel
│   ├── create_tables.py          # Crea tablas vía SQLAlchemy (alternativa a SQL)
│   ├── verify_system.py          # Verifica conectividad de todos los servicios
│   └── create_project_structure.py
│
├── data/
│   ├── images/                   # Imágenes descargadas, subdirectorios por hotel/idioma
│   ├── exports/                  # CSVs y Excel exportados
│   └── logs/                     # Logs rotativos (Loguru)
│
├── alembic/                      # Migraciones de esquema (vacío, se usa init_db.sql)
├── backups/                      # Volcados pg_dump
├── test/                         # Datos de sesiones (logs, CSVs de BD)
│
├── init_db.sql                   # DDL completo: tablas, índices, extensiones
├── migracion_bd_v2.sql           # Migración de esquema v1 → v2 (services/images JSONB)
├── requirements.txt              # Dependencias con versiones exactas
├── .env                          # Variables de entorno (NO versionar)
├── .env.example                  # Template sin credenciales
├── inicio_rapido.bat             # Arranque: limpia cache + inicia uvicorn
├── start_services.bat            # Inicia PostgreSQL, Memurai, Celery
├── stop_services.bat             # Para todos los servicios
├── detener_todo.bat              # Kill forzado de procesos
├── backup_db.bat                 # pg_dump a backups/
└── limpiar_cache.bat             # Elimina __pycache__ y .pyc
```

---

## 4. Arquitectura y componentes

### 4.1 Modo de ejecución

El sistema opera en **modo simplificado**: un único proceso `uvicorn` ejecuta tanto la API REST como el motor de scraping. No se requiere Celery worker activo para el scraping principal.

```
┌────────────────────────────────────────────────────────┐
│                    uvicorn (FastAPI)                    │
│                                                        │
│  ┌──────────────────┐    ┌──────────────────────────┐  │
│  │  HTTP API (sync) │    │  Auto-dispatcher loop    │  │
│  │  /docs           │    │  (asyncio background)    │  │
│  │  /scraping/start │    │  cada 30s consulta       │  │
│  │  /hotels         │    │  url_queue WHERE pending │  │
│  │  /vpn/rotate     │    └──────────┬───────────────┘  │
│  └──────────────────┘               │                  │
│                                     ▼                  │
│                    ┌─────────────────────────────┐     │
│                    │  ThreadPoolExecutor          │     │
│                    │  max_workers=1               │     │
│                    │  scraper_service.scrape_one()│     │
│                    └─────────────────────────────┘     │
└────────────────────────────────────────────────────────┘
         │                          │
         ▼                          ▼
  PostgreSQL (5432)           NordVPN CLI
  (url_queue + hotels)        (rotación por IP)
```

Celery existe en el código (`tasks.py`, `celery_app.py`) pero **no es necesario** para la operación normal. Se activa opcionalmente para tareas periódicas (limpieza de logs, métricas del sistema).

### 4.2 Auto-dispatcher

En `main.py`, la función `_auto_dispatch_loop()` corre como tarea `asyncio` en background desde el lifespan de FastAPI:

```python
async def _auto_dispatch_loop():
    await asyncio.sleep(5)          # espera inicial al arranque
    while True:
        await asyncio.to_thread(_sync_dispatch, settings.BATCH_SIZE)
        await asyncio.sleep(30)     # intervalo entre despachos
```

`_sync_dispatch()` delega en `scraper_service.dispatch_pending()`, que consulta `url_queue WHERE status = 'pending'` y envía cada `url_id` al `ThreadPoolExecutor`.

### 4.3 Módulos y responsabilidades

| Módulo | Responsabilidad única |
|--------|-----------------------|
| `config.py` | Lee `.env` vía Pydantic, expone `settings` global, crea directorios |
| `database.py` | Motor SQLAlchemy, pool `QueuePool(5+10)`, `get_db()`, utilidades SQL |
| `models.py` | Definición ORM de las 5 tablas principales |
| `main.py` | Endpoints FastAPI, lifespan, auto-dispatcher, integración VPN init |
| `scraper_service.py` | Orquestador principal: despacho, secuencia de idiomas, persistencia, VPN |
| `scraper.py` | Descarga de HTML: estrategia cloudscraper → Selenium, manejo de sesión |
| `extractor.py` | Parseo HTML → campos estructurados: 10+ métodos `extract_*()` |
| `image_downloader.py` | Descarga CDN bstatic, validación dimensional, almacenamiento local |
| `vpn_manager_windows.py` | Conexión/desconexión NordVPN, caché de IP, rotación por país |
| `tasks.py` | Tareas Celery: `scrape_hotel_task`, `process_pending_urls`, beat tasks |

---

## 5. Esquema de base de datos

### Tablas principales

```sql
url_queue
  id            SERIAL PK
  url           VARCHAR(512) UNIQUE NOT NULL
  status        VARCHAR(50)   -- pending | processing | completed | failed
  priority      INTEGER DEFAULT 0
  language      VARCHAR(10)   -- idioma base
  retry_count   INTEGER DEFAULT 0
  max_retries   INTEGER DEFAULT 3
  last_error    TEXT
  scraped_at    TIMESTAMP
  created_at    TIMESTAMP
  updated_at    TIMESTAMP

hotels
  id            SERIAL PK
  url_id        INTEGER FK → url_queue.id
  url           VARCHAR(512)
  language      VARCHAR(10)       -- en | es | de | fr | it | ...
  name          VARCHAR(255)
  address       TEXT
  description   TEXT
  rating        FLOAT
  total_reviews INTEGER
  rating_category VARCHAR(100)
  review_scores JSON              -- {"Limpieza": 9.5, "Ubicación": 9.1, ...}
  services      JSON              -- ["WiFi gratis", "Piscina", ...]
  facilities    JSON              -- {"Servicios": ["item1",...], ...}
  house_rules   TEXT
  important_info TEXT
  rooms_info    JSON              -- [{"name": "...", "description": "..."}, ...]
  images_urls   JSON              -- ["https://cf.bstatic.com/...max1280x900/...", ...]
  images_local  JSON              -- rutas locales en data/images/
  images_count  INTEGER
  scraped_at    TIMESTAMP
  updated_at    TIMESTAMP
  UNIQUE (url_id, language)       -- una fila por hotel × idioma

scraping_logs
  id              SERIAL PK
  url_id          INTEGER FK
  status          VARCHAR(50)     -- completed | error | retry | no_data
  language        VARCHAR(10)
  duration_seconds FLOAT
  items_extracted  INTEGER
  error_message    TEXT
  vpn_ip           VARCHAR(50)
  timestamp        TIMESTAMP

vpn_rotations                     -- historial de rotaciones de IP
system_metrics                    -- snapshots periódicos del estado del sistema
```

### Índices relevantes

```sql
-- Despacho de URLs pendientes (consulta crítica, ejecutada cada 30s)
CREATE INDEX idx_url_status_priority ON url_queue(status, priority DESC);

-- Unicidad hotel × idioma
CREATE UNIQUE INDEX ix_hotels_url_language ON hotels(url_id, language);

-- Búsqueda full-text (extensión pg_trgm)
CREATE INDEX idx_hotel_name_trgm        ON hotels USING gin (hotel_name gin_trgm_ops);
CREATE INDEX idx_hotel_description_trgm ON hotels USING gin (description gin_trgm_ops);
```

---

## 6. Flujo de scraping

### 6.1 Ciclo completo por hotel

```
url_queue (status=pending)
         │
         ▼
scraper_service.scrape_one(url_id)
         │
         ├─ 1. Marcar URL como 'processing'
         ├─ 2. Verificar / rotar VPN si corresponde
         │
         ├─ Para cada idioma en ENABLED_LANGUAGES:
         │   │
         │   ├─ Construir URL idiomática:
         │   │   base.html → base.es.html / base.fr.html / ...
         │   │
         │   ├─ scraper.scrape_hotel(url, language)
         │   │   ├─ Intento 1: cloudscraper (HTTP, más rápido)
         │   │   │   └─ Si falla (403, bloqueo) → cloudscraper session reset
         │   │   └─ Intento 2: Selenium / Brave
         │   │       ├─ driver.get(url) + cookies bypass Booking.com
         │   │       ├─ _wait_for_hotel_content() (timeout 30s)
         │   │       ├─ _close_popups() + _scroll_page()
         │   │       ├─ Extraer page_source
         │   │       └─ Si invalid session id → close() + reiniciar driver
         │   │
         │   ├─ extractor.extract_all(html, language) → dict
         │   │
         │   ├─ _save_hotel(db, url_id, lang, data)
         │   │   └─ INSERT ON CONFLICT (url_id, language) DO UPDATE
         │   │
         │   ├─ _download_images(url_id, imgs, lang, driver)
         │   │   └─ Extrae cookies de Brave → sesión autenticada bstatic CDN
         │   │
         │   └─ _log(db, url_id, lang, "completed", duration, items)
         │
         └─ Marcar URL como 'completed' o 'failed'
```

### 6.2 Estrategia de descarga de HTML

`scraper.scrape_hotel()` implementa una cadena de fallback:

```
1. cloudscraper (HTTP puro, sin browser)
   ├─ Headers: User-Agent Windows Chrome, cookies bypass consentimiento
   ├─ Hasta 3 reintentos con backoff: delay * attempt * 1.5 (max 25s)
   ├─ HTTP 403 → session reset (nueva instancia cloudscraper)
   ├─ HTTP 429 → respeta Retry-After header
   └─ Si todos fallan → eleva excepción

2. Selenium / Brave  (USE_SELENIUM=True)
   ├─ Orden de browser: Brave → Chrome → Edge (primer disponible)
   ├─ Flags GPU: --disable-gpu, --disable-software-rasterizer
   │   (evita crashes en sistemas sin GPU dedicada)
   ├─ Un único driver por hotel (compartido entre todos los idiomas)
   ├─ 3 reintentos por URL, con wait aleatorio entre intentos
   ├─ invalid session id → close() + reiniciar browser inmediatamente
   │   (sin esperar el timeout de ~26 min de Selenium)
   └─ Si todos fallan → devuelve None
```

### 6.3 Gestión de errores y recuperación

| Error | Comportamiento |
|-------|---------------|
| `invalid session id` | Driver cerrado y recreado dentro del mismo bucle de reintentos. No se pierden los idiomas ya completados del hotel. |
| HTTP 403 (cloudscraper) | Session reset. Si persiste, escalada a Selenium. |
| HTTP 429 | Sleep de `Retry-After` segundos (fallback: 90s). |
| Cloudflare challenge | Detectado por texto "just a moment" → retry. |
| 3 fallos consecutivos de idioma | VPN rotation forzada. |
| `no_data` (sin nombre extraído) | Registro en `scraping_logs` con `status='no_data'`. El hotel se marca `completed` si al menos 1 idioma tuvo éxito. |
| URL stuck en `processing` | Reset manual vía SQL: `UPDATE url_queue SET status='pending' WHERE status='processing'`. |

---

## 7. Extracción de datos

### 7.1 BookingExtractor

`extractor.py` instancia `BookingExtractor(html: str, language: str)` con BeautifulSoup (parser lxml). El método `extract_all()` invoca cada `extract_*()` y devuelve un diccionario con todos los campos.

### 7.2 Estrategia por campo

Cada campo implementa múltiples estrategias en orden de fiabilidad, retornando en el primer resultado válido:

**`extract_address()`**
```
1. JSON-LD structured data (<script type="application/ld+json">)
   → addr.streetAddress + sub-campos no redundantes + country
   (sub-campos se omiten si ya están en streetAddress, evita duplicación)
2. data-testid="address" → _clean_address()
3. Clase PropertyHeaderAddress
4. XPath: wrap-hotelpage-top/...
5. itemprop="address"
```

**`extract_name()`**
```
1. og:title meta tag
2. <h2> data-testid="header-hotel-name"
3. JSON-LD name
4. <title> tag (extrae solo el nombre, descarta " - Booking.com")
5. XPath XPATH["hotel_name"]
```

**`extract_images()`**
```
1. JSON-LD image array
2. <img> con src que contiene bstatic.com/xdata/images/hotel/
3. data-testid="gallery" imgs
4. Atributos srcset (múltiples resoluciones)
5. b2hotelPage div imgs

Filtros aplicados:
  - _is_hotel_photo(): acepta SOLO bstatic.com/xdata/images/hotel/
    Descarta: banderas (design-assets/), avatares (review/), tracking pixels
  - _normalize_img_url(): normaliza cualquier resolución a max1280x900
    /max500/ → /max1280x900/   (un número)
    /max300/ → /max1280x900/
    /max500x334/ → /max1280x900/ (dos números)
    /square60/ → /max1280x900/ (miniatura cuadrada)
  - Deduplicación por path base (sin query params)
  - Máximo: 30 URLs por hotel
```

**`extract_review_scores()`**
```
1. JSON-LD aggregateRating
2. data-testid="ReviewSubscoresDesktop"
3. data-testid="review-score-component"
4. Clases CSS de puntuación
```

### 7.3 Limpieza de datos

**`_clean_address(v: str) → Optional[str]`**: elimina texto de rating/valoración que Booking.com incrusta en el mismo nodo DOM que la dirección. Patrones detectados (multilingual):

```
Ubicación excelente, puntuada con 9.1/10
Excellent location, Rated by X customers  
Después de reservar, encontrarás todos los datos...
Ver mapa / Show on map
```

---

## 8. Gestión de imágenes

### 8.1 Descarga autenticada

El CDN `cf.bstatic.com` bloquea con HTTP 403 las peticiones directas de `requests.get()`. La solución extrae las cookies activas de Brave WebDriver y las inyecta en una `requests.Session`:

```python
# En scraper_service._download_images()
cookies = {c["name"]: c["value"] for c in driver.get_cookies()}
session = requests.Session()
session.cookies.update(cookies)
ImageDownloader().download_images(urls, hotel_id, lang, session=session)
```

### 8.2 Pipeline por imagen

```
URL normalizada (max1280x900)
        │
        ▼
session.get(url, timeout=30, headers=...)
        │
        ├─ HTTP 200 → io.BytesIO
        │   ├─ PIL.Image.open()
        │   ├─ Verificar dimensiones ≥ 200×150 px
        │   │   (descarta iconos, avatares, tracking pixels)
        │   ├─ _resize_image() si > IMAGE_MAX_WIDTH × IMAGE_MAX_HEIGHT
        │   ├─ img.save(path, quality=85, optimize=True)
        │   └─ Almacenar en data/images/<hotel_id>/<lang>/img_NNNN_<hash8>.jpg
        │
        └─ Error → log + continuar con siguiente imagen
```

### 8.3 Naming de archivos

```
img_0000_ba387a1a0b85.jpg
│    │    └─ 8 chars del hash MD5 del contenido
│    └─ índice de orden (0-padded 4 dígitos)
└─ prefijo fijo
```

### 8.4 Estadísticas por sesión

`ImageDownloader` mantiene contadores `downloaded`, `failed`, `skipped` por operación. Al finalizar reporta: `N/N imágenes OK | M fallidas | K saltadas`.

---

## 9. Gestión de VPN

### 9.1 NordVPNManagerWindows

Implementa tres modos de conexión, autodetectados en orden:

```
method='auto':
  1. cli    → nordvpn.exe disponible en PATH
  2. app    → NordVPN GUI app instalada (via registry HKLM)
  3. manual → guía interactiva (solo en modo development)
```

### 9.2 Rotación automática

La rotación se activa en dos condiciones:

- **Periódica:** cada `VPN_ROTATION_INTERVAL` hoteles completados (default: 50)
- **Por fallos:** cuando hay ≥ 3 fallos consecutivos de scraping

La rotación selecciona un país aleatoriamente de `VPN_COUNTRIES` excluyendo el país actual. Los cambios de IP se registran en la tabla `vpn_rotations`.

### 9.3 Caché de IP y thread safety

```python
# Caché de 30s para evitar saturar servicios externos de detección de IP
# cuando múltiples threads consultan simultáneamente
_ip_cache: Optional[str] = None
_ip_cache_time: float = 0
_ip_lock: threading.Lock = threading.Lock()

def get_current_ip() -> str:
    with _ip_lock:
        if time.time() - _ip_cache_time < 30:
            return _ip_cache
        # consultar api externas (ip-api.com, ifconfig.me, ...)
```

La lógica de `verify_vpn_active()` asume VPN activa cuando no puede obtener la IP real (evita reconexiones en cascada por rate-limit de servicios externos).

---

## 10. API REST

Todos los endpoints son servidos por FastAPI en `http://localhost:8000`. Documentación interactiva en `/docs` (Swagger UI).

### Endpoints por grupo

**Health**
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Info básica de la app |
| GET | `/health` | Estado de la app + conexión DB |

**VPN**
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/vpn/status` | IP actual, país, métricas de rotación |
| POST | `/vpn/rotate` | Fuerza rotación inmediata |
| POST | `/vpn/connect` | Conecta a país específico `{"country": "ES"}` |

**URLs**
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/urls` | Lista url_queue con filtros (status, limit, offset) |
| POST | `/urls/load` | Carga CSV/TXT de URLs (multipart upload) |
| POST | `/urls/reset-failed` | Resetea `failed` → `pending` |

**Scraping**
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/scraping/status` | Estado en tiempo real: activos, completados, últimos logs |
| GET | `/scraping/logs` | Últimos N logs de scraping |
| POST | `/scraping/start` | Despacha batch (async, no bloquea) |
| POST | `/scraping/force-now` | Despacha batch (síncrono, devuelve resultado) |
| POST | `/scraping/test-url` | Prueba scraping de una URL específica |

**Hotels**
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/hotels` | Lista hoteles con filtros (lang, rating, limit) |
| GET | `/hotels/search/` | Búsqueda por nombre o ciudad |
| GET | `/hotels/{hotel_id}` | Detalle completo de un hotel |

**Export**
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/export/csv` | Exporta hotels a CSV |
| GET | `/export/json` | Exporta hotels a JSON |

**System**
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/system/info` | Versión Python, librerías, rutas, stats de disco |
| GET | `/stats` | Métricas globales del sistema |

---

## 11. Configuración

### 11.1 Variables de entorno (`.env`)

Todas las variables son leídas por `config.py` vía `pydantic_settings.BaseSettings`. El archivo `.env` nunca debe versionarse en Git.

```ini
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=booking_scraper
DB_USER=postgres
DB_PASSWORD=<contraseña_segura>     # ← cambiar

# Scraping
USE_SELENIUM=True                   # False = solo cloudscraper (sin JS)
HEADLESS_BROWSER=false              # false en desarrollo, true en servidor
LANGUAGES_ENABLED=en,es,de,fr,it    # idiomas a procesar
MIN_REQUEST_DELAY=2.0               # segundos entre requests
MAX_REQUEST_DELAY=5.0
MAX_RETRIES=3

# VPN
VPN_ENABLED=true
VPN_ROTATION_INTERVAL=50

# Imágenes
DOWNLOAD_IMAGES=true
IMAGE_MAX_WORKERS=5                 # descargas paralelas por hotel

# Celery (opcional)
CELERY_WORKER_CONCURRENCY=1        # SIEMPRE 1 con pool=solo en Windows
```

### 11.2 Idiomas soportados

| Código | Extensión URL | Idioma |
|--------|--------------|--------|
| en | `.html` (base) | English |
| es | `.es.html` | Español |
| de | `.de.html` | Deutsch |
| fr | `.fr.html` | Français |
| it | `.it.html` | Italiano |
| pt | `.pt.html` | Português |
| nl | `.nl.html` | Nederlands |
| ru | `.ru.html` | Русский |
| ar | `.ar.html` | العربية |
| tr | `.tr.html` | Türkçe |
| hu | `.hu.html` | Magyar |
| pl | `.pl.html` | Polski |
| zh | `.zh.html` | 简体中文 |
| no | `.no.html` | Norsk |
| fi | `.fi.html` | Suomi |
| sv | `.sv.html` | Svenska |
| da | `.da.html` | Dansk |
| ja | `.ja.html` | 日本語 |
| ko | `.ko.html` | 한국어 |

### 11.3 Decisión `max_workers=1`

El `ThreadPoolExecutor` está deliberadamente configurado con `max_workers=1`. Aumentarlo requeriría:

- Múltiples instancias de NordVPN activas simultáneamente (no soportado con un único cliente)
- Mayor pool de conexiones DB (actualmente pool_size=5, suficiente para 1 worker)
- Manejo de múltiples sesiones Brave en paralelo

---

## 12. Scripts de operación

### Arranque normal

```batch
cd C:\BookingScraper
inicio_rapido.bat
```

Ejecuta: limpia `__pycache__` → verifica venv → lanza `uvicorn app.main:app --reload`.

El auto-dispatcher arranca 5 segundos después del lifespan de FastAPI y comienza a procesar las URLs pendientes en `url_queue`.

### Carga de URLs

```batch
# Via API (recomendado)
curl -X POST http://localhost:8000/urls/load -F "file=@urls.csv"

# Via script directo
python scripts/load_urls.py --file urls_fichas_booking.csv
```

El CSV puede tener encabezado o no. Se acepta una URL por línea o columna.

### Operaciones de mantenimiento

```batch
backup_db.bat             # pg_dump → backups\booking_scraper_YYYYMMDD.dump
limpiar_cache.bat         # elimina __pycache__ y .pyc en todo el proyecto
detener_todo.bat          # mata uvicorn, celery y procesos Python colgados
```

### Reset de URLs atascadas (SQL)

```sql
-- Después de un Ctrl+C inesperado, las URLs quedan en 'processing'
UPDATE url_queue
SET status = 'pending', retry_count = 0, updated_at = NOW()
WHERE status = 'processing';
```

### Exportación de datos

```batch
python scripts/export_data.py --format csv --output data/exports/hoteles.csv
python scripts/export_data.py --format excel --output data/exports/hoteles.xlsx
```

---

## 13. Versiones y historial de cambios

### extractor.py

| Versión | Cambio principal |
|---------|-----------------|
| v2.1 | `og:title` como primer selector de nombre; 8 fallbacks progresivos |
| v2.2 | `extract_address()` JSON-LD; `extract_images()` CDN bstatic; `extract_rooms()` HPRT |
| v2.3 | Filtro estricto en imágenes: solo `bstatic.com/xdata/images/hotel/` |
| v2.4 | JSON-LD primero en `extract_address()`; `_clean_address()` elimina texto de rating pegado; `_normalize_img_url()` cubre `/max500/`, `/max300/`, `/square60/` |
| **v2.5** | **Fix dirección duplicada**: `streetAddress` ya incluye ciudad/región; sub-campos solo se añaden si no están presentes |

### scraper.py

| Versión | Cambio principal |
|---------|-----------------|
| v2.3 | cloudscraper session reset en 403; `_wait_for_hotel_content()` con señales `og:title`; retry interno con backoff |
| **v2.4** | **Fix `invalid session id`**: el driver se recrea inmediatamente dentro del bucle de reintentos (antes esperaba ~26 min de timeout × 3 intentos = 78 min desperdiciados por idioma) |

### scraper_service.py

| Versión | Cambio principal |
|---------|-----------------|
| v2.1 | Integración VPN; driver Selenium único por hotel (no por idioma) |
| v2.2 | Fix `_save_hotel()`: `CAST(:campo AS jsonb)` en lugar de `::jsonb`; rollback antes de `_log()` en except |
| v2.3 | `_vpn_lock` en `reconnect_if_disconnected()`; `max_workers=1` |

### vpn_manager_windows.py

| Versión | Cambio principal |
|---------|-----------------|
| v1.1 | Eliminado `input()` bloqueante; parámetro `interactive=False` |
| v2.3 | `verify_vpn_active()`: asume VPN activa si IP=Unknown; caché de IP 30s con `threading.Lock` |

### image_downloader.py

| Versión | Cambio principal |
|---------|-----------------|
| v1.1 | `Image.Resampling.LANCZOS`; soporte subdirectorios por idioma |
| v1.2 | Sesión autenticada con cookies de Brave (fix HTTP 403 en bstatic CDN) |
| v1.3 | Filtro de dimensiones mínimas: descarta imágenes < 200×150 px |

---

*Documento generado el 2026-02-23. 