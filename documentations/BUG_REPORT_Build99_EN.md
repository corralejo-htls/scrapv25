# Bug Report — BookingScraper Pro v6.0.0 Build 99

**Date:** 2026-05-05
**Build:** 99 (previous: 98)
**Platform:** Windows 11 Pro / Python 3.14 / PostgreSQL 14+
**Schema:** schema_v77_complete.sql (header updated to build 99; no structural changes)
**Source:** FINAL_Audit_Data_Extraction_EN.md (2026-05-05) + Master_Audit_Prompt_BookingScraper_EN.md

---

## Executive Summary

| ID | Priority | Type | File(s) Modified | Status |
|----|----------|------|-----------------|--------|
| BUG-SVC-DOM-001-FIX | 🔴 CRITICAL | Strategy Reorder | `extractor.py` | ✅ Fixed |
| ENHANCE-GID-001 | 🟡 MEDIUM | Data Quality | `extractor.py`, `languages.json` | ✅ Done |
| GAP-VER-001 | 🟢 LOW | Version Sync | `config.py`, `__init__.py`, `schema_v77_complete.sql` | ✅ Done |

**Schema changes:** Header comment only (build number: 96 → 99).
**ORM changes:** None.
**API contract changes:** None.
**Re-scraping required:** YES — all 11 successfully scraped URLs must be re-scraped. Current `hotels_all_services` data is incomplete for hotels with rich amenity sets.

---

## BUG-SVC-DOM-001-FIX — Apollo JSON Blocking DOM Expansion Data

### Classification
**Priority:** 🔴 CRITICAL
**Type:** Strategy ordering error — data loss
**Module:** `app/extractor.py` → `_extract_all_services()`

### Root Cause

The audit (`FINAL_Audit_Data_Extraction_EN.md`, 2026-05-05) compared database records against live Booking.com page screenshots for two hotels:

| Hotel | DB Items | Page Items | Data Loss | NULL Categories |
|-------|----------|------------|-----------|-----------------|
| vidimo se (78309) | 18 | ~19 unique | ~5% | 61% (11/18) |
| wild & bolz eMotel (78465) | 6 | ~45 | **87%** | 0% (misleading) |

**The scraper was correctly clicking "See all facilities"** via `_expand_facilities()` (verified in `scraper.py` lines 573–653). After the click, Selenium captures an expanded `page_source` containing full `facility-group` DOM elements with all category headings.

**However**, `_extract_all_services()` was ordered with **Strategy 0 (Apollo JSON) first**:

```
Build 98 Strategy Order (WRONG):
  0. Apollo JSON cache    → threshold >=5 → RETURN EARLY ← BUG IS HERE
  1. DOM: property-section--facilities + facility-group
  1.5. DOM: facility-group standalone
  2. DOM: facilit* regex
  3. Popular-wrapper fallback
```

The Apollo JSON embedded in the page contains only the hotel's `BaseFacility` objects — a **hotel-level subset** of 5–20 items, not the full expanded facility list. For wild & bolz eMotel:
- Apollo JSON: **6** `BaseFacility` objects (≥ 5 threshold met)
- Strategy 0 fires → returns 6 items → **never reaches DOM strategies**
- DOM after expansion: **~45 items** across 17 sections — never processed

This explains why vidimo se (simple hotel) suffered only 5% loss while wild & bolz eMotel (rich hotel) suffered 87% loss: **data loss scales with hotel amenity richness**, not with scraper failure.

### Technical Evidence

From `pruebas/78465__wild & bolz eMotel.html` (non-expanded):
- `property-facilities-block-container` exists but is **empty** (React hydrates on client)
- Apollo JSON: 6 `BaseFacility` objects (groupIds: 1, 3, 7, 11, 16)
- Popular wrapper: only 3 items (Free parking, Free WiFi, Non-smoking rooms)

Screenshot evidence (`pruebas/78465__services_.jpg`): **17 categories, ~45 items** visible after page expansion:
- Great for your stay, Private bathroom, Bedroom, View, Room amenities, Pets, Living Area, Media & Technology, Food & Drink, Internet, Free parking, Services, Reception services, Safety & security, General, Accessibility, Languages spoken

### Fix Applied

**File:** `app/extractor.py`

Reordered strategies in `_extract_all_services()`:

```
Build 99 Strategy Order (CORRECT):
  1.   DOM: property-section--facilities + facility-group  ← PRIMARY
  1.5. DOM: facility-group standalone
  2.   DOM: facilit* regex
  3.   Apollo JSON cache (moved here, now FALLBACK)        ← was position 0
  4.   Popular-wrapper (last resort)
```

The Apollo JSON strategy now fires **only if all DOM strategies yield 0 items**, which indicates that Selenium's `_expand_facilities()` could not click the "See all facilities" button (page was blocked, timed out, or had no such button). In that case, JSON serves as the best available fallback.

### Expected Results After Fix

| Hotel | Before Fix | After Fix | Change |
|-------|-----------|-----------|--------|
| wild & bolz eMotel | 6 items, 0% NULL | ~45 items, ~0% NULL | +39 items |
| vidimo se | 18 items, 61% NULL | ~19 items, ~5% NULL | +1 item, -11 NULLs |
| Hotels with DOM expansion | 5–20 items | 20–50 items | ~3–7× improvement |
| Hotels where expansion fails | 5–20 items | 5–20 items | No regression |

### Why This Fix Does Not Break BUG-SVC-002-FIX (Build 98)

Build 98 added a filter in `api_payload_builder.py` to exclude groupId=15 ("Room Amenities") from `services[]`. This filter remains active. With DOM expansion:

- "Room amenities" as a DOM category name will still be filtered (the label matches `room_level_category_labels` in `languages.json`)
- New DOM categories ("Private bathroom", "Bedroom", etc.) will flow through to `services[]`
- These ARE legitimate hotel facilities listed on Booking.com's facilities page

Note: Items like Towels, Toilet paper in "Private bathroom" section are valid hotel-advertised amenities. The `services[]` API consumer receives richer, more accurate data.

---

## ENHANCE-GID-001 — Extended Facility Group Map (10 New GroupIds)

### Classification
**Priority:** 🟡 MEDIUM
**Type:** Data quality enhancement (JSON fallback coverage)
**Modules:** `app/extractor.py` (`_FACILITY_GROUP_MAP`), `languages.json` (`facility_group_map`)

### Rationale

The `_FACILITY_GROUP_MAP` previously contained only 12 groupIds (1,3,7,11,12,13,15,16,21,23,25,26). When the Apollo JSON strategy runs as fallback (DOM failed), groupIds for Private bathroom, Bedroom, Safety & security, etc. would resolve to category="" (empty), causing NULL categories in the database.

### Added GroupIds

| GroupId | English Label | Spanish Label |
|---------|--------------|---------------|
| 2 | Private bathroom | Baño privado |
| 4 | Bedroom | Dormitorio |
| 5 | View | Vistas |
| 6 | Pets | Mascotas |
| 9 | Media & Technology | Medios y tecnología |
| 10 | Living Area | Zona de estar |
| 14 | Safety & security | Seguridad |
| 17 | Accessibility | Accesibilidad |
| 19 | Reception services | Servicios de recepción |
| 24 | Languages spoken | Idiomas hablados |

All 6 scraping languages covered: `en`, `es`, `de`, `fr`, `it`, `pt`.

**Important disclaimer:** These groupId assignments are inferred from the DOM category names visible in the Booking.com facility block screenshot. They cannot be verified from the pre-expansion Apollo JSON (which does not contain these groupIds for hotels with few amenities). Actual groupId values will be confirmed when expanded HTML with these categories is available.

---

## GAP-VER-001 — Version Synchronization

**Files updated:**
- `app/config.py`: `BUILD_VERSION` default: 98 → 99; changelog line added
- `app/__init__.py`: `BUILD_VERSION` constant: 98 → 99
- `schema_v77_complete.sql`: Header comment: build 96 → build 99; CHANGELOG entry added

---

## Verification Steps After Deployment

1. **Re-scrape wild & bolz eMotel** (id_externo: 78465):
   ```sql
   SELECT service_category, COUNT(*) as n
   FROM hotels_all_services
   WHERE url_id = '81c6dfb4-6b44-4d67-b6fa-80e0049342da'
     AND language = 'en'
   GROUP BY service_category
   ORDER BY n DESC;
   ```
   **Expected:** ~8–12 distinct categories, total ~30–45 rows (vs. 6 rows before fix).

2. **Verify DOM strategy fires:**
   Celery logs should show:
   ```
   AllServices: strategy1+group (section+category): NN items lang=en
   ```
   NOT `strategy3-json`.

3. **Verify no regression for services[] API payload:**
   `GET /hotels/url/81c6dfb4-6b44-4d67-b6fa-80e0049342da/api-payload`
   → `data.services.en` should NOT contain "Toilet paper", "Linen", "Socket near the bed" (room items)
   → `data.services.en` SHOULD contain "Parking", "Free WiFi", "Fire extinguishers", "Invoice provided"

4. **Image download gap** (P2, deferred): 2.08 downloads/image instead of 3.0 expected.
   Action: Investigate `image_downloader.py` — this is tracked but not fixed in Build 99.

---

## Files Modified

| File | Change |
|------|--------|
| `app/extractor.py` | Strategy reorder in `_extract_all_services()`; `_FACILITY_GROUP_MAP` extended with 10 new groupIds; build header updated to Build 99 |
| `app/config.py` | `BUILD_VERSION` default: 98 → 99; changelog line added |
| `app/__init__.py` | `BUILD_VERSION`: 98 → 99 |
| `languages.json` | `facility_group_map`: 10 new groupId entries; `_doc` updated |
| `schema_v77_complete.sql` | Header: build 96 → 99; CHANGELOG entry added; no structural changes |

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| groupId assignments in new entries are inferred, not verified | Low — only affects JSON fallback path | DOM strategies now primary; JSON fallback rarely used |
| Re-scraping all URLs generates significant traffic | Medium | Stagger re-scrapes; use VPN rotation as configured |
| "Private bathroom" items now appear in services[] | Low | API consumers filter by category if needed; data is accurate |

---

*Report generated: 2026-05-05*
*Audit basis: FINAL_Audit_Data_Extraction_EN.md + Master_Audit_Prompt_BookingScraper_EN.md*
*Evidence: live page screenshot (78465), Apollo JSON analysis, HTML DOM inspection*
