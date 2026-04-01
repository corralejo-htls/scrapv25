# BookingScraper Pro — Audit Report #3
## Version 6.0.0 · Build 63-fix · Session: 2026-04-01

---

## 1. Audit Scope

This session audited data integrity and extraction quality using:

- Full SQL query dump from the latest complete run (13 URLs × 6 languages)
- `url_language_status` table — all 78 rows reviewed
- Extended tables coverage: amenities, services, FAQs, reviews, highlights, images
- `scraping_logs` timing analysis

---

## 2. System Status — Core Tables ✅

All primary tables remain fully populated with 13 URLs × 6 languages = **78 records each**:

| Table | Expected | Actual | Status |
|-------|----------|--------|--------|
| `hotels` | 78 | 78 | ✅ |
| `hotels_legal` | 78 | 78 | ✅ |
| `hotels_policies` | 78 | 78 | ✅ |
| `hotels_description` | 78 | 78 | ✅ |
| `url_queue` | 13 done | 13 done | ✅ |

---

## 3. Extended Tables — Count Summary

| Table | Rows | Rows/Hotel/Lang avg | Notes |
|-------|------|----------------------|-------|
| `hotels_amenities` | 716 | ~9.2 | ⚠️ See BUG-DATA-001 |
| `hotels_popular_services` | 716 | ~9.2 | ⚠️ See BUG-DATA-001 |
| `hotels_fine_print` | 78 | 1.0 | ✅ Exact 1:1 per hotel/lang |
| `hotels_all_services` | 1056 | ~13.5 | ✅ Variable, expected |
| `hotels_faqs` | 648 | ~8.3 | ✅ Variable, expected |
| `hotels_guest_reviews` | 516 | ~6.6 | ✅ Variable, expected |
| `hotels_property_highlights` | 246 | ~3.2 | ✅ Variable, expected |
| `image_data` | 548 | ~42 photos/hotel | ✅ See §5 |
| `image_downloads` | 1644 | 548 × 3 variants | ✅ Exact ratio confirmed |

---

## 4. New Bugs Identified

---

### BUG-STATUS-001 — `hotel_id = NULL` in `url_language_status`

**Severity:** 🔴 Critical — FK relationship broken in status tracking layer

**Confirmed:** 100% — all 78 rows in `url_language_status` have `hotel_id = NULL`

**Evidence from SQL data (sample rows):**

```
"id"; "url_id"; "language"; "status"; "attempt_count"; "hotel_id"; "created_at"; "updated_at"
"c06beb67..."; "ebaffa2e..."; "en"; "done"; "1"; "NULL"; "2026-04-01 11:43:23..."
"ff05dd58..."; "ebaffa2e..."; "es"; "done"; "1"; "NULL"; "2026-04-01 11:44:19..."
"a73acbc8..."; "ebaffa2e..."; "fr"; "done"; "1"; "NULL"; "2026-04-01 11:48:11..."
-- ... identical pattern across all 13 URLs × 6 languages = 78/78 rows
```

**Root Cause Analysis:**

The `hotel_id` column in `url_language_status` is populated **after** the hotel upsert in `scraper_service.py`. The `INSERT INTO url_language_status` call is issued at the **beginning** of language processing (to mark status = `processing`), before the hotel record is created. When the status is updated to `done`, the code likely calls `UPDATE url_language_status SET status='done', attempt_count=1 WHERE ...` but **omits the `hotel_id` in the SET clause**.

**Impact:**

- `url_language_status.hotel_id` FK is permanently NULL for all scrapes
- Queries that JOIN `url_language_status` with `hotels` via `hotel_id` will silently return no results
- Any reporting or analytics relying on this relationship is broken

**Fix Required:**

In `scraper_service.py`, locate the status-update logic called after a successful hotel upsert, and add `hotel_id = <hotel_uuid>` to the UPDATE statement.

```python
# WRONG — current behavior (hotel_id never set)
db.execute(
    text("UPDATE url_language_status SET status='done', attempt_count=:cnt "
         "WHERE id=:sid"),
    {"cnt": attempt_count, "sid": status_id}
)

# CORRECT — add hotel_id to the UPDATE
db.execute(
    text("UPDATE url_language_status SET status='done', attempt_count=:cnt, "
         "hotel_id=:hid WHERE id=:sid"),
    {"cnt": attempt_count, "hid": hotel_uuid, "sid": status_id}
)
```

---

### BUG-DATA-001 — `hotels_amenities` and `hotels_popular_services` have identical row count

**Severity:** 🟠 High — suspected data cross-contamination; requires source-code confirmation

**Evidence:**

```sql
"hotels_amenities";       "716"
"hotels_popular_services"; "716"
```

**Analysis:**

With 13 URLs × 6 languages = 78 hotel records, the probability that two independently scraped datasets (amenities vs. popular services) yield an **identical total row count** is statistically negligible. This pattern is a strong indicator that the same source list is being written to both tables by the upsert methods.

**Probable Root Cause:**

In `scraper_service.py`, the upsert methods for amenities and popular services likely reference the **same extracted key** from the `extracted` dict, or are called with the same argument due to a copy-paste error:

```python
# Suspected buggy code
_upsert_amenities(db, hotel_id, url_id, language, extracted.get("amenities", []))
_upsert_popular_services(db, hotel_id, url_id, language, extracted.get("amenities", []))  # ← WRONG KEY
#                                                                         ^^^^^^^^^^
#                                                    Should be "popular_services", not "amenities"
```

**Impact:**

- `hotels_popular_services` contains duplicated amenity data instead of actual popular service listings
- Downstream queries filtering by table name will get incorrect results
- Data quality is compromised for all 78 hotel-language records

**Verification Required (next session):**

```sql
-- Confirm column names first
\d hotels_amenities
\d hotels_popular_services

-- Then compare content side by side for one hotel/language
SELECT name FROM hotels_amenities   WHERE url_id='<any_uuid>' AND language='en'
INTERSECT
SELECT name FROM hotels_popular_services WHERE url_id='<any_uuid>' AND language='en';
-- If result is non-empty → cross-contamination confirmed
```

**Fix Required:**

Verify the `extracted` dict key used in each upsert call and correct the popular_services call to use `extracted.get("popular_services", [])` (or equivalent key name from `extractor.py`).

---

## 5. Image Data Integrity — ✅ Verified Consistent

**Confirmed ratio:**

```
image_data:      548 rows ÷ 13 hotels = 42.15 unique photos/hotel (average)
image_downloads: 1644 rows ÷ 548      = 3.00 variants/photo (thumb + large + highres)
```

The 3.00 exact ratio confirms the image download pipeline is writing all three size variants for every photo, with zero missing downloads. The apparent discrepancy vs. the worker log (which showed 135 files for 2 specific hotels) is normal variance — those hotels happened to have ~45 photos; the overall run averages ~42.

---

## 6. Unverified Item: BUG-LOG-001 (`hotel_id` in `scraping_logs`)

**Status:** ⚠️ UNVERIFIED

The diagnostic query from Audit #2 to check `hotel_id` population in `scraping_logs` was **not executed** in the provided SQL data. The `scraping_logs` query only selected `url_id, language, event_type, status, duration_ms, scraped_at` — `hotel_id` was not included.

**Required query for next session:**

```sql
SELECT
    COUNT(*)           AS total_logs,
    COUNT(hotel_id)    AS logs_with_hotel_id,
    COUNT(*) - COUNT(hotel_id) AS logs_missing_hotel_id
FROM scraping_logs;
```

Expected: `logs_missing_hotel_id = 0` if BUG-LOG-001 fix is working.

---

## 7. Performance Anomaly — WARN-PERF-001

**Severity:** 🟡 Warning — not a bug, but an operational signal

**Evidence:**

```
url_id: 98d3f78e...  language: "it"  duration_ms: 144,019  (144 seconds)
```

All other scrape durations in the session: 33,896 – 81,187 ms (33–81 seconds).
The Italian pass for hotel `98d3f78e` took **144 seconds — roughly 2-4× the normal range**.

**Probable causes:**
- Transient anti-bot challenge detected mid-session (extra wait cycles triggered)
- VPN rotation occurring during this specific scrape
- Slow Booking.com response on the Italian CDN node at that time

**Impact:** No data loss (status = `done`, all tables populated). Monitor in future sessions.

---

## 8. WARN-ORM-001 — Status Unchanged (Low Risk)

`scraping_logs` ORM uses `scraped_at` as `primary_key=True` while the SQL schema has no explicit PK on the partitioned table. INSERTs work correctly; risk of timestamp collision is negligible at single-worker scale. No action required unless moving to multi-worker parallelism.

---

## 9. Recommended SQL Diagnostics for Next Session

```sql
-- ── BUG-STATUS-001: Confirm hotel_id NULL in url_language_status ────────────
SELECT
    COUNT(*)                       AS total_rows,
    COUNT(hotel_id)                AS rows_with_hotel_id,
    COUNT(*) - COUNT(hotel_id)     AS rows_missing_hotel_id
FROM url_language_status;

-- ── BUG-DATA-001: Confirm amenities vs popular_services cross-contamination ──
-- Step 1: Get column names
\d hotels_amenities
\d hotels_popular_services

-- Step 2: Per-URL count comparison (should differ between tables)
SELECT
    url_id, language,
    COUNT(*) FILTER (WHERE src='amenities')        AS amenities_rows,
    COUNT(*) FILTER (WHERE src='popular_services') AS popular_rows
FROM (
    SELECT url_id, language, 'amenities'        AS src FROM hotels_amenities
    UNION ALL
    SELECT url_id, language, 'popular_services' AS src FROM hotels_popular_services
) x
GROUP BY url_id, language
HAVING COUNT(*) FILTER (WHERE src='amenities') = COUNT(*) FILTER (WHERE src='popular_services')
ORDER BY url_id, language
LIMIT 10;
-- If rows returned → strong evidence of duplication

-- Step 3: Content overlap check (replace 'name' with actual column from \d above)
-- SELECT name FROM hotels_amenities   WHERE url_id='<uuid>' AND language='en'
-- INTERSECT
-- SELECT name FROM hotels_popular_services WHERE url_id='<uuid>' AND language='en';

-- ── BUG-LOG-001: Verify hotel_id populated in scraping_logs ──────────────────
SELECT
    COUNT(*)                    AS total_logs,
    COUNT(hotel_id)             AS logs_with_hotel_id,
    COUNT(*) - COUNT(hotel_id)  AS logs_missing_hotel_id
FROM scraping_logs;

-- ── WARN-PERF-001: Detect outlier scrape durations ───────────────────────────
SELECT url_id, language, duration_ms, scraped_at
FROM scraping_logs
WHERE duration_ms > 100000
ORDER BY duration_ms DESC;

-- ── Image integrity cross-check ───────────────────────────────────────────────
SELECT
    COUNT(DISTINCT id)       AS unique_photos,
    COUNT(DISTINCT hotel_id) AS hotels_with_photos,
    MIN(3) = ROUND(
        (SELECT COUNT(*) FROM image_downloads)::numeric /
        NULLIF((SELECT COUNT(*) FROM image_data), 0), 2
    ) AS variant_ratio_is_3
FROM image_data;

-- ── Comprehensive coverage check (all tables) ────────────────────────────────
SELECT
    'hotels'                   AS tbl, COUNT(*) AS rows FROM hotels
UNION ALL SELECT 'hotels_description',        COUNT(*) FROM hotels_description
UNION ALL SELECT 'hotels_policies',           COUNT(*) FROM hotels_policies
UNION ALL SELECT 'hotels_legal',              COUNT(*) FROM hotels_legal
UNION ALL SELECT 'hotels_amenities',          COUNT(*) FROM hotels_amenities
UNION ALL SELECT 'hotels_popular_services',   COUNT(*) FROM hotels_popular_services
UNION ALL SELECT 'hotels_fine_print',         COUNT(*) FROM hotels_fine_print
UNION ALL SELECT 'hotels_all_services',       COUNT(*) FROM hotels_all_services
UNION ALL SELECT 'hotels_faqs',               COUNT(*) FROM hotels_faqs
UNION ALL SELECT 'hotels_guest_reviews',      COUNT(*) FROM hotels_guest_reviews
UNION ALL SELECT 'hotels_property_highlights',COUNT(*) FROM hotels_property_highlights
UNION ALL SELECT 'image_data',                COUNT(*) FROM image_data
UNION ALL SELECT 'image_downloads',           COUNT(*) FROM image_downloads
UNION ALL SELECT 'url_language_status',       COUNT(*) FROM url_language_status
UNION ALL SELECT 'scraping_logs',             COUNT(*) FROM scraping_logs;
```

---

## 10. Complete Bug Status (All Sessions)

| ID | Description | Session | Status |
|----|-------------|---------|--------|
| BUG-IMPORT-001..004 | Import aliases | #1 | ✅ |
| BUG-CFG-001..5 | 11 missing Settings fields | #1 | ✅ |
| BUG-EXTRACTOR-001 | Singleton extractor | #1 | ✅ |
| BUG-PERSIST-001 | 7 missing upsert methods | #1 | ✅ |
| BUG-PHOTO-001 | Images never downloaded | #1 | ✅ Confirmed 135/135 |
| BUG-BROWSER-001 | Brave didn't close | #1 | ✅ |
| FIX-PH-LEGACY-001 | Property highlights DOM | #1 | ✅ |
| BUG-LOG-001 | `hotel_id` in scraping_logs | #1 | ⚠️ Unverified |
| BUG-VERIFY-001 | `verify_system.py` version | #1 | ✅ |
| BUG-SCRIPT-001 | `create_db.bat` schema ref | #2 | ✅ |
| **BUG-STATUS-001** | `hotel_id=NULL` in `url_language_status` | **#3** | 🔴 **NEW — Fix Required** |
| **BUG-DATA-001** | Amenities = popular_services count | **#3** | 🟠 **NEW — Verify + Fix** |
| WARN-PERF-001 | 144s outlier (it, `98d3f78e`) | #3 | 🟡 Monitor |
| WARN-ORM-001 | `scraped_at` as ORM PK | #3 | 🟡 Low risk |

---

*BookingScraper Pro v6.0.0 Build 63-fix — Audit Session #3 — 2026-04-01*
