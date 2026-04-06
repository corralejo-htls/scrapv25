"""
BookingScraper Pro v6.0.0 build 68
Platform: Windows 11 + Python 3.14.x

Cambios build 68:
  VPN-PROACTIVE      : scraper_service.dispatch_batch() — rotacion VPN
                       proactiva al inicio de cada batch.
                       CAUSA RAIZ: NordVPNManager se recrea en cada tarea
                       con _last_rotation=0. should_rotate() solo se
                       comprobaba en rutas de fallo — si todos los hoteles
                       tienen exito la IP nunca cambia a pesar de
                       VPN_ROTATION_INTERVAL=50.
                       FIX: bloque proactivo ejecutado antes de despachar
                       URLs. should_rotate() siempre True al inicio del
                       batch (monotonic() - 0 >> 50). VPN rota en cada
                       batch independientemente de exito o fallo.

Cambios build 67:
  BUG-SCRAPER-001-FIX : scraper.py — driver.page_source colgaba 30+ minutos
                         en hoteles con Booking.com anti-bot challenge page
                         ("Max challenge attempts exceeded").
                         Causa raiz: esa cadena no estaba en _BLOCK_INDICATORS,
                         el codigo pasaba al bloque "partial load" y llamaba
                         driver.page_source que espera readyState=complete
                         indefinidamente (JS del challenge nunca termina).
                         Tres cambios:
                           1. _BLOCK_INDICATORS ampliado con 4 nuevas cadenas
                              de Booking.com anti-bot.
                           2. window.stop() antes de page_low check.
                           3. window.stop() antes de html = page_source.
                         Confirmado en log: Pink Sands Club lang=it colgado
                         22:15:25 -> 22:47:11 = 31min 46s (Build 66).
                         Con este fix: deteccion inmediata y reinit_driver().

  COSMETIC-001         : verify_system.py — cabecera "Build 63-fix" corregida.
                         Ahora lee BUILD_VERSION dinamicamente de app.__init__.

Cambios build 66:
  BUG-MAIN-001-FIX : main.py — HotelAmenity no eliminada en build 65.
                     ImportError al arrancar: cannot import name 'HotelAmenity'.
                     Tres cambios en main.py:
                       1. HotelAmenity eliminada del bloque import.
                       2. Bloque query amenity_rows eliminado del endpoint /hotels/{id}.
                       3. Clave "amenities" eliminada del dict de respuesta.
                     Comentarios residuales en extractor.py también limpiados.

Cambios build 65:
  CLEANUP-AMENITIES : hotels_amenities eliminada del sistema completo.
                      La tabla nunca produjo datos en producción (0 filas en todos
                      los ciclos). hotels_popular_services cubre el caso de uso.
                      Archivos modificados:
                        - schema_v60_complete.sql : tabla, índices, comentarios y
                          subquery en v_hotels_full eliminados. Conteo esperado
                          de validación: 17 -> 16 tablas.
                        - app/models.py           : clase HotelAmenity eliminada.
                        - app/extractor.py        : clave 'amenities' y método
                          _extract_amenities() eliminados de extract_all().
                        - app/scraper_service.py  : llamada y método
                          _upsert_hotel_amenities() eliminados.

Cambios build 64:
  BUG-DATA-001-FIX : extractor._extract_amenities() — eliminado Fallback 1
                     (property-most-popular-facilities-wrapper).
                     Causa raíz: ese DOM es la fuente EXCLUSIVA de
                     _extract_popular_services() (STRUCT-008). Al tenerlo
                     también como fallback en _extract_amenities(), ambas
                     funciones retornaban datos idénticos cuando la sección
                     completa (property-section--facilities) no estaba presente.
                     Confirmado: 78/78 pares url×idioma con conteo idéntico.

  BUG-PERF-001-FIX : scraper._fetch_with_selenium() — tres cambios:
    1. SELENIUM_CONTENT_WAIT_TIMEOUT_S (nuevo campo config, default 10 s):
       WebDriverWait por selector cambiado de SCRAPER_REQUEST_TIMEOUT (30 s)
       a content_wait_s (10 s). Peor caso: 4 × 10 s = 40 s (era 120 s).
       Causa de it=144,0 s e it=124,6 s en ciclo 2026-04-01.
    2. driver.set_page_load_timeout(page_timeout): añadido antes de driver.get()
       para acotar el tiempo de navegación total. Antes ausente.
    3. LANG_SCRAPE_DELAY_IT (nuevo campo config, default 5,0 s):
       Delay pre-scrape exclusivo para italiano. Reduce probabilidad de
       desafíos anti-bot acumulados durante la sesión.

  BUG-DB-002-FIX : scraper_service._upsert_legal() — inserción incondicional
                   de registro en hotels_legal aunque no se encuentre bloque
                   legal en el HTML. Elimina el fallo silencioso que dejaba
                   hotels sin registro en hotels_legal para ciertos mercados
                   (BR, UY) donde Booking.com no publica esa sección.

  MODEL-002      : HotelLegal.has_legal_content (BOOLEAN NOT NULL DEFAULT FALSE)
                   Nuevo campo diagnóstico que distingue entre:
                     TRUE  → bloque legal encontrado y extraído con contenido
                     FALSE → página procesada sin sección legal en HTML

  SCHEMA-002     : hotels_legal.has_legal_content añadida.
                   schema_v60_complete.sql actualizado.

NOTA: NO importar celery_app aqui.
  from app.celery_app import celery_app  <- PROHIBIDO en __init__.py
  Causaria importacion circular: celery_app.py -> app.config -> app.__init__
  Celery debe referenciarse siempre con notacion explicita:
      python -m celery -A app.celery_app:celery_app <comando>
"""

__version__ = "6.0.0"
__version_info__ = (6, 0, 0)
APP_VERSION = "6.0.0"
BUILD_VERSION = 78


# Build 63-fix — Fixes acumulados en sesión de auditoría:
#   BUG-IMPORT-001 : ScrapingLogs alias en models.py
#   BUG-IMPORT-002 : BookingExtractor alias en extractor.py
#   BUG-IMPORT-003 : _VALID_VPN_COUNTRIES en config.py
#   BUG-IMPORT-004 : HotelPolicies alias en models.py
#   BUG-CFG-001..5 : APP_NAME/VERSION/BUILD, LOGS_DIR, IMAGES_DIR, DEBUG_HTML_DIR,
#                    database_url, MAX_ERROR_LEN, STMT_TIMEOUT_OLAP_MS
#   BUG-EXTRACTOR-001 : BookingExtractor mal instanciada como singleton
#   BUG-PERSIST-001 : 7 tablas sin upsert (amenities, popular_services, fine_print,
#                     all_services, faqs, guest_reviews, property_highlights)
#   BUG-PHOTO-001   : photos eliminada de extract_all() -> ahora llama extract_hotel_photos()
#   BUG-BROWSER-001 : Brave no cerraba al terminar batch
#   FIX-PH-LEGACY-001: Property highlights DOM legacy div.property-highlights
