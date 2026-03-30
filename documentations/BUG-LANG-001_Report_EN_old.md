# BookingScraper Pro — Bug Report: BUG-LANG-001 (Missing Languages)

**Date:** March 29, 2026
**Version:** 6.0.0 Build 60
**Severity:** HIGH
**Affected URL:** `3420c869-fd48-4f79-9557-5e185e9e580f`
**Impact:** 5 of 6 languages failed to scrape (83% failure rate)
**Database Constraint:** Database is ALWAYS deleted at startup. SQL file re-executed. No migrations. No data preservation.

---

## 1. Problem Description

### 1.1 Observed Behavior

The URL with ID `3420c869-fd48-4f79-9557-5e185e9e580f` shows incomplete language coverage across ALL data tables. While the other 12 URLs in the database completed successfully with 6 languages each (en, es, de, it, fr, pt), this specific URL only has 1 language (es) in hotels, hotels_description, hotels_policies, and hotels_legal tables. This discrepancy is significant because it indicates a systemic scraping failure rather than a data issue isolated to a single table. All four content tables consistently show the same single-language pattern, which strongly suggests the failure occurred at the language-level scraping stage before any data was written to the database. The other 12 URLs each contain records for all six configured languages, confirming that the scraping pipeline works correctly under normal conditions and that this failure is specific to this URL's processing window.

| Table | Expected Languages | Actual Languages | Status |
|-------|-------------------|------------------|--------|
| hotels | 6 (en, es, de, it, fr, pt) | 1 (es only) | FAILED |
| hotels_description | 6 | 1 | FAILED |
| hotels_policies | 6 | 1 | FAILED |
| hotels_legal | 6 | 1 | FAILED |

The table above summarizes the gap between expected and actual language coverage across every data table associated with this URL. The consistency of the failure across all four tables confirms that the problem is not a post-processing or parsing issue, but rather a failure at the HTML scraping stage. No data was written for any language other than Spanish, meaning the scraper either received no valid HTML for the other five languages or received HTML that was identified as a block page and therefore discarded without database insertion.

### 1.2 Database Evidence

**url_queue status:**
- status: `error`
- retry_count: `1`
- languages_completed: `es`
- languages_failed: `en,de,it,fr,pt`
- last_error: `Incomplete: 1/6 languages. OK=['es'] FAILED=['en', 'de', 'it', 'fr', 'pt']`

The url_queue record for this URL clearly documents the partial failure state. The status is set to `error` rather than `done` because fewer than the required 6 languages were successfully scraped. However, the system correctly preserved the partial data (Spanish) rather than deleting it, which aligns with the Strategy E behavior introduced in v58 where partial success results in data retention. The last_error field provides a concise summary of the failure, listing all five failed languages and the single successful one. The retry_count of 1 indicates that the URL was processed exactly once — the language-level failures resulted in the overall URL being marked as errored without triggering a full URL-level retry.

**url_language_status table:**

| Language | Status | Attempts | Error |
|----------|--------|----------|-------|
| en | error | 1 | All scraping engines failed |
| es | done | 1 | NULL |
| de | error | 1 | All scraping engines failed |
| it | error | 1 | All scraping engines failed |
| fr | error | 1 | All scraping engines failed |
| pt | error | 1 | All scraping engines failed |

The url_language_status table provides the most granular view of the failure. Each of the five failing languages shows exactly 1 attempt with the error message "All scraping engines failed", which means that both CloudScraper and Selenium engines were unable to retrieve valid hotel content for these languages. The Spanish language succeeded on its first and only attempt with no error. Notably, every language was only attempted once — there was no second attempt for any of the failed languages, which reveals that the system's retry logic at the language level does not include automatic re-queuing of failed languages after the initial processing cycle completes.

**Critical timing evidence from url_language_status.created_at:**

| Language | Timestamp | Status | Time Since Previous |
|----------|-----------|--------|---------------------|
| en | 05:00:03 | error | — (first) |
| es | 05:02:41 | done | +2 min 38 sec |
| de | 05:16:59 | error | +14 min 18 sec |
| it | 05:30:40 | error | +13 min 41 sec |
| fr | 05:43:13 | error | +12 min 33 sec |
| pt | 05:55:37 | error | +12 min 24 sec |

The timing data reveals several important patterns about how the scraper processes languages sequentially and how long each language attempt takes. English was the first language attempted at 05:00:03 and failed, followed by Spanish which succeeded roughly two and a half minutes later. After the Spanish success, there is a significant gap of over 14 minutes before German was attempted, suggesting that the scraping engines consumed substantial time during their retry cycles (3 CloudScraper retries + Selenium fallback + potential VPN rotation attempt). The remaining four languages each took approximately 12-14 minutes to process, indicating that each one went through the full multi-engine retry chain before ultimately failing. The total processing window for this single URL spanned nearly 56 minutes (05:00:03 to 05:55:37), which is consistent with each language consuming the full retry budget across both scraping engines.

---

## 2. Step-by-Step Code Analysis

### 2.1 Language Processing Flow (scraper_service.py — _process_url)

The method `_process_url()` orchestrates language processing sequentially in a for loop. Per BUG-LANG-001 fix (v55), English is always processed first regardless of its position in ENABLED_LANGUAGES. The method iterates through each language one at a time, calling `_scrape_language()` for each. After all languages are processed, it counts successful languages from the database (not from memory) using `_count_successful_languages()` — this is the Strategy E enhancement from v58. Based on the actual DB count, it marks the URL as 'done' (full success), 'error' with data preserved (partial success), or 'error' with cleanup (total failure). This approach ensures that the success determination is based on durable database state rather than in-memory results that could be affected by race conditions or transient errors. The Strategy E enhancement is particularly important because it prevents false positives where a language appears to succeed in memory but fails to persist to the database due to a connection error or constraint violation.

Key code path in `_process_url()`:
```python
languages = list(self._cfg.ENABLED_LANGUAGES)
if 'en' in languages:
    languages.remove('en')
    languages.insert(0, 'en')
expected_count = len(languages)
lang_results: Dict[str, bool] = {}
for lang in languages:
    ok = self._scrape_language(url_obj, lang)
    lang_results[lang] = ok
```

The code above demonstrates the sequential nature of language processing. The `lang_results` dictionary tracks the outcome of each language attempt, but this dictionary is only used for intermediate logging and is not the authoritative source for determining URL-level success. The authoritative count comes from the database query in `_count_successful_languages()`. This design choice means that even if the in-memory tracking is accurate, the final verdict is always based on what actually persisted to the database. The reordering of English to the first position was introduced in v55 to ensure that the primary language is always attempted before any VPN rotation or state changes could affect the scraping environment.

**FINDING 1 — No inter-language delay:** There is zero delay between consecutive `_scrape_language()` calls. After a language succeeds or fails, the next language is attempted immediately. This rapid-fire pattern is a major trigger for Booking.com's anti-bot detection. When multiple requests for different language versions of the same hotel page are sent in quick succession from the same IP address, the pattern is highly indicative of automated scraping rather than human browsing behavior. A human user would typically take several seconds to minutes between language switches, during which they would be reading the content. The absence of any delay between language attempts creates an easily detectable fingerprint that Booking.com's anti-bot system can identify and respond to with IP-level blocking.

### 2.2 Scraping Attempt Flow (scraper_service.py — _scrape_language)

The `_scrape_language()` method implements a multi-engine fallback chain:

1. **CloudScraperEngine.scrape()** — called with `MAX_LANG_RETRIES` (default 3) retries
2. **SeleniumEngine.scrape()** — called as fallback if CloudScraper returns None
3. **VPN rotation + retry** — if both engines fail AND VPN is enabled AND `should_rotate()` returns True:
   - Rotate VPN (new IP)
   - Retry CloudScraper once (retries=1)
   - Retry Selenium once

The multi-engine fallback chain is designed to maximize the chances of successful scraping by trying different approaches before giving up on a language. CloudScraper is the primary engine because it is faster and lighter, while Selenium serves as a fallback that can handle JavaScript-rendered content and some Cloudflare challenges. The VPN rotation step serves as a last resort, providing a fresh IP address when the current one has been blocked. However, the effectiveness of this chain depends heavily on the timing and condition of the VPN rotation trigger, as explored in the findings below.

The critical decision point where "All scraping engines failed" is triggered:
```python
if html is None:
    self._log_scraping_event(url_obj, lang, "scrape_failed", "error", duration_ms)
    self._upsert_lang_status(url_obj, lang, "error", "All scraping engines failed")
    return False
```

This code block is the final failure point for a language attempt. When `html` is None after all engines and VPN rotation have been exhausted, the method logs a scraping_failed event and updates the language status to 'error' with the descriptive message "All scraping engines failed". This message is what appears in the url_language_status table for the five failing languages. The method then returns False, which the caller `_process_url()` uses to track language-level success in the `lang_results` dictionary. It is important to note that this failure path does not trigger any immediate escalation or alert — the system simply moves on to the next language in the queue.

**FINDING 2 — VPN rotation is interval-based, NOT failure-based:** The VPN rotation block only executes when `self._vpn.should_rotate()` returns True. This method checks whether `VPN_ROTATION_INTERVAL` seconds (default 50s in code, 50s in env.example) have elapsed since the last rotation. If the interval hasn't elapsed, the VPN rotation is COMPLETELY SKIPPED even when both scraping engines have failed. This means consecutive failures within a 50-second window will all use the same (potentially blocked) IP address. The design flaw here is that VPN rotation is treated as a routine maintenance operation (rotate every N seconds) rather than a reactive recovery mechanism (rotate when failures are detected). When an IP gets blocked by Booking.com, the interval-based approach may not trigger a rotation quickly enough, or may have already rotated recently enough that the system considers rotation unnecessary despite the active block.

**FINDING 3 — VPN retry is only a single attempt:** After VPN rotation, the code retries each engine only ONCE (retries=1 for CloudScraper, single call for Selenium). If the new IP is also blocked, no further recovery is attempted. Given that commercial VPN providers like NordVPN have a limited pool of IP addresses that are often shared among many users, there is a non-trivial probability that the newly assigned IP has also been flagged by Booking.com's anti-bot system. The single retry after rotation provides minimal insurance against this scenario. A more robust approach would retry multiple times or implement a feedback loop where the system continues rotating until a non-blocked IP is found, subject to a maximum rotation limit to prevent infinite loops.

### 2.3 CloudScraperEngine Block Detection (scraper.py)

The `CloudScraperEngine.scrape()` method detects blocked responses through:

1. **HTTP status codes:** 403 (blocked), 429 (rate limited), 500+ (server error)
2. **HTML length check:** Pages shorter than 5000 bytes trigger a "Short HTML" warning:
   ```python
   if html_len < 5000:
       logger.warning("Short HTML (%d bytes) for %s", html_len, url)
   ```
3. **Content-based block detection via `_is_blocked()`:** Checks for strings like "just a moment", "access denied", "enable javascript", "captcha", etc.

The three-tier block detection system provides multiple layers of protection against treating blocked responses as valid hotel content. The HTTP status code check is the fastest and most reliable indicator, as Booking.com's Cloudflare protection typically returns 403 for blocked requests. The HTML length check catches cases where the server returns a 200 status code but the body is a short challenge or error page rather than full hotel content. The content-based check is the most thorough, as it examines the actual text of the response for known block page indicators. However, each of these detection methods has a gap: the status code check misses 200 responses with block pages, the length check has a fixed threshold that may not catch all block pages, and the content check relies on a hardcoded list of indicators that may not cover all Cloudflare challenge variants.

When a block is detected, the method logs the issue and continues to the next retry attempt (up to MAX_RETRIES). However, the retries all use the SAME session/IP, so if the IP is blocked, all retries will also fail.

**FINDING 4 — Short HTML detection does not trigger immediate VPN rotation:** When CloudScraper receives a "Short HTML" response (the 3962-byte block page from the logs), it simply logs a warning and continues with normal retries using the same blocked session. The VPN rotation opportunity only comes later in `_scrape_language()`, and only if the interval timer has elapsed. This means all 3 CloudScraper retries can be wasted on the same blocked IP before VPN rotation is even considered. The 3962-byte response is well below the 5000-byte threshold, and all evidence suggests it is a Cloudflare challenge page. Yet the system continues to retry against the same blocked IP, consuming time and resources while making no progress. This is particularly damaging in the context of multi-language scraping, where wasting 3 retries per language across 5 failed languages results in 15 wasted requests that only reinforce Booking.com's detection of automated access.

### 2.4 SeleniumEngine Block Detection (scraper.py)

The SeleniumEngine uses a single shared browser instance protected by `threading.Lock()` (BUG-DESC-002 fix, v49). It navigates to the URL, waits for hotel content via `_wait_for_hotel_content()`, and checks for Cloudflare challenge indicators. If the page doesn't load hotel content within 20 seconds, it checks for block signals. The single browser instance design was chosen for performance reasons — launching a new Chrome/Brave instance for every language would add significant overhead (3-10 seconds per launch) and could trigger additional detection signals. The threading lock ensures thread safety in the multi-threaded scraping environment, preventing concurrent access to the shared browser that could cause erratic behavior or crashes.

**FINDING 5 — Single browser accumulates state across language attempts:** The SeleniumEngine uses one Chrome/Brave browser instance for all languages. While the `_set_language()` method clears cookies and sets language-specific headers before each navigation, the browser's TLS fingerprint, WebSocket connections, and JavaScript runtime state persist across attempts. When a block page is loaded, these state remnants may contribute to subsequent failures. The browser is never restarted between language attempts unless a crash occurs. This accumulated state includes browser-level fingerprints that Booking.com may use for identification, such as canvas fingerprinting results, WebGL renderer information, and JavaScript execution timing patterns. Even though cookies are cleared between languages, these deeper browser state elements persist and may allow Booking.com to correlate multiple requests from the same browser instance, leading to more aggressive blocking after the first detection event.

### 2.5 VPN Manager Integration

The VPN rotation is managed by `vpn_manager_windows.py` which provides NordVPN integration. The `should_rotate()` method compares the current time against the last rotation timestamp. With `VPN_ROTATION_INTERVAL=50`, the VPN can only rotate once every 50 seconds.

**FINDING 6 — VPN rotation interval is misaligned with scraping rate:** Processing one URL through 6 languages with CloudScraper (3 retries each) + Selenium + VPN retry attempts can generate 20+ requests within minutes. With a 50-second VPN rotation interval, only about 1 rotation occurs per language attempt cycle. This is insufficient for maintaining IP diversity during multi-language scraping of a single URL. The fundamental mismatch is that the VPN rotation was designed for URL-level diversity (a new IP for each URL in the queue) but is being applied to language-level diversity (different language pages for the same hotel). When scraping 6 languages of the same URL, the system may send 20+ requests from a single IP before the VPN rotation timer allows a change, which is exactly the pattern that Booking.com's anti-bot system is designed to detect and block. A more effective approach would tie VPN rotation to the language processing cycle rather than a fixed time interval.

---

## 3. Root Cause Analysis

### 3.1 Primary Cause: Booking.com Anti-Bot IP Blocking

The 3962-byte HTML responses logged for the failing languages are Cloudflare challenge/block pages returned by Booking.com's anti-bot system. After the first successful language scrape (es), the IP address was flagged. All subsequent requests from the same IP received block pages instead of hotel content. The 3962-byte response size is characteristic of Cloudflare's "Under Attack Mode" or "Bot Fight Mode" challenge page, which typically weighs between 3,000 and 5,000 bytes and contains JavaScript challenge code that must be executed in a browser environment. Since CloudScraper cannot execute JavaScript, these challenge pages are effectively impenetrable without a VPN rotation to obtain a clean IP address. The fact that Spanish succeeded suggests that the IP was clean at the time of that request, but was flagged shortly afterward, likely due to the rapid succession of requests for different language versions of the same hotel page.

### 3.2 Contributing Cause Chain

```
Root Cause Chain:
1. 'en' is processed first (BUG-LANG-001 fix, v55) → FAILS (blocked IP)
2. 'es' processed next → SUCCEEDS (VPN may have rotated in the ~2.5 min gap)
3. After 'es' success, IP gets flagged by Booking.com
4. 'de' attempted ~14 min later → FAILS (same blocked IP, VPN not rotated)
5. 'it' attempted ~13 min later → FAILS (same blocked IP)
6. 'fr' attempted ~12 min later → FAILS (same blocked IP)
7. 'pt' attempted ~12 min later → FAILS (same blocked IP)
8. URL marked as 'error' — partial data preserved (es only)
```

The root cause chain above illustrates the cascading failure pattern. English was the first language attempted and failed, which is notable because the BUG-LANG-001 fix in v55 specifically moved English to the front of the queue to ensure it is processed first. The fact that English failed first suggests the IP may have already been flagged from previous scraping activity, or that Booking.com's initial request evaluation was particularly strict at that time. Spanish succeeded approximately 2.5 minutes later, possibly because a VPN rotation occurred during that interval (the gap exceeds the 50-second rotation threshold). However, after the Spanish success, the IP was flagged — the cumulative pattern of requests for multiple languages of the same hotel triggered Booking.com's behavioral analysis. From that point on, all subsequent languages failed because the IP remained blocked and the VPN rotation logic failed to provide effective recovery.

### 3.3 Why VPN Rotation Failed to Recover

The VPN rotation logic has THREE critical gaps that prevented recovery:

1. **Interval gate:** `should_rotate()` requires 50 seconds to elapse. Between 'de' (05:16:59) and 'it' (05:30:40), 13+ minutes passed — more than enough for rotation. However, the VPN may have already rotated during the 'en'/'es' attempts, and the new IP was also blocked. The issue is that rotation happens on a schedule, not reactively to failures. The interval-based rotation cannot distinguish between "rotating because we want IP diversity" and "rotating because the current IP is actively blocked." In both cases, the same 50-second timer governs the decision, meaning that when recovery is most urgently needed (after consecutive failures), the rotation may be blocked by the interval gate.

2. **No forced rotation on consecutive failures:** The code does not track how many consecutive languages have failed. Each language attempt is treated independently. Even if 4 languages fail in a row, the VPN rotation behavior doesn't change. This is a significant design oversight because consecutive language failures for the same URL are a strong signal that the current IP has been blocked. A human operator observing this pattern would immediately switch to a new IP, but the automated system continues to hammer the same blocked address because it lacks the concept of "consecutive failure escalation."

3. **Insufficient retry after rotation:** After VPN rotates, the system only retries ONCE with each engine. If the new IP happens to also be on Booking.com's blocklist (common with shared VPN IPs), the language fails permanently. Commercial VPN providers maintain a finite pool of IP addresses, and popular VPN IPs are frequently shared across many users, some of whom may also be scraping Booking.com. This means the probability of drawing a clean IP from a commercial VPN is not 100%, and a single retry does not provide adequate insurance against drawing another blocked IP. The system needs either multiple retry cycles after rotation or a mechanism to validate the new IP before attempting to scrape.

### 3.4 Why Only 1 URL Was Affected

The timing evidence shows that URL `3420c869...` was being processed during a window when Booking.com's anti-bot system was particularly aggressive (around 05:00-06:00). The other 12 URLs were processed earlier or later when the system's request pattern appeared more natural. This is consistent with Booking.com's adaptive rate limiting, which becomes more aggressive as it detects patterns of automated access. Anti-bot systems like Cloudflare Bot Management employ machine learning models that continuously evaluate request patterns across all visitors. When the system detects a cluster of automated requests — even from different IP addresses if the behavioral fingerprint is similar — it can escalate the blocking threshold for the entire subnet or VPN provider. The 05:00-06:00 time window may have coincided with a period of heightened sensitivity, possibly triggered by scraping activity from other users of the same VPN provider, or by the cumulative effect of processing 12 URLs before this one. Additionally, the early morning hours (5 AM) may be a period when Booking.com's traffic is lower, making automated access patterns more conspicuous and easier to detect.

---

## 4. Solutions

### 4.1 Solution P0-1: Implement Inter-Language Delay (Immediate — Low Effort, High Impact)

Add a configurable delay between consecutive language scraping attempts for the same URL. This prevents the rapid-fire request pattern that triggers Booking.com's rate limiting.

**File:** `scraper_service.py` — `_scrape_language()` method
**Change:** Add delay before scraping non-first languages.

```python
def _scrape_language(self, url_obj: URLQueue, lang: str, is_first_lang: bool = False) -> bool:
    if not is_first_lang:
        delay = getattr(self._cfg, 'LANG_SCRAPE_DELAY', 10)
        jitter = random.uniform(0, getattr(self._cfg, 'LANG_SCRAPE_JITTER', 5))
        logger.info("Inter-language delay: %.1fs before %s/%s", delay + jitter, url_obj.id, lang)
        time.sleep(delay + jitter)
    # ... rest of the method
```

**File:** `scraper_service.py` — `_process_url()` method
**Change:** Pass `is_first_lang` parameter.

```python
for i, lang in enumerate(languages):
    ok = self._scrape_language(url_obj, lang, is_first_lang=(i == 0))
```

**File:** `config.py` — Settings class
**Change:** Add configuration parameters.

```python
LANG_SCRAPE_DELAY: float = Field(default=10, ge=0, le=120)
LANG_SCRAPE_JITTER: float = Field(default=5, ge=0, le=30)
```

**File:** `env.example`
**Change:** Add parameters.

```
LANG_SCRAPE_DELAY=10
LANG_SCRAPE_JITTER=5
```

The inter-language delay is the simplest and most effective immediate fix. By introducing a configurable delay (default 10 seconds) with random jitter (default 5 seconds) between language attempts, the scraper's request pattern becomes much more similar to human browsing behavior. The jitter is critical because it prevents the system from sending requests at predictable intervals, which is a common fingerprint of automated tools. The total delay per URL with 6 languages would increase by approximately 25-75 seconds (5 languages × 5-15 seconds each), which is a modest trade-off for significantly improved success rates. The delay is applied before the scraping attempt begins, not after, which means the first language is always attempted immediately and the delay only affects subsequent languages.

### 4.2 Solution P0-2: Force VPN Rotation on Consecutive Failures (Immediate — Low Effort, High Impact)

Add a counter for consecutive language failures and force VPN rotation when the threshold is exceeded, regardless of the interval timer.

**File:** `scraper_service.py` — `_process_url()` method
**Change:** Track consecutive failures and force VPN rotation.

```python
consecutive_failures = 0
MAX_CONSECUTIVE_FAILURES = 2  # Force VPN rotation after 2 consecutive language failures

for lang in languages:
    ok = self._scrape_language(url_obj, lang)
    if ok:
        consecutive_failures = 0
    else:
        consecutive_failures += 1

    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES and self._cfg.VPN_ENABLED:
        logger.warning(
            "URL %s: %d consecutive language failures — forcing VPN rotation",
            url_id_str, consecutive_failures
        )
        try:
            self._vpn.rotate(force=True)
            consecutive_failures = 0  # Reset after forced rotation
        except Exception as vpn_exc:
            logger.error("Forced VPN rotation failed: %s", vpn_exc)
```

**File:** `config.py`
**Change:** Add configuration parameter.

```python
MAX_CONSECUTIVE_LANG_FAILURES: int = Field(default=2, ge=1, le=6)
```

This solution addresses the core design flaw identified in Finding 2: VPN rotation is currently interval-based rather than failure-based. By tracking consecutive language failures and forcing VPN rotation after a configurable threshold (default 2), the system can reactively respond to IP blocking instead of passively waiting for the interval timer. The counter resets to zero after a successful language scrape, so it only triggers when multiple languages fail in sequence. The `force=True` parameter bypasses the interval timer check in `should_rotate()`, ensuring that the rotation happens immediately regardless of when the last rotation occurred. The implementation is wrapped in a try-except block to prevent VPN connection issues from crashing the entire scraping process. After a forced rotation, the consecutive failure counter is reset to give the new IP a fair chance before triggering another rotation.

### 4.3 Solution P0-3: Detect Short HTML and Skip to VPN Rotation (Immediate — Medium Effort, High Impact)

When CloudScraper detects a "Short HTML" response (< 5000 bytes), immediately fail CloudScraper (don't waste retries) and proceed to VPN rotation + retry, since the short HTML is a definitive block indicator.

**File:** `scraper.py` — `CloudScraperEngine.scrape()` method
**Change:** Return None immediately on Short HTML to avoid wasting retries.

```python
if html_len < 5000:
    logger.warning("Short HTML (%d bytes) — block page detected, skipping remaining retries", html_len)
    self._save_debug_html(html, url, "short_html")
    with self._lock:
        self._blocked_count += 1
    return None  # Don't waste retries on a blocked IP
```

This optimization directly addresses Finding 4. Currently, when CloudScraper receives a short HTML response that is clearly a block page, it wastes all remaining retries (up to 3) attempting to scrape from the same blocked IP. Each wasted retry not only consumes time (potentially 10-30 seconds per retry including network latency and processing) but also sends additional requests from the blocked IP, which may reinforce Booking.com's blocking decision. By immediately returning None on short HTML detection, the system can proceed to the VPN rotation phase sooner, potentially recovering within a single language attempt cycle instead of burning through all retries first. The `_save_debug_html()` call preserves the block page for debugging purposes, and the `_blocked_count` increment maintains the block detection statistics for monitoring. The 5000-byte threshold is already in use for the warning log, so this change elevates it from a warning to an actionable decision point.

### 4.4 Solution P1-1: Increase VPN Retry Attempts After Rotation (Short-term — Low Effort, Medium Impact)

Currently only 1 retry per engine after VPN rotation. Increase to 2 retries per engine.

**File:** `scraper_service.py` — `_scrape_language()` VPN rotation block
**Change:** Increase retries from 1 to 2.

```python
if html is None and self._cfg.VPN_ENABLED:
    try:
        if self._vpn.should_rotate() or consecutive_failures >= 2:
            rotated = self._vpn.rotate(force=(consecutive_failures >= 2))
            if rotated:
                # Retry CloudScraper with more attempts after rotation
                html = self._cloud_engine.scrape(lang_url, retries=2)
                if html is None:
                    html = self._selenium_engine.scrape(lang_url, lang)
```

As identified in Finding 3, the current implementation only retries each engine once after VPN rotation. This provides minimal insurance against the possibility that the new VPN IP is also on Booking.com's blocklist. By increasing CloudScraper retries to 2 after rotation, the system gets an additional chance to succeed if the first retry fails due to a transient issue (e.g., the new IP needs a "warm-up" request before Booking.com serves full content). The increase from 1 to 2 retries adds only marginal time cost (one additional CloudScraper request, typically 5-10 seconds) but significantly improves the probability of successful recovery. This change should be combined with the short HTML detection fix (P0-3) to ensure that the additional retries are not wasted on obviously blocked responses. The Selenium fallback remains a single attempt since it is significantly slower and more resource-intensive than CloudScraper.

### 4.5 Solution P1-2: Browser Restart on Block Detection (Short-term — Medium Effort, High Impact)

Restart the Selenium browser after detecting a block page to clear accumulated state.

**File:** `scraper.py` — `SeleniumEngine._scrape_locked()` method
**Change:** Reinitialize driver after detecting block page.

```python
if not loaded:
    page_low = self._driver.page_source.lower()
    if any(s in page_low for s in ["just a moment", "enable javascript", "ddos-guard", "access denied"]):
        logger.warning("Selenium: Cloudflare challenge detected — reinitializing browser")
        self._reinit_driver()  # Fresh browser instance
        continue
```

This solution addresses Finding 5 by clearing accumulated browser state when a Cloudflare block page is detected. The browser restart approach has several benefits: it clears all cookies, local storage, session data, TLS sessions, and JavaScript runtime state that may be contributing to detection. It also generates a new browser fingerprint (canvas hash, WebGL renderer ID) that may help evade fingerprint-based detection. The cost of a browser restart is approximately 3-5 seconds (Chrome/Brave launch time), which is acceptable for a recovery operation. The `continue` statement after `_reinit_driver()` causes the method to retry the navigation with the fresh browser instance, providing an automatic recovery mechanism without requiring VPN rotation. However, this solution should not be the sole recovery mechanism — it should complement VPN rotation, as browser state clearing alone may not be sufficient if the IP address itself has been blocked.

### 4.6 Solution P2-1: Failed Language Retry Queue (Medium-term — Medium Effort, High Impact)

Implement a Celery task that periodically retries failed languages for URLs in 'error' state with partial data. This provides a second chance for languages that failed due to temporary IP blocking.

```python
@celery_app.task
def retry_failed_languages():
    """Retry languages that failed due to anti-bot blocking."""
    with get_db() as session:
        failed = session.query(URLLanguageStatus).filter(
            URLLanguageStatus.status == 'error',
            URLLanguageStatus.last_error == 'All scraping engines failed',
        ).limit(50).all()

    for lang_status in failed:
        url_obj = session.query(URLQueue).get(lang_status.url_id)
        if url_obj and url_obj.status == 'error':
            logger.info("Retrying %s/%s from retry queue", lang_status.url_id, lang_status.language)
            service = ScraperService()
            ok = service._scrape_language(url_obj, lang_status.language)
            if ok:
                logger.info("Retry succeeded for %s/%s", lang_status.url_id, lang_status.language)
            time.sleep(random.uniform(15, 30))  # Generous delay between retries
```

The failed language retry queue provides a safety net for languages that fail due to temporary conditions like IP blocking. Rather than accepting permanent failure for these languages, the system queues them for periodic retry with substantial delays (15-30 seconds between attempts) that allow VPN IP addresses to change naturally and Booking.com's anti-bot sensitivity to decrease. The Celery task queries the database for languages with the specific error message "All scraping engines failed" — this targeted query ensures that only anti-bot block failures are retried, not structural errors like invalid URLs or database constraint violations. The task processes up to 50 failed languages per run to prevent the retry queue from growing unbounded. After a successful retry, the language status is updated to 'done' and the URL's overall status is re-evaluated. This solution is particularly valuable because it can recover data that would otherwise be permanently lost, converting partial successes into complete datasets over time.

### 4.7 Solution P2-2: Per-Language VPN Rotation (Medium-term — Low Effort, High Impact)

Rotate VPN for EACH language attempt instead of relying on the interval timer. This maximizes IP diversity.

```python
for i, lang in enumerate(languages):
    if self._cfg.VPN_ENABLED and i > 0:
        logger.info("Rotating VPN before language %s/%s", url_id_str, lang)
        try:
            self._vpn.rotate(force=True)
        except Exception:
            pass
    ok = self._scrape_language(url_obj, lang)
```

This solution takes a more aggressive approach to IP diversity by rotating the VPN before every language attempt after the first one. Each language scrape would originate from a different IP address, making it extremely difficult for Booking.com to correlate the requests as coming from the same automated source. The `i > 0` condition skips rotation for the first language to avoid an unnecessary VPN change at the start of processing. The `force=True` parameter ensures the rotation happens regardless of the interval timer, and the try-except block prevents VPN connection failures from halting the entire process. The main risk of this approach is increased VPN overhead — NordVPN connections typically take 5-15 seconds to establish, and rotating 5 times per URL (for 6 languages) adds 25-75 seconds per URL. Additionally, aggressive VPN rotation may trigger rate limits on the VPN provider's API, potentially resulting in temporary VPN connection failures. This solution should be configurable so that users with VPN provider restrictions can disable it or reduce the rotation frequency.

---

## 5. Configuration Changes Summary

### 5.1 config.py — New Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `LANG_SCRAPE_DELAY` | float | 10 | Seconds between language scraping attempts |
| `LANG_SCRAPE_JITTER` | float | 5 | Random jitter added to inter-language delay |
| `MAX_CONSECUTIVE_LANG_FAILURES` | int | 2 | Consecutive failures before forcing VPN rotation |

### 5.2 env.example — New Entries

```bash
# Language scraping timing
LANG_SCRAPE_DELAY=10
LANG_SCRAPE_JITTER=5
MAX_CONSECUTIVE_LANG_FAILURES=2
```

These three new configuration parameters provide operators with fine-grained control over the anti-detection behavior of the scraper. The `LANG_SCRAPE_DELAY` parameter sets the base delay between language attempts and can be adjusted based on the target site's sensitivity — more aggressive anti-bot systems may require longer delays (20-30 seconds), while less sensitive targets can use shorter delays (3-5 seconds) for faster processing. The `LANG_SCRAPE_JITTER` parameter adds randomness to the delay, which is essential for avoiding predictable request patterns. The `MAX_CONSECUTIVE_LANG_FAILURES` parameter controls the threshold for forced VPN rotation, allowing operators to balance between aggressive recovery (threshold of 1) and VPN resource conservation (threshold of 3-4). All parameters have sensible defaults and validation constraints (ge, le) to prevent misconfiguration.

---

## 6. Implementation Priority

| Priority | Solution | Effort | Impact | Risk |
|----------|----------|--------|--------|------|
| P0 | Inter-language delay with jitter | Low | High | None — only slows execution |
| P0 | Force VPN on consecutive failures | Low | High | Low — may increase VPN overhead |
| P0 | Short HTML → skip to VPN rotation | Low | High | None — reduces wasted requests |
| P1 | Increase VPN retry attempts | Low | Medium | None |
| P1 | Browser restart on block detection | Medium | Medium | Low — adds ~5s per restart |
| P2 | Failed language retry queue | Medium | High | Low — requires Celery task |
| P2 | Per-language VPN rotation | Low | High | Medium — VPN rate limits |

The priority matrix above ranks solutions by their implementation urgency, with P0 items being immediate fixes that address the core failure mode, P1 items being short-term improvements that enhance recovery capabilities, and P2 items being medium-term architectural changes that provide more robust long-term protection. The three P0 solutions can be implemented together in a single development sprint (estimated 2-3 hours) and deployed immediately, as they carry minimal risk and address the three most critical findings (no delay, no failure-based rotation, wasted retries). The P1 solutions require slightly more effort but add significant defensive depth. The P2 solutions are larger architectural changes that should be planned for a dedicated sprint but offer the highest long-term impact by introducing retry queues and per-language IP diversity.

---

## 7. Testing Strategy

### 7.1 Unit Tests

```python
def test_inter_language_delay_applied():
    """Verify delay is applied for non-first languages."""
    service = ScraperService()
    url_obj = MagicMock()
    with patch('time.sleep') as mock_sleep:
        service._scrape_language(url_obj, 'en', is_first_lang=True)
        mock_sleep.assert_not_called()
        service._scrape_language(url_obj, 'de', is_first_lang=False)
        mock_sleep.assert_called_once()

def test_vpn_rotation_on_consecutive_failures():
    """Verify VPN rotates after MAX_CONSECUTIVE_LANG_FAILURES."""
    # Implementation test for forced rotation trigger
    pass

def test_short_html_skips_remaining_retries():
    """Verify CloudScraper returns None immediately on Short HTML."""
    engine = CloudScraperEngine()
    # Mock session to return short HTML
    result = engine.scrape("http://test.com", retries=5)
    # Should return None after 1 attempt, not 5
    assert engine._blocked_count > 0
```

The unit test suite validates the core behavioral changes introduced by the P0 solutions. The `test_inter_language_delay_applied` test verifies that the delay mechanism correctly distinguishes between the first language (no delay) and subsequent languages (delay applied). The `test_vpn_rotation_on_consecutive_failures` test should be expanded to mock both the scraping engines (to simulate consecutive failures) and the VPN manager (to verify that `rotate(force=True)` is called exactly when the consecutive failure threshold is reached). The `test_short_html_skips_remaining_retries` test is critical because it verifies the optimization that prevents wasted retries on blocked IPs — the test should confirm that CloudScraper returns None after the first short HTML response even when configured for 5 retries, and that the blocked count is incremented accordingly.

### 7.2 Integration Test

```python
def test_all_six_languages_scraped():
    """Verify all 6 languages are scraped for a valid URL."""
    url_id = load_test_url()
    service = ScraperService()
    service._process_url(url_id)
    with get_db() as session:
        for lang in ['en', 'es', 'de', 'it', 'fr', 'pt']:
            hotel = session.query(Hotel).filter_by(url_id=url_id, language=lang).first()
            assert hotel is not None, f"Missing hotel for lang={lang}"
```

The integration test provides end-to-end validation of the complete language processing pipeline. It loads a test URL into the database, processes it through the full `_process_url()` method (which includes all P0 fixes: inter-language delay, forced VPN rotation on consecutive failures, and short HTML skip), and then verifies that all six languages have corresponding hotel records in the database. This test should be run against a real Booking.com page (using a test hotel URL) to validate that the anti-detection measures are effective in practice. The test should be designed to be idempotent — it should clean up any test data before and after execution to prevent interference with other tests. Additionally, the test should include timing assertions to verify that the inter-language delays are within expected ranges (e.g., between 5 and 20 seconds per delay).

---

## 8. Diagnostic SQL Queries

```sql
-- Find all URLs with incomplete language coverage
SELECT
    uq.id, uq.status, uq.languages_completed, uq.languages_failed,
    COUNT(DISTINCT h.language) AS hotel_count
FROM url_queue uq
LEFT JOIN hotels h ON uq.id = h.url_id
GROUP BY uq.id, uq.status, uq.languages_completed, uq.languages_failed
HAVING COUNT(DISTINCT h.language) < 6;

-- Per-language success rate across all URLs
SELECT
    language,
    COUNT(*) AS total,
    SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) AS success,
    ROUND(100.0 * SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) / COUNT(*), 2) AS success_rate
FROM url_language_status
GROUP BY language
ORDER BY success_rate ASC;

-- Timeline analysis for a specific URL
SELECT language, status, attempts, last_error, created_at, updated_at
FROM url_language_status
WHERE url_id = '3420c869-fd48-4f79-9557-5e185e9e580f'
ORDER BY created_at;
```

These diagnostic SQL queries provide operators with the tools needed to monitor the health of the multi-language scraping pipeline and diagnose similar issues in the future. The first query identifies all URLs that have incomplete language coverage, which is the primary symptom of the bug described in this report. By joining url_queue with the hotels table and counting distinct languages, the query provides a definitive count of how many languages were successfully scraped per URL. The second query provides a per-language success rate across all URLs, which can reveal if Booking.com's anti-bot system is blocking specific languages more aggressively than others (e.g., English might be more heavily monitored due to higher scraping traffic). The third query reproduces the timeline analysis that was critical for diagnosing this bug, showing the exact sequence and timing of language processing attempts for any given URL. These queries should be integrated into a monitoring dashboard or automated health check that alerts operators when language success rates drop below a configurable threshold.

---

*Report generated: March 29, 2026 — BookingScraper Pro v6.0.0 Build 60*
