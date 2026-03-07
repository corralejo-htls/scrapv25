@echo off
REM BookingScraper Pro v6.0 - Start Celery Worker
REM Windows: --pool=threads is REQUIRED (no fork/gevent support)
title BookingScraper Pro - Celery Worker
cd /d "%~dp0"
call .venv\Scripts\activate.bat
echo Starting Celery worker (pool=threads)...
celery -A app.celery_app worker --pool=threads --concurrency=4 --loglevel=info --logfile=logs\celery.log
pause
