
C:\BookingScraper>python -m venv .venv

C:\BookingScraper>.venv\Scripts\activate.bat

(.venv) C:\BookingScraper>pip install -r requirements.txt
Requirement already satisfied: fastapi<0.116.0,>=0.115.0 in .\.venv\Lib\site-packages (from -r requirements.txt (line 11)) (0.115.14)
Requirement already satisfied: uvicorn<0.31.0,>=0.29.0 in .\.venv\Lib\site-packages (from uvicorn[standard]<0.31.0,>=0.29.0->-r requirements.txt (line 12)) (0.30.6)
Requirement already satisfied: pydantic<2.13.0,>=2.10.0 in .\.venv\Lib\site-packages (from -r requirements.txt (line 13)) (2.12.5)
Requirement already satisfied: pydantic-settings<2.8.0,>=2.5.0 in .\.venv\Lib\site-packages (from -r requirements.txt (line 14)) (2.7.1)
Requirement already satisfied: psycopg<3.3.0,>=3.2.10 in .\.venv\Lib\site-packages (from psycopg[binary]<3.3.0,>=3.2.10->-r requirements.txt (line 18)) (3.2.13)
Requirement already satisfied: SQLAlchemy<2.1.0,>=2.0.30 in .\.venv\Lib\site-packages (from -r requirements.txt (line 19)) (2.0.48)
Requirement already satisfied: alembic<1.15.0,>=1.14.0 in .\.venv\Lib\site-packages (from -r requirements.txt (line 20)) (1.14.1)
Requirement already satisfied: celery<5.5.0,>=5.4.0 in .\.venv\Lib\site-packages (from -r requirements.txt (line 23)) (5.4.0)
Requirement already satisfied: redis<6.0.0,>=5.0.0 in .\.venv\Lib\site-packages (from -r requirements.txt (line 24)) (5.3.1)
Requirement already satisfied: cloudscraper<1.3.0,>=1.2.71 in .\.venv\Lib\site-packages (from -r requirements.txt (line 27)) (1.2.71)
Requirement already satisfied: requests<3.0.0,>=2.32.0 in .\.venv\Lib\site-packages (from -r requirements.txt (line 28)) (2.32.5)
Requirement already satisfied: beautifulsoup4<5.0.0,>=4.12.0 in .\.venv\Lib\site-packages (from -r requirements.txt (line 29)) (4.14.3)
Requirement already satisfied: selenium<4.29.0,>=4.27.0 in .\.venv\Lib\site-packages (from -r requirements.txt (line 31)) (4.28.1)
Requirement already satisfied: pywin32>=308 in .\.venv\Lib\site-packages (from -r requirements.txt (line 35)) (311)
Requirement already satisfied: psutil<7.0.0,>=6.0.0 in .\.venv\Lib\site-packages (from -r requirements.txt (line 38)) (6.1.1)
Requirement already satisfied: python-multipart<0.0.20,>=0.0.9 in .\.venv\Lib\site-packages (from -r requirements.txt (line 41)) (0.0.19)
Requirement already satisfied: python-dotenv<2.0.0,>=1.0.0 in .\.venv\Lib\site-packages (from -r requirements.txt (line 44)) (1.2.2)
Requirement already satisfied: httpx<0.28.0,>=0.27.0 in .\.venv\Lib\site-packages (from -r requirements.txt (line 45)) (0.27.2)
Requirement already satisfied: starlette<0.47.0,>=0.40.0 in .\.venv\Lib\site-packages (from fastapi<0.116.0,>=0.115.0->-r requirements.txt (line 11)) (0.46.2)
Requirement already satisfied: typing-extensions>=4.8.0 in .\.venv\Lib\site-packages (from fastapi<0.116.0,>=0.115.0->-r requirements.txt (line 11)) (4.15.0)
Requirement already satisfied: click>=7.0 in .\.venv\Lib\site-packages (from uvicorn<0.31.0,>=0.29.0->uvicorn[standard]<0.31.0,>=0.29.0->-r requirements.txt (line 12)) (8.3.1)
Requirement already satisfied: h11>=0.8 in .\.venv\Lib\site-packages (from uvicorn<0.31.0,>=0.29.0->uvicorn[standard]<0.31.0,>=0.29.0->-r requirements.txt (line 12)) (0.16.0)
Requirement already satisfied: annotated-types>=0.6.0 in .\.venv\Lib\site-packages (from pydantic<2.13.0,>=2.10.0->-r requirements.txt (line 13)) (0.7.0)
Requirement already satisfied: pydantic-core==2.41.5 in .\.venv\Lib\site-packages (from pydantic<2.13.0,>=2.10.0->-r requirements.txt (line 13)) (2.41.5)
Requirement already satisfied: typing-inspection>=0.4.2 in .\.venv\Lib\site-packages (from pydantic<2.13.0,>=2.10.0->-r requirements.txt (line 13)) (0.4.2)
Requirement already satisfied: tzdata in .\.venv\Lib\site-packages (from psycopg<3.3.0,>=3.2.10->psycopg[binary]<3.3.0,>=3.2.10->-r requirements.txt (line 18)) (2025.3)
Requirement already satisfied: greenlet>=1 in .\.venv\Lib\site-packages (from SQLAlchemy<2.1.0,>=2.0.30->-r requirements.txt (line 19)) (3.3.2)
Requirement already satisfied: Mako in .\.venv\Lib\site-packages (from alembic<1.15.0,>=1.14.0->-r requirements.txt (line 20)) (1.3.10)
Requirement already satisfied: billiard<5.0,>=4.2.0 in .\.venv\Lib\site-packages (from celery<5.5.0,>=5.4.0->-r requirements.txt (line 23)) (4.2.4)
Requirement already satisfied: kombu<6.0,>=5.3.4 in .\.venv\Lib\site-packages (from celery<5.5.0,>=5.4.0->-r requirements.txt (line 23)) (5.6.2)
Requirement already satisfied: vine<6.0,>=5.1.0 in .\.venv\Lib\site-packages (from celery<5.5.0,>=5.4.0->-r requirements.txt (line 23)) (5.1.0)
Requirement already satisfied: click-didyoumean>=0.3.0 in .\.venv\Lib\site-packages (from celery<5.5.0,>=5.4.0->-r requirements.txt (line 23)) (0.3.1)
Requirement already satisfied: click-repl>=0.2.0 in .\.venv\Lib\site-packages (from celery<5.5.0,>=5.4.0->-r requirements.txt (line 23)) (0.3.0)
Requirement already satisfied: click-plugins>=1.1.1 in .\.venv\Lib\site-packages (from celery<5.5.0,>=5.4.0->-r requirements.txt (line 23)) (1.1.1.2)
Requirement already satisfied: python-dateutil>=2.8.2 in .\.venv\Lib\site-packages (from celery<5.5.0,>=5.4.0->-r requirements.txt (line 23)) (2.9.0.post0)
Requirement already satisfied: PyJWT>=2.9.0 in .\.venv\Lib\site-packages (from redis<6.0.0,>=5.0.0->-r requirements.txt (line 24)) (2.11.0)
Requirement already satisfied: pyparsing>=2.4.7 in .\.venv\Lib\site-packages (from cloudscraper<1.3.0,>=1.2.71->-r requirements.txt (line 27)) (3.3.2)
Requirement already satisfied: requests-toolbelt>=0.9.1 in .\.venv\Lib\site-packages (from cloudscraper<1.3.0,>=1.2.71->-r requirements.txt (line 27)) (1.0.0)
Requirement already satisfied: charset_normalizer<4,>=2 in .\.venv\Lib\site-packages (from requests<3.0.0,>=2.32.0->-r requirements.txt (line 28)) (3.4.5)
Requirement already satisfied: idna<4,>=2.5 in .\.venv\Lib\site-packages (from requests<3.0.0,>=2.32.0->-r requirements.txt (line 28)) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in .\.venv\Lib\site-packages (from requests<3.0.0,>=2.32.0->-r requirements.txt (line 28)) (2.6.3)
Requirement already satisfied: certifi>=2017.4.17 in .\.venv\Lib\site-packages (from requests<3.0.0,>=2.32.0->-r requirements.txt (line 28)) (2026.2.25)
Requirement already satisfied: soupsieve>=1.6.1 in .\.venv\Lib\site-packages (from beautifulsoup4<5.0.0,>=4.12.0->-r requirements.txt (line 29)) (2.8.3)
Requirement already satisfied: trio~=0.17 in .\.venv\Lib\site-packages (from selenium<4.29.0,>=4.27.0->-r requirements.txt (line 31)) (0.33.0)
Requirement already satisfied: trio-websocket~=0.9 in .\.venv\Lib\site-packages (from selenium<4.29.0,>=4.27.0->-r requirements.txt (line 31)) (0.12.2)
Requirement already satisfied: websocket-client~=1.8 in .\.venv\Lib\site-packages (from selenium<4.29.0,>=4.27.0->-r requirements.txt (line 31)) (1.9.0)
Requirement already satisfied: anyio in .\.venv\Lib\site-packages (from httpx<0.28.0,>=0.27.0->-r requirements.txt (line 45)) (4.12.1)
Requirement already satisfied: httpcore==1.* in .\.venv\Lib\site-packages (from httpx<0.28.0,>=0.27.0->-r requirements.txt (line 45)) (1.0.9)
Requirement already satisfied: sniffio in .\.venv\Lib\site-packages (from httpx<0.28.0,>=0.27.0->-r requirements.txt (line 45)) (1.3.1)
Requirement already satisfied: colorama in .\.venv\Lib\site-packages (from click>=7.0->uvicorn<0.31.0,>=0.29.0->uvicorn[standard]<0.31.0,>=0.29.0->-r requirements.txt (line 12)) (0.4.6)
Requirement already satisfied: amqp<6.0.0,>=5.1.1 in .\.venv\Lib\site-packages (from kombu<6.0,>=5.3.4->celery<5.5.0,>=5.4.0->-r requirements.txt (line 23)) (5.3.1)
Requirement already satisfied: packaging in .\.venv\Lib\site-packages (from kombu<6.0,>=5.3.4->celery<5.5.0,>=5.4.0->-r requirements.txt (line 23)) (26.0)
Requirement already satisfied: psycopg-binary==3.2.13 in .\.venv\Lib\site-packages (from psycopg[binary]<3.3.0,>=3.2.10->-r requirements.txt (line 18)) (3.2.13)
Requirement already satisfied: attrs>=23.2.0 in .\.venv\Lib\site-packages (from trio~=0.17->selenium<4.29.0,>=4.27.0->-r requirements.txt (line 31)) (25.4.0)
Requirement already satisfied: sortedcontainers in .\.venv\Lib\site-packages (from trio~=0.17->selenium<4.29.0,>=4.27.0->-r requirements.txt (line 31)) (2.4.0)
Requirement already satisfied: outcome in .\.venv\Lib\site-packages (from trio~=0.17->selenium<4.29.0,>=4.27.0->-r requirements.txt (line 31)) (1.3.0.post0)
Requirement already satisfied: cffi>=1.14 in .\.venv\Lib\site-packages (from trio~=0.17->selenium<4.29.0,>=4.27.0->-r requirements.txt (line 31)) (2.0.0)
Requirement already satisfied: wsproto>=0.14 in .\.venv\Lib\site-packages (from trio-websocket~=0.9->selenium<4.29.0,>=4.27.0->-r requirements.txt (line 31)) (1.3.2)
Requirement already satisfied: pysocks!=1.5.7,<2.0,>=1.5.6 in .\.venv\Lib\site-packages (from urllib3[socks]<3,>=1.26->selenium<4.29.0,>=4.27.0->-r requirements.txt (line 31)) (1.7.1)
Requirement already satisfied: httptools>=0.5.0 in .\.venv\Lib\site-packages (from uvicorn[standard]<0.31.0,>=0.29.0->-r requirements.txt (line 12)) (0.7.1)
Requirement already satisfied: pyyaml>=5.1 in .\.venv\Lib\site-packages (from uvicorn[standard]<0.31.0,>=0.29.0->-r requirements.txt (line 12)) (6.0.3)
Requirement already satisfied: watchfiles>=0.13 in .\.venv\Lib\site-packages (from uvicorn[standard]<0.31.0,>=0.29.0->-r requirements.txt (line 12)) (1.1.1)
Requirement already satisfied: websockets>=10.4 in .\.venv\Lib\site-packages (from uvicorn[standard]<0.31.0,>=0.29.0->-r requirements.txt (line 12)) (16.0)
Requirement already satisfied: pycparser in .\.venv\Lib\site-packages (from cffi>=1.14->trio~=0.17->selenium<4.29.0,>=4.27.0->-r requirements.txt (line 31)) (3.0)
Requirement already satisfied: prompt-toolkit>=3.0.36 in .\.venv\Lib\site-packages (from click-repl>=0.2.0->celery<5.5.0,>=5.4.0->-r requirements.txt (line 23)) (3.0.52)
Requirement already satisfied: wcwidth in .\.venv\Lib\site-packages (from prompt-toolkit>=3.0.36->click-repl>=0.2.0->celery<5.5.0,>=5.4.0->-r requirements.txt (line 23)) (0.6.0)
Requirement already satisfied: six>=1.5 in .\.venv\Lib\site-packages (from python-dateutil>=2.8.2->celery<5.5.0,>=5.4.0->-r requirements.txt (line 23)) (1.17.0)
Requirement already satisfied: MarkupSafe>=0.9.2 in .\.venv\Lib\site-packages (from Mako->alembic<1.15.0,>=1.14.0->-r requirements.txt (line 20)) (3.0.3)

(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>psql -U postgres -c "CREATE DATABASE bookingscraper;"
Contraseña para usuario postgres:

CREATE DATABASE

(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>psql -U postgres -d bookingscraper -f schema_v53_complete.sql
Contraseña para usuario postgres:

psql: error: schema_v53_complete.sql: No such file or directory

(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>psql -U postgres -d bookingscraper -f schema_v54_complete.sql
Contraseña para usuario postgres:

SET
SET
SET
SET
SET
SET
CREATE EXTENSION
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
COMMENT
COMMENT
COMMENT
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
COMMENT
COMMENT
COMMENT
COMMENT
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
COMMENT
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
COMMENT
COMMENT
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
COMMENT
COMMENT
COMMENT
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
COMMENT
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
COMMENT
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
COMMENT
CREATE FUNCTION
CREATE TRIGGER
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
COMMENT
COMMENT
COMMENT
CREATE TABLE
CREATE INDEX
COMMENT
COMMENT
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
COMMENT
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
COMMENT
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
COMMENT
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
COMMENT
COMMENT
COMMENT
CREATE TABLE
CREATE INDEX
CREATE INDEX
COMMENT
COMMENT
CREATE FUNCTION
CREATE TRIGGER
CREATE TRIGGER
CREATE TRIGGER
CREATE TRIGGER
CREATE TRIGGER
CREATE TRIGGER
CREATE VIEW
COMMENT
CREATE VIEW
COMMENT
DO

(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>python scripts\verify_system.py
================================================================
BookingScraper Pro v48 — System Verification
================================================================

[ Python ]
  [OK]   Python 3.14.3
  [INFO] Python 3.14 es pre-release. Para produccion se recomienda 3.11/3.12.

[ Dependencias criticas ]
  [OK]   fastapi
  [OK]   uvicorn
  [OK]   pydantic
  [OK]   pydantic-settings
  [OK]   psycopg (v3)
  [OK]   SQLAlchemy
  [OK]   alembic
  [OK]   celery
  [OK]   redis
  [OK]   cloudscraper
  [OK]   requests
  [OK]   beautifulsoup4
  [OK]   selenium
  [OK]   psutil
  [OK]   python-dotenv
  [OK]   httpx
  [OK]   pywin32

[ Dependencias opcionales ]
  (las marcadas [INFO] no bloquean el arranque)
  [INFO] lxml no instalado — usando html.parser (stdlib)
         Ejecuta fix_lxml.bat para instalar lxml si lo necesitas.
  [OK]   html.parser (stdlib)

[ Configuracion ]
  [OK]   .env cargado — app=BookingScraper Pro v6.0.0 build=54

[ Directorios del proyecto ]
  [OK]   app/
  [OK]   scripts/
  [OK]   tests/
  [OK]   migrations/
  [OK]   data/images/
  [OK]   data/exports/
  [OK]   data/logs/debug/
  [OK]   logs/
  [OK]   backups/

[ Conectividad ]
  [OK]   PostgreSQL localhost:5432/bookingscraper
  [OK]   Redis/Memurai en redis://localhost:6379/0

================================================================
  RESULTADO: Sistema listo para arrancar.
  Ejecuta: start_server.bat / start_celery.bat / start_celery_beat.bat
================================================================

(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>python test_config.py
============================================================
  BookingScraper -- Diagnostico pydantic-settings
============================================================

[INFO] Python:            3.14.3
[INFO] pydantic:          2.12.5
[INFO] pydantic-settings: 2.7.1

[INFO] Firma real de settings_customise_sources:
         settings_cls: type[BaseSettings]
         init_settings: PydanticBaseSettingsSource
         env_settings: PydanticBaseSettingsSource
         dotenv_settings: PydanticBaseSettingsSource
         file_secret_settings: PydanticBaseSettingsSource

[INFO] Firma real de DotEnvSettingsSource.__init__:
         settings_cls: type[BaseSettings] = <class 'inspect._empty'>
         env_file: DotenvType | None = WindowsPath('.')
         env_file_encoding: str | None = None
         case_sensitive: bool | None = None
         env_prefix: str | None = None
         env_nested_delimiter: str | None = None
         env_ignore_empty: bool | None = None
         env_parse_none_str: str | None = None
         env_parse_enums: bool | None = None

[TEST A] os.environ con formato JSON
  [OK] VPN_COUNTRIES     = ['Spain', 'Germany', 'France']
  [OK] ENABLED_LANGUAGES = ['es', 'en', 'de']

[TEST B] os.environ comma SIN _CommaAwareEnvSource (EXPECTED-FAIL)
         Confirma que FIX-CFG-001 es necesario en config.py
  [EXPECTED-FAIL] SettingsError -- confirma bug en EnvSettingsSource

[TEST C] os.environ comma CON _CommaAwareEnvSource (FIX-CFG-001)
  [OK] VPN_COUNTRIES     = ['Spain', 'Germany', 'France']
  [OK] ENABLED_LANGUAGES = ['es', 'en', 'de']

[TEST D] Archivo .env con formato comma (escenario produccion real)
  [OK] VPN_COUNTRIES     = ['Spain', 'Germany', 'France', 'Netherlands', 'Italy']
  [OK] ENABLED_LANGUAGES = ['es', 'en', 'de', 'fr', 'it']

============================================================
  RESUMEN ESPERADO:

  TEST A  JSON en os.environ     -> [OK]
  TEST B  comma SIN fix          -> [EXPECTED-FAIL]  <- confirma bug
  TEST C  comma CON fix env      -> [OK]             <- FIX-CFG-001
  TEST D  comma en archivo .env  -> [OK]

  Si TEST C y TEST D pasan -> app/config.py corregido funciona.
  Si TEST B muestra UNEXPECTED-OK -> pydantic-settings cambio de
  comportamiento en esta version y el fix es inofensivo.
============================================================

(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>diagnostico_vpn.bat
============================================================
 BookingScraper Pro v48 - Diagnostico Pre-Inicio
============================================================

[1/6] NordVPN ejecutable...
  OK - nordvpn.exe encontrado
  INFO - version visible en consola al ejecutar: nordvpn --version
         (nordvpn.exe escribe directo al handle de consola Windows)

[2/6] Verificando .env...
  OK - .env encontrado
  OK - VPN_ENABLED=true
  OK - HEADLESS_BROWSER=false
  OK - VPN_ROTATION_INTERVAL=50
  OK - DB_USER configurado
  OK - DB_PASSWORD configurado

[3/6] Redis (Memurai)...
  OK - Memurai responde PONG (cliente: C:\Program Files\Memurai\memurai-cli.exe)

[4/6] PostgreSQL...
  OK - PostgreSQL aceptando conexiones en localhost:5432

[5/6] Brave Browser...
  OK - Brave encontrado:
       C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe

[6/6] IP publica actual (sin VPN)...
  IP actual: 192.145.39.60
  Cuando NordVPN conecte, el Worker log debe mostrar IP diferente:
    INFO  VPN connected to Spain -- IP: X.X.X.X

============================================================
  DIAGNOSTICO OK -- sistema listo para iniciar

  Orden de inicio:
    1. start_redis.bat    (si Memurai no corre como servicio)
    2. inicio_rapido.bat  (Celery + FastAPI)

  Verificacion SQL (5 min despues):
    psql -U postgres -d bookingscraper -c "SELECT event_type, COUNT(*) FROM scraping_logs GROUP BY event_type;"
============================================================


(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>inicio_rapido.bat
============================================================
 BookingScraper Pro v6.0.0 - Inicio Rapido
============================================================

[0/5] cliente Memurai: C:\Program Files\Memurai\memurai-cli.exe
[1/5] Entorno virtual detectado: .venv
[2/5] .env encontrado OK
[3/5] Verificando Memurai/Redis...
  OK - Memurai ya activo (PONG recibido).
[4/5] Verificando PostgreSQL...
  OK - PostgreSQL activo en localhost:5432
[5/5] Abriendo terminales de servicio...

  [API]    http://127.0.0.1:8000
  [Celery] Worker iniciando...
  [Beat]   Scheduler iniciando...

============================================================
 Sistema arrancando en terminales independientes.

 API:     http://127.0.0.1:8000
 Docs:    http://127.0.0.1:8000/docs
 Swagger: http://127.0.0.1:8000/redoc

 Para detener: stop_server.bat  y  stop_celery.bat
============================================================

 Esta ventana puede cerrarse.
============================================================

(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>python scripts\verify_system.py
================================================================
BookingScraper Pro v48 — System Verification
================================================================

[ Python ]
  [OK]   Python 3.14.3
  [INFO] Python 3.14 es pre-release. Para produccion se recomienda 3.11/3.12.

[ Dependencias criticas ]
  [OK]   fastapi
  [OK]   uvicorn
  [OK]   pydantic
  [OK]   pydantic-settings
  [OK]   psycopg (v3)
  [OK]   SQLAlchemy
  [OK]   alembic
  [OK]   celery
  [OK]   redis
  [OK]   cloudscraper
  [OK]   requests
  [OK]   beautifulsoup4
  [OK]   selenium
  [OK]   psutil
  [OK]   python-dotenv
  [OK]   httpx
  [OK]   pywin32

[ Dependencias opcionales ]
  (las marcadas [INFO] no bloquean el arranque)
  [INFO] lxml no instalado — usando html.parser (stdlib)
         Ejecuta fix_lxml.bat para instalar lxml si lo necesitas.
  [OK]   html.parser (stdlib)

[ Configuracion ]
  [OK]   .env cargado — app=BookingScraper Pro v6.0.0 build=54

[ Directorios del proyecto ]
  [OK]   app/
  [OK]   scripts/
  [OK]   tests/
  [OK]   migrations/
  [OK]   data/images/
  [OK]   data/exports/
  [OK]   data/logs/debug/
  [OK]   logs/
  [OK]   backups/

[ Conectividad ]
  [OK]   PostgreSQL localhost:5432/bookingscraper
  [OK]   Redis/Memurai en redis://localhost:6379/0

================================================================
  RESULTADO: Sistema listo para arrancar.
  Ejecuta: start_server.bat / start_celery.bat / start_celery_beat.bat
================================================================

(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>
(.venv) C:\BookingScraper>