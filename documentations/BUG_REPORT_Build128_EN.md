# SCRAPV25 — Forensic Code Audit (Full Source Verified) BUG_REPORT_Build128_EN

**Repository:** `github.com/corralejo-htls/scrapv25` **read-only**
**Audit date:** 2026-06-18
**Schema (single source of truth):** `schema_v77_complete.sql` — header *"Schema Completo v6.0.0 build 126"*
**Connection check:** confirmed. The exact commit you supplied — `51845ee319a639ebbf81babae970c9e5104d87e3` — resolves and serves `schema_v77_complete.sql`. The blob page carries `meta-robots: noindex, nofollow`, which is why code search could not surface this repository in the previous session.
**Method:** Every finding below was read directly from the uploaded source (the authoritative copies). No claim is taken from the earlier `SCRAPV25_Forensic_Code_Audit_EN.md`; that report is re-tested line-by-line against the real code.

---

## 0. Headline — the codebase has moved to Build 126/127 and has genuinely fixed four of the five prior functional findings

This overturns the previous (access-limited) session, where only a Build-60 schema was reachable on `main`. With the real `app/` package now in hand, the build coordinates are tight and the remediations are real:

| Module | Declared build |
|---|---|
| `app/tasks.py` | 127 |
| `app/config.py` | 127 |
| `app/scraper.py` | 125 |
| `app/scraper_service.py` | 126 (FINDING fixes) |
| `schema_v77_complete.sql` | header build 126 |

Status of the prior audit's findings, each **verified against the live source**:

| Finding | Prior claim | Verified status now | Evidence |
|---|---|---|---|
| **A** Poison-pill infinite loop | CRITICAL, unfixed | **FIXED** | `dispatch_batch()` increments `retry_count` at claim time; `reset_stale_processing_urls()` caps at `max_retries` → permanent `error`; pending `SELECT` filters `retry_count < max_retries`; watchdog kills Brave/ChromeDriver before `os._exit`; `LOCK_TTL` derived from `TASK_WATCHDOG_TIMEOUT_S`. |
| **B** `retry_count` never incremented | HIGH, unfixed | **FIXED** | Claim-time increment in `dispatch_batch()`; `_finalize_url`/`_mark_url_error` deliberately do **not** re-increment (no double-count). |
| **C** batch size conflated with worker count | HIGH, unfixed | **FIXED** | `config.py` now defines `SCRAPER_BATCH_SIZE`; `dispatch_batch()` uses `.limit(SCRAPER_BATCH_SIZE)`; `SCRAPER_MAX_WORKERS` default lowered 2→1. |
| **D** gallery `done`/`incomplete` mismatch | HIGH, unfixed | **STILL LIVE — fixed in this audit** | `_scrape_language()` returns `True` on the gallery-incomplete path, so `url_queue.status` becomes `done` while `url_language_status.en='incomplete'`. See §1. |
| **E** static User-Agent | MEDIUM | **FIXED** | `scraper.py` injects a dynamic UA via `Network.setUserAgentOverride` from the real `browserVersion`; the static `Chrome/149` is only a fallback. |
| **F** four-way version desync | LOW/process | **Largely reconciled** | Code at 125–127, schema header 126. Residual: schema **file** is `schema_v77` while its **header** says *build 126* (two different numbering schemes), and `scraper.py` (125) lags `tasks.py`/`config.py` (127). |

**Net:** one real, high-impact defect remains (FINDING-D). It is fixed in the delivered `scraper_service.py`. No schema change is required — the schema already permits the states the fix uses.

---

## 1. FINDING-D — [HIGH] Gallery-incomplete hotels are silently excluded from export and cannot self-heal

### 1.1 Mechanism (read from source)

1. In `_scrape_language()` (EN pass only), when the gallery modal captures **zero** `gallery_visible` photos while the page badge advertises a gallery, the code correctly writes the **language** row `url_language_status.en = 'incomplete'` … and then executes **`return True`**.
2. In `_process_url()`, the loop did `ok: bool = self._scrape_language(...)`. A `True` result appends `en` to `completed`, so `success_count == total`, and `final_status = "done"`.
3. `_finalize_url()` therefore writes **`url_queue.status = 'done'`** and **`languages_completed` including `en`**.

The two state stores now disagree: `url_queue.status='done'` vs `url_language_status.en='incomplete'`. No reconciliation guard exists.

### 1.2 Impact (verified against the export path)

`ExportSelection.from_all_done_urls()` (api_export_system.py, BUG-EXPORT-003-FIX Build 96) selects `URLQueue.status=='done'` **and** requires *every* required language to be `done` in `url_language_status`. For a gallery-incomplete hotel, `en` is `incomplete`, so `missing=['en']` and the hotel is **silently excluded from the export** — even though all six languages of text are fully persisted and only the EN image gallery is short.

Worse, recovery is blocked: because `languages_completed` lists `en`, the resume logic in `_process_url()` (`if lang in already_done: continue`) will **skip the EN pass** on any later attempt, so the gallery is never recaptured. And since `url_queue.status='done'` is terminal for the auto-loop (`dispatch_batch` selects only `pending`; `reset_stale_processing_urls` touches only `processing`), nothing returns the URL for reprocessing through the normal path. The hotel is stuck: present in the DB, absent from the API, unrepairable by the scraper loop.

### 1.3 Fix delivered (`scraper_service.py`, marked `# FINDING-D-FIX-2`)

- `_scrape_language()` now returns a **tri-state string** `"done" | "incomplete" | "error"` (its only caller is `_process_url`, so the contract change is safe).
- `_process_url()` tracks an `incomplete[]` list separately. Gallery-incomplete languages are **not** added to `completed` and are **not** checkpointed, so they stay out of `languages_completed` and the resume path re-scrapes them. Reconciled final status: `error` if any hard failure; else `incomplete` if any gallery-incomplete; else `done`.
- `_finalize_url()` accepts `incomplete[]`, writes `url_queue.status='incomplete'` (consistent with the language row), does **not** consume a retry (a gallery shortfall is not a failure), and records a descriptive `last_error`.
- Result: `url_queue` can never report `done` while any tracked language is `incomplete`, and the EN gallery becomes recapturable.

**Schema legality (verified):** `schema_v77_complete.sql` defines `chk_url_queue_status` and `chk_uls_status_valid` both as `status IN ('pending','processing','done','error','skipped','incomplete')`, and `models.py` mirrors this. Writing `url_queue.status='incomplete'` is valid; **no schema change is needed.**

### 1.4 Operational requirement
`url_queue.status='incomplete'` is terminal for the auto-loop by design. `scripts/retry_incomplete.py` must reset such rows to `pending` to trigger recapture (it can find them via `CompletenessService.get_incomplete_urls()`, which already returns `incomplete` language rows). Note that claim-time `retry_count` increments apply to recapture attempts too; if operators want unbounded gallery retries, `retry_incomplete.py` should also reset `retry_count`.

---

## 2. Verified-fixed findings (evidence)

### FINDING-A / B — retry accounting & poison-pill (FIXED)
- `dispatch_batch()` bulk-updates claimed URLs `status='processing', retry_count = retry_count + 1` (claim-time counter survives the `os._exit` watchdog kill).
- Pending `SELECT` filters `URLQueue.retry_count < URLQueue.max_retries` (defense-in-depth; exhausted URLs are never re-selected).
- `reset_stale_processing_urls()` enforces the cap: `retry_count >= max_retries` → `status='error'` (no requeue); otherwise `pending`, preserving `retry_count` (incremented at claim, so no double-count).
- `_finalize_url`/`_mark_url_error` decide status from the already-incremented counter and do **not** re-increment.
- Walk-through (max_retries=3): each claim consumes one attempt; on the 3rd, a slow/watchdog kill is converted to permanent `error` by the stale-reset, and the SELECT guard (`3 < 3` false) stops re-selection. The immortal loop is closed.

### FINDING-C — batch/worker decoupling (FIXED)
- `config.py` `SCRAPER_BATCH_SIZE` field present (default = `SCRAPER_MAX_WORKERS` for back-compat); `dispatch_batch()` sizes the query by it. `SCRAPER_MAX_WORKERS` default lowered 2→1, removing the shared-browser race the prior audit flagged (Selenium ops are serialized by `SeleniumEngine._lock`).

### FINDING-E — dynamic User-Agent (FIXED)
- `scraper.py` derives the major version from `driver.capabilities["browserVersion"]` after driver creation and injects the UA via `Network.setUserAgentOverride`; the static `Chrome/149.0.0.0` literal is only a fallback. This removes the UA-vs-CDP mismatch.

### Other corroborated, sound mechanisms
- **Watchdog (tasks.py):** `time_limit`/`soft_time_limit` removed (no-ops on Windows `pool=solo`); `threading.Timer` watchdog kills Brave/ChromeDriver via `psutil` before `os._exit(1)` (Build 116) and is cancelled on every return path via an outer `try/finally` (Build 122).
- **LOCK_TTL:** `max(TASK_WATCHDOG_TIMEOUT_S + 60, 660)` — no longer the hardcoded 280 the prior audit cited.
- **database.py:** lazy engine; `get_readonly_db()` uses `SET TRANSACTION READ ONLY` (correct for SQLAlchemy 2.0 autobegin); `get_olap_db()` int-casts the timeout (no f-string injection); `execute_with_retry` logs full exception context.
- **completeness_service.py:** state machine `_VALID_TRANSITIONS` matches the schema CHECK; `update_language_status()` uses `SELECT FOR UPDATE`; `is_fully_complete()` correctly `.split(",")` the language string.
- **celery_app.py:** `worker_pool=solo`, `concurrency=1`, `prefetch_multiplier=1` on Windows; Beat drives `scrape_pending_urls` every 30 s with the Redis lock guarding overlap.

---

## 3. Schema analysis — `schema_v77_complete.sql` (verified)

- **21 base tables** (the prior audit's count is correct for this schema): the 17 of build-60 plus `hotels_extra_info` (STRUCT-021), `hotels_nearby_places` (STRUCT-022), `hotels_room_types` (STRUCT-023, GIN indexes on `facilities`/`images`), `hotels_seo` (STRUCT-024), and `hotels_individual_reviews` (BUG-SCHEMA-001-FIX, v77).
- **View `v_api_export_images`** present (Build 109; `DISTINCT ON` dedup, BUG-VIEW-DEDUP-001 Build 112) — alongside `v_hotels_full` and `v_scraping_summary`.
- `scraping_logs` partitioned by month with a `default` partition and trigger-based FK emulation; `url_queue`/`url_language_status` status CHECKs include `incomplete`.
- **Verdict:** structurally sound and consistent with the ORM in `models.py`. No structural defect found; no change required for the FINDING-D fix.

---

## 4. Audit coverage (full transparency)

**Deep-read line-by-line:** `tasks.py`; `scraper_service.py` (dispatch/claim/process/scrape_language/finalize/error + method index); `config.py` (build + scraper/VPN/watchdog fields); `scraper.py` (UA/build via index); `completeness_service.py`; `database.py`; `celery_app.py`; `language_config.py`; `models.py` (queue/status/retry fields); `api_export_system.py` (export selection); `schema_v77_complete.sql` (tables, constraints, views).

**Scanned, not line-audited (no change made; not implicated in the findings):** `extractor.py` (4,453 lines), `main.py` (2,402), `api_payload_builder.py`, `image_classifier.py`, `image_downloader.py`, `vpn_manager_windows.py`, `export_ui.py`, `__init__.py`, `alembic_env.py`, `vpn_manager.py`. These warrant a follow-up pass; nothing in the verified pipeline pointed to a defect in them.

---

## 5. Deliverables

1. **`SCRAPV25_Code_Audit_Report_EN.md`** — this document.
2. **`SCRAPV25_Code_Audit_Report_ES.md`** — Spanish translation.
3. **`scraper_service.py`** — corrected module (same filename), FINDING-D-FIX-2, syntax-validated with `py_compile`. This is the only source file requiring a change; A/B/C/E are already fixed and the schema is sound.

---

## 6. Prioritised actions

1. **Adopt the corrected `scraper_service.py`** to close FINDING-D (the only live functional defect).
2. **Confirm `scripts/retry_incomplete.py`** resets `url_queue.status='incomplete'` → `pending` (and consider resetting `retry_count`) so gallery-incomplete hotels recover.
3. **Tidy the residual version drift (FINDING-F):** align `scraper.py` (125) to 127 and reconcile the schema **file name** (`v77`) with its **header** (build 126) — pick one convention and add a CI check that fails when the code `BUILD_VERSION`, schema header, and README diverge.
4. **Follow-up pass** over `extractor.py` and `main.py` (largest unread modules) for completeness.

---

*Every functional finding was traced from the uploaded source → mechanism → impact → fix. The schema (`schema_v77_complete.sql`) was treated as the single source of truth and confirmed to permit the states used by the fix. Connection to the supplied commit was verified before analysis.*
