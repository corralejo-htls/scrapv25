# BookingScraper Pro v6.0 — Informe del Proyecto
## Versión: 48 | Plataforma: Windows 11 + Python 3.11+ + PostgreSQL 15+

---

## 1. RESUMEN DE PROBLEMAS Y REGISTRO DE CORRECCIONES

### Problemas Críticos Resueltos

| ID | Severidad Original | Archivo | Corrección Aplicada |
|----|---------------------|---------|---------------------|
| SCRAP-SEC-001 / BUG-101 | **Crítico** | `config.py` | `SECRET_KEY` genera automáticamente una clave segura aleatoria si está vacía o es el valor por defecto. La clave `change-this-to-a-random-secret-key` es rechazada explícitamente. |
| SCRAP-BUG-009 / BUG-101 | **Crítico** | `tasks.py` | Inyección SQL eliminada. Los nombres de partición son validados con expresión regular estricta `^scraping_logs_\d{4}_(?:0[1-9]|1[0-2])$` antes de cualquier interpolación. |
| SCRAP-BUG-004 / BUG-001 | **Crítico** | `database.py` | La construcción de la URL de base de datos es **diferida** — el motor se crea sólo al primer acceso, no en el momento de la importación. Alembic y pytest pueden importar `app.database` sin credenciales configuradas. |
| BUG-002 | **Crítico** | `main.py` | El fallback del lock en multiproceso registra explícitamente una advertencia `WARNING` de que `threading.Lock` NO es seguro con `uvicorn --workers > 1`. La guía de despliegue exige `workers=1`. |
| BUG-003 / BUG-103 | **Crítico** | `models.py`, `install_clean_v48.sql` | La ausencia de FK en `ScrapingLog` está documentada con advertencia destacada. El trigger `trg_scraping_logs_fk_check` es creado por el script SQL y adjuntado a cada partición. |
| BUG-004 | **Crítico** | `scraper.py` | `build_language_url()` reescrito. Elimina el sufijo de idioma existente antes de añadir el nuevo. Imposible generar doble `.html`. Verificado en pruebas unitarias. |

### Problemas Altos Resueltos

| ID | Severidad Original | Archivo | Corrección Aplicada |
|----|---------------------|---------|---------------------|
| SCRAP-SEC-002 | Alto | `config.py` | `API_KEY` sigue con valor vacío por defecto, pero `REQUIRE_API_KEY=true` lo exige al arrancar con `ValueError`. |
| BUG-102 / SCRAP-BUG-001 | Alto | `main.py` | `_rate_buckets` tiene evicción TTL (`_RATE_BUCKET_TTL_S=300`). La limpieza se ejecuta periódicamente. La memoria queda acotada. |
| BUG-104 / SCRAP-CON-003 | Alto | `scraper_service.py`, `main.py` | Redis usa un singleton `ConnectionPool`. Todos los clientes Redis comparten el pool vía `_get_redis_client()`. |
| BUG-010 | Alto | `database.py` | `execute_with_retry()` registra `type(exc).__name__` Y `str(exc)` — contexto completo preservado. |

### Problemas Medios Resueltos

| ID | Archivo | Corrección Aplicada |
|----|---------|---------------------|
| SCRAP-BUG-005 | `config.py` | `ENABLED_LANGUAGES` validada una sola vez en `model_validator`, usando `@cached_property`. Sin revalidación por llamada. |
| SCRAP-BUG-005 | `database.py` | `get_readonly_db()` abre la transacción con `BEGIN READ ONLY` como primera sentencia. |
| BUG-013 | `scraper.py` | `_is_blocked()` envuelto en `try/except`. Los errores de parsing devuelven `True` (por seguridad). |
| BUG-014 | `config.py` | `DEBUG_HTML_MAX_AGE_HOURS` usa `@field_validator` con `try/except ValueError`. Valores no numéricos usan 24h por defecto con AVISO. |
| BUG-016 | `models.py`, SQL | Restricción `chk_uls_status_valid` incluye `'incomplete'`. |
| BUG-017 | `config.py` | Claves de `LANGUAGE_EXT` validadas contra `ENABLED_LANGUAGES` en `model_validator`. |
| SCRAP-BUG-010 | `vpn_manager_windows.py` | Nombres de país validados contra lista canónica `_VALID_VPN_COUNTRIES`. Subprocess con `shell=False` y argumentos como lista. |
| BUG-108 | `vpn_manager_windows.py` | Fallos de subprocess registran `returncode`, `stderr`, `stdout`. |
| BUG-107 | `extractor.py` | Detección de idioma con 5 estrategias: atributo html-lang, meta content-language, og:locale, meta[name=language], análisis de URL. |
| SCRAP-BUG-016 | `scraper_service.py` | `max_workers` limitado a `SCRAPER_MAX_WORKERS` en tiempo de ejecución. |
| SCRAP-BUG-019 | `windows_service.py` | `_SHUTDOWN_TIMEOUT_MS = 30_000` (era demasiado corto). |
| SCRAP-BUG-023 | `completeness_service.py` | `update_language_status()` usa `SELECT FOR UPDATE` para evitar condiciones de carrera. |
| SCRAP-BUG-024 | `main.py` | Validación de URL reforzada con regex + verificación de `netloc`. |
| SCRAP-BUG-034 | `completeness_service.py` | Tabla de transiciones de estado `_VALID_TRANSITIONS` rechaza cambios no válidos. |

### Problemas Bajos Resueltos

| ID | Archivo | Corrección Aplicada |
|----|---------|---------------------|
| BUG-106 | `scraper.py` | SHA-256 reemplaza MD5 para generación de nombres de archivo. |
| BUG-018 | `scraper.py` | `USER_AGENTS_WIN` ponderado por cuota de mercado real. |
| BUG-019 | `models.py` | `SystemMetrics` tiene índices compuestos en columnas de series temporales. |
| BUG-111 | `alembic.ini` | `script_location = migrations`. Directorio creado con `env.py`. |
| Deriva de versión | Todos | Fuente única de verdad: `APP_VERSION="6.0.0"`, `BUILD_VERSION=48` en `app/__init__.py`. |

---

## 2. MAPA DE ARQUITECTURA

```
Windows 11 — Despliegue en Nodo Único
═══════════════════════════════════════════════════════════════
│
│  PUNTOS DE ENTRADA
│  ┌────────────────────┐  ┌──────────────────────────────┐
│  │   main.py          │  │   windows_service.py         │
│  │   FastAPI/Uvicorn  │  │   Integración Windows SCM    │
│  │   Puerto 8000      │  │   Arranque automático         │
│  │   workers=1 ⚠️     │  │   Cierre graceful 30s        │
│  └────────┬───────────┘  └──────────────────────────────┘
│           │
│  MIDDLEWARE
│  ┌────────────────────────────────────────────────────────┐
│  │  Limitador de tasa (dict con TTL, 10 rps/IP)          │
│  │  CORS (sólo localhost)                                 │
│  │  Autenticación API Key (Bearer token opcional)         │
│  └────────┬───────────────────────────────────────────────┘
│           │
│  LÓGICA DE NEGOCIO
│  ┌────────────────────┐  ┌────────────────────────────────┐
│  │  scraper_service   │  │  completeness_service          │
│  │  - ThreadPoolExec  │  │  - SELECT FOR UPDATE           │
│  │  - Lock Redis      │  │  - Máquina de estados          │
│  │    (pool compart.) │  │  - Seguimiento multiidioma     │
│  └────────┬───────────┘  └────────────────────────────────┘
│           │
│  ┌────────────────────┐  ┌────────────────────────────────┐
│  │  scraper.py        │  │  extractor.py                  │
│  │  - CloudScraper    │  │  - Detección idioma 5 capas    │
│  │  - SeleniumEngine  │  │  - Fallback lxml/html.parser   │
│  │  - UA ponderados   │  │  - Extracción estructurada     │
│  │  - Hashes SHA-256  │  └────────────────────────────────┘
│  └────────────────────┘
│
│  COLA DE TAREAS (Celery / Redis)
│  ┌────────────────────────────────────────────────────────┐
│  │  tasks.py                                              │
│  │  - ensure_log_partitions (SQL validado, SERIALIZABLE)  │
│  │  - purge_old_debug_html                                │
│  │  - collect_system_metrics                              │
│  │  - reset_stale_processing_urls                         │
│  └────────┬───────────────────────────────────────────────┘
│           │
│  ACCESO A DATOS (motor lazy — sin fallos en importación)
│  ┌────────────────────────────────────────────────────────┐
│  │  database.py                                           │
│  │  - get_db()              Sesión lectura/escritura      │
│  │  - get_readonly_db()     BEGIN READ ONLY               │
│  │  - get_olap_db()         statement_timeout por sesión  │
│  │  - get_serializable_db() Aislamiento SERIALIZABLE      │
│  │  - execute_with_retry()  Backoff exponencial           │
│  └────────┬───────────────────────────────────────────────┘
│           │
│  ALMACENAMIENTO
│  ┌────────────────────┐  ┌───────────────┐  ┌───────────┐
│  │  PostgreSQL 15+    │  │  Redis/Memurai│  │  NordVPN  │
│  │  Servicio Windows  │  │  Broker+Caché │  │  CLI      │
│  │  max_conn=50       │  │  Pool=20 conn │  │  Opcional │
│  │  Logs particionados│  └───────────────┘  └───────────┘
│  │  Triggers FK       │
│  └────────────────────┘
═══════════════════════════════════════════════════════════════
```

---

## 3. GUÍA DE INSTALACIÓN (Windows 11 — Entorno Limpio)

### Lista de Verificación de Prerrequisitos

- [ ] Windows 11 Pro o Enterprise (21H2+)
- [ ] Plan de energía "Alto rendimiento" activado
- [ ] PostgreSQL 16 instalado vía instalador EnterpriseDB
- [ ] Redis o Memurai instalado y en ejecución
- [ ] Python 3.11+ x64 instalado desde python.org
- [ ] Git instalado
- [ ] Visual C++ Redistributables instalados (necesario para wheels de lxml)
- [ ] Soporte de rutas largas habilitado:
  ```
  reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
  ```

### Exclusiones de Windows Defender (OBLIGATORIO antes de instalar)

```powershell
# Ejecutar como Administrador
Add-MpPreference -ExclusionPath "C:\Program Files\PostgreSQL"
Add-MpPreference -ExclusionPath "C:\Program Files\Redis"
Add-MpPreference -ExclusionPath "C:\BookingScraper"
Add-MpPreference -ExclusionProcess "python.exe"
```

### Instalación Paso a Paso

```batch
REM 1. Clonar repositorio
git clone https://github.com/corralejo-htls/scrapv25.git BookingScraper
cd BookingScraper

REM 2. Entorno virtual
python -m venv .venv
.venv\Scripts\activate.bat

REM 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

REM 4. Configurar entorno
copy .env.example .env
REM  → Editar .env: configurar DB_USER, DB_PASSWORD, SECRET_KEY (obligatorio)

REM 5. Crear base de datos PostgreSQL
psql -U postgres -c "CREATE DATABASE bookingscraper;"

REM 6. Aplicar esquema completo (OBLIGATORIO — no usar sólo create_tables.py)
psql -U postgres -d bookingscraper -f install_clean_v48.sql

REM 7. Verificar sistema
python scripts\verify_system.py

REM 8. Cargar URLs
python scripts\load_urls.py urls_ejemplo.csv

REM 9. Iniciar servicios (3 terminales)
start_api.bat         (Terminal 1 — Servidor API)
start_worker.bat      (Terminal 2 — Celery worker)
start_beat.bat        (Terminal 3 — Celery Beat)
```

---

## 4. REFERENCIA DE CONFIGURACIÓN

| Variable | Obligatorio | Defecto | Descripción |
|----------|-------------|---------|-------------|
| `SECRET_KEY` | **Sí** | auto-generada | Clave aleatoria de 48+ caracteres. Configurar en `.env`. |
| `DB_USER` | **Sí** | — | Usuario de PostgreSQL |
| `DB_PASSWORD` | **Sí** | — | Contraseña de PostgreSQL |
| `REDIS_URL` | No | `redis://localhost:6379/0` | URL de conexión Redis |
| `SCRAPER_MAX_WORKERS` | No | `2` | Hilos de scraping (máx. 4) |
| `ENABLED_LANGUAGES` | No | `es,en,de,fr,it,nl,pt` | Códigos ISO 639-1 |
| `VPN_ENABLED` | No | `false` | Activar rotación NordVPN |
| `REQUIRE_API_KEY` | No | `false` | Exigir Bearer token |

---

## 5. LISTA DE VERIFICACIÓN POST-INSTALACIÓN

- [ ] `python scripts/verify_system.py` → los 5 checks pasan
- [ ] `curl http://localhost:8000/health` → `{"status":"healthy"}`
- [ ] `psql -c "\dt"` → lista 6+ tablas
- [ ] `psql -c "SELECT tablename FROM pg_tables WHERE tablename LIKE 'scraping_logs_%'"` → muestra particiones
- [ ] `psql -c "SELECT tgname FROM pg_trigger WHERE tgname = 'trg_scraping_logs_fk_check'"` → trigger presente
- [ ] `python scripts/load_urls.py urls_ejemplo.csv` → reporta `inserted > 0`
- [ ] `logs/bookingscraper.log` tiene entradas con formato JSON
- [ ] Visor de eventos de Windows → entradas de BookingScraper Pro visibles

---

## 6. RESOLUCIÓN DE PROBLEMAS

| Síntoma | Causa | Solución |
|---------|-------|----------|
| `EnvironmentError: DB_PASSWORD is not configured` | `.env` no cargado o `DB_PASSWORD` vacío | Asegurarse de que `.env` existe con `DB_PASSWORD=...` |
| `CRITICAL: SECRET_KEY is not configured` | `SECRET_KEY` ausente en `.env` | Copiar la clave generada del log al archivo `.env` |
| `ConnectionRefusedError` al arrancar | PostgreSQL no está en ejecución | Iniciar el servicio PostgreSQL en Windows |
| `rate limit exceeded` en la API | Demasiadas peticiones del cliente | Aumentar `_RATE_LIMIT_RPS` o añadir reintentos en el cliente |
| Selenium driver no encontrado | ChromeDriver no instalado | Configurar variable `CHROMEDRIVER_PATH` o instalar `webdriver-manager` |
| Fallos de conexión VPN | NordVPN no instalado | Configurar `VPN_ENABLED=false` |
| Partición no creada | Error en Celery Beat | Revisar logs; ejecutar `ensure_log_partitions` manualmente |

---

## 7. RIESGOS Y CONSIDERACIONES PENDIENTES

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Punto único de fallo (sin HA) | Alto | Copia de seguridad diaria con `pg_dump`; instantáneas VSS de Windows |
| Reinicios por Windows Update | Medio | Ventana de mantenimiento; reinicio automático del servicio |
| Cambios en el DOM de Booking.com | Alto | Los selectores CSS en `extractor.py` pueden necesitar actualización; monitorizar tasa 404 |
| Agotamiento del Desktop Heap | Medio | `max_connections=50` en postgresql.conf; `pool_size=10` |
| Worker único de uvicorn | Bajo | Intencional para escritorio Windows 11; escalar a servidor si es necesario |
