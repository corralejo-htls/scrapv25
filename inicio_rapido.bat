@echo off
REM inicio_rapido.bat -- Arranca BookingScraper Pro v6.0.0 completo
REM Activa el entorno virtual y abre 3 terminales independientes:
REM   Terminal 1 -- API FastAPI  (http://127.0.0.1:8000)
REM   Terminal 2 -- Celery Worker
REM   Terminal 3 -- Celery Beat
REM BookingScraper Pro v6.0.0 | Windows 11
REM Ejecutar desde C:\BookingScraper (sin .venv activo)
REM
REM FIX-MEMURAI-008: rutas absolutas via %~dp0, independiente del PATH.
REM FIX-MEMURAI-009: Memurai lanzado con "start" directo sin cmd /k.
REM                  cmd /k bloquea el proceso padre durante el polling PONG.
REM FIX-MEMURAI-010: cliente correcto es memurai-cli.exe (no redis-cli.exe).
REM                  Deteccion dinamica con fallback a multiples rutas.
REM FIX-START-001:   Reemplazado TCP check (PowerShell TcpClient) por PONG
REM                  real via memurai-cli. TCP abierto != Memurai operativo.
REM FIX-START-002:   Auto-arranque de Memurai si no responde PONG, con
REM                  liberacion de puerto zombie y polling hasta 25s.
REM                  Version anterior (v48) solo mostraba AVISO y continuaba,
REM                  lo que causaba fallo de Celery al conectar con Redis.
SETLOCAL ENABLEDELAYEDEXPANSION

SET "BASE=%~dp0"
IF "%BASE:~-1%"=="\" SET "BASE=%BASE:~0,-1%"
SET PYTHONPATH=%BASE%
SET PYTHONUNBUFFERED=1

ECHO ============================================================
ECHO  BookingScraper Pro v6.0.0 - Inicio Rapido
ECHO ============================================================
ECHO.

REM -- 0. Localizar memurai-cli (FIX-MEMURAI-010) ---------------------------
SET "REDIS_CLI="
IF EXIST "C:\Program Files\Memurai\memurai-cli.exe" SET "REDIS_CLI=C:\Program Files\Memurai\memurai-cli.exe"
IF NOT DEFINED REDIS_CLI IF EXIST "C:\Memurai\memurai-cli.exe" SET "REDIS_CLI=C:\Memurai\memurai-cli.exe"
IF NOT DEFINED REDIS_CLI IF EXIST "C:\Program Files\Memurai\redis-cli.exe" SET "REDIS_CLI=C:\Program Files\Memurai\redis-cli.exe"
IF NOT DEFINED REDIS_CLI IF EXIST "C:\Program Files\Redis\redis-cli.exe" SET "REDIS_CLI=C:\Program Files\Redis\redis-cli.exe"
IF NOT DEFINED REDIS_CLI (
    WHERE memurai-cli >NUL 2>&1
    IF NOT ERRORLEVEL 1 SET "REDIS_CLI=memurai-cli"
)
IF NOT DEFINED REDIS_CLI (
    WHERE redis-cli >NUL 2>&1
    IF NOT ERRORLEVEL 1 SET "REDIS_CLI=redis-cli"
)
IF NOT DEFINED REDIS_CLI (
    ECHO [ERROR] memurai-cli.exe no encontrado en ninguna ruta conocida.
    ECHO         Ruta esperada: C:\Program Files\Memurai\memurai-cli.exe
    PAUSE & EXIT /B 1
)
ECHO [0/5] cliente Memurai: %REDIS_CLI%

REM -- 1. Entorno virtual ---------------------------------------------------
SET "VENV_ACTIVATE="
IF EXIST "%BASE%\.venv\Scripts\activate.bat" (
    SET "VENV_ACTIVATE=%BASE%\.venv\Scripts\activate.bat"
    ECHO [1/5] Entorno virtual detectado: .venv
) ELSE IF EXIST "%BASE%\venv\Scripts\activate.bat" (
    SET "VENV_ACTIVATE=%BASE%\venv\Scripts\activate.bat"
    ECHO [1/5] Entorno virtual detectado: venv
) ELSE (
    ECHO [ERROR] No se encontro entorno virtual.
    ECHO         Ejecuta primero: python -m venv .venv
    ECHO         Luego:           .venv\Scripts\activate.bat
    ECHO         Y despues:       pip install -r requirements.txt
    PAUSE & EXIT /B 1
)

REM -- 2. .env --------------------------------------------------------------
IF NOT EXIST "%BASE%\.env" (
    ECHO [ERROR] Archivo .env no encontrado.
    ECHO         Ejecuta: copy _env .env
    ECHO         Y configura DB_USER y DB_PASSWORD en .env
    PAUSE & EXIT /B 1
)
ECHO [2/5] .env encontrado OK

REM -- 3. Memurai / Redis (FIX-START-001 + FIX-START-002) ------------------
ECHO [3/5] Verificando Memurai/Redis...
SET "REDIS_OK=0"
SET "REDIS_RESP="
FOR /F "usebackq delims=" %%p IN (`"%REDIS_CLI%" PING 2^>NUL`) DO (
    IF NOT DEFINED REDIS_RESP SET "REDIS_RESP=%%p"
)
IF /I "!REDIS_RESP!"=="PONG" (
    ECHO   OK - Memurai ya activo ^(PONG recibido^).
    SET "REDIS_OK=1"
)

IF "!REDIS_OK!"=="0" (
    SET "MEMURAI_EXE="
    IF EXIST "C:\Program Files\Memurai\memurai.exe" SET "MEMURAI_EXE=C:\Program Files\Memurai\memurai.exe"
    IF NOT DEFINED MEMURAI_EXE IF EXIST "C:\Memurai\memurai.exe" SET "MEMURAI_EXE=C:\Memurai\memurai.exe"

    SET "MEMURAI_CONF=%BASE%\memurai.conf"

    IF DEFINED MEMURAI_EXE (
        ECHO   INFO - Verificando puerto 6379...
        SET "ZOMBIE_PID="
        FOR /F "tokens=5" %%z IN ('netstat -ano 2^>NUL ^| findstr ":6379 " ^| findstr "LISTENING"') DO (
            IF NOT DEFINED ZOMBIE_PID SET "ZOMBIE_PID=%%z"
        )
        IF DEFINED ZOMBIE_PID (
            ECHO   INFO - Liberando PID !ZOMBIE_PID! en puerto 6379...
            taskkill /F /PID !ZOMBIE_PID! >NUL 2>&1
            timeout /t 1 /nobreak >NUL
        ) ELSE (
            ECHO   INFO - Puerto 6379 libre.
        )

        IF NOT EXIST "%BASE%\logs" MKDIR "%BASE%\logs"

        IF EXIST "!MEMURAI_CONF!" (
            ECHO   INFO - Lanzando Memurai con conf: !MEMURAI_CONF!
            start "BSP - Memurai" "!MEMURAI_EXE!" "!MEMURAI_CONF!"
        ) ELSE (
            ECHO   AVISO - memurai.conf no encontrado -- config por defecto.
            start "BSP - Memurai" "!MEMURAI_EXE!"
        )

        ECHO   INFO - Esperando PONG ^(max 25s^)...
        SET /A WAIT=0
        :wait_redis
        timeout /t 1 /nobreak >NUL
        SET "REDIS_RESP2="
        FOR /F "usebackq delims=" %%p IN (`"%REDIS_CLI%" PING 2^>NUL`) DO (
            IF NOT DEFINED REDIS_RESP2 SET "REDIS_RESP2=%%p"
        )
        IF /I "!REDIS_RESP2!"=="PONG" (
            ECHO   OK - Memurai activo y responde PONG ^(!WAIT!s^).
            SET "REDIS_OK=1"
            GOTO :redis_done
        )
        SET /A WAIT+=1
        IF !WAIT! LSS 25 GOTO :wait_redis

        ECHO   ERROR - Memurai no responde tras 25s.
        SET "LOGFILE=%BASE%\logs\memurai.log"
        IF EXIST "!LOGFILE!" (
            ECHO   Ultimas lineas del log:
            powershell -NoProfile -Command "Get-Content '!LOGFILE!' -Tail 10" 2>NUL
        )
        ECHO   Ejecuta manualmente: start_redis.bat
        PAUSE & EXIT /B 1
    ) ELSE (
        ECHO   ERROR - memurai.exe no encontrado.
        ECHO          Instala Memurai: https://www.memurai.com/
        PAUSE & EXIT /B 1
    )
)

:redis_done

REM -- 4. PostgreSQL --------------------------------------------------------
ECHO [4/5] Verificando PostgreSQL...
SET "PG_TMPFILE=%TEMP%\pg_ready_%RANDOM%.tmp"
pg_isready -h localhost -p 5432 > "!PG_TMPFILE!" 2>&1
SET "PG_RESP="
FOR /F "usebackq tokens=* delims=" %%q IN ("!PG_TMPFILE!") DO (
    IF NOT DEFINED PG_RESP SET "PG_RESP=%%q"
)
IF EXIST "!PG_TMPFILE!" DEL "!PG_TMPFILE!" >NUL 2>&1
ECHO !PG_RESP! | findstr /i "accepting aceptando" >NUL 2>&1
IF !ERRORLEVEL! NEQ 0 (
    ECHO   ERROR - PostgreSQL no responde en localhost:5432
    ECHO          Inicia el servicio: net start postgresql-x64-16
    PAUSE & EXIT /B 1
)
ECHO   OK - PostgreSQL activo en localhost:5432

REM -- 5. Lanzar servicios -------------------------------------------------
ECHO [5/5] Abriendo terminales de servicio...
ECHO.

ECHO   [API]    http://127.0.0.1:8000
start "BSP - API Server" cmd /k "cd /d "%BASE%" && call "%VENV_ACTIVATE%" && SET PYTHONPATH=%BASE% && SET PYTHONUNBUFFERED=1 && ECHO. && ECHO ===  BookingScraper API  === && ECHO. && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1 --log-level info --access-log"

timeout /t 2 /nobreak >NUL

ECHO   [Celery] Worker iniciando...
start "BSP - Celery Worker" cmd /k "cd /d "%BASE%" && call "%VENV_ACTIVATE%" && SET PYTHONPATH=%BASE% && SET PYTHONUNBUFFERED=1 && SET FORKED_BY_MULTIPROCESSING=1 && ECHO. && ECHO ===  BookingScraper Celery Worker  === && ECHO. && python -m celery -A app.celery_app worker --loglevel=info --pool=solo --queues=default,maintenance,monitoring --hostname=worker@%%COMPUTERNAME%%"

timeout /t 2 /nobreak >NUL

ECHO   [Beat]   Scheduler iniciando...
start "BSP - Celery Beat" cmd /k "cd /d "%BASE%" && call "%VENV_ACTIVATE%" && SET PYTHONPATH=%BASE% && SET PYTHONUNBUFFERED=1 && ECHO. && ECHO ===  BookingScraper Celery Beat  === && ECHO. && python -m celery -A app.celery_app beat --loglevel=info --scheduler celery.beat.PersistentScheduler --schedule celerybeat-schedule.db"

ECHO.
ECHO ============================================================
ECHO  Sistema arrancando en terminales independientes.
ECHO.
ECHO  API:     http://127.0.0.1:8000
ECHO  Docs:    http://127.0.0.1:8000/docs
ECHO  Swagger: http://127.0.0.1:8000/redoc
ECHO.
ECHO  Para detener: stop_server.bat  y  stop_celery.bat
ECHO ============================================================
ECHO.
ECHO  Esta ventana puede cerrarse.
ECHO ============================================================

ENDLOCAL
