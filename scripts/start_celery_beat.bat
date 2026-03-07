@echo off
REM BookingScraper Pro v6.0 - Start Celery Beat Scheduler
title BookingScraper Pro - Celery Beat
cd /d "%~dp0"
call .venv\Scripts\activate.bat
echo Starting Celery Beat scheduler...
celery -A app.celery_app beat --loglevel=info --logfile=logs\celery_beat.log
pause
