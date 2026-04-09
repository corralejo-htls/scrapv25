# Technical Bug Report — BookingScraper Pro v6.0.0 Build 87
## Deep Audit: `hotels_all_services.service_category` Always Empty

**Date:** 2026-04-10  
**Scope:** Full trace from HTML DOM → Apollo JSON → extractor.py → DB  
**Evidence Base:** 15 HTML files in `pruebas/`, `pruebas/_table__hotels_all_services__.csv`, `app/extractor.py`  
**Schema Authority:** `schema_v77_complete.sql`  

---

## Executive Summary

The `service_category` field in `hotels_all_services` is **100% NULL** across all 7,108 records and all 6 languages. The root cause is not a single bug but **five interconnected defects** in `app/extractor.py`, affecting both the Apollo JSON strategy (wrong name resolution + no category output) and the DOM strategy (wrong icon `data-testid` + missing `<p>` in heading search).

---

## Data Evidence

```
hotels_all_services: 7,108 rows (13 hotels × ~6 langs × ~91 svcs)
service_category NULL/empty: 7,108 (100%)
service_category non-empty:       0 (  0%)
```

Sample CSV rows showing empty category:
```
id,hotel_id,url_id,language,service,service_category,created_at
1,...,en,Breakfast,,2026-04-09 07:30:42
2,...,en,Private bathroom,,2026-04-09 07:30:42
3,...,en,Air conditioning,,2026-04-09 07:30:42
```

---

## Root Cause Analysis: 5 Defects

### Defect A — `service_category` always `""` in Apollo JSON strategy

**File:** `app/extractor.py` — `_extract_all_services()` Strategy 0  
**Severity:** 🔴 Critical  

`_extract_services_from_json()` returned `List[str]`. The caller `_extract_all_services()` passed every result with `category=""`:

```python
# BEFORE (broken):
for svc in json_services:
    _add(svc, category="")   # ← always empty
```

**Fix:** `_extract_services_from_json()` now returns `List[Dict[str,str]]` with `{service, service_category}`. The caller uses the dict directly.

---

### Defect B — Wrong name resolution (ID namespace collision)

**File:** `app/extractor.py` — `_extract_services_from_json()`  
**Severity:** 🟠 High  

The method crossed `BaseFacility.id` values against `hotelfacility/name.items` keys. These are **two different ID namespaces**:

| `BaseFacility.id` | Correct name (from `instances`) | Old name (from `hotelfacility/name`) |
|---|---|---|
| 3 | Minibar | Restaurant ❌ |
| 89 | Kitchenware | Ticket service ❌ |
| 85 | Dining area | NOT FOUND ❌ |
| 433 | Indoor swimming pool | Swimming pool (approximate) |

**Evidence from HTML analysis:**
- `hotelfacility/name` IDs are display IDs (1–372)
- `BaseFacility.id` values are internal IDs (e.g. 433 for swimming pool)
- Overlap is coincidental and incomplete

**Fix:** Use `BaseFacility.instances[0].__ref.title` which contains the actual translated display name already in the requested language:

```python
# Instance object in Apollo JSON:
"instances": [{"__ref": 'Instance:{"id":1170776,"title":"Indoor swimming pool"}'}]

# Spanish page:
"instances": [{"__ref": 'Instance:{"id":...,"title":"Piscina al aire libre"}'}]
```

---

### Defect C — Wrong `data-testid` for facility icon

**File:** `app/extractor.py` — `_extract_all_services()` Strategy 1.5  
**Severity:** 🔴 Critical  

Strategy 1.5 attempts to remove the SVG facility icon before extracting the category heading text. The code searched for `data-testid="facility-group-icon"`, which **does not exist** in Booking.com's DOM. The actual testid is `"facility-icon"` (without the "group-" prefix).

```python
# BEFORE (broken):
icon_el = group.find(attrs={"data-testid": "facility-group-icon"})
# → always None — icon NOT removed — SVG text contaminates heading search

# AFTER (fixed):
icon_el = group.find(attrs={"data-testid": "facility-icon"})
```

**Evidence:** Grep of all 15 HTML files in `pruebas/`:
```
facility-group-icon occurrences: 0   ← testid used in code — NEVER EXISTS
facility-icon occurrences:       20  ← actual testid in DOM
```

---

### Defect D — Missing `<p>` tag in facility category heading search

**File:** `app/extractor.py` — `_extract_all_services()` Strategy 1.5  
**Severity:** 🟠 High  

After removing the icon, the code searched for the category heading in `["div", "span", "h3", "h4"]` elements only. The actual Booking.com DOM uses `<p>` for the group heading in the expanded facilities section:

```html
<!-- Actual Booking.com structure (post-expansion): -->
<div data-testid="facility-group">
  <span data-testid="facility-icon" aria-hidden="true"><svg/></span>
  <div>
    <p class="...">Internet</p>   ← <p> NOT in the search list!
    <ul><li>Free WiFi</li></ul>
  </div>
</div>
```

**Fix:** Add `"p"` to the tag list:
```python
for child in content_div.find_all(
    ["div", "span", "h3", "h4", "p"],  # added "p"
    recursive=False
):
```

---

### Defect E — Apollo JSON threshold too high (>=30)

**File:** `app/extractor.py` — `_extract_all_services()` Strategy 0  
**Severity:** 🟠 High  

Strategy 0 only used the Apollo JSON result if it returned ≥30 items. Apollo JSON only contains hotel-level `BaseFacility` objects — the actual count is **5–25 per hotel** (never 30+). This caused the strategy to always fall through to the popular-wrapper fallback (which has no category and only ~10 items).

```python
# BEFORE (broken):
if json_services and len(json_services) >= 30:  # impossible threshold

# AFTER (fixed):
if json_services and len(json_services) >= 5:   # realistic minimum
```

---

## Fix Verification

The corrected logic was validated against all available HTML test files:

**Golden Beach Resort (EN):**
```
[Pool & Wellness     ] Indoor swimming pool
[Parking             ] Parking
[Internet            ] Internet services
[General             ] Family rooms
[General             ] Airport shuttle
[Food & Drink        ] Minibar
[Kitchen             ] Kitchenware
[Kitchen             ] Microwave
```

**The Pink Sands Club (ES):**
```
[Piscina y bienestar ] Piscina al aire libre
[Exteriores y vistas ] Situado frente a la playa
[Alimentos y bebidas ] Bar
[Alimentos y bebidas ] Restaurante
[Internet            ] Internet
```

---

## Facility Group Map

The static `_FACILITY_GROUP_MAP` resolves Booking.com `groupId` → category name (6 languages):

| groupId | EN | ES | DE | FR | IT | PT |
|---------|----|----|----|----|----|----|
| 1 | General | General | Allgemein | Général | Generale | Geral |
| 3 | Services | Servicios | Dienstleistungen | Services | Servizi | Serviços |
| 7 | Food & Drink | Alimentos y bebidas | Speisen & Getränke | Alimentation | Cibo e bevande | Comida e bebidas |
| 11 | Internet | Internet | Internet | Internet | Internet | Internet |
| 12 | Kitchen | Cocina | Küche | Cuisine | Cucina | Cozinha |
| 13 | Outdoors & View | Exteriores y vistas | Außenbereich | Extérieur | Spazi esterni | Exterior |
| 15 | Room Amenities | Comodidades | Zimmerausstattung | Équipements | Dotazioni camera | Comodidades |
| 16 | Parking | Aparcamiento | Parken | Parking | Parcheggio | Estacionamento |
| 21 | Pool & Wellness | Piscina y bienestar | Pool & Wellness | Piscine & bien-être | Piscina & benessere | Piscina e bem-estar |
| 23 | Reception | Recepción | Rezeption | Réception | Ricevimento | Recepção |
| 25 | Family & Kids | Familia e hijos | Familie & Kinder | Famille & Enfants | Famiglia e bambini | Família e crianças |
| 26 | Cleaning Services | Limpieza | Reinigung | Nettoyage | Pulizia | Limpeza |

---

## Secondary Finding: Room-Level Facilities in hotels_all_services

The current data in `hotels_all_services` (200+ items per hotel) includes **room-level facilities** (`Private bathroom`, `Toilet paper`, `Hairdryer`, `Flat-screen TV`) that belong to the room, not the hotel. These originate from the Selenium-expanded DOM which loads all facilities including room-specific ones after the "See all N facilities" click.

This is a data quality issue (not a code bug) — `hotels_all_services` mixes hotel and room facilities. The `_API_.md` `services[]` field is intended for hotel-level services only. The Apollo JSON strategy (now primary) correctly returns **only hotel-level** `BaseFacility` objects (5–25 items), while the DOM strategies return the mixed set.

**Status:** Data quality concern, documented. No immediate code change required. Addressed by the priority of Apollo JSON strategy (now uses >=5 threshold).

---

## Files Modified

| File | Changes |
|------|---------|
| `app/extractor.py` | BUG-SVC-CAT-001-FIX (A,B,C,D,E) + BUG-SVC-NAME-001-FIX |

---

*Build 87 — Audit: `service_category` empty defect — 2026-04-10*
