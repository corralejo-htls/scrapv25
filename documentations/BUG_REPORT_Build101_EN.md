# 🟠 BUG REPORT — BookingScraper Pro Build 101
## BUG-SVC-NULL-001: NULL service_category epidemic in hotels_all_services
### Date: 2026-05-05 | Audited Hotels: 78465, 78309, 76569

---

## 1. EXECUTIVE SUMMARY

Build 99 successfully fixed the catastrophic data loss (87% item loss) by reordering
extraction strategies (DOM strategies now run before Apollo JSON fallback). Build 101
addresses the remaining critical issue: **NULL categories for 40–60% of all extracted
service items** in the three audited hotels.

| Hotel | ID | NULL Before (Build 99) | NULL Expected After (Build 101) | Improvement |
|---|---|---|---|---|
| wild & bolz eMotel | 78465 | 22/37 = **59%** | <4/37 = **<11%** | ~48 pp |
| vidimo se | 78309 | 11/18 = **61%** | <2/18 = **<11%** | ~50 pp |
| Hotel Aquamarin | 76569 | 34/57 = **60%** | <6/57 = **<11%** | ~49 pp |

---

## 2. ROOT CAUSE ANALYSIS

### 2.1 Insufficient `_SERVICE_CATEGORY_RULES`

`_infer_service_category()` is called:
- When the DOM strategy does not provide a facility-group heading (category = "")
- As a post-process for items extracted without category context

The pre-Build-101 rules only covered **5 categories**: Food & Drink, Outdoors & View,
Services (partial), General (partial), Room Amenities. Seven critical categories were
completely absent:

| Missing Category | groupId | Example NULL Items |
|---|---|---|
| Languages spoken | 24 | German, Alemán, Croatian, Serbian, Bosnian |
| Pets | 6 | Pets are allowed, Admite mascotas |
| Safety & security | 14 | Fire extinguishers, CCTV, Smoke alarms, Key card access |
| Accessibility | 17 | Upper floors accessible by elevator |
| Reception services | 19 | Invoice provided, Proporciona factura |
| Internet (descriptive) | 11 | WiFi is available in all areas…, WiFi gratis |
| Parking (extended) | 16 | Electric vehicle charging station, Free parking, Private parking |

Additionally, several items were **miscategorized**:
- `"English"`, `"Inglés"`, `"Anglais"` → **Services (3)** instead of **Languages spoken (24)**
- Missing General keywords: lift/ascensor, hardwood floors, heating, calefacción

### 2.2 `_add()` did not apply inference as fallback

The `_add()` function inside `_extract_all_services()` stored items with `category=""`
directly without attempting keyword inference. This meant:
- Items from facility-group headings that failed DOM extraction → NULL
- Items from Strategy 1 flat-list → NULL (no inference applied)
- Items from Strategy 4 (popular-wrapper) → category inferred, but only for covered rules

### 2.3 `GenericFacilityHighlight` objects not extracted

The Apollo JSON cache contains `GenericFacilityHighlight` objects (e.g., Private bathroom,
Shower, Free parking, Key card access) with `title` but no `groupId`. These were not
processed by `_extract_services_from_json()`, leaving additional items uncaptured.

---

## 3. FIXES APPLIED (Build 101)

### Fix 1: `_add()` auto-inference fallback

**File:** `app/extractor.py`  
**Function:** `_extract_all_services()` → nested `_add()`

```python
# BEFORE (Build 99):
services.append({
    "service": t,
    "service_category": (category or "").strip()[:128],
})

# AFTER (Build 101):
resolved_category = (category or "").strip()
if not resolved_category:
    resolved_category = self._infer_service_category(t, lang_key)
services.append({
    "service": t,
    "service_category": resolved_category[:128] if resolved_category else "",
})
```

**Impact:** ALL items with empty category heading now receive automatic inference.
This guarantees consistent categorization regardless of whether the facility-group
DOM heading was successfully captured.

### Fix 2: Expanded `_SERVICE_CATEGORY_RULES`

**File:** `app/extractor.py`  
**Class attribute:** `HotelExtractor._SERVICE_CATEGORY_RULES`

7 new category groups added. Rule order changed to prevent conflicts:

1. **Languages spoken (24)** — FIRST (was absent; "English" was in Services)
2. **Pets (6)** — NEW: "pets are allowed", "admite mascotas", multi-lang
3. **Safety & security (14)** — NEW: fire extinguisher, CCTV, smoke alarm, key card
4. **Accessibility (17)** — NEW: "upper floors accessible by elevator", wheelchair
5. **Reception services (19)** — NEW: "invoice provided", "proporciona factura"
6. **Internet descriptive (11)** — NEW: "WiFi is available in all areas…", "WiFi gratis"
7. **Food & Drink (7)** — Extended: wine/champagne, minibar added
8. **Parking (16)** — Extended: EV charging, free/private/accessible parking multi-lang
9. **Services (3)** — Fixed: removed language names (moved to #1); added shared lounge
10. **General (1)** — Extended: lift/ascensor, hardwood floors, heating/calefacción
11. **Room Amenities (15)** — Unchanged (catch-all)

**Total keywords added:** ~120 new keywords across 6 languages.

### Fix 3: `GenericFacilityHighlight` extraction in Apollo JSON

**File:** `app/extractor.py`  
**Function:** `_extract_services_from_json()`

The script scanning loop now also collects `GenericFacilityHighlight:` objects alongside
`BaseFacility:` objects. Since these have `title` but no `groupId`, `_infer_service_category()`
is applied to assign the correct category. Deduplication via `seen_titles` prevents conflicts.

---

## 4. IMPACT ASSESSMENT

| Finding | Files Affected | Risk Level |
|---|---|---|
| `_add()` auto-inference | extractor.py | Low (isolated) |
| `_SERVICE_CATEGORY_RULES` expansion | extractor.py | Low (additive, no renames) |
| GenericFacilityHighlight extraction | extractor.py | Low (deduplication in place) |
| Build version increment | config.py, `__init__.py` | Trivial |

**Dependencies:** No changes to schema, ORM, or API payload builder required.
`service_category` column already exists as `VARCHAR(128) NULL` since Build 82.

**API impact:** `GET /hotels/{hotel_id}` services array will show more items with
non-NULL `service_category` values. No breaking changes.

---

## 5. VERIFICATION CHECKLIST

| # | Check | Expected Result |
|---|---|---|
| 1 | Re-scrape wild & bolz eMotel (78465) | NULL categories < 4 of 37 items |
| 2 | Re-scrape vidimo se (78309) | NULL categories < 2 of 18 items |
| 3 | Re-scrape Hotel Aquamarin (76569) | NULL categories < 6 of 57 items |
| 4 | Verify "German" → Languages spoken | Not Services |
| 5 | Verify "Fire extinguishers" → Safety & security | Not NULL |
| 6 | Verify "Invoice provided" → Reception services | Not NULL |
| 7 | Verify "WiFi gratis" / "WiFi is available…" → Internet | Not NULL |
| 8 | Verify "Pets are allowed…" → Pets | Not NULL |
| 9 | Verify "Ascensor" / "Lift" → General | Not NULL |
| 10 | Verify "Hardwood or parquet floors" → General | Not NULL |

**SQL verification query:**
```sql
SELECT service_category,
       COUNT(*) as total,
       COUNT(CASE WHEN service_category IS NULL THEN 1 END) as null_count,
       ROUND(100.0 * COUNT(CASE WHEN service_category IS NULL THEN 1 END) / COUNT(*), 1) as null_pct
FROM hotels_all_services
WHERE url_id IN (
    SELECT url_id FROM hotels WHERE id_externo IN (78465, 78309, 76569)
)
AND language = 'en'
GROUP BY service_category
ORDER BY null_count DESC;
```

**Expected:** NULL row shows < 5 items total across the 3 hotels (was 67 before).

---

## 6. OUT OF SCOPE (Future Builds)

- **Wrong category assignments** (e.g., Flat-screen TV in Room Amenities instead of
  Media & Technology): These arise when DOM strategy 1.5 correctly captures the heading
  but it differs from the auditors' expectation. Fixing this would require changing
  the `_FACILITY_GROUP_MAP` translations or accepting Booking.com's category naming.
- **Image download gap** (2.08 downloads/image vs 3.0 expected): separate investigation needed.
- **3 failed URLs** (21% failure rate): VPN or Selenium session issue, not related to extraction.

---

## 7. FILES MODIFIED

| File | Change | Build |
|---|---|---|
| `app/extractor.py` | _add() inference fallback + expanded rules + GenericFacilityHighlight | 101 |
| `app/config.py` | BUILD_VERSION 99 → 101 | 101 |
| `app/__init__.py` | Build comment updated | 101 |

---

*Report generated: 2026-05-05 | Build: 101 | Author: Automated Technical Audit*
