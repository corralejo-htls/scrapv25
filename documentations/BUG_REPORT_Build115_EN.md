# BookingScraper Pro v6.0.0 — Build 115 Bug Report (EN)

**Build:** 115  
**Base build:** 114  
**Platform:** Windows 11 / Python 3.14 / PostgreSQL 14+ / Brave 148 / ChromeDriver 148  
**Date:** 2026-06-02  
**Incident refs:** INC-2026-0602-VILLADVOR-001 · INC-2026-0602-RADISSON-001  
**Severity:** CRITICAL (process halt, 2h45m scraping blackout confirmed in logs)

---

## 1. Executive Summary

Build 115 addresses **five root-cause bugs** confirmed by cross-referencing the
incident report (`INC-2026-0602-VILLADVOR-001`), the four uploaded log files, and
the GitHub repository codebase (Build 114). All five bugs are distinct failure
modes that can independently cause the worker to hang indefinitely or fail to
recover after a forced shutdown.

| Bug ID | Severity | Root Cause | Status |
|--------|----------|-----------|--------|
| BUG-BROWSER-RESTART-HANG-001 | **CRITICAL** | `driver.quit()` blocks forever on Windows when Brave is frozen | Fixed |
| BUG-BROWSER-LAUNCH-HANG-001 | **HIGH** | `webdriver.Chrome()` blocks forever if Brave/ChromeDriver don't respond | Fixed |
| BUG-CHAL-DETECT-002 | **HIGH** | Challenge redirect detected only BEFORE `driver.get()`, not after | Fixed |
| BUG-GALLERY-CHAL-001 | **HIGH** | Gallery click can trigger challenge redirect without detection | Fixed |
| BUG-WORKER-NORESTART-001 | **CRITICAL** | Worker not restarted after watchdog `os._exit(1)` | Fixed |
| BUG-BLOCK-IND-002 | MEDIUM | Missing Cloudflare challenge indicators in `_BLOCK_INDICATORS` | Fixed |

---

## 2. Log Analysis — Confirmed Timeline (2026-06-02)

### 2.1 Confirmed Sequence (from uploaded logs)

```
15:52:40  Worker started (Celery Beat + Worker)
15:53:44  141 URLs loaded via POST /urls/load-csv
15:53:45  First real batch starts (task 95c05aab, 430s runtime)
          → Processes 2 URLs: fd38ceca + 77b3927e (both complete 6/6 langs)
16:00:55  Batch 1 complete (430.30s)
16:00:57  Batch 2 starts (pending=139, dispatches 2 workers)
          → URL c186be75 (wild-bolz-emotel) lang=en SUCCESS at 16:02:29
          → GalleryModalExtractor: 22 photos (badge mismatch: 22 vs 44)
16:02:44  VPN rotation triggered (93s ≥ 50s threshold)
16:02:55  VPN connected → Switzerland IP 194.15.111.47
16:02:55  reset_browser() begins: "Restarting Selenium browser after VPN rotation"
          *** HANG: driver.quit() never returns ***
          *** "Browser reset complete" message NEVER appears ***
16:03:04  WATCHDOG fires → os._exit(1) → worker process killed
          [Watchdog task ID = "None" — timing matches ~600s from batch start]
16:03:12  Beat continues sending tasks every 30s with NO worker to consume them
          ...
18:49:12  Beat log ends — 2h46m of task accumulation with no worker
```

### 2.2 Villa Dvor Challenge Incident (separate session)

The URL from the incident report contains `chal_t=1780412536589` (UTC timestamp
~18:02:16 on 2026-06-02 = ~20:02 Madrid local time). This is **after** the worker
died at ~16:03 local time, confirming it occurred in a **separate, later session**
not fully captured in the provided logs. The analysis applies directly to any
future session where Booking.com redirects to a challenge URL.

---

## 3. Bug Details and Fixes

### BUG-BROWSER-RESTART-HANG-001 (CRITICAL) — Confirmed Root Cause of Worker Hang

**Root Cause:**  
`driver.quit()` inside `reset_browser()` (within `self._lock`) blocked
indefinitely because Brave was frozen on a JavaScript challenge page
(triggered by gallery/facility operations from the previous scrape pass).
ChromeDriver maintained the IPC pipe waiting for Brave's response to the
quit command. Brave's JS challenge loop never yielded control.

**Evidence:** Log line at 16:02:55: `"BUG-LANG-002-FIX: Restarting Selenium
browser after VPN rotation."` — the subsequent `"Browser reset complete"`
message **never appeared**. Watchdog fired 9 seconds later, but the watchdog
had been started ~600s earlier (from a prior task), confirming the actual
hang origin.

**Fix (Build 115):**  
`driver.quit()` now runs inside a daemon thread with `join(BROWSER_QUIT_TIMEOUT_S=30s)`.
If the timeout expires: `psutil` force-kills the ChromeDriver/Brave process tree
by PID. `self._driver = None` is always set so the lock is released.

**Files:** `app/scraper.py` (`reset_browser`), `app/config.py` (`BROWSER_QUIT_TIMEOUT_S`)

---

### BUG-BROWSER-LAUNCH-HANG-001 (HIGH) — Companion to RESTART-HANG

**Root Cause:**  
`webdriver.Chrome()` instantiation inside `_get_driver()` (also within
`self._lock`) could similarly block indefinitely if Brave or ChromeDriver do
not respond during initialization — for example, immediately after a VPN
rotation when the system network stack is re-initializing.

**Fix (Build 115):**  
`webdriver.Chrome()` now runs in a daemon thread with `join(BROWSER_LAUNCH_TIMEOUT_S=60s)`.
On timeout, a `WebDriverException` is raised so the language pass fails cleanly
and will be retried in the next batch cycle.

**Files:** `app/scraper.py` (`_get_driver`), `app/config.py` (`BROWSER_LAUNCH_TIMEOUT_S`)

---

### BUG-CHAL-DETECT-002 (HIGH) — Post-Navigation Challenge Not Detected

**Root Cause:**  
`BUG-CHAL-DETECT-001-FIX` (Build 114) checked the URL for challenge params
(`chal_t=`, `force_referer=`) **before** calling `driver.get()`. However,
Booking.com/Cloudflare can redirect to a challenge URL **after** the initial
page loads — triggered when the page's JS fingerprinting script evaluates
browser characteristics.

**Evidence from incident report:**  
The frozen URL `villa-dvor.en-gb.html?lang=en-gb&chal_t=1780412536589&force_referer=&activeTab=photosGallery#hp_facilities_box` was the **result of a redirect**, not the original URL. The `activeTab=photosGallery` segment suggests the gallery JS triggered the fingerprint evaluation.

**Fix (Build 115):**  
After `driver.get(url)` completes, `driver.current_url` is immediately checked
via `_url_has_challenge_params()`. If challenge params are present:
- `window.stop()` is called to halt any pending JS
- `None` is returned → the caller rotates VPN and retries

**Files:** `app/scraper.py` (`_fetch_with_selenium`)

---

### BUG-GALLERY-CHAL-001 (HIGH) — Gallery Navigation Triggers Challenge Undetected

**Root Cause:**  
The `_open_gallery()` method calls `trigger.click()` on the first hotel image.
This click can trigger a JS event chain that causes Booking.com to redirect the
browser to a challenge URL. After the click, `driver.current_url` was never
inspected — the challenge page would silently become the active page, and
subsequent operations (JS extraction, `page_source` read) would hang or produce
garbage.

**Fix (Build 115):**  
After `trigger.click()` and `time.sleep(1.5)`, `driver.current_url` is checked
for challenge params. If detected: `window.stop()` is called and `0` is returned
(graceful degradation — gallery skipped, scraping of other data continues).

The same check is applied in `GalleryModalExtractor.extract()` after `driver.get(url)`
when a URL is explicitly passed.

**Files:** `app/scraper.py` (`_open_gallery`), `app/image_classifier.py` (`GalleryModalExtractor.extract`)

---

### BUG-WORKER-NORESTART-001 (CRITICAL) — No Auto-Restart After Watchdog Kill

**Root Cause:**  
When the watchdog calls `os._exit(1)`, the Celery worker process dies with
exit code 1. The `cmd /k` terminal window launched by `inicio_rapido.bat`
stays open (empty prompt) but no process is running. The Celery Beat continues
sending tasks every 30 seconds, queueing them in Redis, but no worker consumes
them.

**Evidence:** Beat log from 16:03 to 18:49 — **2h46m** of continuous
`auto-scrape-pending-every-30s` sends with zero worker activity.

**Fix (Build 115):**  
`start_celery.bat` now contains a `:RESTART_LOOP`. After the Celery process
exits:
- Exit code **0** (graceful shutdown via Ctrl+C): no restart, terminal shows
  "Worker stopped cleanly."
- Exit code **!= 0** (watchdog kill, crash): waits 10 seconds and restarts.
  Ctrl+C during the 10-second wait cancels the restart.

`inicio_rapido.bat` updated to call `start_celery.bat` instead of inlining the
`python -m celery` command directly.

**Files:** `start_celery.bat`, `inicio_rapido.bat`

---

### BUG-BLOCK-IND-002 (MEDIUM) — Missing Cloudflare Challenge Indicators

**Root Cause:**  
`_BLOCK_INDICATORS` did not include several Cloudflare challenge page text
variants. Challenge pages with custom templates (e.g. Booking.com's branded
challenge) may not contain "just a moment" or "checking your browser" but do
contain `"verifying your browser"`, `"please wait while we verify"`, or
have `"chal_t"` embedded as a JavaScript variable in the page source.

**Fix (Build 115):**  
Three new indicators added: `"verifying your browser"`, `"please wait while
we verify"`, `"chal_t"` (as page source text, distinct from URL parameter).

**Files:** `app/scraper.py` (`_BLOCK_INDICATORS`)

---

## 4. Gallery Count Mismatch (Observation — Not a Bug)

**Observed:** `Gallery count mismatch for hotel 5de7dc22: classified=22 vs page badge=44`

This warning (`16:02:14`) indicates the gallery modal scroll captured only 22
photos while the page hero badge shows 44. This is a **data quality gap**, not
a blocking bug. Probable cause: the `GALLERY_MODAL_SCROLL_ITERATIONS=8`
setting is insufficient for hotels with 44+ gallery photos. Consider increasing
to 12-15 for hotels where the mismatch is > 50%.

No code change required in Build 115 — recommend monitoring and adjusting
`GALLERY_MODAL_SCROLL_ITERATIONS` in `.env` if needed.

---

## 5. Configuration Changes

| Variable | Default | Description |
|----------|---------|-------------|
| `BROWSER_QUIT_TIMEOUT_S` | `30` | Timeout for `driver.quit()` thread join |
| `BROWSER_LAUNCH_TIMEOUT_S` | `60` | Timeout for `webdriver.Chrome()` thread join |
| `VPN_SUBPROCESS_TIMEOUT_S` | `45` | (Build 114, now documented in env.example) |
| `VPN_ROTATE_TIMEOUT_S` | `90` | (Build 114, now documented in env.example) |
| `TASK_WATCHDOG_TIMEOUT_S` | `600` | (Build 114, now documented in env.example) |

**Action required:** Add to `.env`:
```
BROWSER_QUIT_TIMEOUT_S=30
BROWSER_LAUNCH_TIMEOUT_S=60
VPN_SUBPROCESS_TIMEOUT_S=45
VPN_ROTATE_TIMEOUT_S=90
TASK_WATCHDOG_TIMEOUT_S=600
```

Also verify `VPN_ROTATION_INTERVAL` in `.env`. Logs show `50s` threshold
(Build 114 raised the default to `120s` but the `.env` was not updated).
Set: `VPN_ROTATION_INTERVAL=120`

---

## 6. Files Modified

| File | Changes |
|------|---------|
| `app/__init__.py` | `BUILD_VERSION = 115`, changelog entries |
| `app/config.py` | `BUILD_VERSION default=115`, `BROWSER_QUIT_TIMEOUT_S`, `BROWSER_LAUNCH_TIMEOUT_S` |
| `app/scraper.py` | `_BLOCK_INDICATORS` (2 new), `_get_driver` (launch timeout), `reset_browser` (quit timeout+psutil), `_fetch_with_selenium` (post-nav check), `_open_gallery` (challenge check) |
| `app/image_classifier.py` | `GalleryModalExtractor.extract()` challenge check after `driver.get(url)` |
| `start_celery.bat` | Auto-restart loop (`:RESTART_LOOP`) |
| `inicio_rapido.bat` | Calls `start_celery.bat` instead of inline command |
| `env.example` | Documents all Build 114+115 timeout variables |

---

## 7. Recovery Procedure for Current State

1. **Stop all services:** `stop_server.bat` + `stop_celery.bat`
2. **Check database URL status:**
   ```sql
   SELECT url, status, languages_completed, languages_failed 
   FROM url_queue 
   WHERE status IN ('processing', 'error') 
   ORDER BY updated_at DESC;
   ```
3. **Reset stuck processing URLs:**
   ```sql
   UPDATE url_queue SET status = 'pending' 
   WHERE status = 'processing' AND updated_at < NOW() - INTERVAL '30 minutes';
   ```
4. **Deploy Build 115 files** (replace modified files)
5. **Update `.env`** with new variables above
6. **Restart via `inicio_rapido.bat`** — worker now has auto-restart

---

*Build 115 — Generated 2026-06-02*  
*Sources: app/scraper.py, app/image_classifier.py, app/config.py, app/__init__.py, start_celery.bat, inicio_rapido.bat, env.example*  
*Incident refs: INC-2026-0602-VILLADVOR-001, INC-2026-0602-RADISSON-001*
