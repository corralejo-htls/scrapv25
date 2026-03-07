@echo off
REM BookingScraper Pro v6.0 - Stop FastAPI Server
title BookingScraper Pro - Stop Server
echo Stopping BookingScraper Pro server (port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 "') do (
    echo Killing PID %%a
    taskkill /PID %%a /F
)
echo Done.
pause
