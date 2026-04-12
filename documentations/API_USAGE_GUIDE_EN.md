# API Usage Guide — BookingScraper Pro → External API
## Integration: Scraped Hotel Data → `_API_.md` Format

**Version:** BookingScraper Pro v6.0.0 Build 90  
**Date:** 2026-04-12  
**Scope:** Complete guide for exporting scraped hotel data to the external API

---

## TABLE OF CONTENTS

1. [Coverage Assessment](#1-coverage-assessment)
2. [API Structure](#2-api-structure)
3. [Field Reference](#3-field-reference)
4. [Endpoints](#4-endpoints)
5. [Export Workflow](#5-export-workflow)
6. [API Call Examples](#6-api-call-examples)
7. [Field Limitations](#7-field-limitations)
8. [Verification Queries](#8-verification-queries)

---

## 1. COVERAGE ASSESSMENT

### 1.1 Summary

| Metric | Value |
|--------|-------|
| Total API fields | 22 |
| Fields with ≥80% coverage | **18 / 22 (82%)** |
| Average coverage | **86%** |
| Status | ✅ **READY — exceeds 80% threshold** |

### 1.2 Field Coverage Matrix

| API Field | Coverage | Status | Source Table |
|-----------|:--------:|--------|-------------|
| `name` | 100% | ✅ FULL | `hotels.hotel_name` |
| `rating` | 92% | ✅ FULL | `hotels.star_rating` |
| `address` | 100% | ✅ FULL | `hotels` (multi-column) |
| `geoPosition` | 100% | ✅ FULL | `hotels.latitude/longitude` |
| `services` | 100% | ✅ FULL | `hotels_all_services` |
| `conditions` | 92% | ✅ FULL | `hotels_policies` |
| `toConsider` | 85% | ✅ FULL | `hotels_fine_print` + `hotels_legal` |
| `images` | 100% | ✅ FULL | `image_downloads` |
| `scoreReview` | 100% | ✅ FULL | `hotels.review_score` |
| `scoreReviewBasedOn` | 92% | ✅ FULL | `hotels.review_count` |
| `accommodationType` | 100% | ✅ FULL | `hotels.atnm_en` |
| `extraInfo` | 85% | ✅ FULL | `hotels_extra_info` |
| `longDescription` | 100% | ✅ FULL | `hotels_description` |
| `categoryScoreReview` | 100% | ✅ FULL | `hotels_guest_reviews` |
| `nearbyPlaces` | 100% | ✅ FULL | `hotels_nearby_places` |
| `guestValues` | 92% | ✅ FULL | `hotels_faqs` |
| `seoDescription` | 100% | ✅ FULL | `hotels_seo` |
| `keywords` | 100% | ✅ FULL | `hotels_seo` |
| `roomsQuantity` | 69% | ⚠️ PARTIAL | `hotels.rooms_quantity` |
| `rooms` | 69% | ⚠️ PARTIAL | `hotels_room_types` |
| `reviews` | 15% | ⚠️ PARTIAL | `hotels_individual_reviews` |
| `priceRange` | 0% | ❌ N/A | `hotels.price_range` |

### 1.3 Limitations

| Field | Limitation | Reason |
|-------|-----------|--------|
| `priceRange` | Always `null` | Requires check-in/check-out date parameters in the URL. Booking.com does not show prices on static pages. |
| `roomsQuantity` | NULL ~31% of hotels | Also requires date parameters to render the room table. |
| `rooms.adults/children` | Often NULL | Room occupancy data requires date parameters. Room names are available. |
| `reviews` | Empty for 11/14 hotels | Booking.com only renders individual review cards in static HTML for hotels with ≤10 total reviews. |

---

## 2. API STRUCTURE

### 2.1 Request Format

```
PATCH https://web.com/api/en/{api_key}/update/{hotel_id}.json
Content-Type: application/json
```

**Replace:**
- `{api_key}` → your API key (e.g. `543-clave-api`)
- `{hotel_id}` → Booking.com `hotel_id_booking` value from the `hotels` table

### 2.2 Payload Structure

```json
{
    "data": {
        "name":               { "en": "...", "es": "..." },
        "rating":             0,
        "address":            { "en": "...", "es": "..." },
        "geoPosition":        { "latitude": 0.0, "longitude": 0.0 },
        "services":           { "en": [...], "es": [...] },
        "conditions":         { "en": [...], "es": [...] },
        "toConsider":         { "en": "...", "es": "..." },
        "images":             ["https://..."],
        "scoreReview":        9.2,
        "scoreReviewBasedOn": null,
        "roomsQuantity":      0,
        "accommodationType":  "hotel",
        "priceRange":         null,
        "extraInfo":          null,
        "longDescription":    { "en": "...", "es": "..." },
        "reviews":            { "en": [...], "es": [...] },
        "categoryScoreReview":{ "en": {...}, "es": {...} },
        "rooms":              { "en": [...], "es": [...] },
        "nearbyPlaces":       { "en": [...], "es": [...] },
        "guestValues":        { "en": [...], "es": [...] },
        "seoDescription":     { "en": "...", "es": "..." },
        "keywords":           { "en": "...", "es": "..." }
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

### 2.3 Rules

| Rule | Description |
|------|-------------|
| `en` mandatory | English locale must always be included |
| `en` first | When mixing languages, `"en"` must appear first in every multilingual object |
| Text linebreaks | Use `\n` — never `<p>` HTML tags |
| Optional fields | Any field can be omitted; only `args.locales` is required |
| HTTP method | `PATCH` (updates existing record) |

---

## 3. FIELD REFERENCE

### 3.1 `name` — Hotel name per language

**Source:** `hotels.hotel_name`  
**Type:** `{ [lang]: string }`

```json
"name": {
    "en": "Villa Dvor",
    "es": "Villa Cerro Verde"
}
```

### 3.2 `rating` — Star rating

**Source:** `hotels.star_rating`  
**Type:** `number (0–5)` · Language-independent  
**Note:** Some resort-type properties may have `null` (not all properties have a star category).

```json
"rating": 4
```

### 3.3 `address` — Full address per language

**Source:** `hotels.street_address`, `hotels.postal_code`, `hotels.city_name`, `hotels.address_city`, `hotels.address_country`  
**Type:** `{ [lang]: string }`  
**Built by:** `_build_address()` — priority: `city_name` (Build 89) → `address_city` → `address_locality`

```json
"address": {
    "en": "Boro Sain 20, 6000 Ohrid, North Macedonia",
    "es": "Boro Sain 20, 6000 Ohrid, Macedonia del Norte"
}
```

### 3.4 `geoPosition` — Coordinates

**Source:** `hotels.latitude`, `hotels.longitude`  
**Type:** `{ latitude: float, longitude: float }` · Language-independent

```json
"geoPosition": { "latitude": 41.113532, "longitude": 20.794691 }
```

### 3.5 `services` — All hotel services grouped by category

**Source:** `hotels_all_services` (service + service_category)  
**Type:** `{ [lang]: [ { [category]: [string] } ] }`

```json
"services": {
    "en": [
        {
            "Internet": ["WiFi is available in all areas and is free of charge."],
            "Outdoors":  ["Sun terrace", "Garden", "BBQ facilities"]
        }
    ]
}
```

### 3.6 `conditions` — Check-in/out and policies

**Source:** `hotels_policies` (policy_name + policy_details)  
**Type:** `{ [lang]: [ { condition: string, detail: string } ] }`

```json
"conditions": {
    "en": [
        { "condition": "Check-in",  "detail": "From 3:00 PM to 10:00 PM" },
        { "condition": "Check-out", "detail": "From 8:00 AM to 11:00 AM" }
    ]
}
```

### 3.7 `toConsider` — Fine print and important notices

**Source:** `hotels_fine_print.fp` + `hotels_legal.legal_info` (concatenated with `\n`)  
**Type:** `{ [lang]: string }` — multi-paragraph text using `\n`

```json
"toConsider": {
    "en": "Guests are required to show a photo ID upon check-in.\nQuiet hours are between 22:00 and 08:00."
}
```

### 3.8 `images` — Photo URLs

**Source:** `image_downloads` (category = `highres_url` → fallback `large_url`)  
**Type:** `[string]` · Language-independent  
**Note:** Build 90 — up to 273 photos per hotel. `highres_url` (max1280x900) for first ~45; `large_url` (max1024x768) for remainder.

```json
"images": [
    "https://cf.bstatic.com/xdata/images/hotel/max1280x900/146556730.jpg?k=...",
    "https://cf.bstatic.com/xdata/images/hotel/max1024x768/580336162.jpg?k=..."
]
```

### 3.9 `scoreReview` — Overall review score

**Source:** `hotels.review_score`  
**Type:** `number (0–10)` · Language-independent

```json
"scoreReview": 9.2
```

### 3.10 `scoreReviewBasedOn` — Number of reviews

**Source:** `hotels.review_count`  
**Type:** `integer | null` · Language-independent

```json
"scoreReviewBasedOn": 1647
```

### 3.11 `roomsQuantity` — Number of room types

**Source:** `hotels.rooms_quantity`  
**Type:** `integer | null` · Language-independent  
**Note:** NULL when URL has no date parameters (~31% of hotels).

### 3.12 `accommodationType` — Property type

**Source:** `hotels.atnm_en` (primary, Build 89) → `hotels.accommodation_type`  
**Type:** `string` · Language-independent  
**Values:** `"hotel"`, `"resort"`, `"guest_house"`, `"apartment"`, `"villa"`, etc.

```json
"accommodationType": "hotel"
```

### 3.13 `priceRange` — Nightly price range

**Source:** `hotels.price_range`  
**Type:** `string | null` · Language-independent  
**Always `null`** — requires check-in/checkout date URL parameters.

### 3.14 `extraInfo` — Extra hotel information

**Source:** `hotels_extra_info.extra_info`  
**Type:** `{ [lang]: string | null }`  
**Contains:** "Good to know" block with parking, pets, smoking, and other property-specific info.

### 3.15 `longDescription` — Full property description

**Source:** `hotels_description.description`  
**Type:** `{ [lang]: string }`

```json
"longDescription": {
    "en": "Essential Facilities: Villa Dvor offers a sun terrace and free WiFi.\n\nComfortable Accommodations: Rooms include private bathrooms."
}
```

### 3.16 `reviews` — Individual guest reviews

**Source:** `hotels_individual_reviews`  
**Type:** `{ [lang]: [ { name, score, title, comments: {positive, negative}, country, bookingId } ] }`  
**Limitation:** Only populated for hotels with ≤10 total reviews. For 11/14 hotels in the dataset, this field returns `[]`.

```json
"reviews": {
    "en": [
        {
            "name":     "Shelly",
            "score":    10,
            "title":    "Amazing stay",
            "comments": { "positive": "Great location", "negative": "None" },
            "country":  "United States",
            "bookingId": null
        }
    ]
}
```

### 3.17 `categoryScoreReview` — Category review scores

**Source:** `hotels_guest_reviews` (category text + score)  
**Type:** `{ [lang]: { hotel_services, hotel_clean, hotel_comfort, hotel_value, hotel_location, hotel_wifi, total } }`

```json
"categoryScoreReview": {
    "en": {
        "hotel_services":  { "category": "Facilities",    "score": 9.1 },
        "hotel_clean":     { "category": "Cleanliness",   "score": 9.3 },
        "hotel_comfort":   { "category": "Comfort",       "score": 9.2 },
        "hotel_value":     { "category": "Value for money","score": 9.3 },
        "hotel_location":  { "category": "Location",      "score": 9.4 },
        "hotel_wifi":      { "category": "Free Wifi",     "score": 9.3 },
        "total":           { "category": "Total",         "score": 9.2 }
    }
}
```

### 3.18 `rooms` — Room types

**Source:** `hotels_room_types`  
**Type:** `{ [lang]: [ { name, adults, children, description, images, info, facilities } ] }`  
**Note:** `adults` and `children` are NULL for most hotels (require date parameters).

```json
"rooms": {
    "en": [
        {
            "name":        "Double Room with Garden View",
            "adults":      2,
            "children":    1,
            "description": "This double room features soundproofing.",
            "images":      ["https://cf.bstatic.com/..."],
            "info":        null,
            "facilities":  []
        }
    ]
}
```

### 3.19 `nearbyPlaces` — Points of interest

**Source:** `hotels_nearby_places`  
**Type:** `{ [lang]: [ { name, distance, category } ] }`  
**Category codes:** 1=Airport, 2=Restaurant, 3=Beach, 4=Transport, 5=Nature, 6=Attraction

```json
"nearbyPlaces": {
    "en": [
        { "name": "St. Andrew's Church", "distance": "0.1 miles", "category": 1 }
    ]
}
```

### 3.20 `guestValues` — FAQs

**Source:** `hotels_faqs`  
**Type:** `{ [lang]: [ { topic, topicComments } ] }`

```json
"guestValues": {
    "en": [
        {
            "topic":         "Do your rates include access to the spa?",
            "topicComments": "Our rates include access to the pool and sauna."
        }
    ]
}
```

### 3.21 `seoDescription` — SEO meta description

**Source:** `hotels_seo.seo_description`  
**Type:** `{ [lang]: string }`

### 3.22 `keywords` — SEO keywords

**Source:** `hotels_seo.keywords`  
**Type:** `{ [lang]: string }` — comma-separated keyword list

---

## 4. ENDPOINTS

BookingScraper Pro provides two endpoints to generate the API payload:

### 4.1 `GET /hotels/url/{url_id}/api-payload`

Generates the complete payload for a single hotel aggregating data from 14 tables.

```bash
curl -X GET "http://localhost:8000/hotels/url/{url_id}/api-payload" \
     -H "Authorization: Bearer {API_KEY}"
```

**Response:** Full `{"data": {...}, "args": {...}}` payload in `_API_.md` format.

### 4.2 `POST /export/payload/{url_id}` (dry run)

Returns the filtered payload with optional field/language selection.

```bash
curl -X POST "http://localhost:8000/export/payload/{url_id}?languages=en,es&fields=name,address,scoreReview" \
     -H "Authorization: Bearer {API_KEY}"
```

**Query params:**
- `fields` — comma-separated API field names (default: all recommended)
- `languages` — comma-separated locale codes (default: all scraped languages; `en` always included)

### 4.3 `POST /export/batch`

Exports all hotels with `status=done` to the external API.

```bash
# Dry run (preview only)
curl -X POST "http://localhost:8000/export/batch?dry_run=true&languages=en,es" \
     -H "Authorization: Bearer {API_KEY}"

# Live export to external API
curl -X POST "http://localhost:8000/export/batch?dry_run=false&base_url=https://web.com/api&api_key_ext=543-clave-api" \
     -H "Authorization: Bearer {API_KEY}"
```

**Query params:**
- `dry_run` — `true` (default) or `false`
- `fields` — comma-separated field names
- `languages` — comma-separated locale codes
- `base_url` — external API base URL (required when `dry_run=false`)
- `api_key_ext` — external API key (required when `dry_run=false`)

---

## 5. EXPORT WORKFLOW

```
Step 1: Verify data is scraped
  GET /scraping/status
  → confirm all URLs have status = "done"

Step 2: Preview single hotel payload
  GET /hotels/url/{url_id}/api-payload
  → inspect the payload structure
  → note any null fields (priceRange, rooms.adults, reviews)

Step 3: Preview batch (dry run)
  POST /export/batch?dry_run=true&languages=en,es
  → review {total, success, failed, skipped}
  → check validation_errors for any hotels

Step 4: Export to external API
  POST /export/batch?dry_run=false
                     &base_url=https://web.com/api
                     &api_key_ext=543-clave-api
                     &languages=en,es
  → monitor {success, failed}
  → check errors array for any failed hotels
```

---

## 6. API CALL EXAMPLES

### 6.1 Minimal update (name + score only)

```bash
curl -X PATCH "https://web.com/api/en/543-clave-api/update/3607049.json" \
     -H "Content-Type: application/json" \
     -d '{
    "data": {
        "name":        { "en": "Villa Dvor", "es": "Villa Cerro Verde" },
        "scoreReview": 9.2
    },
    "args": { "locales": ["en", "es"] }
}'
```

### 6.2 Full hotel update — all available fields

```bash
curl -X PATCH "https://web.com/api/en/543-clave-api/update/3607049.json" \
     -H "Content-Type: application/json" \
     -d '{
    "data": {
        "name": { "en": "Villa Dvor", "es": "Villa Cerro Verde" },
        "rating": 4,
        "address": {
            "en": "Boro Sain 20, 6000 Ohrid, North Macedonia",
            "es": "Boro Sain 20, 6000 Ohrid, Macedonia del Norte"
        },
        "geoPosition": { "latitude": 41.113532, "longitude": 20.794691 },
        "accommodationType": "guest_house",
        "scoreReview": 9.2,
        "scoreReviewBasedOn": 67,
        "roomsQuantity": 6,
        "priceRange": null,
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
        "images": ["https://cf.bstatic.com/xdata/images/hotel/max1280x900/146556730.jpg?k=..."],
        "nearbyPlaces": {
            "en": [{ "name": "Saraiste Beach", "distance": "0.3 miles", "category": 3 }],
            "es": [{ "name": "Playa Saraiste", "distance": "0.4 kms",   "category": 3 }]
        },
        "categoryScoreReview": {
            "en": {
                "hotel_services":  { "category": "Facilities",     "score": 9.1 },
                "hotel_clean":     { "category": "Cleanliness",    "score": 9.3 },
                "hotel_comfort":   { "category": "Comfort",        "score": 9.2 },
                "hotel_value":     { "category": "Value for money","score": 9.3 },
                "hotel_location":  { "category": "Location",       "score": 9.4 },
                "hotel_wifi":      { "category": "Free Wifi",      "score": 9.3 },
                "total":           { "category": "Total",          "score": 9.2 }
            }
        },
        "seoDescription": {
            "en": "Villa Dvor features garden accommodations in Ohrid, a 9-minute walk from Church of St. John.",
            "es": "Villa Dvor ofrece alojamiento con jardín en Ohrid, a 9 minutos de la iglesia de San Juan."
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
}'
```

---

## 7. FIELD LIMITATIONS

| Field | Behaviour | Recommendation |
|-------|-----------|----------------|
| `priceRange` | Always `null` | Omit from payload — never include |
| `reviews` | `[]` for most hotels | Include field; API accepts empty array |
| `rooms.adults/children` | Often `null` | Include rooms array with name/description; omit occupancy |
| `roomsQuantity` | NULL ~31% | Send `0` when NULL |
| `rating` | NULL for some resort properties | Send `0` when NULL |

---

## 8. VERIFICATION QUERIES

### 8.1 Check payload readiness before export

```sql
-- Hotels ready for API export (status=done, English scraped)
SELECT
    uq.external_ref,
    h.hotel_name,
    h.hotel_id_booking,
    h.city_name,
    h.atnm_en,
    h.review_score,
    h.star_rating,
    COUNT(DISTINCT hd.id)   AS descriptions,
    COUNT(DISTINCT has_.id) AS services,
    COUNT(DISTINCT hp.id)   AS policies,
    COUNT(DISTINCT hgr.id)  AS review_scores,
    COUNT(DISTINCT id_.id)  AS images
FROM url_queue uq
JOIN hotels h          ON h.url_id = uq.id AND h.language = 'en'
LEFT JOIN hotels_description   hd  ON hd.url_id = uq.id AND hd.language = 'en'
LEFT JOIN hotels_all_services  has_ ON has_.url_id = uq.id AND has_.language = 'en'
LEFT JOIN hotels_policies      hp  ON hp.url_id = uq.id AND hp.language = 'en'
LEFT JOIN hotels_guest_reviews hgr ON hgr.url_id = uq.id AND hgr.language = 'en'
LEFT JOIN image_downloads      id_ ON id_.hotel_id = h.id AND id_.category = 'large_url'
WHERE uq.status = 'done'
GROUP BY uq.external_ref, h.hotel_name, h.hotel_id_booking,
         h.city_name, h.atnm_en, h.review_score, h.star_rating
ORDER BY uq.external_ref;
```

### 8.2 Get hotel_id_booking for API URL construction

```sql
SELECT
    uq.external_ref,
    h.hotel_name,
    h.hotel_id_booking,
    uq.external_url
FROM url_queue uq
JOIN hotels h ON h.url_id = uq.id AND h.language = 'en'
WHERE uq.status = 'done'
ORDER BY uq.external_ref;
```

---

*Guide generated: 2026-04-12 · BookingScraper Pro v6.0.0 Build 90*
