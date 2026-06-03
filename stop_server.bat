@echo off
REM stop_server.bat — Detiene el servidor FastAPI
SETLOCAL
ECHO Deteniendo servidor FastAPI...
FOR /F "tokens=5" %%a IN ('netstat -aon ^| findstr ":8000"') DO (
    taskkill /PID %%a /F >NUL 2>&1
)
ECHO Servidor detenido.
ENDLOCAL
