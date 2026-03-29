# BookingScraper Pro v6.0.0 - Bug List by Severity
**Build 58 | March 28, 2026**

---

## Legend

| Severity | Description | Response Time |
|----------|-------------|---------------|
| 🔴 Critical | Data loss, corruption, or system instability | Immediate |
| 🟠 High | Significant functionality impact | Next release |
| 🟡 Medium | Moderate impact, workarounds exist | Soon |
| 🟢 Low | Minor issues, cosmetic | Backlog |

---

## 🔴 Critical Bugs (Fix Immediately)

### CRIT-1: Incomplete Language Processing Leaves URLs in Inconsistent State

| Attribute | Value |
|-----------|-------|
| **Component** | scraper_service.py - _process_url() |
| **Line Numbers** | 357-447 |
| **Status** | Confirmed |
| **First Detected** | Build 58 |

**Description:**
Some URLs are being marked with incomplete language processing. The SQL query shows URL `130cce12-0d6d-4f13-9db2-3fa4ab2c94ec` has only 1 language instead of the expected 6.

**Root Cause:**
The `lang_results` dictionary tracks scrape attempts, but there's a gap between attempt tracking and actual database commits. Some languages may fail silently during extraction or upsert operations.

**Impact:**
- Data inconsistency in the hotels table
- Incomplete datasets for affected URLs
- Difficulty in identifying which languages actually succeeded

**Reproduction:**
```sql
SELECT url_id, count(url_id) as lang_count 
FROM hotels 
GROUP BY url_id 
HAVING count(url_id) < 6;
```

**Proposed Fix:**
1. Add explicit verification after each language upsert
2. Query DB immediately after each language scrape to confirm commit
3. Add reconciliation step before final status determination

**Code Reference:**
```python
# Add after each language scrape:
actual_count = self._count_successful_languages(url_obj.id)
if actual_count != len([l for l, ok in lang_results.items() if ok]):
    logger.warning("Mismatch between lang_results and DB for %s", url_id)
```

---

### CRIT-2: hotels_fine_print Stores Wrapper HTML Instead of Content

| Attribute | Value |
|-----------|-------|
| **Component** | extractor.py - _extract_fine_print() |
| **Line Numbers** | 1444-1587 |
| **Status** | Confirmed |
| **First Detected** | Build 58 |

**Description:**
The fine print extraction stores the entire HTML section including wrapper elements, headers, and containers. The requirement is to store only the paragraph content.

**Current Output:**
```html
<div><section><div><div><div><h2><div>The fine print</div></h2>
<div>Need-to-know information for guests at this property</div></div>
<div><button><span>See availability</span></button></div></div>
<div><div><div><p>The property can be reached by seaplanes...</p>
<p>Seaplane transfer takes 45 minutes...</p></div></div></div></div></section></div>
```

**Expected Output:**
```html
<p>The property can be reached by seaplanes...</p>
<p>Seaplane transfer takes 45 minutes...</p>
<p>Standard Transfer Times: Daylight hours.</p>
...
```

**Root Cause:**
The `_sanitize_html_fragment()` method keeps all HTML structure instead of extracting just the paragraph content.

**Proposed Fix:**
```python
def _extract_fine_print(self) -> Optional[str]:
    # ... existing section finding code ...
    
    if section:
        # Extract only <p> elements
        paragraphs = section.find_all("p")
        content = ""
        for p in paragraphs:
            # Skip empty or very short paragraphs (likely headers)
            text = p.get_text(strip=True)
            if len(text) > 10:
                content += str(p)
        return content if content else None
```

---

### CRIT-3: hotels_property_highlights Missing Category/Detail Structure

| Attribute | Value |
|-----------|-------|
| **Component** | extractor.py, scraper_service.py |
| **Line Numbers** | 2188-2323 (extractor), 1443-1548 (service) |
| **Status** | Confirmed |
| **First Detected** | Build 58 |

**Description:**
The current implementation stores only highlight text. The requirement specifies a category/detail structure that matches Booking.com's display format.

**Current Structure:**
| hotel_id | language | highlight |
|----------|----------|-----------|
| uuid | es | Free WiFi |
| uuid | es | Swimming pool |

**Required Structure:**
| language | highlight | highlight_detail |
|----------|-----------|------------------|
| es | Ideal para tu estancia | Baño privado |
| es | Ideal para tu estancia | Parking |
| es | Baño | Baño privado |
| es | Baño | Secador de pelo |

**Root Cause:**
The `_extract_property_highlights()` method doesn't parse the category grouping from the DOM structure.

**Proposed Fix:**
1. Modify the model to include `highlight_category` column
2. Parse the DOM to extract category headers and their associated items
3. Store each item with its parent category

---

## 🟠 High Severity Bugs (Fix in Next Release)

### HIGH-1: Missing URLs in hotels_property_highlights Table

| Attribute | Value |
|-----------|-------|
| **Component** | extractor.py - _extract_property_highlights() |
| **Line Numbers** | 2188-2323 |
| **Status** | Confirmed |
| **First Detected** | Build 58 |

**Description:**
Only 4 out of 14 processed URLs have entries in the hotels_property_highlights table. Expected all processed URLs to have data.

**SQL Evidence:**
```sql
SELECT COUNT(DISTINCT url_id) FROM hotels_property_highlights;  -- Returns: 4
SELECT COUNT(DISTINCT url_id) FROM hotels WHERE status = 'done'; -- Returns: 14
```

**Root Cause:**
1. Selectors may not match all Booking.com page variants
2. No fallback strategies when primary selectors fail
3. Different hotel types may have different DOM structures

**Proposed Fix:**
1. Add multiple selector strategies with fallback
2. Implement keyword-based detection
3. Add logging to track why extraction fails

---

### HIGH-2: No Verification of Actual DB Commits vs lang_results

| Attribute | Value |
|-----------|-------|
| **Component** | scraper_service.py - _process_url() |
| **Line Numbers** | 403-406 |
| **Status** | Confirmed |
| **First Detected** | Build 58 |

**Description:**
The code tracks language results in a dictionary but doesn't verify that the database actually contains the expected records before making status decisions.

**Current Code:**
```python
lang_results: Dict[str, bool] = {}
for lang in languages:
    ok = self._scrape_language(url_obj, lang)
    lang_results[lang] = ok  # This tracks attempt, not actual commit

actual_count = self._count_successful_languages(url_obj.id)
```

**Risk:**
A language could return True from `_scrape_language()` but fail during the upsert phase, leading to incorrect status determination.

**Proposed Fix:**
```python
# After all languages processed, verify consistency
expected_success = len([l for l, ok in lang_results.items() if ok])
if actual_count != expected_success:
    logger.error("Mismatch: lang_results says %d, DB has %d", 
                 expected_success, actual_count)
    # Reconcile and update lang_results accordingly
```

---

### HIGH-3: Property Highlights Extraction Lacks Fallback Strategies

| Attribute | Value |
|-----------|-------|
| **Component** | extractor.py - _extract_property_highlights() |
| **Line Numbers** | 2188-2323 |
| **Status** | Confirmed |
| **First Detected** | Build 58 |

**Description:**
The property highlights extraction only tries specific data-testid selectors. If Booking.com changes their DOM structure, extraction fails completely.

**Current Selectors:**
```python
_HIGHLIGHT_SELECTORS = [
    {"attrs": {"data-testid": "property-highlights"}},
    {"attrs": {"data-testid": re.compile(r"property.highlight|highlights", re.I)}},
    {"attrs": {"class": re.compile(r"property.highlight|propertyHighlight", re.I)}},
]
```

**Proposed Fix:**
Add keyword-based fallback similar to other extractors:
```python
# Add keyword-based detection
_HL_KEYWORDS = {
    "en": ["property highlights", "highlights", "top features"],
    "es": ["aspectos destacados", "destacados del alojamiento"],
    # ... more languages
}
```

---

### HIGH-4: Fine Print Selector May Not Match All Booking.com Variants

| Attribute | Value |
|-----------|-------|
| **Component** | extractor.py - _extract_fine_print() |
| **Line Numbers** | 1487-1498 |
| **Status** | Confirmed |
| **First Detected** | Build 58 |

**Description:**
The fine print selectors were updated in v56 but may still not cover all page variants.

**Current Selectors:**
```python
_SELECTORS = [
    {"attrs": {"data-testid": "PropertyFinePrintDesktop-wrapper"}},
    {"attrs": {"id": "important_info"}},
    {"attrs": {"data-testid": "property-section--fine-print"}},
]
```

**Risk:**
Different hotel types or A/B tests may use different DOM structures.

**Proposed Fix:**
1. Add more class-based fallbacks
2. Implement content-based detection (looking for specific phrases)
3. Add metrics to track extraction success rate

---

## 🟡 Medium Severity Bugs (Address Soon)

### MED-1: No Idempotency Keys for Language Processing

| Attribute | Value |
|-----------|-------|
| **Component** | scraper_service.py |
| **Line Numbers** | N/A |
| **Status** | Design Gap |
| **First Detected** | Build 58 |

**Description:**
Concurrent processing of the same URL/language combination could lead to race conditions and duplicate data.

**Risk:**
- Duplicate entries in satellite tables
- Inconsistent data states
- Harder to debug processing issues

**Proposed Fix:**
Add unique constraint: `(url_id, language, attempt_timestamp)`

---

### MED-2: Concurrent Processing May Cause Race Conditions

| Attribute | Value |
|-----------|-------|
| **Component** | scraper_service.py - dispatch_batch() |
| **Line Numbers** | 277-328 |
| **Status** | Confirmed |
| **First Detected** | Build 58 |

**Description:**
The ThreadPoolExecutor allows concurrent processing, but there's no database-level locking to prevent race conditions when updating related tables.

**Risk:**
- Two threads could process the same URL simultaneously
- Satellite table updates could interleave incorrectly

**Proposed Fix:**
1. Use SELECT FOR UPDATE when fetching URLs
2. Implement advisory locks in PostgreSQL
3. Use Redis distributed locks per URL

---

### MED-3: Image Download Failures Not Tracked Per URL

| Attribute | Value |
|-----------|-------|
| **Component** | scraper_service.py - _download_images() |
| **Line Numbers** | 750-816 |
| **Status** | Confirmed |
| **First Detected** | Build 58 |

**Description:**
Image download failures are logged as warnings but not tracked in the database per URL.

**Impact:**
- No visibility into which hotels have incomplete image sets
- Difficult to retry failed image downloads

**Proposed Fix:**
Add image download status to url_queue or create image_download_summary table.

---

### MED-4: No Validation of Satellite Table Consistency

| Attribute | Value |
|-----------|-------|
| **Component** | N/A - System-wide |
| **Line Numbers** | N/A |
| **Status** | Design Gap |
| **First Detected** | Build 58 |

**Description:**
There's no automated validation that satellite tables are consistent with the main hotels table.

**Example Inconsistency:**
- hotels table has 6 languages for URL X
- hotels_property_highlights has 0 languages for URL X

**Proposed Fix:**
Create a daily consistency check job:
```sql
SELECT h.url_id, h.language, 'missing_in_highlights'
FROM hotels h
LEFT JOIN hotels_property_highlights ph 
    ON h.url_id = ph.url_id AND h.language = ph.language
WHERE ph.id IS NULL;
```

---

### MED-5: Retry Logic Doesn't Distinguish Retryable vs Permanent Errors

| Attribute | Value |
|-----------|-------|
| **Component** | scraper_service.py, database.py |
| **Line Numbers** | 162-197 (database.py) |
| **Status** | Confirmed |
| **First Detected** | Build 58 |

**Description:**
The retry logic treats all errors as retryable, including permanent failures like constraint violations.

**Impact:**
- Wasted resources retrying permanent failures
- Delayed processing of valid URLs

**Proposed Fix:**
Classify errors:
```python
RETRYABLE_ERRORS = (OperationalError, InterfaceError, TimeoutError)
PERMANENT_ERRORS = (IntegrityError, DataError, ProgrammingError)
```

---

### MED-6: No Cleanup of Orphaned Satellite Records

| Attribute | Value |
|-----------|-------|
| **Component** | N/A - System-wide |
| **Line Numbers** | N/A |
| **Status** | Design Gap |
| **First Detected** | Build 58 |

**Description:**
If a hotel record is deleted or reprocessed, orphaned records may remain in satellite tables.

**Proposed Fix:**
1. Add ON DELETE CASCADE to foreign keys
2. Create periodic cleanup job
3. Add referential integrity constraints

---

## 🟢 Low Severity Bugs (Nice to Have)

### LOW-1: Logging Verbosity Could Be Reduced for Production

| Attribute | Value |
|-----------|-------|
| **Component** | All modules |
| **Line Numbers** | N/A |
| **Status** | Enhancement |
| **First Detected** | Build 58 |

**Description:**
DEBUG level logging generates significant volume in production.

**Proposed Fix:**
- Reduce DEBUG logging in hot paths
- Add sampling for high-frequency logs
- Use structured logging with log levels

---

### LOW-2: Missing Indexes on Some Satellite Table Queries

| Attribute | Value |
|-----------|-------|
| **Component** | models.py |
| **Line Numbers** | N/A |
| **Status** | Enhancement |
| **First Detected** | Build 58 |

**Description:**
Some queries may benefit from additional indexes.

**Proposed Indexes:**
```sql
CREATE INDEX CONCURRENTLY ON hotels (url_id, language, created_at);
CREATE INDEX CONCURRENTLY ON hotels_property_highlights (url_id, language, highlight);
```

---

### LOW-3: No Batch Cleanup for Old scraping_logs Partitions

| Attribute | Value |
|-----------|-------|
| **Component** | N/A - Maintenance |
| **Line Numbers** | N/A |
| **Status** | Enhancement |
| **First Detected** | Build 58 |

**Description:**
The scraping_logs table is partitioned by month but old partitions are not automatically dropped.

**Proposed Fix:**
Create a scheduled job to drop partitions older than retention period.

---

### LOW-4: VPN Rotation Could Be More Aggressive

| Attribute | Value |
|-----------|-------|
| **Component** | scraper_service.py, vpn_manager_windows.py |
| **Line Numbers** | 595-616 |
| **Status** | Enhancement |
| **First Detected** | Build 58 |

**Description:**
VPN rotation only happens after a failure and when the interval has elapsed.

**Proposed Fix:**
- Rotate on multiple consecutive failures
- Add proactive rotation based on success rate

---

### LOW-5: No Metrics on Extraction Success Rates by Field

| Attribute | Value |
|-----------|-------|
| **Component** | extractor.py |
| **Line Numbers** | N/A |
| **Status** | Enhancement |
| **First Detected** | Build 58 |

**Description:**
No visibility into which extractors are working well and which are failing.

**Proposed Metrics:**
```python
# Track per-field extraction success
extraction_metrics = {
    "hotel_name": {"attempts": 100, "success": 98},
    "fine_print": {"attempts": 100, "success": 45},
    "property_highlights": {"attempts": 100, "success": 30},
}
```

---

## Summary Statistics

| Severity | Count | Percentage |
|----------|-------|------------|
| 🔴 Critical | 3 | 17% |
| 🟠 High | 4 | 22% |
| 🟡 Medium | 6 | 33% |
| 🟢 Low | 5 | 28% |
| **Total** | **18** | **100%** |

---

*Report generated: March 28, 2026*
*Repository: https://github.com/corralejo-htls/scrapv25.git*
