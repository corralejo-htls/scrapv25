"""
BookingScraper Pro v6.0.0 build 86
Platform: Windows 11 + Python 3.14.x

Cambios build 86:
  BUG-SVC-CAT-STR3-FIX : extractor.py — hotels_all_services.service_category
                          siempre NULL para hoteles cuyas páginas no contienen
                          Apollo JSON con groupId ni facility-group DOM agrupado.
                          Causa raíz: las Estrategias 1-flat, 2 y 3 llamaban
                          _add() sin argumento category, dejando service_category
                          como "" → NULL en BD.
                          Confirmado en ciclo 2026-04-09: 238 filas NULL sobre
                          1 único hotel (url_id=bb9e1557), 6 idiomas × ~40 items.
                          Los otros 12 hoteles tenían categoría correcta porque
                          llegaban a Estrategia 0 (Apollo JSON) o 1.5 (facility-group).
                          Tres cambios en extractor.py:
                            1. Nueva variable de clase _SERVICE_CATEGORY_RULES:
                               lista de (keywords_tuple, groupId) con 223 servicios
                               en 6 idiomas clasificados en Food & Drink (7),
                               Outdoors & View (13), Services (3), General (1)
                               y Room Amenities (15).
                            2. Nuevo método _infer_service_category(text, lang_key):
                               busca substrings case-insensitive, retorna categoría
                               traducida desde _FACILITY_GROUP_MAP.
                            3. Estrategias 1-flat, 2 y 3: cada item llama ahora
                               _infer_service_category() antes de _add(),
                               garantizando service_category poblado en todas
                               las rutas de extracción.
                          lang_key añadido al inicio de _extract_all_services()
                          (necesario para el nuevo método).

Cambios build 85:
  BUG-BUILD-001-FIX : app/__init__.py — docstring desincronizado con BUILD_VERSION.
                       El docstring decía "build 83" mientras BUILD_VERSION=84.
                       Ahora refleja build 85 y documenta los cambios de este ciclo.
  BUG-VIEW-001-FIX  : schema_v77_complete.sql — v_hotels_full.room_types_detail
                       solo incluía {room_name, description, facilities}. Faltaban
                       los campos adults, children, images, info añadidos en Build 80
                       (GAP-SCHEMA-002-FIX). La vista entregaba datos incompletos a
                       cualquier consumidor de la API que los leyese desde la view.
  BUG-VIEW-002-FIX  : schema_v77_complete.sql — v_hotels_full.nearby_places
                       solo exponía hnp.category (VARCHAR). La API destino espera
                       category como INTEGER. La columna category_code (SMALLINT)
                       añadida en Build 82 (GAP-SCHEMA-003-FIX) no estaba incluida
                       en la vista. Añadido campo category_code al jsonb_build_object.
  BUG-VIEW-003-FIX  : schema_v77_complete.sql — v_hotels_full.all_services era
                       un array_agg(service) plano, sin la columna service_category
                       añadida en Build 82 (GAP-API-001-FIX). La vista ahora produce
                       jsonb_agg con {service, service_category} para todos los
                       consumidores de v_hotels_full, facilitando la transformación
                       al formato anidado que requiere _API_.md.
  BUG-SQL-001-FIX   : _Bug_Query-SQL_v85.sql — fichero de diagnóstico corregido.
                       Las queries originales referenciaban hotels_amenities (tabla
                       eliminada en Build 65), lo que abortaba la transacción psql
                       completa. Todas las queries posteriores fallaban en cascada
                       con "transacción abortada". Fichero corregido sin referencias
                       a hotels_amenities y con ROLLBACK/BEGIN de seguridad.

Cambios build 83:
  BUG-NEARBY-001-FIX: extractor._extract_nearby_places() — place_name limpio.
                       Usa div.d1bc97eb82 (nombre) con span.f0595bb7c6 extraído
                       antes de get_text(). Usa div.cbf0753d0c para distancia.
                       Clases verificadas en HTML real de pruebas/.
  BUG-LEGAL-001-FIX : extractor._extract_legal() — legal_info sin título.
                       find_next_siblings(h2) como fuente primaria del cuerpo.
                       El título queda solo en campo 'legal'.
  BUG-POLICY-001-FIX: extractor._extract_policies() — múltiples filas por hotel.
                       Strategy 0: section#policies / HouseRules-wrapper +
                       clases b0400e5749 (row), a776c0ae8b (label), c92998be48 (value).
  BUG-STAR-001-FIX  : extractor._extract_star_rating() — aria-label primario.
                       Parsea "X out of 5 stars" desde aria-label del span.
                       Sin dependencia del conteo de SVGs.

Cambios build 82:
  GAP-API-001-FIX   : extractor.py — _extract_all_services() ahora devuelve
                       List[Dict{service, service_category}] en lugar de List[str].
                       La categoría se extrae del heading del bloque facility-group.
                       scraper_service._upsert_hotel_all_services() actualizado.
                       schema + models: service_category VARCHAR(128) NULL añadida.
  GAP-SCHEMA-003-FIX: extractor.py — _extract_nearby_places() incluye category_code
                       (int|None) usando _NEARBY_CATEGORY_CODE_MAP (1-6).
                       scraper_service._upsert_hotel_nearby_places() persiste código.
                       schema + models: category_code SMALLINT NULL añadida con
                       constraint chk_hnp_category_code (1-99).

Cambios build 81:
  GAP-SCHEMA-001-FIX : extractor.py — _extract_individual_reviews() implementada.
                       Extrae reseñas textuales individuales (reviewer_name,
                       score, title, positive_comment, negative_comment,
                       reviewer_country, booking_id) con selector primario
                       data-testid="review-card".  extract_all() incluye
                       la clave 'individual_reviews'.
  GAP-SCHEMA-001-FIX : scraper_service.py — _upsert_hotel_individual_reviews()
                       añadida; estrategia delete-before-insert por url_id+lang.
                       Llamada al final de _persist_hotel_data() antes de
                       session.commit(). Mismo patrón que BUG-PERSIST-001/002/003.

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
BUILD_VERSION = 86


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
