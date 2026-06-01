"""
BookingScraper Pro v6.0.0 build 113
Platform: Windows 11 + Python 3.14.x

BUG-VPN-POPUP-DIRECT-001-FIX (Build 113) : popup «¿Pausar la conexión
    automática en esta sesión?» persiste en pantalla durante la rotación VPN.
    Problema (verificado contra captura de pantalla del operador 2026-06-01):
    el popup de NordVPN aparece REPETIDAMENTE en cada rotación de IP aunque el
    código ya tenía maquinaria de descarte (pywin32 BM_CLICK + hilo en segundo
    plano, Build 73). La maquinaria existente descarta el popup DESPUÉS de que
    aparece, pero no puede descartarlo de forma 100% fiable en todos los
    tiempos de renderizado de la GUI de NordVPN. El popup bloquea la atención
    del operador y en algunos casos no recibe clic a tiempo, dejando la VPN en
    estado desconectado hasta que el operador interviene manualmente.
    Causa raíz: rotate() llama self.disconnect() → nordvpn.exe -d → la GUI
    de NordVPN interpreta el comando de desconexión explícita y presenta
    «¿Pausar la conexión automática?» para confirmar. Si el operador tiene
    la función auto-connect activa (por defecto en NordVPN), SIEMPRE aparece.
    Solución verificada: pruebas/extraer_imagenes.py (benchmark externo
    validado con 141 hoteles) usa nordvpn -c -g "country" DIRECTAMENTE sin
    llamar nordvpn -d primero. NordVPN gestiona el cambio de servidor
    internamente sin mostrar el popup de pausa de auto-conexión. Este
    script NO genera el popup en ningún caso. Conclusión: la omisión del
    paso disconnect() elimina el trigger del popup por diseño.
    Fix:
      - rotate() ya no llama self.disconnect() (ni el sub-hilo de descarte).
        Llama self.connect(new_country) directamente — mismo patrón que
        extraer_imagenes.py. NordVPN reemplaza el servidor activo.
      - Se elimina el time.sleep(5) de espera de teardown de túnel (ya no
        aplica). El tiempo total de rotación se reduce ~5 s.
      - La maquinaria de descarte existente (_dismiss_nordvpn_popup, hilo de
        fondo, BM_CLICK pywin32) se conserva intacta como red de seguridad
        para cualquier popup residual inesperado, pero ya no se activa en la
        ruta normal de rotación.
      - Nuevo toggle VPN_ROTATE_SKIP_DISCONNECT (default True) en config.py
        para control del operador. False = comportamiento legacy con disconnect.
      - pruebas/extraer_imagenes.py: mejora de robustez de la función nordvpn():
        subprocess.run usa lista de argumentos (no string shell=True), y añade
        creationflags + startupinfo para evitar ventanas UAC (BUG-VPN-004
        pattern). Preserva el enfoque NO-DISCONNECT validado.
    Archivos: app/vpn_manager_windows.py, app/config.py, app/__init__.py,
              pruebas/extraer_imagenes.py.

BUG-CONFIG-SYNC-001-FIX (Build 112) : config.py BUILD_VERSION default desincronizado.
    Problema: app/config.py declaraba BUILD_VERSION: int = Field(default=107, ...)
    mientras app/__init__.py ya tenía BUILD_VERSION = 111. El campo Pydantic
    Settings devuelve el valor por defecto cuando BUILD_VERSION no está definido
    en el .env, por lo que Settings().BUILD_VERSION retornaba 107 en todos los
    entornos sin variable de entorno. El encabezado del fichero decía "Build 111"
    pero el campo tenía el default congelado en Build 107 (momento de introducción
    del campo). Causa raíz: cada build actualiza el comentario de cabecera y la
    constante en __init__.py, pero olvida actualizar el default del campo Pydantic.
    Fix: default=112 (sincronizado). Se añade nota en el campo para recordar
    actualizar el default en cada ciclo de build.
    Archivos: app/config.py, app/__init__.py.

BUG-ONLYTITLE-001-FIX (Build 112) : args.onlyTitle hardcodeado a True en el
    payload de exportación.
    Problema verificado en dos rutas independientes:
      1. app/api_payload_builder.py: build_payload() construye la sección "args"
         con "onlyTitle": True fijo. Cuando el endpoint REST
         GET /hotels/url/{url_id}/api-payload devuelve este payload directamente,
         el operador recibe siempre onlyTitle=True y, si lo envía a la API sin
         modificar, solo se actualiza el campo name (y/o longDescription).
         El resto de los 21 campos de data[] construidos correctamente son
         ignorados por la API externa.
      2. app/api_export_system.py: ExportTemplate.args_config default tiene
         "onlyTitle": True, que es el valor que _filter_payload() usa para
         construir la sección "args" del payload enviado por APIExporter.
         Todos los hoteles exportados en producción recibían onlyTitle=True,
         lo que significa que solo name/longDescription eran actualizados
         incluso en exportaciones de campo completo.
    Causa raíz: valor copiado de los payloads de prueba de conexión API
    (intencionales para ese fin) y nunca corregido al pasar a producción.
    Fix: nuevo toggle API_EXPORT_ONLY_TITLE (bool, default False) en config.py.
    build_payload() lee el toggle via getattr(cfg, 'API_EXPORT_ONLY_TITLE', False).
    ExportTemplate.args_config default cambia a "onlyTitle": False.
    Retrocompatibilidad: operadores con plantillas JSON guardadas que tengan
    "onlyTitle": true las mantienen intactas. La variable de entorno permite
    forzar True en entornos de prueba sin tocar el código.
    Archivos: app/config.py, app/api_payload_builder.py, app/api_export_system.py,
              app/__init__.py.

BUG-VIEW-DEDUP-001-FIX (Build 112) : v_api_export_images retornaba múltiples
    filas por foto (una por cada variante de talla: thumb_url/large_url/highres_url)
    pese a que el comentario de la vista declaraba "Prioriza highres_url > large_url
    > thumb_url por foto". El JOIN entre image_data e image_downloads sin cláusula
    DISTINCT ON producía hasta 3 filas por id_photo. El código Python
    (_load_gallery_image_urls) manejaba correctamente la deduplicación en memoria,
    pero cualquier consulta SQL directa sobre la vista obtenía conteos inflados
    (p. ej. 59 fotos de galería → 177 filas = 59×3 tallas). La vista era
    inconsistente con su propio contrato documentado.
    Fix: se reescribe la vista con subconsulta DISTINCT ON (hotel_id, id_photo)
    ordenada por prioridad de talla (highres=1, large=2, thumb=3), envuelta en
    una consulta exterior ORDER BY gallery_order. Ahora devuelve exactamente
    1 fila por foto de galería con la mejor URL disponible. Alineado con el
    comportamiento Python existente.
    Archivos: schema_v77_complete.sql, app/__init__.py.

BUG-SVC-DOC-001-FIX (Build 112) : docstring obsoleto en api_payload_builder.py
    hacía referencia a _ROOM_LEVEL_CATEGORIES (filtro de categorías de
    habitación en services[]) que fue eliminado en Build 103 junto con
    room_level_category_labels. El comentario del módulo seguía describiendo
    el filtro como activo, induciendo a error en la revisión del código.
    Fix: docstring actualizado para reflejar el estado real post-Build 103:
    service_category verbatim del DOM, sin filtrado por categoría de habitación.
    Archivos: app/api_payload_builder.py, app/__init__.py.

BUG-SVC-POPULAR-CAT-001-FIX (Build 111) : service_category vacía en el fallback
    "Most popular facilities".
    Problema (auditoría Build 110→111, verificada contra
    pruebas/_table__hotels_all_services__.csv): 510 servicios (0,77% de 66.432)
    en 53 pares (hotel,idioma) — el 6,3% de los 840 pares — quedaban con
    service_category="". Causa raíz verificada: cuando TODAS las estrategias de
    facility-group-container (E45, 1, 1.5, 2, 3) no encuentran nada, el único
    origen de servicios es property-most-popular-facilities-wrapper (Strategy 4),
    que descartaba la cabecera <h3> del bloque y asignaba category="". Confirmado
    con datos: el 95,1% de las filas vacías coinciden con hotels_popular_services,
    y los 53 pares tienen TODOS sus servicios vacíos (E45 falló por completo). El
    encabezado SÍ existe en el DOM real (verificado en
    pruebas/HTML_76033__Hotel-Topazz.html y HTML_1001_Villa-Dvor_Ohrid.html):
        <div data-testid="property-most-popular-facilities-wrapper">
          <div><h3><div>Most popular facilities</div></h3><ul>…</ul></div>
        </div>
    Fix: nuevo helper BookingExtractor._popular_facilities_category() que extrae
    VERBATIM la cabecera <h3> del wrapper (sin <ul>/<li>) y Strategy 4 la usa como
    service_category. Es texto LITERAL del DOM — sin inferencia ni traducción
    (coherente con la política Build 103). Nuevo toggle
    SVC_POPULAR_FALLBACK_CATEGORY_ENABLED (default True). Cambios coordinados:
    app/extractor.py, app/config.py, app/__init__.py. schema_v77_complete.sql NO
    cambia: NO se añade NOT NULL a service_category (rompería la recreación de BD
    sin migración, y los fallbacks Apollo/flat aún pueden devolver "").

BUG-GALLERY-MODAL-001-FIX (Build 110) : Robustez de captura del modal de galería.
    Problema (auditoría Build 109→110, verificado contra pruebas/*.csv): la
    clasificación de imágenes funciona cuando el modal se abre (Villa Dvor 59/59,
    jagdhof 136/136, wild&bolz 22/22), pero el modal NO se abrió en 50/140 hoteles
    (35.7%) → 0 fotos gallery_visible → el payload recae en el SUPERCONJUNTO
    (p. ej. Topazz 76033: 56 fotos js_array, galería real = 38). Causas
    verificadas: (a) el overlay de consentimiento (OneTrust) reaparece tras el
    borrado de cookies (BUG-LANG-002-FIX) e intercepta el clic del abridor — la
    referencia validada extraer_imagenes.py SÍ lo acepta; (b) _open_gallery()
    deja un lightbox parásito abierto; (c) la página queda scrolleada al fondo.
    Fix: GalleryModalExtractor._prepare_page() (scroll-top + ESC + descarte de
    consentimiento) + bucle de reintentos (GALLERY_MODAL_OPEN_RETRIES). Nuevo
    toggle API_IMAGES_STRICT_GALLERY para no exportar el superconjunto cuando el
    modal falle. Cambios coordinados: app/config.py, app/image_classifier.py,
    app/api_payload_builder.py, app/__init__.py. NOTA: schema_v77_complete.sql NO
    cambia — las columnas gallery_visible/source/subcategory/gallery_order y la
    vista v_api_export_images ya existen desde Build 109.

BUG-IMG-CLASS-001-FIX (Build 109) : Sistema de clasificación de imágenes.
    Problema: el pipeline captura un SUPERCONJUNTO de fotos (todo id_photo con
    token k= en el HTML; p.ej. Villa Dvor=106) mientras la galería pública del
    modal (validada por pruebas/extraer_imagenes.py) es un subconjunto (=59).
    Verificado: el HTML estático/renderizado NO contiene la rejilla del modal
    (0 ocurrencias de gallery-grid-photo-action / GalleryGridViewModal en los
    snapshots de pruebas/), por lo que la IDENTIDAD de las fotos de galería solo
    se obtiene abriendo el modal en vivo.
    Fix:
      - app/image_classifier.py (NUEVO): GalleryModalExtractor (captura modal),
        NonGallerySubcategorizer (heurística + cruce con room images),
        PhotoClassifier (orquestador), y gallery_count_from_html() (fórmula del
        badge "+N photos" como validación de conteo: previews + N; verificada
        exacta — Villa Dvor 8+51=59, wild&bolz 8+14=22).
      - scraper.py: _capture_gallery_modal() abre la rejilla real (no la primera
        imagen) solo en el pase EN; take_gallery_photos() expone el resultado
        sin carreras (índice por URL).
      - scraper_service.py: clasifica en el pase EN con cruce de id_photo contra
        hotels_room_types.images.
      - image_downloader.py: persiste gallery_visible/source/subcategory/
        gallery_order (galería con prioridad, sin degradación).
      - models.py + schema_v77_complete.sql: 4 columnas nuevas + 2 índices +
        vista v_api_export_images. SIN migración (la BD se recrea siempre desde
        el esquema; corrige la recomendación errónea del spec adjunto).
      - api_payload_builder.py: images[] = solo gallery_visible, ordenadas por
        gallery_order, con red de seguridad ante hoteles sin galería.
      - config.py: IMAGE_CLASSIFICATION_ENABLED, API_IMAGES_GALLERY_ONLY,
        GALLERY_MODAL_TIMEOUT_S, GALLERY_MODAL_SCROLL_ITERATIONS,
        GALLERY_MODAL_SCROLL_PAUSE_S.

BUG-EN-LAZY-001-FIX : scraper.py _expand_facilities() Strategy 4 + pre-scroll
    7 hotels showed EN-only empty service_category (Apollo JSON fallback with 5-10
    items, category='') while identical hotels extracted 40-150 properly categorised
    services in all other languages (es/de/fr/it/pt).  Root cause: the English
    Booking.com page IntersectionObserver for facility-group-container did not fire
    within the original single 15-second wait.  Fix:
      - Pre-scroll step now scrolls to page BOTTOM first (warms all lazy loaders),
        then scrolls facility container into view.
      - Strategy 4 replaced with 3-attempt retry loop (3 × 8s = 24s max): each
        attempt re-scrolls and re-dispatches scroll event before waiting.
BUG-IMG-CAP-002-FIX : image_downloader.py — removed hard task_cap=900.
    Previous cap (300 photos × 3 sizes) silently dropped images for hotels
    with >300 photos extracted by extract_hotel_photos_from_html().
    All extracted photos are now processed without a count ceiling.

BUG-SVC-LAZY-001-FIX : scraper.py _expand_facilities() — Booking.com lazy-loads
    property-facilities-block-container via IntersectionObserver.  The container
    was present but EMPTY for 14 hotels (10% of dataset) because window.stop()
    halted JS before the observer fired.  Adds:
      - Pre-scroll step (BEFORE _expand_facilities) that scrolls the container
        into viewport and dispatches a synthetic scroll event.
      - Strategy 4 inside _expand_facilities(): scrollIntoView + wait up to 15s
        for facility-group-container to appear.
      - EC.any_of() in Strategies 1/2/3 covering both modern selector
        (facility-group-container) and legacy (property-section--facilities).
      - Fast-path: returns immediately if facility-group-container already in DOM.
    Impact: 14 hotels previously showing 7-16 uncategorised services (Strategy 4
    popular-wrapper fallback) should now extract 44-144 categorised services via
    Strategy E45 (property-facilities-block-container).
    Ver: BUG_REPORT_Build105_EN.md

Cambios build 103:
  BUG-SVC-EXTRAER4-001-V45: extractor.py — _extract_all_services() v4.5.
    Strategy E45 (PRIMARY): extraer4.py v4.5 (Main-Only). Phase 1 ELIMINADA.
    Usa data-testid="facility-group-container" + "property-facilities-block-container"
    para extraer categorías DOM reales de Booking.com post-expansión Selenium:
      Phase 1: facility-group-container fuera de property-facilities-block-container
               -> "Great for your stay" con servicios de <ul><li>.
      Phase 2: property-facilities-block-container -> facility-group-container
               -> categoría del primer <h3> con SVG + servicios Option 1/2/3.
    Solo Phase 2: property-facilities-block-container → facility-group-container.
    service_category verbatim desde DOM — sin inferencia, sin traducción.
    Eliminados: _FACILITY_GROUP_MAP, _SERVICE_CATEGORY_RULES, _infer_service_category().
    Eliminados de languages.json: room_level_category_labels, category_key_map,
      facility_group_map, service_category_rules.
    language_config.py actualizado: solo lang_url_codes, lang_accept_headers,
      category_labels, see_all_patterns.
    api_payload_builder.py: room_level_filter eliminado, category_key_map eliminado.
    Reducción esperada de NULL service_category: de ~60% a <5%.

Cambios build 101:
  BUG-SVC-NULL-001-FIX: _SERVICE_CATEGORY_RULES expandida con 7 nuevas
    categorías. _add() aplica inferencia automática como fallback.
    GenericFacilityHighlight procesado en Apollo JSON strategy.
    Reducción esperada de NULL service_category de ~55% a <10%.

Cambios build 97:
  BUG-HTML-FP-001-FIX : api_payload_builder.py — toConsider contenía HTML crudo
                         (<p> tags, &amp;). Fix: _html_to_plaintext() convierte
                         <p>/<br> a \n y elimina entidades antes de concatenar.
                         El campo fp de hotels_fine_print almacena HTML preservado;
                         la conversión ahora ocurre en la capa de transformación.
  BUG-CATMAP-001-FIX  : api_payload_builder.py — 5 variantes reales de Booking.com
                         no estaban en _CATEGORY_KEY_MAP y se descartaban silenciosamente:
                         "kostenfreies wlan"(DE), "relación calidad-precio"(ES),
                         "rapporto qualità-prezzo"(IT), "situation géographique"(FR),
                         "wifi gratuito"(IT). Todas añadidas al mapa.
  BUG-LOCALES-EN-001-FIX : api_payload_builder.py — build_payload() ordenaba langs
                         alfabéticamente ('de'<'en'). El contrato _API_.md exige
                         'en' siempre primero en args.locales y en los dicts.
                         Fix: reordenamiento explícito post-query.
  BUG-PRIMARY-EN-001-FIX : api_payload_builder.py — primary se tomaba de hotel_rows[0]
                         (registro 'de' por orden alfabético). Ahora se usa hotel_by_lang
                         .get('en', hotel_rows[0]) para garantizar que los campos
                         language-independent provengan del registro inglés canónico.
  BUG-PAYLOAD-002-FIX : api_payload_builder.py — rating emitia 0 para NULL; fix: None.
  BUG-PAYLOAD-003-FIX : api_payload_builder.py — roomsQuantity emitia 0 para NULL; fix: None.
  BUG-PAYLOAD-004-FIX : api_payload_builder.py — toConsider elif->if: incluye legal_details cuando legal_info tambien existe.
  BUG-PAYLOAD-005-FIX : api_payload_builder.py — negative_comment literales "None","Nada","No"->None.
  BUG-EXPORT-001-FIX  : api_export_system.py — requests.Session() para reutilizacion HTTP.
  BUG-EXPORT-002-FIX  : api_export_system.py — X-Idempotency-Key en cada PATCH.
  BUG-EXPORT-003-FIX  : api_export_system.py — from_db_all_pending() verifica idiomas completos.
  BUG-HEADER-001..005 : Cabeceras desincronizadas en main.py, tasks.py, schema, create_db.bat, config.py.

Cambios build 95:
  BUG-REVIEWS-DOM-001-FIX : extractor.py — _extract_individual_reviews()
                            CAUSA RAÍZ: data-testid="review-card" NO existe
                            en el DOM estático de Booking.com (0 ocurrencias
                            en todos los HTML de pruebas/). Las reseñas
                            individuales se renderizan via React hydration y
                            no están presentes en el HTML initial del servidor.
                            Sin embargo, los datos SÍ están en el Apollo/GraphQL
                            JSON cache embebido en <script type="application/json">
                            como objetos FeaturedReview:ID.
                            Estructura verificada en 2 HTML reales:
                              - atlántico-rio EN: 10 FeaturedReview objects
                              - Art Hotel Spielberg EN: 10 FeaturedReview objects
                            Campos extraídos:
                              guestName       → reviewer_name
                              averageScore    → score (0-10)
                              guestCountryCode→ reviewer_country (ISO 2-letter)
                              positiveText    → positive_comment
                              negativeText    → negative_comment
                              title           → title
                              id              → booking_id (fallback: reviewUrl)
                            Estrategia implementada:
                              Strategy 0 (PRIMARIA): Escanea todos los
                                <script type="application/json"> buscando
                                "FeaturedReview:" → json.loads() → extrae
                                todos los objetos cuya clave comienza con
                                "FeaturedReview:". Retorna inmediatamente si
                                encuentra datos.
                              Strategy 1 (FALLBACK): data-testid="review-card"
                                DOM search — mantenida como salvaguarda por si
                                Booking.com implementa SSR de reviews en futuras
                                versiones del DOM.
                            Resultado esperado: hotels_individual_reviews
                              pasará de 128 bytes (header only) a datos reales
                              (~10 reseñas × 6 idiomas × 13 hoteles).

  BUG-BROWSER-002-FIX     : scraper_service.py — dispatch_batch()
                            Se reemplaza reset_browser() por quit() en el
                            bloque post-batch para terminación definitiva
                            del proceso Brave. reset_browser() era semántica
                            de "reiniciar para reutilizar" — correcto durante
                            rotación VPN mid-batch. quit() es semántica de
                            "terminar definitivamente" — correcto al finalizar
                            el batch completo. El comportamiento observable
                            (data:, en la ventana de Brave al inicio del
                            siguiente batch) es esperado: Selenium carga una
                            página en blanco al crear el nuevo driver, antes
                            de navegar a la primera URL del nuevo batch.


Cambios build 94:
  (ver documentations/Technical_Audit_Report_BookingScraper_v77_EN.md)
  STRUCT-EXPORT-002 : main.py + config.py + env.example
                      Rediseno de endpoints de exportacion a la API externa.
                      Problema: los endpoints /export/batch y /export/payload
                      (Build 88) requerían pasar base_url y api_key_ext como
                      parametros en cada llamada. No había opcion visible en
                      el menu de /docs. No era usable desde Swagger UI.
                      Solucion:
                        1. Nuevos campos en config.py + env.example:
                           EXT_API_BASE_URL, EXT_API_KEY,
                           EXT_API_DEFAULT_LANGUAGES
                        2. 6 nuevos endpoints en tag "Export" de /docs:
                           GET  /export/config       ver config actual
                           POST /export/config       actualizar en runtime
                           GET  /export/preview/{url_id}  dry-run 1 hotel
                           GET  /export/preview      dry-run todos
                           POST /export/send/{url_id}     enviar 1 hotel
                           POST /export/send         enviar todos
                        3. ExportConfigBody y ExportSendBody: Pydantic models
                           con ejemplos para Swagger UI.
                        4. Helpers _parse_languages() y _parse_fields()
                           centralizan la logica de parseo.


Cambios build 90:
  BUG-PHOTO-LIMIT-001-FIX : extractor.py — extract_hotel_photos_from_html()
                            Booking.com limita hotelPhotos JS a ~45 entradas
                            en el HTML estatico. Las fotos adicionales (hasta
                            270+) estan presentes como <img> tags con URLs
                            autenticadas (k= token) en el mismo HTML estatico.
                            No se necesita interaccion Selenium con la galeria.
                            Solucion: extraccion dual en dos fases:
                              Fase 1 (JS): hotelPhotos var -> metadatos ricos
                                (~45 fotos: alt, orientation, dimensions).
                              Fase 2 (img): regex sobre max1024x768 y max200
                                URLs -> todas las fotos adicionales con k=.
                            Merge: JS photos son primarias; img URLs las
                            completan y anaden las fotos extra.
                            Validado en 13 HTMLs de pruebas/:
                              south-bank:  45 -> 273 (esperado 266) +507%
                              leroy:       45 -> 144 (esperado 144) 100%
                              cb-seychelles: 45 -> 97 (esperado 97) 100%
                              TOTAL: 607 -> 1.524 (esperado 1.369) 111.3%

  BUG-PHOTO-LIMIT-001-FIX : image_downloader.py — download_photo_batch()
                            Cap de seguridad actualizado: 300 (100 fotos x3)
                            -> 900 (300 fotos x3). Timeout dinamico: max
                            (600s, n_tasks * 3s) en lugar de fijo 600s.
                            La tasa de descarga esperada mejora de 44.3%
                            (607/1.369) a ~100% (1.369+/1.369).


Cambios build 89:
  BUG-ENV-REGEX-001-FIX : extractor.py — _extract_city_metadata()
                          Build 88 buscaba b_atnm_en y b_city_name (con
                          prefijo b_). El HTML real usa atnm_en y city_name
                          SIN prefijo. Confirmado en 13 HTMLs reales.
                          Resultado en producción Build 88: atnm_en y
                          city_name siempre NULL pese a estar presentes.
                          Regexes corregidas:
                            city_name  busqueda: "city_name:"
                            atnm_en    busqueda: "atnm_en:"
                            (b_ufi ya era correcto)

  STRUCT-CITY-002-FIX   : extractor.py — 3 nuevos campos extraídos:
                          dest_id: JS context_dest_id en bloque
                          autocomplete_vars (ej. "-666610", "900060557").
                          Mismo valor que dest_ufi para hoteles individuales.
                          region_name: breadcrumb items[3] cuando el breadcrumb
                          NO comienza con término genérico ("All resorts" etc.).
                          Validado: Amazonas, Maldonado, Rio de Janeiro State.
                          district_name: breadcrumb items[5] cuando n==7 y
                          NO genérico. Validado: Copacabana, Peninsula,
                          Joao Fernandes.
                          Algoritmo breadcrumb detecta términos genéricos
                          en items[2] y omite region_name en esos hoteles.

  STRUCT-CITY-002-FIX   : models.py — Hotel: 3 nuevas columnas ORM:
                          dest_id (String 64, indexed),
                          region_name (String 256),
                          district_name (String 256).

  STRUCT-CITY-002-FIX   : schema_v77_complete.sql — 3 nuevas columnas
                          en tabla hotels con COMMENTs e índices.
                          Vista v_hotels_full actualizada.

  STRUCT-CITY-002-FIX   : scraper_service.py — _upsert_hotel() persiste
                          dest_id, region_name, district_name.

  BUG-ATNM-API-001-FIX  : api_payload_builder.py — accommodationType
                          usa atnm_en como fuente primaria (Booking.com
                          específico: "hotel", "resort", "guest_house").
                          Fallback: accommodation_type (JSON-LD @type).
                          Antes: siempre "Hotel" (genérico del JSON-LD).


Cambios build 88:
  STRUCT-CITY-001-FIX  : extractor.py — Nuevo método _extract_city_metadata().
                          Extrae city_name, dest_ufi y atnm_en desde el script
                          inline booking.env (regex sobre b_city_name, b_ufi,
                          b_atnm_en). Fallback DOM breadcrumb (#subheader-wrap
                          nav ol → penúltimo <li>) para city_name.
                          extract_all() incluye **self._extract_city_metadata()
                          para propagar las 3 claves al dict de datos.
                          Problema previo: address_city usaba addressRegion
                          (puede ser estado/región, ej. "Amazonas") en lugar
                          del nombre de ciudad preciso (ej. "Manaus").

  STRUCT-CITY-001-FIX  : models.py — Hotel: nuevas columnas ORM
                          city_name (VARCHAR 256), dest_ufi (VARCHAR 64),
                          atnm_en (VARCHAR 64).

  STRUCT-CITY-001-FIX  : schema_v77_complete.sql — Nuevas columnas en tabla
                          hotels, con COMMENTs. Vista v_hotels_full actualizada
                          para exponer city_name, dest_ufi, atnm_en.

  STRUCT-CITY-001-FIX  : scraper_service.py — _upsert_hotel() persiste
                          city_name, dest_ufi, atnm_en.

  STRUCT-CITY-001-FIX  : api_payload_builder.py — _build_address() usa
                          city_name (booking.env) como fuente primaria de
                          ciudad en vez de address_city (addressRegion JSON-LD).
                          Prioridad: city_name → address_city → address_locality.

  STRUCT-EXPORT-001    : app/api_export_system.py — Nuevo módulo completo de
                          exportación a la API externa (_API_.md).
                          Componentes: APIField (Enum 22 campos), ExportTemplate
                          (campos + idiomas + args, garantía en-primero),
                          TemplateManager (plantillas built-in + disco),
                          ExportSelection (desde archivo JSON/TXT o BD),
                          APIConfig (base_url, api_key, PATCH con reintentos),
                          APIExporter (filtrado, validación, envío, dry-run),
                          user_panel_cli (panel interactivo CLI).
                          Plantillas built-in: default, full, minimal.

  STRUCT-EXPORT-001    : main.py — 2 nuevos endpoints FastAPI:
                          POST /export/payload/{url_id} — dry run de un hotel.
                          POST /export/batch — exportación masiva (dry_run=true
                          por defecto; dry_run=false envía a la API).


Cambios build 87:
  BUG-COMMIT-STATUS-001-FIX : scraper_service.py — dispatch_batch()
                              Las 14 URLs cargadas permanecían en estado
                              'pending' indefinidamente; ningún scraping
                              se ejecutaba a pesar de que Celery Beat
                              lanzaba scrape_pending_urls cada 30s.
                              Causa raíz: Build 86 eliminó el commit
                              explícito en el bloque que marca URLs como
                              'processing', confiando en que get_db()
                              lo gestionaría. Correcto si los objetos
                              pertenecen a la sesión activa. INCORRECTO
                              aquí: los objetos URLQueue se cargaron en
                              un primer bloque get_db() ya cerrado
                              (session.close() en finally). Al abrirse
                              el segundo bloque get_db(), los objetos
                              están detached — la nueva sesión no los
                              rastrea y su commit() no persiste nada.
                              Resultado observado: url_queue mostraba
                              todas las filas en 'pending', hotels
                              vacía, Redis lock ocupado cada 280s.
                              Fix: se extraen los PKs de los objetos
                              detached (legibles por expire_on_commit=
                              False) y se ejecuta un UPDATE masivo
                              via session.query().filter().update()
                              con synchronize_session=False dentro
                              de una sesión fresca que posee las filas.

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
BUILD_VERSION = 113

# Build 108 — BUG-IMG-NAME-001: nuevo campo name_jpg en image_downloads.
#   Se extrae el nombre de archivo (basename) de la URL de cada imagen,
#   descartando el query string (k=, o=, hp=), y se persiste en image_downloads.
#   Ejemplo: '.../max1024x768/146312477.jpg?k=...' -> '146312477.jpg'. Idéntico
#   para las 3 tallas (max200/max1024x768/max1280x900) de la misma foto.
#   Cambios coordinados: schema_v77_complete.sql (columna VARCHAR(255) + COMMENT),
#   app/models.py (ImageDownload.name_jpg), app/image_downloader.py (helper
#   _name_jpg_from_url() + populado en éxito y error + backfill en update).
#   Sin migración: la columna existe desde la recreación de BD (la BD siempre
#   se borra al arrancar y schema_v77_complete.sql se re-ejecuta).

# Build 107 — Auditoría de datos Build 106 (verificada contra CSV/HTML reales):
#   BUG-IMG-DERIVE-001-FIX : extractor.extract_hotel_photos_from_html() ahora
#       deriva las TRES tallas (max200/max1024x768/max1280x900) para toda foto
#       reutilizando el token k= compartido. Elimina el techo de ~45 fotos para
#       highres_url. Cobertura verificada en HTML real: 49,3% -> 100% highres,
#       93,1% -> 100% thumb. Proyección: 28.544 -> 35.316 descargas.
#       Causa real NO era timeout (solo 81 errores/28.544); era falta de
#       derivación de highres en la fuente supplement. Requisito cumplido:
#       "no limitar la extracción de imágenes".
#   Hallazgos del informe v2 refutados con datos reales (sin cambio de código):
#     - hotels 841 vs 840: FALSO. Baseline SQL y dump coinciden en 840, 0 dups.
#     - Déficit de servicios en pt: FALSO. 140 hoteles con servicios en 6 idiomas.
#     - Categorías vacías "grupo Skiing": 0,71% real, afecta facilities populares
#       sin cabecera de grupo en todos los idiomas (no se añade NOT NULL: rompería
#       la recreación de BD sin migración).



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
