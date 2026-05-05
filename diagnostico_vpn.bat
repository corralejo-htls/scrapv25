@echo off
REM diagnostico_vpn.bat - BookingScraper Pro v48
REM
REM FIX-BAT-001: GOTO eliminado de bloque FOR
REM FIX-BAT-002: redis-cli sin pipe (pipe abortaba el script en [3/6])
REM FIX-BAT-003: NordVPN version via archivo temporal
REM FIX-BAT-004: Deteccion _env/env y copia automatica a .env
REM FIX-BAT-005: pg_isready acepta salida en ingles Y espanol
REM              "accepting connections" o "aceptando conexiones"
REM              (pg_isready usa el locale del sistema Windows)
REM FIX-BAT-006: NordVPN version marcada como INFO, no ERROR
REM              nordvpn.exe escribe via WriteConsole() al handle de
REM              consola directamente — ni >, 2>&1, ni archivo temporal
REM              pueden capturarlo. Es una limitacion del ejecutable.
REM FIX-BAT-007: [3/6] Redis — reemplazado redis-cli hardcodeado por
REM              deteccion dinamica de memurai-cli.exe (FIX-MEMURAI-010).
REM              redis-cli no existe en instalaciones Memurai; el comando
REM              devolvía vacío → falso ERROR aunque Memurai estuviera activo.
REM              Ahora usa la misma logica que start_redis.bat e inicio_rapido.bat.
REM
REM Ejecutar desde C:\BookingScraper con el venv activo.

SETLOCAL ENABLEDELAYEDEXPANSION
ECHO ============================================================
ECHO  BookingScraper Pro v48 - Diagnostico Pre-Inicio
ECHO ============================================================
ECHO.

SET "BASE=%~dp0"
SET /A ERRORES=0

REM ── 0. Detectar archivo sin punto ─────────────────────────────────────────
IF NOT EXIST "!BASE!.env" (
    IF EXIST "!BASE!_env" (
        ECHO [0] Copiando _env a .env...
        copy "!BASE!_env" "!BASE!.env" >NUL 2>&1
        IF !ERRORLEVEL! EQU 0 (ECHO     OK - _env copiado a .env
        ) ELSE (ECHO     ERROR - ejecuta: copy _env .env & SET /A ERRORES+=1)
        ECHO.
    ) ELSE IF EXIST "!BASE!env" (
        ECHO [0] Copiando env a .env...
        copy "!BASE!env" "!BASE!.env" >NUL 2>&1
        IF !ERRORLEVEL! EQU 0 (ECHO     OK - env copiado a .env
        ) ELSE (ECHO     ERROR - ejecuta: copy env .env & SET /A ERRORES+=1)
        ECHO.
    )
)

REM ── 1. NordVPN ejecutable ─────────────────────────────────────────────────
ECHO [1/6] NordVPN ejecutable...
SET "NORDVPN_EXE=C:\Program Files\NordVPN\nordvpn.exe"

IF NOT EXIST "!NORDVPN_EXE!" (
    ECHO   ERROR - nordvpn.exe NO encontrado en:
    ECHO          !NORDVPN_EXE!
    ECHO          Instalar desde https://nordvpn.com/download/
    SET /A ERRORES+=1
    GOTO :check_env
)
ECHO   OK - nordvpn.exe encontrado

REM FIX-BAT-006: nordvpn.exe usa WriteConsole() — no capturamos la version.
REM La linea "Current NordVPN version: X.X.X.X" aparece en pantalla
REM pero no en ninguna redireccion (>, 2>&1, archivo temporal).
REM Se mantiene como INFO porque verify_system.py ya confirma el entorno.
ECHO   INFO - version visible en consola al ejecutar: nordvpn --version
ECHO          ^(nordvpn.exe escribe directo al handle de consola Windows^)
ECHO.

REM ── 2. .env ───────────────────────────────────────────────────────────────
:check_env
ECHO [2/6] Verificando .env...
IF NOT EXIST "!BASE!.env" (
    ECHO   ERROR - .env NO existe. Ejecutar: copy _env .env
    SET /A ERRORES+=1
    GOTO :check_redis
)
ECHO   OK - .env encontrado

findstr /i /r "^VPN_ENABLED=true" "!BASE!.env" >NUL 2>&1
IF !ERRORLEVEL! EQU 0 (ECHO   OK - VPN_ENABLED=true) ELSE (
    ECHO   *** ERROR - VPN_ENABLED no es 'true' en .env ***
    SET /A ERRORES+=1
)

SET "HB_LINE="
FOR /F "usebackq tokens=* delims=" %%h IN (`findstr /i /r "^HEADLESS_BROWSER=" "!BASE!.env" 2^>NUL`) DO (
    IF NOT DEFINED HB_LINE SET "HB_LINE=%%h"
)
IF DEFINED HB_LINE (ECHO   OK - !HB_LINE!) ELSE (
    ECHO   *** ERROR - HEADLESS_BROWSER no existe en .env ***
    SET /A ERRORES+=1
)

SET "VRI_LINE="
FOR /F "usebackq tokens=* delims=" %%r IN (`findstr /i /r "^VPN_ROTATION_INTERVAL=" "!BASE!.env" 2^>NUL`) DO (
    IF NOT DEFINED VRI_LINE SET "VRI_LINE=%%r"
)
IF DEFINED VRI_LINE (ECHO   OK - !VRI_LINE!) ELSE (
    ECHO   AVISO - VPN_ROTATION_INTERVAL ausente ^(default 300s^). Recomendado: 50
)

findstr /i /r "^DB_USER=" "!BASE!.env" >NUL 2>&1
IF !ERRORLEVEL! EQU 0 (ECHO   OK - DB_USER configurado) ELSE (
    ECHO   *** ERROR - DB_USER no existe en .env *** & SET /A ERRORES+=1
)
findstr /i /r "^DB_PASSWORD=" "!BASE!.env" >NUL 2>&1
IF !ERRORLEVEL! EQU 0 (ECHO   OK - DB_PASSWORD configurado) ELSE (
    ECHO   *** ERROR - DB_PASSWORD no existe en .env *** & SET /A ERRORES+=1
)
ECHO.

REM ── 3. Redis / Memurai ────────────────────────────────────────────────────
:check_redis
ECHO [3/6] Redis ^(Memurai^)...

REM FIX-BAT-007: deteccion dinamica de memurai-cli.exe (mismo orden que start_redis.bat)
REM   Memurai NO instala redis-cli.exe — usar redis-cli hardcodeado siempre falla.
SET "DIAG_CLI="
IF EXIST "C:\Program Files\Memurai\memurai-cli.exe" SET "DIAG_CLI=C:\Program Files\Memurai\memurai-cli.exe"
IF NOT DEFINED DIAG_CLI IF EXIST "C:\Memurai\memurai-cli.exe" SET "DIAG_CLI=C:\Memurai\memurai-cli.exe"
IF NOT DEFINED DIAG_CLI IF EXIST "C:\Program Files\Memurai\redis-cli.exe" SET "DIAG_CLI=C:\Program Files\Memurai\redis-cli.exe"
IF NOT DEFINED DIAG_CLI IF EXIST "C:\Program Files\Redis\redis-cli.exe" SET "DIAG_CLI=C:\Program Files\Redis\redis-cli.exe"
IF NOT DEFINED DIAG_CLI (
    WHERE memurai-cli >NUL 2>&1
    IF NOT ERRORLEVEL 1 SET "DIAG_CLI=memurai-cli"
)
IF NOT DEFINED DIAG_CLI (
    WHERE redis-cli >NUL 2>&1
    IF NOT ERRORLEVEL 1 SET "DIAG_CLI=redis-cli"
)

IF NOT DEFINED DIAG_CLI (
    ECHO   ERROR - memurai-cli.exe no encontrado en ninguna ruta conocida.
    ECHO          Instala Memurai: https://www.memurai.com/
    SET /A ERRORES+=1
) ELSE (
    SET "REDIS_RESP="
    FOR /F "usebackq delims=" %%p IN (`"!DIAG_CLI!" PING 2^>NUL`) DO (
        IF NOT DEFINED REDIS_RESP SET "REDIS_RESP=%%p"
    )
    IF /I "!REDIS_RESP!"=="PONG" (
        ECHO   OK - Memurai responde PONG ^(cliente: !DIAG_CLI!^)
    ) ELSE IF DEFINED REDIS_RESP (
        ECHO   ERROR - Memurai responde inesperadamente: '!REDIS_RESP!'
        ECHO          Verificar estado de Memurai
        SET /A ERRORES+=1
    ) ELSE (
        ECHO   ERROR - Memurai no responde ^(sin respuesta^)
        ECHO          Memurai no esta corriendo. Ejecutar: start_redis.bat
        SET /A ERRORES+=1
    )
)
ECHO.

REM ── 4. PostgreSQL ─────────────────────────────────────────────────────────
ECHO [4/6] PostgreSQL...

REM FIX-BAT-005: pg_isready devuelve texto segun el locale del SO Windows.
REM   Ingles: "localhost:5432 - accepting connections"
REM   Espanol: "localhost:5432 - aceptando conexiones"
REM Solucion: capturar en archivo temporal y buscar AMBAS cadenas.
SET "PG_TMPFILE=%TEMP%\pg_ready_%RANDOM%.tmp"
pg_isready -h localhost -p 5432 > "!PG_TMPFILE!" 2>&1
SET "PG_RESP="
FOR /F "usebackq tokens=* delims=" %%q IN ("!PG_TMPFILE!") DO (
    IF NOT DEFINED PG_RESP SET "PG_RESP=%%q"
)
IF EXIST "!PG_TMPFILE!" DEL "!PG_TMPFILE!" >NUL 2>&1

SET "PG_OK=0"
REM Buscar "accepting" (ingles) o "aceptando" (espanol)
ECHO !PG_RESP! | findstr /i "accepting aceptando" >NUL 2>&1
IF !ERRORLEVEL! EQU 0 SET "PG_OK=1"

IF "!PG_OK!"=="1" (
    ECHO   OK - PostgreSQL aceptando conexiones en localhost:5432
) ELSE (
    ECHO   ERROR - PostgreSQL no responde correctamente
    IF DEFINED PG_RESP ECHO          Detalle: !PG_RESP!
    ECHO          Verificar servicio: sc query postgresql*
    ECHO          Iniciar:            net start postgresql-x64-16
    SET /A ERRORES+=1
)
ECHO.

REM ── 5. Brave Browser ──────────────────────────────────────────────────────
ECHO [5/6] Brave Browser...
SET "BRAVE_FOUND=0"
SET "BRAVE1=C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
SET "BRAVE2=C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
SET "BRAVE3=%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"

SET "BRAVE_PATH="
IF EXIST "!BRAVE1!" (SET "BRAVE_FOUND=1" & SET "BRAVE_PATH=!BRAVE1!")
IF "!BRAVE_FOUND!"=="0" IF EXIST "!BRAVE2!" (SET "BRAVE_FOUND=1" & SET "BRAVE_PATH=!BRAVE2!")
IF "!BRAVE_FOUND!"=="0" IF EXIST "!BRAVE3!" (SET "BRAVE_FOUND=1" & SET "BRAVE_PATH=!BRAVE3!")

IF "!BRAVE_FOUND!"=="1" (
    ECHO   OK - Brave encontrado:
    ECHO        !BRAVE_PATH!
) ELSE (
    ECHO   ERROR - Brave NO encontrado. Rutas verificadas:
    ECHO          !BRAVE1!
    ECHO          !BRAVE2!
    ECHO          !BRAVE3!
    ECHO          Instalar: https://brave.com/download/
    SET /A ERRORES+=1
)
ECHO.

REM ── 6. IP publica actual ──────────────────────────────────────────────────
ECHO [6/6] IP publica actual ^(sin VPN^)...
SET "CURRENT_IP="
SET "IP_TMPFILE=%TEMP%\myip_%RANDOM%.tmp"
curl -s --max-time 8 https://api.ipify.org > "!IP_TMPFILE!" 2>NUL
FOR /F "usebackq delims=" %%i IN ("!IP_TMPFILE!") DO (
    IF NOT DEFINED CURRENT_IP SET "CURRENT_IP=%%i"
)
IF EXIST "!IP_TMPFILE!" DEL "!IP_TMPFILE!" >NUL 2>&1
IF DEFINED CURRENT_IP (
    ECHO   IP actual: !CURRENT_IP!
    ECHO   Cuando NordVPN conecte, el Worker log debe mostrar IP diferente:
    ECHO     INFO  VPN connected to Spain -- IP: X.X.X.X
) ELSE (
    ECHO   AVISO - no se pudo obtener IP publica
)
ECHO.

REM ── Resumen ───────────────────────────────────────────────────────────────
ECHO ============================================================
IF !ERRORES! EQU 0 (
    ECHO   DIAGNOSTICO OK -- sistema listo para iniciar
    ECHO.
    ECHO   Orden de inicio:
    ECHO     1. start_redis.bat    ^(si Memurai no corre como servicio^)
    ECHO     2. inicio_rapido.bat  ^(Celery + FastAPI^)
    ECHO.
    ECHO   Verificacion SQL ^(5 min despues^):
    ECHO     psql -U postgres -d bookingscraper -c "SELECT event_type, COUNT(*) FROM scraping_logs GROUP BY event_type;"
) ELSE (
    ECHO   ERRORES ENCONTRADOS: !ERRORES!
    ECHO.
    ECHO   Ayuda rapida:
    ECHO     Redis caido     -^>  start_redis.bat
    ECHO     Postgres caido  -^>  net start postgresql-x64-16
    ECHO     .env faltante   -^>  copy _env .env
    ECHO     Brave ausente   -^>  https://brave.com/download/
)
ECHO ============================================================
ECHO.
ENDLOCAL
