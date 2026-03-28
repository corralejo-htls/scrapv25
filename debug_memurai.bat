@echo off
REM debug_memurai.bat — Lanza Memurai con salida en consola (sin logfile)
REM BookingScraper Pro v6.0.0 | Windows 11
REM
REM PROBLEMA: La ventana "BSP - Memurai" esta negra porque memurai.conf
REM   tiene   logfile "C:/BookingScraper/logs/memurai.log"
REM   Memurai escribe todo al archivo — nada aparece en la consola.
REM
REM SOLUCION DE DIAGNOSTICO: pasar --loglevel verbose y --logfile "" por
REM   linea de comandos. En Memurai/Redis, los argumentos de linea de
REM   comandos tienen MAYOR prioridad que el archivo .conf, por lo que
REM   --logfile "" fuerza la salida a consola aunque el conf diga otra cosa.
REM
REM USO: Ejecuta este script. Una nueva ventana mostrara el log de Memurai
REM   en tiempo real. Si hay un error, sera visible. Presiona Ctrl+C para
REM   cerrar Memurai cuando hayas visto el error.
REM
SETLOCAL ENABLEDELAYEDEXPANSION

SET "BASE=%~dp0"
IF "%BASE:~-1%"=="\" SET "BASE=%BASE:~0,-1%"

ECHO ============================================================
ECHO  BookingScraper Pro — DEBUG Memurai (salida en consola)
ECHO  Base: %BASE%
ECHO ============================================================
ECHO.

REM ── Localizar Memurai ─────────────────────────────────────────────────────
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
ECHO [OK] Memurai encontrado: %MEMURAI_EXE%
ECHO.

REM ── Liberar puerto 6379 si hay zombie ────────────────────────────────────
SET "ZOMBIE_PID="
FOR /F "tokens=5" %%z IN ('netstat -ano 2^>NUL ^| findstr ":6379 " ^| findstr "LISTENING"') DO (
    IF NOT DEFINED ZOMBIE_PID SET "ZOMBIE_PID=%%z"
)
IF DEFINED ZOMBIE_PID (
    ECHO [INFO] Liberando puerto 6379 (PID !ZOMBIE_PID!)...
    taskkill /F /PID !ZOMBIE_PID! >NUL 2>&1
    timeout /t 1 /nobreak >NUL
)

REM ── Lanzar Memurai en ESTA ventana (sin start) para ver el output ─────────
ECHO ============================================================
ECHO  Lanzando Memurai con logfile en CONSOLA (modo debug)...
ECHO  El log aparecera aqui. Busca lineas con # o [error].
ECHO  Presiona Ctrl+C para detener.
ECHO ============================================================
ECHO.

REM Estrategia:
REM   --loglevel verbose  → mas detalle
REM   --logfile ""        → fuerza stdout (override del .conf)
REM   --port 6379         → confirmar puerto
REM
REM NOTA: Si el conf tiene 'enable-protected-configs no' (default Memurai),
REM   'dir' es inmutable en runtime pero SI se puede pasar desde el conf.
REM   No se pasa --dir aqui porque viene del .conf.

SET "MEMURAI_CONF=%BASE%\memurai.conf"

IF EXIST "%MEMURAI_CONF%" (
    ECHO   Usando conf: %MEMURAI_CONF%
    ECHO   Override:    --logfile "" --loglevel verbose
    ECHO.
    "%MEMURAI_EXE%" "%MEMURAI_CONF%" --logfile "" --loglevel verbose --port 6379
) ELSE (
    ECHO   [AVISO] memurai.conf no encontrado — usando solo argumentos CLI
    ECHO.
    "%MEMURAI_EXE%" --logfile "" --loglevel verbose --port 6379 --bind 127.0.0.1 --dir "%BASE%\data"
)

ECHO.
ECHO ============================================================
ECHO  Memurai se ha detenido (ver error arriba).
ECHO.
ECHO  Pasos siguientes segun el error:
ECHO.
ECHO   "bind: address already in use"
ECHO     → Un proceso tiene el 6379. Cierra y ejecuta de nuevo.
ECHO.
ECHO   "Permission denied" / "Access is denied"
ECHO     → Permisos NTFS en data\ o logs\. Ejecuta como Administrador.
ECHO.
ECHO   "Invalid argument" / "unknown directive"
ECHO     → Directiva no soportada en memurai.conf.
ECHO       Ejecuta: setup_memurai.bat /genonly
ECHO.
ECHO   "license" / "trial expired"
ECHO     → La licencia Developer de Memurai expiro (90 dias).
ECHO       Reinstala Memurai: https://www.memurai.com/
ECHO.
ECHO   "dump.rdb" / "rdb checksum"  
ECHO     → Archivo RDB corrupto. Ejecuta: del "%BASE%\data\dump.rdb"
ECHO.
ECHO ============================================================
PAUSE
ENDLOCAL
