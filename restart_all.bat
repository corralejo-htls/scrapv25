@echo off
REM BookingScraper Pro v6.0 - Restart All Services
title BookingScraper Pro - Restart All
cd /d "%~dp0"
echo Stopping services...
call stop_server.bat
call stop_celery.bat
echo.
echo Starting services...
start "BookingScraper - Web Server" start_server.bat
timeout /t 3 /nobreak
start "BookingScraper - Celery Worker" start_celery.bat
echo.
echo All services restarted.
pause
