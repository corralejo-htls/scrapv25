# API Usage Guide — BookingScraper Pro
## Scraper → External API · Complete Integration Guide

**Version:** BookingScraper Pro v6.0.0 Build 91  
**Date:** 2026-04-12  
**Local interface:** `http://localhost:8000/docs`

---

## TABLE OF CONTENTS

1. [Coverage Assessment](#1-coverage-assessment)
2. [Quick Start — 4 Steps](#2-quick-start--4-steps)
3. [Step 1 — Configure Credentials in `.env`](#3-step-1--configure-credentials-in-env)
4. [Step 2 — Swagger UI Export Menu](#4-step-2--swagger-ui-export-menu)
5. [Step 3 — Preview Before Sending](#5-step-3--preview-before-sending)
6. [Step 4 — Send to External API](#6-step-4--send-to-external-api)
7. [API Field Reference](#7-api-field-reference)
8. [External API Payload Format](#8-external-api-payload-format)
9. [Field Limitations](#9-field-limitations)
10. [Verification SQL](#10-verification-sql)

---

## 1. COVERAGE ASSESSMENT

| Metric | Value |
|--------|-------|
| Total API fields | 22 |
| Fields ≥ 80% populated | **18 / 22 (82%)** |
| Average coverage | **86%** |
| **Status** | ✅ **READY — exceeds 80% threshold** |

| Status | Fields | Count |
|--------|--------|:-----:|
| ✅ FULL (≥ 80%) | name, rating, address, geoPosition, services, conditions, toConsider, images, scoreReview, scoreReviewBasedOn, accommodationType, extraInfo, longDescription, categoryScoreReview, nearbyPlaces, guestValues, seoDescription, keywords | 18 |
| ⚠️ PARTIAL | roomsQuantity, rooms, reviews | 3 |
| ❌ N/A | priceRange | 1 |

---

## 2. QUICK START — 4 STEPS

```
Step 1  Edit .env                → add EXT_API_BASE_URL, EXT_API_KEY
Step 2  Restart server           → inicio_rapido.bat (or restart FastAPI)
Step 3  http://localhost:8000/docs → Export menu → GET /export/config
Step 4  Export menu → POST /export/send
```

---

## 3. STEP 1 — CONFIGURE CREDENTIALS IN `.env`

Open `C:\BookingScraper\.env` and add (or update) these three lines:

```ini
# External API — _API_.md format
EXT_API_BASE_URL=https://web.com/api
EXT_API_KEY=543-clave-api
EXT_API_DEFAULT_LANGUAGES=en,es
```

| Variable | Required | Example | Description |
|----------|:--------:|---------|-------------|
| `EXT_API_BASE_URL` | ✅ | `https://web.com/api` | Base URL of the external API |
| `EXT_API_KEY` | ✅ | `543-clave-api` | External API authentication key |
| `EXT_API_DEFAULT_LANGUAGES` | optional | `en,es` | Default locales for every export (`en` always added automatically) |

**After editing `.env`, restart the server:**
```bat
stop_server.bat
start_server.bat
```

---

## 4. STEP 2 — SWAGGER UI EXPORT MENU

Open **`http://localhost:8000/docs`** and expand the **Export** section.  
Six endpoints are available:

```
Export
│
├── GET  /export/config              View current external API configuration
├── POST /export/config              Update credentials at runtime (no restart needed)
│
├── GET  /export/preview/{url_id}    Dry-run payload for ONE hotel
├── GET  /export/preview             Dry-run payload for ALL completed hotels
│
├── POST /export/send/{url_id}       Send ONE hotel to external API
└── POST /export/send                Send ALL completed hotels to external API
```

### 4.1 `GET /export/config` — Verify credentials

Click **Try it out → Execute**.

Expected response when correctly configured:

```json
{
    "ext_api_base_url":          "https://web.com/api",
    "ext_api_key":               "***api",
    "ext_api_default_languages": "en,es",
    "ready":                     true,
    "note": "Edit .env to change permanently. Use POST /export/config to update without restart."
}
```

`"ready": false` means `EXT_API_BASE_URL` or `EXT_API_KEY` is missing.

### 4.2 `POST /export/config` — Update credentials without restart

Useful for testing different credentials without editing `.env`.

Click **Try it out** and fill in the request body:

```json
{
    "ext_api_base_url":          "https://web.com/api",
    "ext_api_key":               "543-clave-api",
    "ext_api_default_languages": "en,es"
}
```

⚠️ **Temporary** — valid only until next server restart. Edit `.env` to make permanent.

---

## 5. STEP 3 — PREVIEW BEFORE SENDING

### 5.1 `GET /export/preview/{url_id}` — Single hotel dry run

Click **Try it out** and enter the `url_id` from the `url_queue` table:

| Ref | Hotel | url_id |
|-----|-------|--------|
| 1001 | Manaus Hotéis Millennium | `ee210b41-9541-440c-a102-d8925d548beb` |
| 1002 | Colonna Park | `b5ecd4eb-2edf-4a92-a6e1-c3b9d5ec0337` |
| 1009 | Grace Bay Club | `1a803735-5517-4645-b9ed-ce8437167493` |
| 1014 | Villa Dvor | `ed97a898-e064-45d6-9867-ebab0185c7f4` |

Optional query parameters:
- `languages` — e.g. `en,es` (leave blank to use `EXT_API_DEFAULT_LANGUAGES`)
- `fields` — e.g. `name,address,scoreReview` (leave blank for all recommended fields)

Response includes:
```json
{
    "url_id":            "ee210b41-...",
    "hotel_id":          "563173",
    "payload":           { "data": { ... }, "args": { ... } },
    "validation_errors": [],
    "sent":              false,
    "error":             null
}
```

Review `payload.data` to confirm data quality before sending.

### 5.2 `GET /export/preview` — All hotels dry run

Click **Try it out → Execute** (no parameters required).

Response:
```json
{
    "total":    14,
    "success":  14,
    "failed":   0,
    "skipped":  0,
    "dry_run":  true
}
```

If `failed > 0`, check the `errors` array for details.

---

## 6. STEP 4 — SEND TO EXTERNAL API

### 6.1 `POST /export/send` — Send ALL hotels

Click **Try it out**.

The request body is **fully optional** — leave it as-is to use defaults:

```json
{
    "languages": null,
    "fields":    null,
    "dry_run":   false
}
```

- `languages: null` → uses `EXT_API_DEFAULT_LANGUAGES` from `.env`
- `fields: null` → exports all recommended fields
- `dry_run: false` → sends data to the external API

Response:
```json
{
    "total":   14,
    "success": 14,
    "failed":  0,
    "skipped": 0,
    "errors":  []
}
```

### 6.2 `POST /export/send/{url_id}` — Send ONE hotel

Enter the `url_id` and optionally customise the body:

```json
{
    "languages": "en,es,de",
    "fields":    "name,address,scoreReview,images,categoryScoreReview,longDescription",
    "dry_run":   false
}
```

### 6.3 Custom field selection — `fields` parameter

To export only specific fields, pass their names as a comma-separated string:

| Preset | Value |
|--------|-------|
| **Minimum** | `name,scoreReview,categoryScoreReview` |
| **Standard** | `name,rating,address,geoPosition,services,conditions,images,scoreReview,accommodationType,longDescription,categoryScoreReview,nearbyPlaces,seoDescription,keywords` |
| **Full** | *(leave `fields` blank)* |

All 22 available field names:

```
name  rating  address  geoPosition  services  conditions  toConsider
images  scoreReview  scoreReviewBasedOn  roomsQuantity  accommodationType
priceRange  extraInfo  longDescription  reviews  categoryScoreReview
rooms  nearbyPlaces  guestValues  seoDescription  keywords
```

---

## 7. API FIELD REFERENCE

### Fields mapping: BookingScraper DB → External API

| API Field | DB Source | Languages | Coverage |
|-----------|-----------|:---------:|:--------:|
| `name` | `hotels.hotel_name` | ✅ per lang | 100% |
| `rating` | `hotels.star_rating` | ✗ single | 92% |
| `address` | `hotels`: street + postal + city_name + country | ✅ per lang | 100% |
| `geoPosition` | `hotels.latitude` / `longitude` | ✗ single | 100% |
| `services` | `hotels_all_services` (grouped by category) | ✅ per lang | 100% |
| `conditions` | `hotels_policies` (policy_name + detail) | ✅ per lang | 92% |
| `toConsider` | `hotels_fine_print` + `hotels_legal` | ✅ per lang | 85% |
| `images` | `image_downloads` (highres → large fallback) | ✗ single | 100% |
| `scoreReview` | `hotels.review_score` (0–10) | ✗ single | 100% |
| `scoreReviewBasedOn` | `hotels.review_count` | ✗ single | 92% |
| `roomsQuantity` | `hotels.rooms_quantity` | ✗ single | 69% ⚠️ |
| `accommodationType` | `hotels.atnm_en` → `accommodation_type` | ✗ single | 100% |
| `priceRange` | `hotels.price_range` | ✗ single | 0% ❌ |
| `extraInfo` | `hotels_extra_info.extra_info` | ✅ per lang | 85% |
| `longDescription` | `hotels_description.description` | ✅ per lang | 100% |
| `reviews` | `hotels_individual_reviews` | ✅ per lang | 15% ⚠️ |
| `categoryScoreReview` | `hotels_guest_reviews` | ✅ per lang | 100% |
| `rooms` | `hotels_room_types` | ✅ per lang | 69% ⚠️ |
| `nearbyPlaces` | `hotels_nearby_places` (name + distance + category) | ✅ per lang | 100% |
| `guestValues` | `hotels_faqs` (question + answer) | ✅ per lang | 92% |
| `seoDescription` | `hotels_seo.seo_description` | ✅ per lang | 100% |
| `keywords` | `hotels_seo.keywords` | ✅ per lang | 100% |

---

## 8. EXTERNAL API PAYLOAD FORMAT

### 8.1 Request

```
PATCH https://web.com/api/en/{api_key}/update/{hotel_id_booking}.json
Content-Type: application/json
```

The `hotel_id_booking` is the Booking.com internal ID stored in `hotels.hotel_id_booking`.

### 8.2 Full payload example (Villa Dvor, en + es)

```json
{
    "data": {
        "name":    { "en": "Villa Dvor", "es": "Villa Cerro Verde" },
        "rating":  4,
        "address": {
            "en": "Boro Sain 20, 6000 Ohrid, North Macedonia",
            "es": "Boro Sain 20, 6000 Ohrid, Macedonia del Norte"
        },
        "geoPosition": { "latitude": 41.113532, "longitude": 20.794691 },
        "accommodationType": "guest_house",
        "scoreReview":         9.2,
        "scoreReviewBasedOn":  67,
        "roomsQuantity":       6,
        "priceRange":          null,
        "longDescription": {
            "en": "Villa Dvor in Ohrid offers a sun terrace and free WiFi.\nGuests can relax in the outdoor seating area.",
            "es": "Villa Dvor en Ohrid ofrece solárium y wifi gratis.\nLos huéspedes pueden relajarse al aire libre."
        },
        "services": {
            "en": [{ "Internet": ["Free WiFi in all areas"], "Outdoors": ["Sun terrace", "Garden"] }],
            "es": [{ "Internet": ["WiFi gratis en todo el hotel"], "Exteriores": ["Solárium", "Jardín"] }]
        },
        "conditions": {
            "en": [
                { "condition": "Check-in",  "detail": "From 3:00 PM to 10:00 PM" },
                { "condition": "Check-out", "detail": "From 8:00 AM to 11:00 AM" }
            ],
            "es": [
                { "condition": "Entrada", "detail": "Desde las 3:00 PM hasta 10:00 PM" },
                { "condition": "Salida",  "detail": "Desde las 8:00 AM hasta 11:00 AM" }
            ]
        },
        "toConsider": {
            "en": "Guests must show a photo ID at check-in.\nQuiet hours: 22:00 to 08:00.",
            "es": "Los huéspedes deben mostrar un documento de identidad.\nHorario de silencio: 22:00 a 08:00."
        },
        "images": [
            "https://cf.bstatic.com/xdata/images/hotel/max1280x900/146556730.jpg?k=...",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/580336162.jpg?k=..."
        ],
        "categoryScoreReview": {
            "en": {
                "hotel_services":  { "category": "Facilities",     "score": 9.1 },
                "hotel_clean":     { "category": "Cleanliness",    "score": 9.3 },
                "hotel_comfort":   { "category": "Comfort",        "score": 9.2 },
                "hotel_value":     { "category": "Value for money","score": 9.3 },
                "hotel_location":  { "category": "Location",       "score": 9.4 },
                "hotel_wifi":      { "category": "Free Wifi",      "score": 9.3 },
                "total":           { "category": "Total",          "score": 9.2 }
            },
            "es": {
                "hotel_services":  { "category": "Instalaciones",  "score": 9.1 },
                "hotel_clean":     { "category": "Limpieza",       "score": 9.3 },
                "hotel_comfort":   { "category": "Comodidad",      "score": 9.2 },
                "hotel_value":     { "category": "Precio calidad", "score": 9.3 },
                "hotel_location":  { "category": "Ubicación",      "score": 9.4 },
                "hotel_wifi":      { "category": "Wifi gratis",    "score": 9.3 },
                "total":           { "category": "Total",          "score": 9.2 }
            }
        },
        "nearbyPlaces": {
            "en": [{ "name": "Saraiste Beach", "distance": "0.3 miles", "category": 3 }],
            "es": [{ "name": "Playa Saraiste", "distance": "0.4 kms",   "category": 3 }]
        },
        "guestValues": {
            "en": [{ "topic": "Do rates include spa access?", "topicComments": "Yes, pool and sauna are included." }],
            "es": [{ "topic": "¿Las tarifas incluyen acceso al spa?", "topicComments": "Sí, piscina y sauna incluidos." }]
        },
        "seoDescription": {
            "en": "Villa Dvor features garden accommodations in Ohrid.",
            "es": "Villa Dvor ofrece alojamiento con jardín en Ohrid."
        },
        "keywords": {
            "en": "Villa Dvor, Ohrid, North Macedonia, Guest House",
            "es": "Villa Dvor, Ohrid, Macedonia del Norte, Casa de Huéspedes"
        }
    },
    "args": {
        "seoFormatKey":  "",
        "onlyTitle":     true,
        "regenerateSeo": true,
        "append":        false,
        "cache":         true,
        "locales":       ["en", "es"]
    }
}
```

### 8.3 Rules

| Rule | Description |
|------|-------------|
| `en` mandatory | English must always be present |
| `en` first | In every multilingual object, `"en"` must come first |
| Line breaks | Use `\n` — never `<p>` HTML tags |
| Optional fields | Any field can be omitted; only `args.locales` is required |
| `priceRange` | Always send `null` |

---

## 9. FIELD LIMITATIONS

| Field | Behaviour | Recommendation |
|-------|-----------|----------------|
| `priceRange` | Always `null` | Omit from payload — never include |
| `reviews` | `[]` for hotels with >10 reviews | Include field; API accepts empty array |
| `rooms.adults` / `.children` | Often `null` | Include array with name/description; occupancy left null |
| `roomsQuantity` | `null` ~31% of hotels | Send `0` when null |
| `rating` | `null` for some resort properties | Send `0` when null |

---

## 10. VERIFICATION SQL

### Check which hotels are ready for export

```sql
SELECT
    uq.external_ref,
    h.hotel_name,
    h.hotel_id_booking,
    h.city_name,
    h.atnm_en          AS type,
    h.review_score,
    h.star_rating,
    COUNT(DISTINCT id_.id) AS images,
    uq.status
FROM url_queue uq
JOIN hotels h ON h.url_id = uq.id AND h.language = 'en'
LEFT JOIN image_downloads id_ ON id_.hotel_id = h.id AND id_.category = 'large_url'
WHERE uq.status = 'done'
GROUP BY uq.external_ref, h.hotel_name, h.hotel_id_booking,
         h.city_name, h.atnm_en, h.review_score, h.star_rating, uq.status
ORDER BY uq.external_ref;
```

### Get url_id for use in `/export/preview/{url_id}` and `/export/send/{url_id}`

```sql
SELECT
    uq.external_ref,
    uq.id          AS url_id,
    h.hotel_name,
    h.hotel_id_booking
FROM url_queue uq
JOIN hotels h ON h.url_id = uq.id AND h.language = 'en'
ORDER BY uq.external_ref;
```

---

*Guide v2.0 · BookingScraper Pro v6.0.0 Build 91 · 2026-04-12*
