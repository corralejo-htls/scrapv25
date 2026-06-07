@echo off
REM show_status.bat — Muestra el estado actual del sistema
SETLOCAL
SET PYTHONPATH=%~dp0

IF EXIST "venv\Scripts\activate.bat" CALL "venv\Scripts\activate.bat"

ECHO ============================================================
ECHO  BookingScraper Pro v48 - Estado del Sistema
ECHO ============================================================
ECHO.

ECHO [API Server]
curl -s http://127.0.0.1:8000/health 2>NUL || ECHO   Servidor no disponible

ECHO.
ECHO [Procesos activos]
tasklist /FI "IMAGENAME eq python.exe" /FO TABLE 2>NUL

ECHO.
ECHO [Puerto 8000]
netstat -ano | findstr ":8000" 2>NUL || ECHO   Puerto 8000 libre

ECHO ============================================================
ENDLOCAL
