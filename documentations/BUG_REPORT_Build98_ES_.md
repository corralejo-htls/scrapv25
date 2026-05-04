## ✅ BUG-SVC-002 — Refactor completo: control total desde `.env`

### Arquitectura resultante

Todo lo que antes era hardcoded en el código Python ahora vive en `.env` / `config.py` con defaults seguros. Añadir japonés, ruso o árabe **no requiere tocar ningún `.py`**:

```ini
# .env — añadir idioma ru completo en 3 líneas

ENABLED_LANGUAGES=en,es,de,it,fr,pt,ru

ROOM_LEVEL_CATEGORY_LABELS=en:room amenities,es:comodidades,de:zimmerausstattung,it:dotazioni camera,pt:comodidades,ru:удобства в номере

CATEGORY_KEY_MAP_EXTRA=чистота:hotel_clean,удобства:hotel_services,расположение:hotel_location,комфорт:hotel_comfort,соотношение цены и качества:hotel_value,бесплатный wifi:hotel_wifi,общая оценка:total

CATEGORY_LABELS_EXTRA=hotel_services.ru:Удобства,hotel_clean.ru:Чистота,hotel_comfort.ru:Комфорт,hotel_value.ru:Соотношение цены и качества,hotel_location.ru:Расположение,hotel_wifi.ru:Бесплатный Wi-Fi,total.ru:Общая оценка
```

---

### Flujo de carga al arrancar

```
uvicorn start
    │
    ├─ api_payload_builder.py se importa
    │   ├─ _build_supported_languages()   ← lee ENABLED_LANGUAGES
    │   ├─ _build_room_level_categories() ← lee ROOM_LEVEL_CATEGORY_LABELS
    │   ├─ _build_category_key_map()      ← base + CATEGORY_KEY_MAP_EXTRA
    │   └─ _build_category_labels()       ← base + CATEGORY_LABELS_EXTRA
    │
    └─ lifespan() en main.py
        └─ LanguageCoverageValidator().validate_and_log(enabled_langs)
            ├─ Check 1: ROOM_LEVEL_CATEGORY_LABELS cubre todos los langs?
            ├─ Check 2: _CATEGORY_LABELS tiene los 7 api_keys por lang?
            ├─ Check 3: _CATEGORY_KEY_MAP tiene texto de entrada por lang?
            └─ Check 4: SUPPORTED_LANGUAGES coherente y 'en' primero?
                        → INFO si ✅ / WARNING si ⚠️ (no bloquea arranque)
```

---

### Archivos modificados en este paso

| Archivo | Cambio |
|---------|--------|
| `api_payload_builder.py` | Eliminados todos los hardcodes; 3 builders dinámicos + `LanguageCoverageValidator` completo |
| `config.py` | `ENABLED_LANGUAGES` + 3 nuevos campos: `ROOM_LEVEL_CATEGORY_LABELS`, `CATEGORY_KEY_MAP_EXTRA`, `CATEGORY_LABELS_EXTRA` |
| `main.py` | Llamada a `LanguageCoverageValidator().validate_and_log()` en `lifespan()` |
| `env.example` | Sección de idiomas completamente documentada con ejemplos ru/ja/zh/ar/ko/sr |


----

Creo la arquitectura completa: 
un archivo `languages.json` como fuente de verdad + `language_config.py` como singleton validador + integración en todos los módulos. actualizo `config.py` (solo añado el nuevo campo, limpio los anteriores): actualizo `main.py` para usar `init_language_config` en lugar del validador anterior:

## ✅ Arquitectura de idiomas — Sin hardcoding. Validación bloqueante en startup.

### Flujo completo

```
.env
  ENABLED_LANGUAGES=en,es,de,it,fr,pt,ru,ja,zh
  LANGUAGES_CONFIG_FILE=languages.json
        │
        ▼
  languages.json  ←── única fuente de verdad para TODOS los idiomas
  (8 secciones)        (Latin / Cirílico / CJK / Árabe / Turco...)
        │
        ▼
  language_config.py  ──  LanguageConfigLoader.load()
  (nuevo módulo)           │
                           ├── valida TODAS las secciones × TODOS los langs
                           ├── construye LanguageConfig (singleton tipado)
                           └── raise LanguageConfigError si hay gaps
                                    │
                                    ▼
                             main.py lifespan()
                             SystemExit(1) si error crítico
                             (arranque BLOQUEADO con log detallado)
        │
        ▼
  api_payload_builder.py  →  _lc().category_key_map
  scraper.py (pendiente)  →  _lc().lang_url_codes, get_accept_header()
  extractor.py (pendiente)→  _lc().facility_group_map, service_category_rules
```

### Lo que se eliminó

| Antes | Ahora |
|-------|-------|
| `_CATEGORY_KEY_MAP_BASE` hardcoded (50+ entradas) | `languages.json → category_key_map` |
| `_CATEGORY_LABELS_BASE` hardcoded | `languages.json → category_labels` |
| `_ROOM_LEVEL_CATEGORIES_BASE` hardcoded | `languages.json → room_level_category_labels` |
| `SUPPORTED_LANGUAGES = ["en","es",...]` hardcoded | derivado de `ENABLED_LANGUAGES` |
| `_CATEGORY_KEY_MAP_EXTRA`, `_CATEGORY_LABELS_EXTRA` en .env | integrado en `languages.json` directamente |
| WARNING al arranque (no bloqueante) | **SystemExit(1)** si falta cualquier idioma |

### Añadir japonés — solo 2 pasos

1. `.env`: `ENABLED_LANGUAGES=en,es,de,it,fr,pt,ja`
2. `languages.json`: ya tiene `ja` en todas las secciones — **cero cambios en código**

### Smoke-test con 9 idiomas (EN+ES+DE+IT+FR+PT+RU+JA+ZH)

```
✅ All checks passed for 9 languages (including ru, ja, zh)
  flat_map['чистота']         = hotel_clean   ← Cirílico
  flat_map['清潔さ']           = hotel_clean   ← CJK japonés
  'コストパフォーマンス' in flat_map = True       ← hotel_value japonés
  facility_group_map['15']['zh'] = 客房设施     ← groupId=15 chino
```

**Pendiente de aplicar el mismo patrón** (fuera del scope de este build): `scraper.py` (`LANG_URL_MAP`, `LANG_TO_ACCEPT_LANGUAGE`) y `extractor.py` (`_FACILITY_GROUP_MAP`, `_SERVICE_CATEGORY_RULES`, `_SEE_ALL_PATTERN`) — ya están en `languages.json` y `LanguageConfig` los expone; solo falta sustituir las referencias en esos módulos (verificar).

