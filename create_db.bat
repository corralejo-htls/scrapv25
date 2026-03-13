@echo off
REM create_db.bat — Crea la base de datos y aplica el esquema completo
REM BookingScraper Pro v49 | Windows 11
SETLOCAL

ECHO ============================================================
ECHO  BookingScraper Pro v49 - Creacion de Base de Datos
ECHO ============================================================
ECHO.

SET /P PGUSER=Usuario PostgreSQL (por defecto: postgres): 
IF "%PGUSER%"=="" SET PGUSER=postgres

SET /P PGHOST=Host PostgreSQL (por defecto: localhost): 
IF "%PGHOST%"=="" SET PGHOST=localhost

ECHO.
ECHO Creando base de datos 'bookingscraper'...
psql -U %PGUSER% -h %PGHOST% -c "CREATE DATABASE bookingscraper ENCODING 'UTF8';" 2>NUL
IF ERRORLEVEL 1 ECHO   (La base de datos puede ya existir - continuando...)

ECHO Aplicando esquema completo (install_clean_v49.sql)...
psql -U %PGUSER% -h %PGHOST% -d bookingscraper -f install_clean_v49.sql
IF ERRORLEVEL 1 (
    ECHO ERROR: Fallo al aplicar el esquema.
    PAUSE & EXIT /B 1
)

ECHO.
ECHO Base de datos creada correctamente.
ECHO Verifica la instalacion con: verify_system.bat
ENDLOCAL
