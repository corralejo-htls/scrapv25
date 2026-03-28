# BookingScraper Pro v6.0.0 - Comprehensive Audit Report
**Build 58 | Date: March 28, 2026**

---

## Executive Summary

This report presents a comprehensive audit of the BookingScraper workflow codebase (https://github.com/corralejo-htls/scrapv25.git). The audit analyzed all 8 phases of the scraping pipeline, verified the implementation of critical strategies, and identified data integrity issues.

### Key Findings

| Category | Count | Status |
|----------|-------|--------|
| Critical Bugs | 3 | Requires immediate attention |
| High Severity | 4 | Should be fixed in next release |
| Medium Severity | 6 | Should be addressed soon |
| Low Severity | 5 | Nice to have improvements |
| Verified Strategies | 3 | Working as expected |

---

## 1. Architecture Overview

### 1.1 System Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BookingScraper Pro v6.0.0                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  API Layer (main.py)                                                        │
│  ├── URL Management (/urls/load, /urls/load-csv)                           │
│  ├── Scraping Control (/scraping/force-now, /scraping/status)              │
│  ├── Hotel Data (/hotels, /hotels/{id})                                    │
│  └── Audit Logs (/logs/audit, /logs/audit/summary)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  Service Layer (scraper_service.py)                                         │
│  ├── ScraperService.dispatch_batch()                                       │
│  ├── ScraperService._process_url()                                         │
│  └── Strategy E Implementation                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  Scraping Engines (scraper.py)                                              │
│  ├── CloudScraperEngine                                                    │
│  └── SeleniumEngine                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  Data Extraction (extractor.py)                                             │
│  └── HotelExtractor.extract_all()                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  Persistence Layer (models.py, database.py)                                 │
│  ├── 14 Database Tables                                                    │
│  └── SQLAlchemy ORM with PostgreSQL                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Phase-by-Phase Analysis

### Phase 1: Initialization

**Files:** `app/main.py`, `app/config.py`, `app/database.py`

| Component | Status | Notes |
|-----------|--------|-------|
| Logging Setup | PASS | RotatingFileHandler for Windows compatibility |
| Rate Limiter | PASS | TTL-based cleanup (SCRAP-BUG-001) |
| Redis Pool | PASS | Shared connection pool (SCRAP-CON-003) |
| Database Engine | PASS | Lazy initialization (SCRAP-BUG-004) |
| Settings Validation | PASS | Comma-aware env parsing |

**Findings:**
- ✅ Windows 11 ProactorEventLoop properly configured
- ✅ API key validation working
- ✅ VPN countries validated against canonical list
- ✅ Language extensions validated against ENABLED_LANGUAGES

---

### Phase 2: URL Loading

**Files:** `app/main.py` (lines 427-774)

| Feature | Status | Notes |
|---------|--------|-------|
| URL Validation | PASS | Regex + netloc check (SCRAP-BUG-024) |
| Language Normalization | PASS | Strips .es.html and ?lang= params |
| CSV Parsing | PASS | Supports 3-column format (STRUCT-009) |
| Duplicate Handling | PASS | ON CONFLICT DO UPDATE |

**Findings:**
- ✅ URLs normalized before validation
- ✅ External ref and external_url properly handled
- ✅ Format auto-detection working (header vs no-header)

---

### Phase 3: Processing

**Files:** `app/scraper_service.py` (lines 357-447)

| Feature | Status | Notes |
|---------|--------|-------|
| Distributed Lock | PASS | Redis SET NX with TTL |
| Language Ordering | PASS | 'en' always processed first (BUG-LANG-001) |
| Strategy E | PASS | Conditional commit logic |

**Strategy E Implementation (BUG-INTEGRITY-001 FIX):**

```python
# Decision tree (3 cases):
# Case 1: actual_count == expected  -> mark 'done'        (full success)
# Case 2: actual_count > 0          -> mark 'error'       (partial - data PRESERVED)
# Case 3: actual_count == 0         -> cleanup + 'error'  (total failure)
```

---

### Phase 4: Scraping Engines

**Files:** `app/scraper.py`

| Engine | Status | Notes |
|--------|--------|-------|
| CloudScraperEngine | PASS | Primary engine with retries |
| SeleniumEngine | PASS | Fallback with gallery photo extraction |
| VPN Rotation | PASS | Automatic on block detection |

**Findings:**
- ✅ VPN connect before batch start
- ✅ VPN rotate on failure with retry
- ✅ Gallery photos extracted via hotelPhotos JS variable

---

### Phase 5: Extraction

**Files:** `app/extractor.py`

| Extractor | Status | Notes |
|-----------|--------|-------|
| Hotel Name | PASS | Multiple selector strategies |
| Description | PASS | Language validation (BUG-EXTR-004) |
| Review Score | PASS | data-review-score attr (BUG-EXTR-001) |
| Review Count | PASS | JSON-LD reviewCount (BUG-EXTR-003) |
| Star Rating | PASS | Normalized to 0-5 (BUG-EXTR-007) |
| City | PASS | addressRegion from JSON-LD (BUG-EXTR-006) |
| Amenities | PASS | Full facilities section (STRUCT-005) |
| Popular Services | PASS | Curated subset (STRUCT-008) |
| Policies | PASS | Dict with name/details (STRUCT-006) |
| Legal | PASS | Multi-language title detection (FIX-LEGAL-001) |
| Fine Print | PARTIAL | Needs improvement (see Bug #3) |
| All Services | PASS | Apollo JSON cache (BUG-ALL-SERVICES-001) |
| FAQs | PASS | With answers (BUG-FAQ-ANSWERS) |
| Guest Reviews | PASS | review-subscore selector (BUG-EXTR-010) |
| Property Highlights | PARTIAL | Needs improvement (see Bug #4) |

---

### Phase 6: Persistence

**Files:** `app/scraper_service.py` (lines 818-1548), `app/models.py`

| Table | Status | Notes |
|-------|--------|-------|
| url_queue | PASS | With languages_completed/failed tracking |
| hotels | PASS | Core hotel data |
| hotels_description | PASS | Separate TEXT table (STRUCT-001) |
| hotels_amenities | PASS | One row per amenity (STRUCT-005) |
| hotels_policies | PASS | One row per policy (STRUCT-006) |
| hotels_legal | PASS | One row per hotel/lang (STRUCT-007) |
| hotels_popular_services | PASS | One row per service (STRUCT-008) |
| hotels_fine_print | PARTIAL | HTML storage needs refinement |
| hotels_all_services | PASS | Complete service list (STRUCT-014) |
| hotels_faqs | PASS | With answers (STRUCT-015) |
| hotels_guest_reviews | PASS | Category scores (STRUCT-016) |
| hotels_property_highlights | PARTIAL | Structure needs redesign |
| image_downloads | PASS | Photo tracking (STRUCT-002) |
| image_data | PASS | Photo metadata |

---

### Phase 7: Image Handling

**Files:** `app/image_downloader.py`, `app/scraper_service.py` (lines 750-816)

| Feature | Status | Notes |
|---------|--------|-------|
| Photo Batch Download | PASS | download_photo_batch() returns Dict |
| URL Batch Download | PASS | Fallback for URL-only lists |
| Image Data Persistence | PASS | id_photo, category, dimensions |

**Fix Applied (BUG-IMG-UNPACK v55):**
```python
# Before (caused ValueError):
downloaded, total = downloader.download_photo_batch(...)

# After (correct):
results = downloader.download_photo_batch(...)
downloaded = sum(results.values()) if isinstance(results, dict) else 0
```

---

### Phase 8: Error Handling

**Files:** `app/scraper_service.py`, `app/database.py`

| Feature | Status | Notes |
|---------|--------|-------|
| DB Retry Logic | PASS | Exponential backoff (BUG-010) |
| Exception Logging | PASS | Full context preserved (BUG-015) |
| Partial Failure | PASS | Data preserved for retry |
| Total Failure Cleanup | PASS | _cleanup_empty_url() |

---

## 3. Strategy Verification

### 3.1 _count_successful_languages()

**Location:** `app/scraper_service.py` (lines 450-473)

**Status:** ✅ IMPLEMENTED CORRECTLY

```python
def _count_successful_languages(self, url_id: uuid.UUID) -> int:
    """Count language records committed to the hotels table for this URL."""
    try:
        with get_db() as session:
            count = (
                session.query(func.count(Hotel.id))
                .filter(Hotel.url_id == url_id)
                .scalar()
            )
            return int(count or 0)
    except Exception as exc:
        logger.error(...)
        return 0
```

**Verification:**
- ✅ Uses database as source of truth
- ✅ Returns int (0..N)
- ✅ Exception handling with fallback to 0

---

### 3.2 _mark_incomplete()

**Location:** `app/scraper_service.py` (lines 475-515)

**Status:** ✅ IMPLEMENTED CORRECTLY

```python
def _mark_incomplete(self, url_obj, error_msg, success_langs, failed_langs):
    """Mark URL as 'error' while PRESERVING partial scraping data."""
    row.status = "error"
    row.last_error = error_msg[:2000]
    row.languages_completed = ",".join(success_langs or [])
    row.languages_failed = ",".join(failed_langs or [])
    row.retry_count += 1
```

**Verification:**
- ✅ Status set to 'error' (not 'done')
- ✅ Data preserved in database
- ✅ Languages tracked for diagnostics
- ✅ Retry count incremented

---

### 3.3 _cleanup_empty_url()

**Location:** `app/scraper_service.py` (lines 517-566)

**Status:** ✅ IMPLEMENTED CORRECTLY

```python
def _cleanup_empty_url(self, url_id: uuid.UUID) -> None:
    """Delete all scraping artefacts for a URL with ZERO successful languages."""
    satellite_models = [
        HotelDescription, HotelAmenity, HotelPolicy, HotelLegal,
        HotelPopularService, HotelFinePrint, HotelAllService,
        HotelFAQ, HotelGuestReview, HotelPropertyHighlights,
    ]
    for model in satellite_models:
        session.query(model).filter(model.url_id == url_id).delete()
    session.query(Hotel).filter(Hotel.url_id == url_id).delete()
    session.query(URLLanguageStatus).filter(URLLanguageStatus.url_id == url_id).delete()
```

**Verification:**
- ✅ Only called when actual_count == 0
- ✅ All 10 satellite tables cleaned
- ✅ hotels table cleaned
- ✅ url_language_status cleaned

---

## 4. Data Integrity Issues

### 4.1 Bug #1: Incomplete Language Processing

**SQL Query:**
```sql
SELECT url_id, count(url_id) FROM hotels GROUP BY url_id;
```

**Result:**
| url_id | count |
|--------|-------|
| d15e1aa5-32b2-4451-99fd-8a80e3c301d1 | 6 |
| bdec8c7e-05ec-47ca-a6e2-829ffa43688a | 6 |
| 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec | **1** |
| 67bbbef6-d0c9-4d44-9273-9f66a22957d5 | 6 |

**Analysis:**
- URL `130cce12-0d6d-4f13-9db2-3fa4ab2c94ec` has only 1 language instead of 6
- This indicates partial processing failure

**Root Cause:**
The Strategy E implementation correctly identifies partial failures and marks them as 'error' while preserving data. However, the issue is that:

1. Some languages may fail silently during extraction
2. The `lang_results` dict tracks scrape attempts, not actual DB commits
3. Race conditions in concurrent processing may cause inconsistencies

**Recommendation:**
- Add verification step after each language scrape
- Implement idempotency keys for each language processing

---

### 4.2 Bug #2: Missing URLs in Satellite Tables

**SQL Query:**
```sql
SELECT url_id, count(url_id) FROM hotels_property_highlights GROUP BY url_id;
```

**Result:**
| url_id | count |
|--------|-------|
| 653550be-6f27-44b3-9c40-6ae08a9d3d90 | 60 |
| a2f386b2-21a2-424f-9467-6f6b72d6e482 | 60 |
| d15e1aa5-32b2-4451-99fd-8a80e3c301d1 | 60 |

**Analysis:**
- Only 4 URLs have property highlights data
- Expected: All processed URLs should have entries

**Root Cause:**
1. Property highlights extraction depends on DOM structure that may vary
2. The `_extract_property_highlights()` method may return None for some pages
3. No fallback strategy when primary selectors fail

---

### 4.3 Bug #3: hotels_fine_print HTML Parsing

**Current Behavior:**
- Stores entire HTML block with wrapper elements
- Includes unnecessary container divs

**Expected Behavior:**
- Store only the content between first `<p>` and last `</p>`
- Remove wrapper containers

**Example Current Output:**
```html
<div><section><div><div><div><h2><div>The fine print</div></h2>...
```

**Expected Output:**
```html
<p>The property can be reached by seaplanes...</p>
<p>Seaplane transfer takes 45 minutes...</p>
...
```

**Root Cause:**
The `_extract_fine_print()` method in `extractor.py` (lines 1444-1587) extracts the entire section HTML and sanitizes it, but doesn't extract just the paragraph content.

---

### 4.4 Bug #4: hotels_property_highlights Structure

**Current Behavior:**
- Stores parsed text items from HTML
- One row per highlight text

**Expected Behavior (per requirements):**
Should store both category and detail:
| language | highlight | highlight_detail |
|----------|-----------|------------------|
| es | Ideal para tu estancia | Baño privado |
| es | Ideal para tu estancia | Parking |
| es | Baño | Baño privado |
| es | Baño | WC |

**Root Cause:**
The current implementation in `_upsert_property_highlights()` (lines 1443-1548) extracts only the highlight text from `<li>` elements, but doesn't capture the category/detail structure that Booking.com displays.

---

## 5. Bug Severity Classification

### Critical (Fix Immediately)

| ID | Bug | Impact |
|----|-----|--------|
| CRIT-1 | Incomplete language processing leaves URLs in inconsistent state | Data integrity |
| CRIT-2 | hotels_fine_print stores wrapper HTML instead of content | Data quality |
| CRIT-3 | hotels_property_highlights missing category/detail structure | Missing data |

### High (Fix in Next Release)

| ID | Bug | Impact |
|----|-----|--------|
| HIGH-1 | Missing URLs in hotels_property_highlights table | Incomplete dataset |
| HIGH-2 | No verification of actual DB commits vs lang_results | False positives |
| HIGH-3 | Property highlights extraction lacks fallback strategies | Missing data |
| HIGH-4 | Fine print selector may not match all Booking.com variants | Missing data |

### Medium (Address Soon)

| ID | Bug | Impact |
|----|-----|--------|
| MED-1 | No idempotency keys for language processing | Duplicate risk |
| MED-2 | Concurrent processing may cause race conditions | Data inconsistency |
| MED-3 | Image download failures not tracked per URL | Missing monitoring |
| MED-4 | No validation of satellite table consistency | Data integrity |
| MED-5 | Retry logic doesn't distinguish retryable vs permanent errors | Efficiency |
| MED-6 | No cleanup of orphaned satellite records | Database bloat |

### Low (Nice to Have)

| ID | Bug | Impact |
|----|-----|--------|
| LOW-1 | Logging verbosity could be reduced for production | Performance |
| LOW-2 | Missing indexes on some satellite table queries | Query performance |
| LOW-3 | No batch cleanup for old scraping_logs partitions | Maintenance |
| LOW-4 | VPN rotation could be more aggressive | Success rate |
| LOW-5 | No metrics on extraction success rates by field | Observability |

---

## 6. Recommendations

### Immediate Actions

1. **Fix hotels_fine_print extraction**
   - Modify `_extract_fine_print()` to extract only `<p>` elements
   - Join paragraphs with proper spacing

2. **Redesign hotels_property_highlights**
   - Add `highlight_category` and `highlight_detail` columns
   - Parse the category structure from Booking.com DOM

3. **Add extraction verification**
   - Verify each language actually committed to DB
   - Add reconciliation between lang_results and DB count

### Short-term Improvements

4. **Add fallback selectors**
   - Implement multiple strategies for property highlights
   - Add keyword-based fallback for fine print

5. **Implement idempotency**
   - Add unique constraint on (url_id, language, attempt_id)
   - Track each processing attempt separately

6. **Add consistency checks**
   - Daily validation: hotels count vs satellite tables
   - Alert on inconsistencies

### Long-term Enhancements

7. **Improve concurrency handling**
   - Use database-level locking
   - Implement proper distributed transactions

8. **Add comprehensive metrics**
   - Per-field extraction success rates
   - Language-specific failure patterns

---

## 7. Conclusion

The BookingScraper Pro v6.0.0 build 58 has a solid foundation with Strategy E implementation correctly handling partial failures. The main issues are:

1. **Data extraction completeness** - Some fields (fine_print, property_highlights) need refinement
2. **Data structure alignment** - The property_highlights table structure doesn't match requirements
3. **Verification gaps** - Need stronger verification between attempted and actual commits

The critical strategies (_count_successful_languages, _mark_incomplete, _cleanup_empty_url) are correctly implemented and working as designed.

---

## Appendix A: File References

| File | Purpose | Lines |
|------|---------|-------|
| app/main.py | FastAPI application, URL management | 1216 |
| app/config.py | Settings, validation | 472 |
| app/database.py | DB connection, session management | 264 |
| app/models.py | SQLAlchemy ORM models | 1119 |
| app/scraper_service.py | Main scraping orchestration | 1632 |
| app/scraper.py | Scraping engines | - |
| app/extractor.py | Data extraction logic | 2324 |
| app/image_downloader.py | Image download management | - |

---

## Appendix B: Database Schema Version

**Schema Version:** v58 complete
**Tables:** 14
**Partitioning:** scraping_logs by month (RANGE)

---

*Report generated: March 28, 2026*
*Auditor: AI Code Analysis System*
*Repository: https://github.com/corralejo-htls/scrapv25.git*
