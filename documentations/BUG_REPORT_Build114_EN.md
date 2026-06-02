# BUG REPORT — BookingScraper Pro v6.0.0 Build 114
**Incident:** INC-2026-0602-RADISSON-001  
**Platform:** Windows 11 Pro / Python 3.14 / Celery solo pool / NordVPN / Brave + Selenium  
**Date:** 2026-06-02  
**Previous Build:** 113  
**Current Build:** 114  

---

## Executive Summary

The Celery worker for task `d1c14507-3c8c-48c0-b3b8-3594f366d546` froze for **6 hours and 13 minutes** (02:16:23 → 08:16:07) during a VPN rotation triggered before loading `radisson-graz.de`. The browser window remained visible displaying a challenge-annotated URL. No new URLs were processed during the entire freeze. Four root causes were identified and fixed.

---

## Verified Timeline

| Time | Event | Source |
|------|-------|--------|
| 02:12:26 | Task `d1c14507` received — batch of 2 URLs | Celery Worker |
| 02:12:42 | Proactive VPN rotation → France (FR) | Worker INFO |
| 02:14:01 | `radisson-graz.en` SUCCESS — 84 photos | Worker INFO |
| 02:14:19 | `minihotel-graz.en` Cloudflare challenge **1/3** | Worker WARNING |
| 02:14:28 | `radisson-graz.es` begins | Worker INFO |
| 02:14:43 | VPN rotation → US (time-based, 121s elapsed) | Worker INFO |
| 02:14:49 | `minihotel-graz.en` Cloudflare challenge **2/3** | Worker WARNING |
| 02:14:56 | VPN connected → US (IP: 194.124.76.64) | Worker INFO |
| 02:15:18 | `minihotel-graz.en` Cloudflare challenge **3/3** | Worker WARNING |
| 02:15:21 | `minihotel-graz.en` FAILS — error-triggered VPN rotation → DE | Worker ERROR |
| 02:15:22 | Brave browser reset | Worker INFO |
| 02:16:09 | **`radisson-graz.es` SUCCESS** | Worker INFO |
| 02:16:09 | Inter-language delay 14s before `.de` | Worker INFO |
| **02:16:23** | **VPN rotation starts before `radisson-graz.de` — LAST LOG ENTRY** | Worker INFO |
| **[6-HOUR GAP]** | **Zero log output — complete freeze** | — |
| 08:16:07 | Chromium USB error (OS-level, frozen process) | ERROR |

---

## Root Cause Analysis

### BUG-VPN-HANG-001 — `subprocess.run` pipe hang on Windows 11 (PRIMARY CAUSE)

**File:** `app/vpn_manager_windows.py` → `_connect_via_cli()`

**Problem:**  
`subprocess.run([nordvpn.exe, ...], capture_output=True, timeout=60)` can hang **indefinitely beyond its declared timeout** on Windows 11 when `nordvpn.exe` spawns child processes (service communication processes, helper executables) that inherit the `stdout`/`stderr` pipe handles.

When the `timeout` parameter expires, Python's `subprocess` module kills the **parent** process. However, child processes that inherited the pipe handles keep those handles open. `communicate()` then waits indefinitely for EOF on the captured pipes — a wait that never arrives because child processes remain alive.

**Evidence:** Last log at 02:16:23 was `VPN: direct reconnect to <country> (no disconnect — popup-free)` immediately before `self.connect(new_country)` → `_connect_via_cli()`. Zero subsequent logs for 6 hours. The Chromium USB error at 08:16:07 confirms the process was still alive but completely frozen.

**Fix:** `_subprocess_run_safe()` method added. Executes `nordvpn.exe` via `subprocess.Popen` inside a **daemon thread**. `threading.Thread.join(timeout+5)` provides a guaranteed wall-clock cutoff regardless of pipe state. If the thread is still alive after join, it is abandoned (daemon threads are cleaned up on process exit) and `(-1, "", "TIMEOUT:Ns")` is returned. The caller treats this as a connection failure.

---

### BUG-TASK-HANG-001 — Celery `time_limit` non-functional on Windows 11 (SECONDARY CAUSE)

**File:** `app/tasks.py` → `@shared_task` decorator

**Problem:**  
The `@shared_task` decorator for `scrape_pending_urls` declared `time_limit=300` (5 min hard kill) and `soft_time_limit=240` (4 min warning). These parameters are implemented via POSIX signals `SIGKILL` and `SIGUSR1` respectively. **Neither signal exists on Windows 11.** With `pool=solo`, the Celery worker runs in the same process as the task — even if signals were available, there is no separate process to receive them.

**Evidence:** The previous task `136f0f21` completed in **484 seconds** (> 300s `time_limit`) with no issues. Task `d1c14507` ran for **22,000+ seconds** without being terminated.

**Fix:** `time_limit` and `soft_time_limit` removed from the decorator. A `threading.Timer` watchdog added inside the task body. If the task does not complete within `TASK_WATCHDOG_TIMEOUT_S` (default 600s), `os._exit(1)` is called to force the worker process to exit. This is recoverable: `start_celery.bat` or NSSM auto-restart will bring the worker back online within seconds, unblocking the queue.

---

### BUG-CHAL-DETECT-001 — No detection of Booking.com challenge URL parameters

**File:** `app/scraper.py` → `_fetch_with_selenium()`

**Problem:**  
When Booking.com/Cloudflare detects scraping activity, it redirects to URLs containing `chal_t=` (challenge timestamp token) and `force_referer=` parameters. The scraper received these challenge-annotated URLs in the retry loop but attempted to navigate to them with `driver.get()`. These URLs produce either an indefinite page load or a JavaScript challenge that Selenium cannot solve.

**Evidence:** The URL visible in the frozen browser window: `radisson-graz.es.html?lang=es&chal_t=1780362976169&force_referer=#hp_facilities_box`. The `chal_t` timestamp (1780362976169ms ≈ 2026-06-01 20:16:16 UTC) confirms this was a real-time bot detection event.

**Fix:** `_url_has_challenge_params()` function added. Called in `_fetch_with_selenium()` **before** `driver.get()`. If challenge parameters are detected, returns `None` immediately. The caller (`_scrape_language()`) treats this as a fetch failure → triggers VPN rotation → retry with clean session.

---

### CFG-VPN-INTERVAL-001 — `VPN_ROTATION_INTERVAL=50s` too aggressive

**File:** `app/config.py`

**Problem:**  
With `VPN_ROTATION_INTERVAL=50s` and `SCRAPER_MAX_WORKERS=2`, both concurrent threads trigger independent VPN rotations approximately every 50 seconds. This creates near-continuous VPN switching, which increases bot-detection probability and multiplies exposure to the subprocess hang bug (more rotations = more opportunities to trigger the hang).

**Fix:** `VPN_ROTATION_INTERVAL` default increased from `50` to `120` seconds.

---

## Changes by File

### `app/vpn_manager_windows.py`

| Change | Description |
|--------|-------------|
| `_subprocess_run_safe()` | New method. Executes nordvpn.exe commands in a daemon thread with guaranteed `join(timeout+5)` cutoff. Replaces all `subprocess.run(capture_output=True, timeout=N)` calls. |
| `_connect_via_cli()` | Uses `_subprocess_run_safe()`. Reads `VPN_SUBPROCESS_TIMEOUT_S` (default 45s) from config. Returns `False` immediately on timeout instead of hanging. `FileNotFoundError` handling preserved. |
| `disconnect()` | Uses `_subprocess_run_safe()`. Timeout is treated as successful disconnect (tunnel drops anyway). |
| `get_current_ip()` | Added global 30-second deadline across all 5 IP-lookup services. Prevents rare DNS hang from blocking for 40+ seconds. Per-service timeout reduced from 8s to 6s. |

### `app/tasks.py`

| Change | Description |
|--------|-------------|
| `time_limit=300` removed | Non-functional on Windows 11 solo pool (POSIX SIGKILL). Removed to avoid false confidence. |
| `soft_time_limit=240` removed | Non-functional on Windows 11 solo pool (POSIX SIGUSR1). Removed. |
| `threading.Timer` watchdog | Added inside `scrape_pending_urls()`. Fires `os._exit(1)` if task exceeds `TASK_WATCHDOG_TIMEOUT_S` (default 600s). `threading.Event` ensures watchdog is cancelled cleanly on normal completion. |
| `import threading` | Added to module imports. |

### `app/scraper.py`

| Change | Description |
|--------|-------------|
| `_BOOKING_CHALLENGE_URL_PARAMS` | New module-level constant: `("chal_t=", "force_referer=", "challenged_by=")` |
| `_url_has_challenge_params()` | New function. Returns `True` if URL contains any challenge parameter. |
| `_fetch_with_selenium()` | Calls `_url_has_challenge_params(url)` before `driver.get(url)`. Returns `None` immediately if challenge URL detected. |

### `app/scraper_service.py`

| Change | Description |
|--------|-------------|
| `_rotate_vpn_with_timeout()` | New method. Wraps `self._vpn.rotate()` in a daemon thread with `VPN_ROTATE_TIMEOUT_S` (default 90s) timeout. Returns `False` if rotate hangs, so the language loop is never blocked by a frozen VPN operation. |
| Time-based rotation | Replaced `self._vpn.rotate(force=False)` + `try/except` with `self._rotate_vpn_with_timeout(force=False)`. |
| Error-triggered rotation | Replaced `self._vpn.rotate(force=True)` + `try/except` with `self._rotate_vpn_with_timeout(force=True)`. |
| Log reference | `VPN_ROTATION_INTERVAL` default updated from 50 to 120 in log message. |

### `app/config.py`

| Parameter | Change | Notes |
|-----------|--------|-------|
| `BUILD_VERSION` | `113` → `114` | Synchronized with `__init__.py` |
| `VPN_ROTATION_INTERVAL` | default `50` → `120` | Reduce rotation frequency |
| `VPN_SUBPROCESS_TIMEOUT_S` | **New** — default `45` | Timeout for nordvpn.exe subprocess |
| `VPN_ROTATE_TIMEOUT_S` | **New** — default `90` | Timeout for complete rotation operation |
| `TASK_WATCHDOG_TIMEOUT_S` | **New** — default `600` | Windows watchdog timer for scrape task |

### `app/__init__.py`

`BUILD_VERSION = 113` → `BUILD_VERSION = 114`. Full Build 114 changelog entry added.

---

## Deployment Checklist

- [ ] Replace `app/vpn_manager_windows.py` with Build 114 version
- [ ] Replace `app/tasks.py` with Build 114 version
- [ ] Replace `app/scraper.py` with Build 114 version
- [ ] Replace `app/scraper_service.py` with Build 114 version
- [ ] Replace `app/config.py` with Build 114 version
- [ ] Replace `app/__init__.py` with Build 114 version
- [ ] **No `.env` changes required** (new config params have safe defaults)
- [ ] **No schema changes** (`schema_v77_complete.sql` unchanged)
- [ ] Restart Celery Worker (`stop_celery.bat` → `start_celery.bat`)
- [ ] Restart Celery Beat (`start_celery_beat.bat`)
- [ ] Verify startup log shows `build 114` in first INFO message
- [ ] Monitor first batch for `BUG-VPN-HANG-001-FIX` and `BUG-CHAL-DETECT-001` log entries

---

## Operational Notes

**If a future 6-hour hang occurs despite Build 114:**  
The watchdog (`TASK_WATCHDOG_TIMEOUT_S=600`) will fire `os._exit(1)` after 10 minutes, killing the worker. Restart it manually with `start_celery.bat`. The batch that was in progress will be reset by `reset_stale_processing_urls` (runs every 30 minutes) and retried automatically.

**`minihotel-graz` (UUID `af916ea0`):**  
This hotel is cancelled on Booking.com. Its URL consistently triggers 3× Cloudflare challenges on every attempt. Consider removing it from `urls_cargas.csv` or setting its status to `skipped` via the API.

**Gallery count mismatch warnings:**  
Logs show `classified=93 vs page badge=186` for some hotels. This is a known non-blocking condition from Build 109-110. The `badge` counts ALL internal photos; `classified` reflects only those captured from the gallery modal. Monitoring ongoing.

---

*Build 114 — Generated 2026-06-02*  
*Incident: INC-2026-0602-RADISSON-001*  
*Files modified: 6 (app/vpn_manager_windows.py, app/tasks.py, app/scraper.py, app/scraper_service.py, app/config.py, app/__init__.py)*
