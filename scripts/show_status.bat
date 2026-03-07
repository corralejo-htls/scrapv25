@echo off
REM BookingScraper Pro v6.0 - Show System Status
title BookingScraper Pro - Status
cd /d "%~dp0"
call .venv\Scripts\activate.bat
echo === BookingScraper Pro v6.0 Status ===
echo.
echo --- Port 8000 (API Server) ---
netstat -ano | findstr ":8000" || echo   Not running
echo.
echo --- Celery processes ---
tasklist | findstr "celery" || echo   Not running
echo.
echo --- PostgreSQL service ---
sc query postgresql-x64-16 2>nul || sc query postgresql 2>nul || echo   Check PostgreSQL service name
echo.
echo --- Memurai/Redis service ---
sc query Memurai 2>nul || echo   Memurai not installed
echo.
echo --- Health check ---
curl -s http://127.0.0.1:8000/health 2>nul || echo   API not responding
echo.
pause
