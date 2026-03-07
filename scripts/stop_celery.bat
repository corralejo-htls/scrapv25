@echo off
REM BookingScraper Pro v6.0 - Stop Celery Worker
title BookingScraper Pro - Stop Celery
echo Stopping Celery workers...
taskkill /F /IM "celery.exe" 2>nul
taskkill /F /FI "WINDOWTITLE eq BookingScraper Pro - Celery Worker" 2>nul
echo Done.
pause
