@echo off
REM setup_memurai.bat — Regenera memurai.conf y verifica Memurai
REM BookingScraper Pro v6.0.0 | Windows 11
REM
REM FIX-MEMURAI-005: genera memurai.conf con Python (pathlib) en lugar de sed.
REM   La causa raíz del fallo anterior era que sed producía dobles backslashes:
REM     logfile C:\\\\BookingScraper\\\\logs\\\\memurai.log
REM   Memurai no podía abrir el archivo de log y abortaba silenciosamente.
REM
REM FIX-MEMURAI-006: usa %~dp0 (ruta absoluta del .bat) como directorio base.
REM   Al lanzar via cmd /k, el directorio de trabajo puede ser C:\Windows\System32.
REM   %~dp0 siempre apunta al directorio REAL del script, sin importar desde dónde
REM   se ejecute.
REM
REM Uso:
REM   Doble clic  — genera conf y arranca Memurai
REM   /genonly    — solo regenera memurai.conf, no arranca Memurai
REM
SETLOCAL ENABLEDELAYEDEXPANSION

REM ── Ruta base ABSOLUTA del proyecto (FIX-MEMURAI-006) ─────────────────────
SET "BASE=%~dp0"
REM Quitar la barra final que agrega %~dp0 (C:\BookingScraper\ → C:\BookingScraper)
IF "%BASE:~-1%"=="\" SET "BASE=%BASE:~0,-1%"

ECHO ============================================================
ECHO  BookingScraper Pro — Setup Memurai
ECHO  Base: %BASE%
ECHO ============================================================
ECHO.

REM ── 1. Localizar Python del venv ──────────────────────────────────────────
SET "PYTHON_EXE="
IF EXIST "%BASE%\.venv\Scripts\python.exe" (
    SET "PYTHON_EXE=%BASE%\.venv\Scripts\python.exe"
) ELSE IF EXIST "%BASE%\venv\Scripts\python.exe" (
    SET "PYTHON_EXE=%BASE%\venv\Scripts\python.exe"
) ELSE (
    WHERE python >NUL 2>&1
    IF NOT ERRORLEVEL 1 SET "PYTHON_EXE=python"
)

IF NOT DEFINED PYTHON_EXE (
    ECHO [ERROR] Python no encontrado. Activa el entorno virtual o instala Python.
    PAUSE & EXIT /B 1
)
ECHO [1/3] Python: %PYTHON_EXE%

REM ── 2. Generar memurai.conf ────────────────────────────────────────────────
SET "SCRIPT=%BASE%\scripts\gen_memurai_conf.py"
IF NOT EXIST "%SCRIPT%" (
    ECHO [ERROR] Script no encontrado: %SCRIPT%
    ECHO         Verifica que gen_memurai_conf.py esta en %BASE%\scripts\
    PAUSE & EXIT /B 1
)

ECHO [2/3] Generando memurai.conf...
"%PYTHON_EXE%" "%SCRIPT%" --base "%BASE%" --output "%BASE%\memurai.conf"
IF ERRORLEVEL 1 (
    ECHO [ERROR] Fallo al generar memurai.conf
    PAUSE & EXIT /B 1
)
ECHO.

REM ── Modo solo generación (/genonly) ───────────────────────────────────────
IF /I "%~1"=="/genonly" (
    ECHO [OK] memurai.conf regenerado. Listo.
    GOTO :END
)

REM ── 3. Verificar si Memurai ya responde ───────────────────────────────────
ECHO [3/3] Verificando Memurai en puerto 6379...
SET "RESP="
FOR /F "usebackq delims=" %%p IN (`redis-cli PING 2^>NUL`) DO (
    IF NOT DEFINED RESP SET "RESP=%%p"
)
IF /I "!RESP!"=="PONG" (
    ECHO [OK] Memurai ya activo ^(PONG recibido^). No se relanza.
    GOTO :END
)

REM ── 4. Liberar puerto zombie si lo hay ────────────────────────────────────
SET "ZOMBIE_PID="
FOR /F "tokens=5" %%z IN ('netstat -ano 2^>NUL ^| findstr ":6379 " ^| findstr "LISTENING"') DO (
    IF NOT DEFINED ZOMBIE_PID SET "ZOMBIE_PID=%%z"
)
IF DEFINED ZOMBIE_PID (
    ECHO [INFO] Puerto 6379 ocupado por PID !ZOMBIE_PID! sin responder PING. Liberando...
    taskkill /F /PID !ZOMBIE_PID! >NUL 2>&1
    timeout /t 1 /nobreak >NUL
)

REM ── 5. Localizar Memurai ──────────────────────────────────────────────────
SET "MEMURAI_EXE="
IF EXIST "C:\Program Files\Memurai\memurai.exe" (
    SET "MEMURAI_EXE=C:\Program Files\Memurai\memurai.exe"
) ELSE IF EXIST "C:\Memurai\memurai.exe" (
    SET "MEMURAI_EXE=C:\Memurai\memurai.exe"
)

IF NOT DEFINED MEMURAI_EXE (
    ECHO [ERROR] Memurai no encontrado.
    ECHO         Descarga: https://www.memurai.com/
    PAUSE & EXIT /B 1
)

REM ── 6. Lanzar Memurai con la conf correcta ────────────────────────────────
SET "MEMURAI_CONF=%BASE%\memurai.conf"
ECHO [INFO] Lanzando Memurai...
ECHO        EXE : %MEMURAI_EXE%
ECHO        CONF: %MEMURAI_CONF%
ECHO.

REM FIX-MEMURAI-004: dobles comillas externas para rutas con espacios en cmd /k
start "BSP - Memurai" cmd /k ""%MEMURAI_EXE%" "%MEMURAI_CONF%""

REM ── 7. Esperar PONG hasta 25 s ────────────────────────────────────────────
SET /A WAIT=0
:wait_pong
timeout /t 1 /nobreak >NUL
SET "RESP2="
FOR /F "usebackq delims=" %%p IN (`redis-cli PING 2^>NUL`) DO (
    IF NOT DEFINED RESP2 SET "RESP2=%%p"
)
IF /I "!RESP2!"=="PONG" (
    ECHO [OK] Memurai activo y responde PONG.
    GOTO :END
)
SET /A WAIT+=1
IF !WAIT! LSS 25 GOTO :wait_pong

ECHO.
ECHO [ERROR] Memurai no responde tras 25 segundos.
ECHO         Abre la ventana "BSP - Memurai" para ver el error.
ECHO.
ECHO  Causas comunes:
ECHO   - memurai.conf tiene ruta incorrecta en 'logfile'
ECHO   - El directorio de logs no existe ^(se crea automaticamente^)
ECHO   - Puerto 6379 bloqueado por firewall
ECHO.
PAUSE
EXIT /B 1

:END
ENDLOCAL
