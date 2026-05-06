@echo off
REM backup_db.bat — Crea un backup de la base de datos PostgreSQL
REM Los backups se guardan en backups\
SETLOCAL

SET TIMESTAMP=%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
SET TIMESTAMP=%TIMESTAMP: =0%
SET BACKUP_FILE=backups\bookingscraper_%TIMESTAMP%.sql

IF NOT EXIST "backups" MKDIR backups

ECHO Creando backup en %BACKUP_FILE%...
pg_dump -U bookingscraper_user -h localhost bookingscraper > "%BACKUP_FILE%"
IF ERRORLEVEL 1 (
    ECHO ERROR: Fallo al crear el backup.
    PAUSE & EXIT /B 1
)

ECHO Backup creado: %BACKUP_FILE%
ENDLOCAL
