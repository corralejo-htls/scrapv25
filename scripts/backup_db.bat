@echo off
REM BookingScraper Pro v6.0 - Backup PostgreSQL Database
title BookingScraper Pro - Backup DB
cd /d "%~dp0"
set BACKUP_DIR=C:\BookingScraper\backups
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
set TIMESTAMP=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_FILE=%BACKUP_DIR%\bookingscraper_%TIMESTAMP%.dump
set /p DB_USER="Enter PostgreSQL username (default: bookingscraper_app): "
if "%DB_USER%"=="" set DB_USER=bookingscraper_app
set /p DB_NAME="Enter database name (default: bookingscraper): "
if "%DB_NAME%"=="" set DB_NAME=bookingscraper
echo Creating backup: %BACKUP_FILE%
pg_dump -U %DB_USER% -d %DB_NAME% -Fc -f "%BACKUP_FILE%"
if %errorlevel%==0 (
    echo Backup created: %BACKUP_FILE%
) else (
    echo ERROR: Backup failed.
)
pause
