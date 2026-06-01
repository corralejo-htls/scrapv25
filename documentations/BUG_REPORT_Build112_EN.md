# Bug Report — BookingScraper Pro v6.0.0 Build 112
## Audit: Build 111 → 112 | Image Pipeline, API Payload & Schema Integrity

**Report Date:** 2026-06-01  
**Build Analyzed:** 111 (committed code, GitHub `corralejo-htls/scrapv25`)  
**New Build:** 112  
**Schema Source of Truth:** `schema_v77_complete.sql`  
**API Contract:** `documentations/_API_.md`  
**Severity Distribution:** 1 Critical · 1 High · 1 Medium · 1 Low · 2 Advisory  

---

## 1. EXECUTIVE SUMMARY

This report covers the full audit of Build 111 code performed on 2026-06-01,
integrating the findings of the previously uploaded
`Technical_Audit_Report_Scrapv25_Image_API_Compliance_EN.md` (Build 109/110
scope) and a live code review of the current GitHub repository.

**Key findings in Build 111 code:**

| # | Bug ID | Severity | File | Root Cause |
|---|--------|----------|------|------------|
| 1 | BUG-ONLYTITLE-001 | 🔴 Critical | `api_payload_builder.py`, `api_export_system.py` | `args.onlyTitle` hardcoded `True` — all 20 non-title fields ignored by API |
| 2 | BUG-CONFIG-SYNC-001 | 🟠 High | `app/config.py` | `BUILD_VERSION` Pydantic default frozen at 107 (was 111 at time of audit) |
| 3 | BUG-VIEW-DEDUP-001 | 🟡 Medium | `schema_v77_complete.sql` | `v_api_export_images` returned 3 rows/photo (all sizes) despite claiming to prioritize `highres>large>thumb` |
| 4 | BUG-SVC-DOC-001 | 🔵 Low | `api_payload_builder.py` | Stale docstring described removed `_ROOM_LEVEL_CATEGORIES` filter as active |
| A | GAP-SCROLL-STABLE-001 | Advisory | `image_classifier.py` | Fixed scroll (8×1000 px) adequate for tested hotels; configurable for larger |
| B | GAP-ROOMS-HIGHRES-001 | Advisory | `api_payload_builder.py` | `rooms[].images` uses raw extraction URLs rather than classified `highres_url` |

**All 4 confirmed bugs are fixed in Build 112.**

---

## 2. BUILD 112 — CONFIRMED BUGS & FIXES

---

### BUG-ONLYTITLE-001 🔴 CRITICAL

**Title:** `args.onlyTitle` hardcoded `True` — 20 API fields silently suppressed

**Discovery Method:** Live code review of `api_payload_builder.py` + cross-reference with `_API_.md` contract.

**Root Cause (verified in two code paths):**

**Path 1 — Direct endpoint** `GET /hotels/url/{url_id}/api-payload`
```python
# app/api_payload_builder.py — Build 111 (BEFORE FIX)
args: Dict[str, Any] = {
    "seoFormatKey":  "",
    "onlyTitle":     True,   # ← hardcoded True
    "regenerateSeo": True,
    "append":        False,
    "cache":         True,
    "locales":       langs,
}
```
When `build_payload()` is called directly from the REST endpoint, the caller receives
`args.onlyTitle = True`. If this payload is forwarded to the external API as-is,
the API interprets it as "only process the `name`/title field" and ignores all
other 20 fields in `data[]` regardless of their content.

**Path 2 — `APIExporter` (production export path)**
```python
# app/api_export_system.py — ExportTemplate.args_config (Build 111)
args_config: Dict[str, Any] = field(default_factory=lambda: {
    "seoFormatKey": "",
    "onlyTitle": True,       # ← hardcoded True
    "regenerateSeo": True,
    "append": False,
    "cache": True,
})
```
`_filter_payload()` constructs the final `args` section from `template.args_config`,
OVERRIDING the `build_payload()` args entirely. This means ALL production exports
via `APIExporter` sent `onlyTitle=True`, causing the external API to process only
`name`/`longDescription` even when all 21 fields were correctly built in `data[]`.

**Impact:**
- `rating`, `address`, `geoPosition`, `services`, `conditions`, `toConsider`,
  `images`, `scoreReview`, `rooms`, `nearbyPlaces`, `guestValues`, `seoDescription`,
  `keywords`, and 7 other fields: all correctly built but **never updated in the
  external system**.
- The issue was masked because the test payloads (`payload_villa_dvor_1001.json`,
  etc.) used `onlyTitle=True` intentionally for connection testing, and the behavior
  appeared "correct" in that context.

**Fix (Build 112):**

1. New config toggle `API_EXPORT_ONLY_TITLE: bool = Field(default=False)` in `config.py`.
2. `build_payload()` reads the toggle:
   ```python
   only_title: bool = bool(getattr(self._cfg, "API_EXPORT_ONLY_TITLE", False))
   args = {"onlyTitle": only_title, ...}
   ```
3. `ExportTemplate.args_config` default updated:
   ```python
   "onlyTitle": False,  # was True
   ```

**Backward Compatibility:** Operators with saved template JSON files that contain
`"onlyTitle": true` are NOT affected — those files take precedence over the default.
To revert to test-mode behavior: set `API_EXPORT_ONLY_TITLE=true` in `.env`.

**Files modified:** `app/config.py`, `app/api_payload_builder.py`,
`app/api_export_system.py`, `app/__init__.py`.

---

### BUG-CONFIG-SYNC-001 🟠 HIGH

**Title:** `config.py` `BUILD_VERSION` Pydantic default frozen at 107

**Discovery Method:** `grep -n "BUILD_VERSION" app/config.py` vs `grep "^BUILD_VERSION" app/__init__.py`.

**Root Cause:**
```python
# app/config.py — Build 111 (BEFORE FIX)
BUILD_VERSION: int = Field(
    default=107,          # ← frozen since Build 107; never updated
    description="Incremental build number.",
)
```
```python
# app/__init__.py — Build 111 (correct)
BUILD_VERSION = 112       # incremented each session
```

Each build session updates:
- The comment header of `config.py` → updated correctly
- `BUILD_VERSION` in `app/__init__.py` → updated correctly
- The `default=` value of the Pydantic `Field` → **never updated since Build 107**

When `BUILD_VERSION` is not set in `.env` (most development environments),
`Settings().BUILD_VERSION` returns `107` instead of the actual build number.
Any log message, health-check endpoint, or monitoring system reading
`settings.BUILD_VERSION` reports a stale value, making build tracing unreliable.

**Fix (Build 112):**
```python
# app/config.py — Build 112 (AFTER FIX)
BUILD_VERSION: int = Field(
    default=112,
    description=(
        "Incremental build number. "
        "⚠️ MANTENER SINCRONIZADO con BUILD_VERSION en app/__init__.py "
        "al inicio de cada ciclo de build."
    ),
)
```
An explicit reminder was added to the `description` field to prevent future drift.

**Files modified:** `app/config.py`, `app/__init__.py`.

---

### BUG-VIEW-DEDUP-001 🟡 MEDIUM

**Title:** `v_api_export_images` returned 3 rows per gallery photo, not 1

**Discovery Method:** Schema analysis — `v_api_export_images` definition vs. its
documented contract ("Prioriza highres_url > large_url > thumb_url por foto").

**Root Cause:**
```sql
-- schema_v77_complete.sql — Build 111 (BEFORE FIX, simplified)
CREATE OR REPLACE VIEW v_api_export_images AS
SELECT i.hotel_id, i.id_photo, i.gallery_order,
       d.category, d.url, d.local_path, d.status
FROM image_data i
JOIN image_downloads d
      ON d.id_photo = i.id_photo AND d.hotel_id = i.hotel_id
WHERE i.gallery_visible = TRUE AND d.status = 'done'
ORDER BY i.hotel_id, i.gallery_order NULLS LAST, i.id_photo;
```
`image_downloads` stores **one row per size per photo** (`thumb_url`, `large_url`,
`highres_url`). The plain `JOIN` without `DISTINCT ON` produced up to 3 rows for
each `id_photo`, inflating counts by a factor of up to 3:

| Hotel | Gallery photos | View rows (before fix) | Expected |
|-------|---------------|------------------------|---------|
| Villa Dvor | 59 | up to 177 | 59 |
| Hotel Topazz | 38 | up to 114 | 38 |

The **Python code** (`_load_gallery_image_urls`) handled deduplication correctly
in memory and was unaffected. However, any **operator querying the view directly**
(e.g., for reporting, diagnostics, or custom integrations) would receive inflated
row counts and potentially duplicate URLs.

**Fix (Build 112):**
```sql
-- schema_v77_complete.sql — Build 112 (AFTER FIX)
CREATE OR REPLACE VIEW v_api_export_images AS
SELECT hotel_id, id_photo, gallery_order, category, url, local_path, status
FROM (
    SELECT DISTINCT ON (i.hotel_id, i.id_photo)
        i.hotel_id, i.id_photo, i.gallery_order,
        d.category, d.url, d.local_path, d.status
    FROM image_data i
    JOIN image_downloads d
          ON d.id_photo = i.id_photo AND d.hotel_id = i.hotel_id
    WHERE i.gallery_visible = TRUE AND d.status = 'done'
    ORDER BY
        i.hotel_id, i.id_photo,
        CASE d.category
            WHEN 'highres_url' THEN 1
            WHEN 'large_url'   THEN 2
            WHEN 'thumb_url'   THEN 3
            ELSE 4
        END
) sub
ORDER BY hotel_id, gallery_order NULLS LAST, id_photo;
```
`DISTINCT ON (hotel_id, id_photo)` with `CASE`-based ordering selects the best
available URL per photo. The outer `ORDER BY` applies `gallery_order` after
deduplication.

**Note:** No application restart needed — `CREATE OR REPLACE VIEW` is applied
on the next database recreation at startup (the DB is always dropped and
recreated from the SQL file).

**Files modified:** `schema_v77_complete.sql`, `app/__init__.py`.

---

### BUG-SVC-DOC-001 🔵 LOW

**Title:** Stale docstring in `api_payload_builder.py` described removed filter as active

**Discovery Method:** Cross-reference between module docstring (Build 98 language)
and actual code post-Build 103.

**Root Cause:**
The module-level docstring contained `BUG-SVC-002-FIX (Build 98)` describing
`_ROOM_LEVEL_CATEGORIES` — a set-based filter that excluded room-level amenity
categories from `services[]` in the API payload. This filter was **removed in
Build 103** along with `room_level_category_labels` from `languages.json` and
`category_key_map`. The docstring was never updated, causing confusion:
- Code reviewers would search for `_ROOM_LEVEL_CATEGORIES` and not find it.
- The `_load_services()` inline comment `# BUILD-103: room_level_category_labels
  removed` contradicted the module docstring.
- The stale text referenced a `BUG-SVC-002-FIX` that described behavior no
  longer present.

**Fix (Build 112):**
Module docstring fully replaced with accurate, current descriptions. `_load_services()`
docstring updated to reflect verbatim-DOM, no-filter state post-Build 103, with
explicit `BUG-SVC-DOC-001-FIX` note.

**Files modified:** `app/api_payload_builder.py`, `app/__init__.py`.

---

## 3. ADVISORY FINDINGS (No Code Change)

### GAP-SCROLL-STABLE-001 📋 Advisory

**Title:** Gallery modal scroll is fixed-iteration (8×1000 px)

**Context:** `GalleryModalExtractor._scroll_modal()` scrolls 8 iterations × 1000 px
= 8,000 px. Build 110 changelog confirms **136/136** photos captured for Jagdhof
Hubler (the largest test hotel). The config parameter `GALLERY_MODAL_SCROLL_ITERATIONS`
(default 8, max 40) allows operator adjustment without code change.

**For hotels with galleries > 200 images** (estimated scroll depth > 16,000 px),
operators should consider increasing `GALLERY_MODAL_SCROLL_ITERATIONS` to 16–20
in `.env`. No code change is needed; the existing config already provides this
flexibility.

**Status:** No fix required. Documented for operator awareness.

---

### GAP-ROOMS-HIGHRES-001 📋 Advisory

**Title:** `rooms[].images` uses raw extraction URLs, not classified `highres_url`

**Context:** `_build_rooms()` populates `rooms[].images` from
`hotels_room_types.images` (JSONB), which stores the URLs as extracted from
Booking.com during the scraping pass. These are typically `max1024x768`
(large_url) quality. Meanwhile, `image_data` records with `subcategory='room'`
have `highres_url` (`max1280x900`) available after the `PhotoClassifier` pass.

**Current behavior:** The API contract shows `max1024x768` URLs for room images
(`"images": ["https://cf.bstatic.com/.../max1024x768/147158994.jpg"]`), which
matches the current extraction. The `highres_url` upgrade is a data quality
improvement, not a compliance gap.

**Potential future improvement:** Cross-reference `hotels_room_types.images`
with `image_data.subcategory='room'` to substitute `highres_url` where
available. This would require a join in `_load_rooms()` + `_build_rooms()`.

**Status:** No fix in Build 112. Documented as a future enhancement.

---

## 4. AUDIT INTEGRATION — Previous Report Findings

The uploaded `Technical_Audit_Report_Scrapv25_Image_API_Compliance_EN.md` covered
builds 109/110. Verifying its action items against Build 111 code:

| Previous Gap | Status in Build 111/112 |
|---|---|
| **8.1** Full payload generation verification | ✅ All 21 `data[]` fields correctly built in `build_payload()`. BUG-ONLYTITLE-001 explains why API didn't process them — **fixed Build 112**. |
| **8.2** Room image association in `data.rooms[].images[]` | ⚠️ `_build_rooms()` uses raw JSONB URLs. Classified `highres_url` not used. See GAP-ROOMS-HIGHRES-001 (Advisory). |
| **8.3** Service category grouping | ✅ `_load_services()` correctly groups by `service_category` into `[{"Cat": ["item1",...]}]` matching `_API_.md` format. NULL → `"Other"`. |
| **8.4** `toConsider` plaintext | ✅ `_html_to_plaintext()` from Build 97 confirmed active. HTML stripped, `\n` separators. |
| **8.5** Scroll logic for large galleries | ✅ Build 110 confirmed 136/136 for Jagdhof. Advisory documented (GAP-SCROLL-STABLE-001). |
| **8.6** Subcategorized image review process | ℹ️ `image_data.subcategory` values stored. No API destination field beyond `gallery` and `room`. No change needed per user requirements. |

---

## 5. SCHEMA INTEGRITY VERIFICATION

All changes in Build 112 are **additive or view-replacement only**. No table
structure changes were made.

| Constraint | Status |
|---|---|
| DB always deleted at startup — schema re-executed | ✅ Compatible — `CREATE OR REPLACE VIEW` idempotent |
| No `NOT NULL` added to existing columns | ✅ Confirmed |
| No table column additions | ✅ Confirmed |
| `v_api_export_images` view replaced with `CREATE OR REPLACE` | ✅ No restart needed beyond DB recreation |

---

## 6. FILE CHANGE SUMMARY

| File | Bug Fixed | Change Type |
|---|---|---|
| `app/__init__.py` | All 4 bugs | Version bump + changelog entries |
| `app/config.py` | BUG-CONFIG-SYNC-001, BUG-ONLYTITLE-001 | `BUILD_VERSION` default 107→112, new `API_EXPORT_ONLY_TITLE` field |
| `app/api_payload_builder.py` | BUG-ONLYTITLE-001, BUG-SVC-DOC-001 | `onlyTitle` reads config toggle; module docstring corrected |
| `app/api_export_system.py` | BUG-ONLYTITLE-001 | `ExportTemplate.args_config` `"onlyTitle": False` |
| `schema_v77_complete.sql` | BUG-VIEW-DEDUP-001 | `v_api_export_images` rewritten with `DISTINCT ON` |

---

## 7. VALIDATION CHECKLIST

- [x] All modified Python files pass `ast.parse()` syntax validation
- [x] `BUILD_VERSION = 112` in `app/__init__.py`
- [x] `BUILD_VERSION: int = Field(default=112)` in `app/config.py`
- [x] `API_EXPORT_ONLY_TITLE: bool = Field(default=False)` in `app/config.py`
- [x] `"onlyTitle": only_title` (from config) in `build_payload()` args
- [x] `"onlyTitle": False` in `ExportTemplate.args_config` default
- [x] `v_api_export_images` uses `DISTINCT ON` + `CASE` priority ordering
- [x] No `NOT NULL` constraints added (schema recreate compatibility preserved)
- [x] No table structure changes (only view replacement)
- [x] Bilingual reports generated (EN + ES)

---

*End of Bug Report — BookingScraper Pro v6.0.0 Build 112*  
*Audit scope: Build 111 committed code (GitHub `corralejo-htls/scrapv25`)*  
*Generated: 2026-06-01*
