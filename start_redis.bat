@echo off
REM BookingScraper Pro v6.0 - Start Memurai (Redis for Windows)
REM Memurai is the recommended Redis-compatible server for Windows 11
REM Download: https://www.memurai.com/
title BookingScraper Pro - Memurai/Redis
sc start Memurai
if %errorlevel%==0 (
    echo Memurai service started.
) else (
    echo Trying to start Redis manually...
    where redis-server >nul 2>&1
    if %errorlevel%==0 (
        redis-server
    ) else (
        echo ERROR: Neither Memurai nor redis-server found.
        echo Install Memurai from https://www.memurai.com/
    )
)
pause
