# BookingScraper Pro v6.0 — Informe de Modificaciones v40 y Manual Operativo

**Repositorio:** https://github.com/corralejo-htls/scrapv25.git
**Fecha:** 2026-03-06
**Versión:** v40 (instalación limpia lista para producción)
**Entorno:** Windows 11 — Escritorio local (sin cloud, sin contenedores)

---

## Parte I — Modificaciones Aplicadas en v40

### Resumen de Cambios

| Categoría | Archivos Modificados | Issues Cerrados |
|-----------|---------------------|----------------|
| Correcciones críticas | 4 | CRIT-40-001, CRIT-40-002, CRIT-40-003, CRIT-006, CRIT-008 |
| Prioridad alta | 5 | HIGH-40-001 a HIGH-40-005, HIGH-005, HIGH-009, HIGH-010 |
| Prioridad media | 6 | MED-40-001 a MED-40-007 |
| Prioridad baja / archivos nuevos | 4 | LOW-40-001 a LOW-40-005 |
| Archivos nuevos creados | 2 | `.env.example`, `requirements-dev.txt` |

---

### CRIT-40-001 — Constraint FK en tabla particionada (ScrapingLog)
**Archivo:** `app/models.py`

El modelo `ScrapingLog` tenía `ForeignKey("url_queue.id")` que provoca que `create_all()` lance `FeatureNotSupported` en PostgreSQL 15+. Las tablas particionadas no admiten constraints FK sobre columnas que no son la clave de partición.

**Corrección:** Se eliminó `ForeignKey` de la columna `url_id`. La integridad referencial es gestionada por el trigger `trg_scraping_logs_fk_check` ya definido en `install_clean_v31.sql`. Se cambió `Column(Integer, primary_key=True)` a `Column(BigInteger, ...)` para coincidir con el esquema SQL (`BIGSERIAL`).

---

### CRIT-40-002 — Fallo de binding IN :ids en reset_stale_urls
**Archivo:** `app/tasks.py`

SQLAlchemy `text()` con `IN :ids` + tupla Python produce `operator does not exist: integer = record` en PostgreSQL. Las tuplas de un solo elemento `(42,)` eran especialmente problemáticas.

**Corrección:** Se reemplazó `WHERE url_id IN :ids` por `WHERE url_id = ANY(:ids)`. PostgreSQL `ANY(:ids)` acepta una lista Python mediante binding de arrays de psycopg3, que es el enfoque parametrizado correcto para pruebas de pertenencia a conjuntos.

---

### CRIT-40-003 — _VALID_ISO_639_1 sin ClassVar en Pydantic v2
**Archivo:** `app/config.py`

En Pydantic v2 `BaseSettings`, los atributos de clase sin anotación `ClassVar` son tratados como campos del modelo. `set` no es un tipo de campo Pydantic válido para binding de variables de entorno.

**Corrección:** Se cambió la anotación a `_VALID_ISO_639_1: ClassVar[Set[str]]`. Se añadieron `ClassVar, Set` al import de `typing`.

---

### CRIT-006 — Race condition threading.Lock en /scraping/force-now
**Archivo:** `app/main.py`

`threading.Lock()` es local al proceso. En despliegues uvicorn multi-proceso, dos procesos pueden pasar la comprobación `acquire()` simultáneamente.

**Corrección:** Se sustituyó por un lock distribuido respaldado en Redis usando `SET NX EX` (set-si-no-existe con TTL). Se añadieron las funciones auxiliares `_acquire_force_now_lock()` y `_release_force_now_lock()` con fallback a `threading.Lock` cuando Redis no está disponible. TTL=30s previene deadlocks en caso de caída del proceso.

---

### CRIT-008 — Sin validación HTML antes de parsear
**Archivo:** `app/extractor.py`

`BookingExtractor` pasaba cualquier HTML directamente a `BeautifulSoup` sin comprobar páginas CAPTCHA, bloqueos o errores.

**Corrección:** Se añadió `_validate_html_pre_parse()` invocado en `__init__()` antes de instanciar `BeautifulSoup`. Comprueba: (1) tamaño mínimo de contenido de 20KB, (2) señales conocidas de bloqueo en los primeros 10KB del documento (cadenas CAPTCHA, 403 Forbidden, señales de DDoS Guard). Lanza `ValueError` con mensaje diagnóstico claro.

---

### HIGH-40-001 — Comprobación DB_PASSWORD en tiempo de importación del módulo
**Archivo:** `app/database.py`

El `EnvironmentError` a nivel de módulo fallaba en `alembic revision`, `pytest` y `celery inspect` en cualquier importación donde `DB_PASSWORD` no estuviera definido.

**Corrección:** La comprobación se movió al interior de `_build_database_url()`, que sólo se invoca cuando `create_engine()` es llamado (ruta de inicio de la aplicación). La ejecución en tiempo de importación ahora es libre de efectos secundarios.

---

### HIGH-40-002 — env_file=".env" relativo al CWD
**Archivo:** `app/config.py`

`pydantic-settings` resolvía `.env` relativo al directorio de trabajo del proceso. Al lanzar desde el Programador de tareas o desde un directorio no-proyecto, `.env` no se encontraba silenciosamente.

**Corrección:** Se calculó `_DOTENV_PATH = os.path.join(_REPO_ROOT, ".env")` a nivel de módulo usando resolución de ruta relativa a `__file__`. `model_config` ahora usa `env_file=_DOTENV_PATH`.

---

### HIGH-40-003 — Alembic sys.path resuelve al directorio incorrecto
**Archivo:** `alembic_env.py`

`sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))` añadía el padre de la raíz del proyecto en lugar de la raíz del proyecto.

**Corrección:** Se cambió a `_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))` e inserta directamente `_PROJECT_ROOT`.

---

### HIGH-40-004 — f-string SQL en completeness_service.py
**Archivo:** `app/completeness_service.py`

`f"SET LOCAL lock_timeout = '{_lock_timeout_ms}ms'"` era un antipatrón de inyección SQL.

**Corrección:** Se reemplazó por `"SET LOCAL lock_timeout = " + str(validated_int)`. Se añadió limitación con `max()/min()` a rango seguro (100ms–60000ms). Se eliminó la forma con cadena entrecomillada para ser consistente con `database.py`.

---

### HIGH-40-005 — f-string SQL en database.py get_olap_db
**Archivo:** `app/database.py`

Mismo antipatrón que HIGH-40-004 en la fábrica de sesiones OLAP.

**Corrección:** Se reemplazó por `"SET LOCAL statement_timeout = " + str(validated_int)`. Se añadió limitación al rango 1000ms–3600000ms.

---

### HIGH-005 — Sesión de browser no verificada tras recreación
**Archivo:** `app/scraper.py`

Tras recrear el driver Selenium por `invalid session id`, la nueva sesión no se verificaba como funcional.

**Corrección:** Se añadió prueba `_ = self.driver.current_url` inmediatamente después de la recreación. Si la prueba lanza excepción, el driver se establece a `None` y se intenta el siguiente browser en la cadena de fallback.

---

### HIGH-009 — Carga de memoria Pillow sin límite
**Archivo:** `app/image_downloader.py`

Las imágenes se transmitían completamente a memoria sin comprobaciones de tamaño, permitiendo agotamiento de memoria con imágenes grandes.

**Corrección:** Se añadió una doble capa de guardia de tamaño: (1) comprobación de cabecera `Content-Length` antes del streaming, (2) contador acumulativo de bytes durante el streaming. Ambas abortan al llegar a 20MB. El límite de 20MB está muy por encima de cualquier imagen de hotel legítima (~500KB típico).

---

### HIGH-010 — Regex de idioma en URL incompleta
**Archivo:** `app/scraper.py`

El regex `r'\.([a-z]{2}(?:-[a-z]{2,4})?)\.(html?)'` no capturaba todas las variantes de URL de Booking.com.

**Corrección:** Se amplió a `r'\.([a-z]{2,3}(?:-[a-z]{2,4})?)\.(html?)(?:\?|$)'` para cubrir códigos de idioma de 3 caracteres y asegurar que el ancla `(?:\?|$)` termina correctamente la coincidencia.

---

### MED-40-001 — Referencia obsoleta a install_clean_v32.sql
**Archivo:** `app/models.py`

Un comentario referenciaba un archivo inexistente `install_clean_v32.sql` y una función inexistente `cleanup_orphaned_hotels()`.

**Corrección:** Se actualizó el comentario para reflejar el estado actual: la función aún no está implementada; el archivo de esquema es `install_clean_v31.sql`.

---

### MED-40-002 — Archivo de esquema inexistente en completeness_service.py
**Archivo:** `app/completeness_service.py`

El docstring referenciaba `bookingscraper_schema_v6.sql` que no existe.

**Corrección:** Se actualizó para referenciar el archivo real `install_clean_v31.sql`.

---

### MED-40-003 — Archivo de migración inexistente en main.py
**Archivo:** `app/main.py`

El docstring listaba `migration_v2_url_language_status.sql` como prerequisito.

**Corrección:** Se corrigió para referenciar `install_clean_v31.sql`.

---

### MED-40-004 — Configuración de timeouts Celery conflictiva
**Archivo:** `app/celery_app.py`

Los valores globales `task_soft_time_limit=540` / `task_time_limit=600` conflictían silenciosamente con los valores por defecto por tarea de variables de entorno de 150s/180s.

**Corrección:** Se alinearon los valores globales a 150s/180s con un comentario explicativo listando todos los overrides a nivel de tarea.

---

### MED-40-005 — disk_path no inicializado en bloque except
**Archivo:** `app/tasks.py`

`disk_path` era asignado dentro del bloque `try` pero referenciado en el bloque `except`, arriesgando `UnboundLocalError` si `settings.BASE_DATA_PATH` lanzaba excepción.

**Corrección:** Se inicializó `disk_path = "C:\\"` antes del bloque `try`. Se añadió `AttributeError` a los tipos de excepción capturados.

---

### MED-40-006 — Meta-comando \connect de psql en el script SQL
**Archivo:** `install_clean_v31.sql`

`\connect booking_scraper` falla en todos los clientes que no son psql.

**Corrección:** Se eliminó la línea `\connect`. Se reemplazó por un bloque de comentario detallado que explica cómo ejecutar el script correctamente en psql, pgAdmin, DBeaver y clientes Python.

---

### MED-40-007 — extra="allow" acepta silenciosamente errores tipográficos
**Archivo:** `app/config.py`

Se cambió a `extra="forbid"` para que los errores tipográficos en nombres de variables `.env` sean detectados inmediatamente con un `ValidationError` claro.

---

### LOW-40-001 — Documentación del archivo vpn_manager.py
**Archivo:** `app/vpn_manager.py`

Se añadió documentación explícita aclarando que el archivo SÍ es utilizado (es la fachada de plataforma importada por `scraper_service.py`).

---

### LOW-40-003 — Dependencias de desarrollo en requirements.txt
**Archivos:** `requirements.txt`, nuevo: `requirements-dev.txt`

Se creó `requirements-dev.txt` con todas las dependencias de desarrollo y test correctamente extraídas.

---

### LOW-40-004 — Constantes de ruta en tiempo de definición de clase
**Archivo:** `app/config.py`

Se movieron `_THIS_DIR`, `_REPO_ROOT` y `_DEFAULT_DATA` al nivel de módulo (fuera del cuerpo de la clase). Los valores por defecto de los campos ahora referencian constantes de nivel de módulo, haciéndolos estables en escenarios de prueba.

---

### Archivos Nuevos Creados

| Archivo | Propósito |
|---------|-----------|
| `.env.example` | Plantilla de configuración completa con todas las variables de entorno soportadas, descripciones y notas específicas para Windows |
| `requirements-dev.txt` | Dependencias de desarrollo y test extraídas de los comentarios inline en `requirements.txt` |
| `app/__init__.py` | Marcador de paquete para que el directorio `app` sea un paquete Python válido |

---

## Parte II — Estructura de Archivos

```
BookingScraper_v40/
├── .env.example                  ← Plantilla de configuración (copiar a .env, rellenar contraseñas)
├── alembic.ini                   ← Configuración de migraciones Alembic
├── alembic_env.py                ← Entorno Alembic — CORREGIDO: sys.path apunta a la raíz del proyecto
├── install_clean_v31.sql         ← Script de instalación limpia de BD — CORREGIDO: \connect eliminado
├── requirements.txt              ← Dependencias Python de producción (Python 3.14, Windows)
├── requirements-dev.txt          ← NUEVO: Dependencias de desarrollo/test
└── app/
    ├── __init__.py               ← Marcador de paquete Python
    ├── config.py                 ← CORREGIDO: ClassVar, ruta .env absoluta, extra=forbid
    ├── database.py               ← CORREGIDO: comprobación DB_PASSWORD diferida, SET LOCAL SQL seguro
    ├── models.py                 ← CORREGIDO: FK ScrapingLog eliminado (tabla particionada)
    ├── main.py                   ← CORREGIDO: lock distribuido Redis para /force-now
    ├── scraper_service.py        ← Circuit breaker Redis, backpressure (sin cambios necesarios)
    ├── scraper.py                ← CORREGIDO: verificación sesión recreada, regex URL ampliado
    ├── extractor.py              ← CORREGIDO: validación HTML pre-parseo antes de BeautifulSoup
    ├── completeness_service.py   ← CORREGIDO: SET LOCAL SQL seguro, referencia esquema corregida
    ├── image_downloader.py       ← CORREGIDO: límite tamaño en streaming antes de carga Pillow
    ├── tasks.py                  ← CORREGIDO: binding ANY(:ids), disk_path no inicializado
    ├── celery_app.py             ← CORREGIDO: timeouts de tarea globales alineados
    ├── vpn_manager.py            ← CORREGIDO: rol clarificado en docstring
    └── vpn_manager_windows.py    ← Sin cambios requeridos
```

---

## Parte III — Guía de Instalación (Windows 11 — Instalación Limpia)

### Prerequisitos

Instalar los siguientes componentes en orden antes de ejecutar la aplicación:

| Software | Versión | Descarga |
|----------|---------|---------|
| Python | 3.14.x (build estándar, GIL habilitado) | https://www.python.org/downloads/ |
| PostgreSQL | 15+ | https://www.postgresql.org/download/windows/ |
| Memurai (Redis para Windows) | Latest | https://www.memurai.com/ |
| Git | Latest | https://git-scm.com/ |
| Brave / Chrome / Edge | Latest | Navegador de tu preferencia |
| NordVPN (opcional) | Latest | Solo si `VPN_ENABLED=true` |

### Paso 1 — Clonar o Descargar el Proyecto

```cmd
git clone https://github.com/corralejo-htls/scrapv25.git BookingScraper
cd BookingScraper
```

O extraer el ZIP v40 en una carpeta de tu elección, por ejemplo `C:\BookingScraper`.

### Paso 2 — Crear Entorno Virtual Python

```cmd
python -m venv venv
venv\Scripts\activate
```

### Paso 3 — Instalar Dependencias

```cmd
pip install -r requirements.txt
```

Para desarrollo (opcional):

```cmd
pip install -r requirements-dev.txt
```

### Paso 4 — Configurar el Entorno

```cmd
copy .env.example .env
notepad .env
```

Establecer estos valores requeridos en `.env`:

```ini
DB_PASSWORD=tu_contraseña_postgresql
```

Todos los demás valores tienen configuración por defecto apropiada para desarrollo local en Windows 11.

> **Nota importante:** Con `extra="forbid"` (v40), cualquier nombre de variable de entorno mal escrito en `.env` producirá inmediatamente `ValidationError: Extra inputs are not permitted`. Verifica que todos los nombres coincidan exactamente con los de `.env.example`.

### Paso 5 — Crear la Base de Datos

Abrir un Símbolo del sistema y ejecutar:

```cmd
psql -U postgres -c "CREATE DATABASE booking_scraper ENCODING='UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0;"
psql -U postgres -d booking_scraper -f install_clean_v31.sql
```

Verificar que la instalación se completó correctamente:

```cmd
psql -U postgres -d booking_scraper -c "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"
```

Tablas esperadas: `hotels`, `scraping_logs_YYYY_MM` (partición del mes actual y siguiente), `system_metrics`, `url_language_status`, `url_queue`, `vpn_rotations`.

> **Usuarios de pgAdmin / DBeaver:** La instrucción `\connect` ha sido eliminada (corregido MED-40-006). Ejecutar el script en dos pasos: primero `CREATE DATABASE` conectado a la BD `postgres`, luego el resto del script conectado a `booking_scraper`.

### Paso 6 — Iniciar Memurai (Redis)

Memurai se inicia automáticamente como servicio Windows después de la instalación. Verificar que está en funcionamiento:

```cmd
memurai-cli ping
```

Respuesta esperada: `PONG`

Si no está en ejecución:

```cmd
net start Memurai
```

### Paso 7 — Iniciar la Aplicación

Abrir **tres ventanas separadas del Símbolo del sistema** (todas con el entorno virtual activado):

**Ventana 1 — Servidor FastAPI:**

```cmd
cd BookingScraper
venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Ventana 2 — Worker Celery:**

```cmd
cd BookingScraper
venv\Scripts\activate
celery -A app.celery_app worker --pool=solo --loglevel=info
```

**Ventana 3 — Beat Celery (Planificador):**

```cmd
cd BookingScraper
venv\Scripts\activate
celery -A app.celery_app beat --loglevel=info
```

### Paso 8 — Verificar la Instalación

Abrir un navegador y acceder a:

```
http://localhost:8000/health
http://localhost:8000/docs
```

El endpoint `/health` devuelve el estado de la aplicación, conexión PostgreSQL, conexión Redis y estadísticas actuales de la cola.

---

## Parte IV — Manual Operativo

### Cargar URLs

**Mediante API (archivo CSV):**

```cmd
curl -X POST "http://localhost:8000/urls/load" ^
  -F "file=@hoteles.csv" ^
  -H "X-API-Key: tu_api_key_si_configurado"
```

Formato CSV (con cabecera):

```csv
url
https://www.booking.com/hotel/es/nombre-hotel.es.html
https://www.booking.com/hotel/gb/hotel-name.en.html
```

O lista simple (sin cabecera, una URL por línea):

```
https://www.booking.com/hotel/es/nombre-hotel.es.html
https://www.booking.com/hotel/gb/hotel-name.en.html
```

Las URLs se normalizan automáticamente: los sufijos de idioma (`.es`, `.en-gb`, etc.) se eliminan y se almacena la URL base.

**Mediante API (URL única):**

```cmd
curl -X POST "http://localhost:8000/urls/load" ^
  -H "Content-Type: application/json" ^
  -d "{\"urls\": [\"https://www.booking.com/hotel/es/nombre-hotel.html\"]}"
```

### Iniciar y Detener el Scraping

**Iniciar scraping automático (Celery Beat gestiona el despacho automáticamente):**

Celery Beat despacha URLs cada 30 segundos. Una vez que Celery Worker y Beat están en ejecución, el scraping comienza automáticamente.

**Despacho manual forzado:**

```cmd
curl -X POST "http://localhost:8000/scraping/force-now?batch_size=10"
```

**Comprobar estado del scraping:**

```cmd
curl http://localhost:8000/stats
curl http://localhost:8000/scraping/status
```

**Comprobar completitud de URLs:**

```cmd
curl http://localhost:8000/urls/{url_id}/completeness
```

**Ver URLs incompletas (algunos idiomas fallaron):**

```cmd
curl http://localhost:8000/urls/incomplete
```

### Exportar Datos

```cmd
curl "http://localhost:8000/hotels/export?format=csv" -o hoteles_export.csv
curl "http://localhost:8000/hotels/export?format=excel" -o hoteles_export.xlsx
curl "http://localhost:8000/hotels/export?format=json" -o hoteles_export.json
```

### Gestión de la Cola

**Resetear una URL específica para volver a raspar:**

```cmd
curl -X POST "http://localhost:8000/urls/{url_id}/rollback?keep_logs=true"
```

**Obtener estadísticas de la cola:**

```cmd
curl http://localhost:8000/urls/stats
```

### Gestión de VPN (cuando VPN_ENABLED=true)

```cmd
curl http://localhost:8000/vpn/status
curl -X POST "http://localhost:8000/vpn/rotate"
curl -X POST "http://localhost:8000/vpn/connect" -d "{\"country\": \"ES\"}"
```

### Monitorización

**Utilización del pool y estado de la aplicación:**

```cmd
curl http://localhost:8000/health
```

**Documentación de la API (Swagger UI):**

```
http://localhost:8000/docs
```

**Logs en tiempo real:**

Los logs se escriben en `<proyecto>/data/logs/` y también a la consola. El nivel de log se controla con la variable `LOG_LEVEL` en `.env`.

---

## Parte V — Problemas Comunes y Diagnóstico

### La aplicación no arranca

**Síntoma:** `ValueError: DB_PASSWORD no puede estar vacío`

**Causa:** Archivo `.env` no encontrado o `DB_PASSWORD` no establecido.

**Comprobación:**
1. Verificar que `.env` existe en la raíz del proyecto (misma carpeta que `requirements.txt`).
2. Confirmar que `DB_PASSWORD=tucontraseña` está en `.env` (sin comillas, sin espacios alrededor del `=`).
3. Con `extra="forbid"` (v40), cualquier nombre de variable de entorno mal escrito producirá: `Extra inputs are not permitted`.

---

**Síntoma:** `EnvironmentError: DB_PASSWORD environment variable is not set`

**Causa:** La aplicación fue iniciada sin el entorno virtual activado, por lo que `.env` no fue cargado.

**Solución:** Activar siempre el entorno virtual antes de iniciar: `venv\Scripts\activate`

---

**Síntoma:** `Extra inputs are not permitted [type=extra_forbidden]`

**Causa:** Se usó un nombre de variable de entorno no reconocido en `.env` (por ejemplo `DB_PASWORD` en lugar de `DB_PASSWORD`).

**Solución:** Comparar el `.env` con `.env.example` línea por línea. Con `extra="forbid"` (corrección MED-40-007), los errores tipográficos se detectan inmediatamente en el arranque.

---

### Fallo de conexión PostgreSQL

**Síntoma:** `✗ Error de conexión a PostgreSQL: OperationalError`

**Comprobación:**
1. Verificar que el servicio PostgreSQL está en ejecución: `net start postgresql-x64-15` (ajustar versión)
2. Probar conexión: `psql -U postgres -d booking_scraper -c "SELECT 1;"`
3. Verificar `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` en `.env`

---

### Redis / Memurai no disponible

**Síntoma:** `[ARCH-001/002] Redis/Memurai no disponible`

Sin Redis disponible, el sistema usa estado en memoria (seguro para proceso único). La cola de tareas Celery no funcionará.

**Solución:** Iniciar servicio Memurai: `net start Memurai` o reinstalar desde https://www.memurai.com/

---

### El worker Celery no procesa tareas

**Síntoma:** Las URLs permanecen en estado `pending` indefinidamente.

**Comprobación:**
1. Verificar que el worker Celery está en ejecución (Ventana 2) y no muestra errores de inicio.
2. Verificar que Celery Beat está en ejecución (Ventana 3).
3. Comprobar conexión Redis: `memurai-cli ping` → `PONG`
4. Si las URLs están bloqueadas en estado `processing` más de 30 minutos, la tarea `reset_stale_urls` las recuperará automáticamente.

---

### Scraping bloqueado por Booking.com

**Síntoma:** `[CRIT-008] Block/CAPTCHA signal detected`

**Opciones:**
1. Aumentar `MIN_REQUEST_DELAY` y `MAX_REQUEST_DELAY` en `.env` (probar 3.0 y 8.0).
2. Habilitar VPN: `VPN_ENABLED=true` con NordVPN CLI instalado.
3. Cambiar a modo Selenium: `USE_SELENIUM=true` con un navegador real instalado.

---

### Error al ejecutar el script SQL en pgAdmin o DBeaver

**Síntoma:** El script se detiene en la línea 58 o produce un error de sintaxis.

**Causa:** El meta-comando `\connect` ha sido eliminado en v40 (corrección MED-40-006). Si se usa un script más antiguo, todavía puede estar presente.

**Solución:** Usar el archivo `install_clean_v31.sql` de esta versión v40. Ejecutar en dos pasos: primero crear la BD conectado a `postgres`, luego ejecutar el resto conectado a `booking_scraper`.

---

### Alembic falla con ModuleNotFoundError

**Síntoma:** `ModuleNotFoundError: No module named 'app'` al ejecutar `alembic revision`

**Causa:** El `sys.path` en `alembic_env.py` apuntaba al directorio padre incorrecto (error HIGH-40-003, corregido en v40).

**Verificación:** Asegurarse de usar el archivo `alembic_env.py` de la versión v40.

**Ejecución correcta de Alembic:**

```cmd
cd BookingScraper
venv\Scripts\activate
alembic revision --autogenerate -m "descripcion"
alembic upgrade head
```

---

## Parte VI — Referencia de Variables de Entorno

| Variable | Valor por defecto | Descripción |
|----------|------------------|-------------|
| `DB_HOST` | `localhost` | Host PostgreSQL |
| `DB_PORT` | `5432` | Puerto PostgreSQL |
| `DB_USER` | `postgres` | Usuario de base de datos |
| `DB_PASSWORD` | *(requerido)* | Contraseña de base de datos |
| `DB_NAME` | `booking_scraper` | Nombre de la base de datos |
| `REDIS_HOST` | `localhost` | Host Redis/Memurai |
| `REDIS_PORT` | `6379` | Puerto Redis |
| `VPN_ENABLED` | `false` | Habilitar rotación NordVPN |
| `USE_SELENIUM` | `false` | Usar scraping con navegador |
| `LANGUAGES_ENABLED` | `en,es,de,fr,it` | Idiomas a raspar |
| `SCRAPER_MAX_WORKERS` | `1` | Hilos de scraping paralelos |
| `DOWNLOAD_IMAGES` | `true` | Descargar imágenes de hoteles |
| `API_KEY` | *(vacío)* | Clave de protección API |
| `LOG_LEVEL` | `INFO` | Nivel de verbosidad de logs |
| `DEBUG` | `false` | Logging de queries SQL |

Ver `.env.example` para la referencia completa con todas las variables disponibles.

---

## Parte VII — Tabla de Correspondencia Issues → Correcciones

| ID Issue | Severidad | Archivo | Corrección Aplicada |
|----------|-----------|---------|-------------------|
| CRIT-40-001 | Crítico | `models.py` | FK eliminado; integridad via trigger SQL |
| CRIT-40-002 | Crítico | `tasks.py` | `IN :ids` → `ANY(:ids)` con lista Python |
| CRIT-40-003 | Crítico | `config.py` | `ClassVar[Set[str]]` en `_VALID_ISO_639_1` |
| CRIT-006 | Crítico | `main.py` | Lock Redis distribuido con fallback en memoria |
| CRIT-008 | Crítico | `extractor.py` | Validación pre-parseo HTML con señales de bloqueo |
| HIGH-40-001 | Alto | `database.py` | Comprobación DB_PASSWORD diferida a `_build_database_url()` |
| HIGH-40-002 | Alto | `config.py` | `env_file` con ruta absoluta relativa a `__file__` |
| HIGH-40-003 | Alto | `alembic_env.py` | `sys.path` apunta a la raíz del proyecto correcta |
| HIGH-40-004 | Alto | `completeness_service.py` | `SET LOCAL` con entero validado, sin f-string |
| HIGH-40-005 | Alto | `database.py` | `SET LOCAL` con entero validado, sin f-string |
| HIGH-005 | Alto | `scraper.py` | Verificación de sesión con `current_url` tras recrear |
| HIGH-009 | Alto | `image_downloader.py` | Límite 20MB en streaming antes de Pillow |
| HIGH-010 | Alto | `scraper.py` | Regex URL ampliado: `[a-z]{2,3}`, ancla `(?:\?|$)` |
| MED-40-001 | Medio | `models.py` | Referencia a v32.sql corregida a v31.sql |
| MED-40-002 | Medio | `completeness_service.py` | Referencia `bookingscraper_schema_v6.sql` corregida |
| MED-40-003 | Medio | `main.py` | Referencia `migration_v2_*.sql` corregida |
| MED-40-004 | Medio | `celery_app.py` | Timeouts globales alineados con valores por tarea |
| MED-40-005 | Medio | `tasks.py` | `disk_path` inicializado antes del bloque `try` |
| MED-40-006 | Medio | `install_clean_v31.sql` | `\connect` eliminado; instrucciones de uso añadidas |
| MED-40-007 | Medio | `config.py` | `extra="allow"` → `extra="forbid"` |
| LOW-40-001 | Bajo | `vpn_manager.py` | Documentación del rol clarificada |
| LOW-40-003 | Bajo | `requirements.txt` | `requirements-dev.txt` creado con dependencias dev |
| LOW-40-004 | Bajo | `config.py` | Constantes de ruta movidas a nivel de módulo |

---

*BookingScraper Pro v6.0 — Documentación v40*
*Despliegue Local Windows 11*
*2026-03-06*
