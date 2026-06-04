@echo off
REM restart_all.bat — Reinicia todos los servicios
REM BookingScraper Pro v48 | Windows 11
SETLOCAL
ECHO Reiniciando todos los servicios...
CALL stop_server.bat
CALL stop_celery.bat
timeout /t 3 /nobreak >NUL
ECHO.
ECHO Iniciando servicios...
ECHO   Abre 3 terminales y ejecuta:
ECHO   Terminal 1: start_server.bat
ECHO   Terminal 2: start_celery.bat
ECHO   Terminal 3: start_celery_beat.bat
ENDLOCAL
