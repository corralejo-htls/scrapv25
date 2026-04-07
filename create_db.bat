@echo off
REM create_db.bat - Crea la base de datos y aplica el esquema completo
REM BookingScraper Pro v6.0.0 Build 82 | Windows 11
REM
REM BUG-SCRIPT-001 (Build 63-fix): Referencia corregida de
REM   install_clean_v49.sql  ->  schema_v60_complete.sql
REM BUG-SCRIPT-002 (Build 82-fix): Referencia actualizada de
REM   schema_v60_complete.sql  ->  schema_v77_complete.sql
REM   El script referenciaba un fichero SQL obsoleto (v60) mientras el sistema
REM   opera con schema_v77_complete.sql (22 tablas, Build 82 columns).
REM   Consecuencia: create_db.bat aplicaba un schema sin las columnas
REM   accommodation_type, adults, children, images, info, service_category,
REM   category_code ni la tabla hotels_individual_reviews.
REM
REM IMPORTANTE: Este script ELIMINA completamente la base de datos existente
REM y la recrea desde cero con schema_v77_complete.sql.
REM Ningun dato es preservado (comportamiento by design).
SETLOCAL

ECHO ============================================================
ECHO  BookingScraper Pro v6.0.0 Build 82 - Creacion de Base de Datos
ECHO ============================================================
ECHO.
ECHO  ATENCION: Este proceso ELIMINA la base de datos existente.
ECHO  Todos los datos seran borrados. Esto es por diseno.
ECHO.

SET /P PGUSER=Usuario PostgreSQL (por defecto: postgres): 
IF "%PGUSER%"=="" SET PGUSER=postgres

SET /P PGHOST=Host PostgreSQL (por defecto: localhost): 
IF "%PGHOST%"=="" SET PGHOST=localhost

ECHO.
ECHO Eliminando base de datos existente (si existe)...
psql -U %PGUSER% -h %PGHOST% -c "DROP DATABASE IF EXISTS bookingscraper;" 2>NUL
IF ERRORLEVEL 1 ECHO   (No se pudo eliminar - puede que no existiera)

ECHO Creando base de datos bookingscraper...
psql -U %PGUSER% -h %PGHOST% -c "CREATE DATABASE bookingscraper ENCODING UTF8;"
IF ERRORLEVEL 1 (
    ECHO ERROR: No se pudo crear la base de datos.
    PAUSE & EXIT /B 1
)

ECHO Aplicando esquema completo (schema_v77_complete.sql)...
psql -U %PGUSER% -h %PGHOST% -d bookingscraper -f schema_v77_complete.sql
IF ERRORLEVEL 1 (
    ECHO ERROR: Fallo al aplicar el esquema.
    PAUSE & EXIT /B 1
)

ECHO.
ECHO Base de datos creada correctamente con schema v77 (Build 82).
ECHO  Tablas creadas : 22
ECHO  Incluye        : accommodation_type, service_category, category_code,
ECHO                   hotels_individual_reviews, adults/children/images/info
ECHO.
ECHO Verifica la instalacion con: verify_system.bat
ENDLOCAL
