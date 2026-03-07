@echo off
REM BookingScraper Pro v6.0 - Start FastAPI Server
REM Platform: Windows 11
title BookingScraper Pro - Web Server
cd /d "%~dp0"
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found. Run setup_env.bat first.
    pause & exit /b 1
)
call .venv\Scripts\activate.bat
echo Starting BookingScraper Pro server...
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --loop asyncio
pause
