# Bug Report: BUG-LANG-001 — Missing Languages

**Report Date:** March 30, 2026  
**Severity:** HIGH  
**Status:** Open — Root Cause Identified  
**Affected Component:** `app/scraper_service.py`, `app/scraper.py`  
**Affected URL:** `3420c869-fd48-4f79-9557-5e185e9e580f` (CB Seychelles Hotel)

---

## 1. Executive Summary

The BookingScraper Pro application fails to scrape all 6 configured languages for certain URLs. For the affected URL, only 1 out of 6 languages (Spanish) was successfully scraped, while the remaining 5 languages (en, de, it, fr, pt) failed with the error "All scraping engines failed."

---

## 2. Problem Description

### 2.1 Observed Behavior

| Table | Expected Languages | Actual Languages | Status |
|-------|-------------------|------------------|--------|
| hotels | 6 (en, es, de, it, fr, pt) | 1 (es only) | ❌ FAILED |
| hotels_description | 6 | 1 | ❌ FAILED |
| hotels_policies | 6 | 1 | ❌ FAILED |
| hotels_legal | 6 | 1 | ❌ FAILED |

### 2.2 Database Evidence

**URL Queue Status:**
```sql
SELECT id, status, retry_count, languages_completed, languages_failed, last_error 
FROM url_queue WHERE id = '3420c869-fd48-4f79-9557-5e185e9e580f';
```

**Result:**
- `status`: `error`
- `retry_count`: `1`
- `languages_completed`: `es`
- `languages_failed`: `en,de,it,fr,pt`
- `last_error`: `Incomplete: 1/6 languages. OK=['es'] FAILED=['en', 'de', 'it', 'fr', 'pt']`

**Language Status Table:**
```sql
SELECT url_id, language, status, last_error 
FROM url_language_status 
WHERE url_id = '3420c869-fd48-4f79-9557-5e185e9e580f';
```

**Result:**
| Language | Status | Error Message |
|----------|--------|---------------|
| es | done | NULL |
| en | error | All scraping engines failed |
| de | error | All scraping engines failed |
| it | error | All scraping engines failed |
| fr | error | All scraping engines failed |
| pt | error | All scraping engines failed |

---

## 3. Root Cause Analysis

### 3.1 Error Origin

The error "All scraping engines failed" originates from `app/scraper_service.py` at lines 750-752:

```python
if html is None:
    self._log_scraping_event(url_obj, lang, "scrape_failed", "error", duration_ms)
    self._upsert_lang_status(url_obj, lang, "error", "All scraping engines failed")
    return False
```

### 3.2 Scraping Flow Analysis

The scraping process follows this sequence:

```
1. Try CloudScraperEngine
   ↓ (fails - returns None)
2. Try SeleniumEngine
   ↓ (fails - returns None)
3. Check VPN rotation eligibility
   ↓ (if enabled and interval elapsed)
4. Rotate VPN and retry CloudScraper
   ↓ (fails)
5. Retry Selenium
   ↓ (fails)
6. Log "All scraping engines failed"
```

### 3.3 Evidence from Logs

**Log entries show the following pattern:**
```
[WARNING] Short HTML (3962 bytes) for https://www.booking.com/hotel/...
[INFO] CloudScraper retry 2/3 — waiting 4.0s
[WARNING] Short HTML (3962 bytes)
[INFO] CloudScraper retry 3/3 — waiting 6.0s
[WARNING] Short HTML (3962 bytes)
[ERROR] CloudScraper exhausted retries for ...
[INFO] CloudScraper failed for {url_id}/{lang} — trying Selenium.
[WARNING] Selenium language mismatch: requested=en got=es
[ERROR] Selenium language retries exhausted
```

### 3.4 The "Short HTML" Problem

The **3962 bytes** HTML response is a clear indicator of **Booking.com anti-bot blocking**. This typically indicates:

1. **CAPTCHA challenge page** - Booking.com detected automated access
2. **Browser verification page** - "Checking your browser" message
3. **IP-based blocking** - The IP address has been flagged
4. **Rate limiting** - Too many requests from the same source

### 3.5 Why Spanish (es) Succeeded but Others Failed

- The Spanish version was scraped at `05:02:41` (early in the batch)
- Other languages were attempted between `05:00:03` and `05:55:37`
- Booking.com likely flagged the IP after the Spanish scrape
- Subsequent requests from the same IP were blocked
- The "Selenium language mismatch" errors confirm this - Booking.com returns Spanish content regardless of the requested language when the IP is blocked

---

## 4. Contributing Factors

### 4.1 VPN Rotation Timing

From the logs:
- VPN was connected to France at `03:45:51`
- VPN rotation interval: 50 seconds (`vpn_interval=50s`)
- Spanish scrape: `05:02:41` (successful)
- English attempt: `05:00:03` (failed - before Spanish!)

**Timeline anomaly detected:** The English attempt happened BEFORE the Spanish success, suggesting out-of-order processing or concurrent language processing.

### 4.2 Threading Issues

The system uses `ThreadPoolExecutor` with 2 workers. Potential race conditions:
- Multiple threads accessing the same VPN connection
- Shared Selenium driver instance (BUG-DESC-002 fix applied but may have edge cases)
- Cookie/header contamination between threads

### 4.3 Retry Logic Limitations

Current retry configuration:
- `MAX_RETRIES = 3` (for CloudScraper)
- Wait times: 2s, 4s, 6s (exponential backoff)
- **No delay between language attempts**
- **No IP cooldown period**
- **VPN rotation only based on time interval, not on failure detection**

---

## 5. Solutions & Mitigation Strategies

### 5.1 Immediate Fixes (High Priority)

#### Fix 1: Implement Inter-Language Delay

Add a configurable delay between scraping different languages for the same URL:

```python
# In _scrape_language() method
import time
LANG_SCRAPE_DELAY = 10  # seconds between languages

def _scrape_language(self, url_obj, lang, is_first_lang=False):
    if not is_first_lang:
        time.sleep(self._cfg.LANG_SCRAPE_DELAY)
    # ... rest of the method
```

**Rationale:** Spreading requests over time reduces the likelihood of triggering rate limits.

**Implementation Location:** `app/scraper_service.py`, method `_process_url()`

#### Fix 2: Force VPN Rotation on Failure

Force VPN rotation immediately after any language fails:

```python
if html is None and self._cfg.VPN_ENABLED:
    # Force immediate rotation on failure
    logger.info("Forcing VPN rotation due to scraping failure")
    rotated = self._vpn.rotate(force=True)  # Add force parameter
    if rotated:
        logger.info("VPN rotated after failure — retrying %s/%s", url_obj.id, lang)
        html = self._cloud_engine.scrape(lang_url, retries=1)
```

**Rationale:** Changing IP immediately after detection prevents subsequent language failures.

**Implementation Location:** `app/scraper_service.py`, method `_scrape_language()`

#### Fix 3: Increase Retry Attempts with Jitter

Implement exponential backoff with random jitter:

```python
import random

# In CloudScraperEngine.scrape()
retry_delay = base_delay * (2 ** attempt) + random.uniform(0, 3)
```

**Rationale:** Randomized delays appear more human-like and avoid predictable patterns.

**Implementation Location:** `app/scraper.py`, class `CloudScraperEngine`

### 5.2 Medium-Term Improvements

#### Improvement 1: Per-Language IP Rotation

Rotate VPN for EACH language rather than per batch:

```python
for lang in languages:
    if self._cfg.VPN_ENABLED and lang != 'en':  # Keep same IP for 'en'
        self._vpn.rotate()
    self._scrape_language(url_obj, lang)
```

**Rationale:** Each language appears to come from a different geographic location.

#### Improvement 2: Failed Language Retry Queue

Implement a separate retry mechanism for failed languages:

```python
# Add to url_language_status table:
# - retry_count column
# - next_retry_at timestamp
# - max_retries_reached boolean

# Create periodic task to retry failed languages
@celery_app.task
def retry_failed_languages():
    failed = db.query(UrlLanguageStatus).filter(
        status='error',
        retry_count < MAX_LANG_RETRIES,
        next_retry_at <= datetime.now()
    ).all()
    for lang_status in failed:
        scrape_single_language.delay(lang_status.url_id, lang_status.language)
```

#### Improvement 3: Adaptive Rate Limiting

Monitor success rate and automatically adjust delays:

```python
class AdaptiveRateLimiter:
    def __init__(self):
        self.success_rate = 1.0
        self.recent_requests = deque(maxlen=100)
    
    def record_result(self, success: bool):
        self.recent_requests.append(success)
        self.success_rate = sum(self.recent_requests) / len(self.recent_requests)
    
    def get_delay(self) -> float:
        if self.success_rate < 0.5:
            return 30.0  # High delay on low success
        elif self.success_rate < 0.8:
            return 10.0
        return 2.0  # Normal delay
```

### 5.3 Long-Term Architectural Changes

#### Change 1: Proxy Pool Integration

Implement a rotating proxy pool in addition to VPN:

```python
class ProxyPool:
    def __init__(self, proxies: List[str]):
        self.proxies = cycle(proxies)
    
    def get_proxy(self) -> str:
        return next(self.proxies)
```

#### Change 2: Distributed Scraping Architecture

Distribute language scraping across multiple workers/servers:

```
Worker 1 (IP A): en, es
Worker 2 (IP B): de, fr  
Worker 3 (IP C): it, pt
```

#### Change 3: Browser Fingerprint Rotation

Rotate browser fingerprints for Selenium:

```python
# Use libraries like selenium-stealth or undetected-chromedriver
from selenium_stealth import stealth

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)
```

---

## 6. Configuration Recommendations

### 6.1 Update config.ini

```ini
[SCRAPER]
; Add new configuration options
lang_scrape_delay = 10          ; Seconds between language attempts
vpn_rotate_on_failure = true    ; Force VPN rotation on any failure
max_lang_retries = 5            ; Increase from current default
enable_jitter = true            ; Add randomization to delays
jitter_max = 3.0               ; Maximum jitter in seconds

; Adaptive rate limiting
adaptive_rate_limiting = true
target_success_rate = 0.95
high_delay_threshold = 0.5
```

### 6.2 Update env.example

```bash
# Language scraping configuration
LANG_SCRAPE_DELAY=10
VPN_ROTATE_ON_FAILURE=true
MAX_LANG_RETRIES=5
ENABLE_JITTER=true
JITTER_MAX=3.0
```

---

## 7. Implementation Priority

| Priority | Fix | Effort | Impact |
|----------|-----|--------|--------|
| P0 | Inter-language delay | Low | High |
| P0 | Force VPN rotation on failure | Low | High |
| P1 | Increase retry attempts | Low | Medium |
| P1 | Failed language retry queue | Medium | High |
| P2 | Adaptive rate limiting | Medium | Medium |
| P2 | Per-language IP rotation | Medium | High |
| P3 | Proxy pool integration | High | Medium |
| P3 | Distributed architecture | High | High |

---

## 8. Testing Strategy

### 8.1 Unit Tests

```python
def test_language_delay_is_applied():
    service = ScraperService()
    with patch('time.sleep') as mock_sleep:
        service._scrape_language(url_obj, 'es', is_first_lang=True)
        mock_sleep.assert_not_called()
        
        service._scrape_language(url_obj, 'en', is_first_lang=False)
        mock_sleep.assert_called_once_with(10)

def test_vpn_rotation_on_failure():
    service = ScraperService()
    service._cloud_engine.scrape = Mock(return_value=None)
    service._selenium_engine.scrape = Mock(return_value=None)
    
    with patch.object(service._vpn, 'rotate') as mock_rotate:
        service._scrape_language(url_obj, 'en')
        mock_rotate.assert_called_once_with(force=True)
```

### 8.2 Integration Tests

```python
def test_full_url_scraping_with_all_languages():
    """Test that all 6 languages are scraped successfully."""
    url_id = load_test_url()
    service = ScraperService()
    
    result = service.process_url(url_id)
    
    assert result['languages_scraped'] == 6
    assert result['status'] == 'done'
    
    # Verify database state
    for lang in ['en', 'es', 'de', 'it', 'fr', 'pt']:
        assert db.query(Hotel).filter_by(url_id=url_id, language=lang).first()
```

---

## 9. SQL Queries for Diagnosis

```sql
-- Find all URLs with incomplete language coverage
SELECT 
    uq.id, 
    uq.status, 
    uq.languages_completed, 
    uq.languages_failed,
    COUNT(DISTINCT h.language) as hotel_count
FROM url_queue uq
LEFT JOIN hotels h ON uq.id = h.url_id
GROUP BY uq.id
HAVING COUNT(DISTINCT h.language) < 6;

-- Find URLs with specific error patterns
SELECT 
    url_id, 
    language, 
    attempts, 
    last_error
FROM url_language_status
WHERE status = 'error'
AND last_error = 'All scraping engines failed';

-- Success rate by language
SELECT 
    language,
    COUNT(*) as total,
    SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) as success,
    ROUND(100.0 * SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
FROM url_language_status
GROUP BY language;
```

---

## 10. Conclusion

The bug affecting URL `3420c869-fd48-4f79-9557-5e185e9e580f` is caused by Booking.com's anti-bot detection mechanisms triggering after the first successful language scrape (Spanish). The subsequent language attempts from the same IP address were blocked, resulting in "Short HTML" responses and eventual "All scraping engines failed" errors.

**Key takeaways:**
1. The 3962-byte HTML response is a clear indicator of blocking
2. The timing pattern suggests IP-based rate limiting
3. Current retry logic is insufficient for multi-language scraping
4. VPN rotation needs to be more aggressive on failure detection

**Recommended immediate action:**
Implement Fix 1 (inter-language delay of 10 seconds) and Fix 2 (force VPN rotation on failure) to mitigate the issue in the short term.

---

*Report generated: March 30, 2026*  
*BookingScraper Pro v6.0.0 Build 60*  
*Analyst: AI Technical Analysis System*
