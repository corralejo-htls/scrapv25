# TECHNICAL AUDIT & REMEDIATION REPORT — BookingScraper Pro (SCRAPV25)

**Repository:** `corralejo-htls/scrapv25` (read-only clone — HTTP 200, 211 files) — *no repository writes performed.*
**Build before this work:** **125** (`app/__init__.py:779`)
**Build delivered:** **126**
**Date:** 2026-06-16
**Scope:** Independent verification of the supplied forensic audit `audit_scrapv25_build125_EN.md`, against the live code line-by-line, plus remediation of every confirmed finding.
**Method:** Clone → static analysis with exact line references → schema reconciliation (`schema_v77_complete.sql` is the single source of truth) → patch → `ast.parse()` on every Python file → targeted unit tests executed (4/4 pass) → version-sync check executed.

> **Platform reality (Windows 11, single-node):** Celery runs `pool=solo`; POSIX `time_limit`/`soft_time_limit` are no-ops, so a `threading.Timer` + `os._exit(1)` watchdog is the only real timeout. The database is destroyed and recreated from `schema_v77_complete.sql` on every startup — therefore **all fixes are application-logic only**; no schema structure was changed (the header comment was the sole SQL edit).

---

## 1. Verification verdict — the prior audit was correct

Every one of the five findings in `audit_scrapv25_build125_EN.md` was reproduced against the actual code. Summary:

| ID | Severity | Verified? | Evidence (file:line) |
|----|----------|-----------|----------------------|
| FINDING-A | CRITICAL | ✅ Confirmed | `tasks.py:513` `os._exit(1)`; `scraper_service.py:1767/1813` (only increment sites); `dispatch_batch` claim UPDATE had no increment; pending SELECT had no `max_retries` guard; `tasks.py:374` stale-reset preserved `retry_count`, no cap |
| FINDING-B | HIGH | ✅ Confirmed | `scraper_service.py` gallery block: on `gallery_visible==0 && badge>0` it only logged a WARNING; EN was still written `done` at end of `_scrape_language` |
| FINDING-C | MEDIUM | ✅ Confirmed | `config.py` `SCRAPER_MAX_WORKERS default=2`; `ThreadPoolExecutor(max_workers=2)`; VPN manager + language loop are shared, unsynchronized state |
| FINDING-D | MEDIUM | ✅ Confirmed | `scraper.py:448` static UA `Chrome/149.0.0.0` |
| FINDING-E | LOW | ✅ Confirmed | schema header read `build 120` while code at 125 |

I did **not** take the audit's suggested patch sketch at face value: its FINDING-A sketch *adds* a claim-time increment while *keeping* the finalize-time increment, which double-counts and silently halves the retry budget. The delivered fix removes the finalize-time increments instead (see §2.1).

---

## 2. Remediation delivered (Build 126)

### 2.1 FINDING-A [CRITICAL] — Poison-pill loop / watchdog defeats `max_retries`

**Mechanism.** `_watchdog_action()` ends in `os._exit(1)` (`tasks.py`), which bypasses `finally`/`atexit`/`__del__`. For a URL whose processing exceeds `TASK_WATCHDOG_TIMEOUT_S`, neither `_finalize_url()` nor `_mark_url_error()` runs — and those were the **only** two places `retry_count` was incremented. The URL stayed `processing` with `retry_count=0`; `reset_stale_processing_urls()` returned it to `pending` (preserving `retry_count`, no cap); `dispatch_batch()` orders by `created_at ASC` so the old URL was re-selected first → worker dies on a ~90-minute cycle; the queue never drains. This — not `SCRAPER_BATCH_SIZE` — is the true cause of the "31/141 completed" symptom.

**Design chosen — single increment at claim time.** `retry_count` now means *"attempts started"* and is incremented exactly once, at the moment the URL is flipped to `processing`. This survives `os._exit`. The finalize methods no longer increment; they only decide the next status from the already-incremented counter. With `max_retries=3` this yields exactly 3 attempts then permanent `error`, identically across fast-fail, fatal-error and watchdog-kill paths.

**Edits (`app/scraper_service.py`):**
- `dispatch_batch()` pending SELECT now filters `retry_count < max_retries` (defense-in-depth — an exhausted URL can never be re-selected).
- `dispatch_batch()` claim UPDATE now sets `retry_count = URLQueue.retry_count + 1` alongside `status='processing'`.
- `_finalize_url()` no longer increments; on failure it marks `pending` if `retry_count < max_retries`, else permanent `error`.
- `_mark_url_error()` same treatment.

**Edit (`app/tasks.py`):**
- `reset_stale_processing_urls()` now caps: if `retry_count >= max_retries` it sets `status='error'` (permanent, no requeue) instead of `pending`; docstring corrected.

**Schema alignment.** `url_queue.retry_count SMALLINT NOT NULL DEFAULT 0` and `max_retries SMALLINT NOT NULL DEFAULT 3` already exist; the `status` CHECK already allows `'error'`. No SQL structure change required.

**Test.** `tests/test_strategy_e.py::TestFindingARetryCap` (4 cases) — asserts no double-increment and permanent-error at the cap. **All 4 pass.**

### 2.2 FINDING-B [HIGH] — Gallery-modal capture failure not flagged

**Mechanism.** When the EN gallery modal captured `0` gallery-visible photos but the page badge advertised `>0`, the code logged a warning and still wrote the EN language row as `done`, so the hotel reached export and the API `images[]` fell back to the unfiltered downloaded superset (count/identity mismatch for ~1 in 5 completed hotels).

**Fix (`app/scraper_service.py`).** A `_gallery_capture_failed` flag is set in that exact branch; at the end of `_scrape_language` the EN row is written `incomplete` (not `done`) with a descriptive `last_error`, and a `scrape_partial` event is logged. Text data is still fully persisted (no loss).

**Why this is sufficient.** `completeness_service.is_fully_complete()` requires *all* languages `== "done"`, so the hotel is automatically excluded from export until repaired. `get_incomplete_urls()` and `scripts/retry_incomplete.py --fix-legacy` (which evaluates each `done` URL against its own `url_language_status`) will detect and re-queue it. The `'incomplete'` value is already permitted by both the `url_queue` and `url_language_status` status CHECK constraints.

**Operator action.** Run `python scripts/retry_incomplete.py --fix-legacy` (or `--dry-run` first) to re-queue affected hotels. Monitoring query:
```sql
SELECT url_id FROM url_language_status
WHERE language='en' AND status='incomplete';
```

### 2.3 FINDING-C [MEDIUM] — Real 2-thread concurrency over a shared VPN manager

**Mechanism.** `SeleniumEngine._lock` serializes the browser, but `NordVPNManager.rotate()`, `reset_browser()` and the per-language loop are shared mutable state touched by both threads (observed: duplicate "Browser reset complete" pairs; one thread resetting the browser mid-scrape of the other; and a watchdog kill from the poison-pill thread discarding the concurrent legitimate URL). With the browser already serialized, the second worker delivers **zero** throughput benefit.

**Fix (`app/config.py`).** `SCRAPER_MAX_WORKERS` default lowered `2 → 1`. Zero throughput loss, eliminates the race. (Alternative for a future multi-process design: give each worker its own `SeleniumEngine` in a separate Celery process, or guard `rotate()`/`reset_browser()` with a dedicated lock.)

### 2.4 FINDING-D [MEDIUM] — User-Agent hardcoded (latent bot-evasion regression)

**Mechanism.** `scraper.py` injects a static `Chrome/149.0.0.0`. Build 123 only bumped the literal (131→149). When `webdriver-manager` auto-updates Brave/ChromeDriver to 150+, the UA-vs-CDP version mismatch (a strong Cloudflare signal) returns — exactly `BUG-USER-AGENT-STALE-001`.

**Fix (`app/scraper.py`).** In `_get_driver()`, after the driver is created, the real major version is read from `driver.capabilities["browserVersion"]` and injected via `execute_cdp_cmd("Network.setUserAgentOverride", …)`. The static literal in `_build_chrome_options()` remains only as a fallback (annotated). The UA now self-synchronizes on every browser auto-update; no maintenance needed.

### 2.5 FINDING-E [LOW] — Schema header drift

**Fix (`schema_v77_complete.sql`).** Header comment updated `build 120 → build 126`, with an explicit note that the Build 126 fixes are application-logic only and require no structural change. **Comment-only edit** — the recreate-from-scratch path is untouched.

---

## 3. Files delivered (original names & paths preserved)

| File | Change |
|------|--------|
| `app/scraper_service.py` | FINDING-A (claim-time `retry_count`, SELECT guard, finalize/error decision) + FINDING-B (gallery → `incomplete`) |
| `app/tasks.py` | FINDING-A (permanent-error cap in stale-reset) |
| `app/scraper.py` | FINDING-D (dynamic UA via CDP) |
| `app/config.py` | FINDING-C (`SCRAPER_MAX_WORKERS` 2→1) + Build 126 header/changelog + canonical fallback 125→126 |
| `app/__init__.py` | `BUILD_VERSION = 126` + changelog |
| `schema_v77_complete.sql` | FINDING-E header comment 120→126 (no structural change) |
| `tests/test_strategy_e.py` | `TestFindingARetryCap` (4 new regression tests, all passing) |

---

## 4. Validation performed

- `ast.parse()` — all 6 modified Python files: **OK**.
- Version sync — `app.BUILD_VERSION == Settings().BUILD_VERSION == 126`: **OK**. `SCRAPER_MAX_WORKERS == 1`: **OK**.
- Unit tests — `tests/test_strategy_e.py::TestFindingARetryCap`: **4 passed**.
- Schema header now reads `build 126`.

**Pre-existing issue noted (out of scope, not fixed):** the legacy `service` fixture in `tests/test_strategy_e.py` still patches `app.scraper_service.CloudScraperEngine`, a symbol removed in Build 63; tests using that fixture error at collection. The new tests are deliberately self-contained (via `__new__`) to avoid it. Recommend repairing the fixture in a follow-up.

---

## 5. Post-deployment checklist

1. Deploy the 7 files; restart all services (DB is recreated from `schema_v77_complete.sql`).
2. Confirm in logs: `Selenium: command timeout set…`, `FINDING-D-FIX: User-Agent dinámico…`, and that no single `url_id` recurs hundreds of times.
3. Confirm the watchdog no longer fires on a fixed ~90-min cycle.
4. Run `python scripts/retry_incomplete.py --fix-legacy --dry-run`, then without `--dry-run`, to reprocess gallery-incomplete hotels.
5. Watch for any URL reaching permanent `error` after 3 attempts (expected for genuine poison-pills) — investigate those URLs individually rather than letting them loop.

*All findings traced log/audit → code line → mechanism → fix → test. Schema treated as the single source of truth. No repository writes performed.*
