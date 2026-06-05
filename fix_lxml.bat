@echo off
REM fix_lxml.bat — Soluciona el error de instalación de lxml en Python 3.14
REM BookingScraper Pro v48 | Windows 11
REM ============================================================================
SETLOCAL

ECHO ============================================================
ECHO  BookingScraper Pro v48 - Solucion para lxml en Python 3.14
ECHO ============================================================
ECHO.

IF EXIST ".venv\Scripts\activate.bat" (
    CALL ".venv\Scripts\activate.bat"
) ELSE IF EXIST "venv\Scripts\activate.bat" (
    CALL "venv\Scripts\activate.bat"
)

ECHO Detectando version de Python...
python --version
ECHO.

ECHO Intentando instalar lxml con wheel binario precompilado...
pip install lxml --prefer-binary --only-binary=lxml 2>NUL
IF NOT ERRORLEVEL 1 (
    ECHO [OK] lxml instalado correctamente con wheel binario.
    GOTO :END
)

ECHO.
ECHO [INFO] No hay wheel binario de lxml para tu version de Python.
ECHO.
ECHO Esto ocurre con Python 3.14 (pre-release) porque lxml aun no
ECHO ha publicado wheels compilados para esta version.
ECHO.
ECHO ============================================================
ECHO  OPCIONES (elige una):
ECHO ============================================================
ECHO.
ECHO  OPCION 1 (RECOMENDADA): Usar sin lxml
ECHO  ----------------------------------------
ECHO  BookingScraper funciona completamente sin lxml.
ECHO  El extractor usa html.parser (incluido en Python) automaticamente.
ECHO  No se necesita hacer nada mas.
ECHO.
ECHO  OPCION 2: Instalar Visual C++ Build Tools (para compilar lxml)
ECHO  ---------------------------------------------------------------
ECHO  Descarga e instala desde:
ECHO  https://visualstudio.microsoft.com/visual-cpp-build-tools/
ECHO  Selecciona: "C++ build tools" (workload)
ECHO  Luego ejecuta: pip install -r requirements-optional.txt
ECHO.
ECHO  OPCION 3: Usar Python 3.11 o 3.12 (recomendado para produccion)
ECHO  -----------------------------------------------------------------
ECHO  Python 3.14 es pre-release. Para produccion se recomienda 3.11/3.12.
ECHO  Descarga: https://www.python.org/downloads/windows/
ECHO  Luego: python -m venv .venv ^& pip install -r requirements.txt
ECHO.

:END
ECHO ============================================================
ECHO  Verificando instalacion sin lxml...
ECHO ============================================================
python -c "from bs4 import BeautifulSoup; print('[OK] beautifulsoup4 OK')"
python -c "from bs4 import BeautifulSoup; s=BeautifulSoup('<p>test</p>','html.parser'); print('[OK] html.parser funciona correctamente')"
ECHO.
ECHO  El sistema esta listo para funcionar sin lxml.
ECHO ============================================================
ENDLOCAL
