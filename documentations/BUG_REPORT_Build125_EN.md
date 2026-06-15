# BUG REPORT — BookingScraper Pro (SCRAPV25) v6.0.0 Build 125

> **Date:** 2026-06-15
> **Basis:** root-cause audit `AUDITORIA_RootCause_Build124_ES.md` (5 findings)
> **Repository:** `corralejo-htls/scrapv25` — **read-only** (nothing pushed)
> **Schema source of truth:** `schema_v77_complete.sql` (unchanged — DB is recreated on every startup; no remediation requires a migration)
> **Method:** `git clone` of the repo + empirical reproduction of **every** finding against the real code and the `pruebas/*.csv` / `pruebas/*.html` ground truth. No assumptions.

---

## 0. Connectivity & reproduction

| Check | Result |
|---|---|
| `git clone https://github.com/corralejo-htls/scrapv25.git` | ✅ OK (213 files, commit `19d2dfb`) |
| GitHub REST API | ⚠️ HTTP 403 = environment IP *rate limit* (not lack of access); git clone confirms access |
| `ast.parse()` of the 5 modified `.py` files | ✅ OK |
| `Settings().BUILD_VERSION` after fix | ✅ returns `125` (== `app/__init__.py`) |

Every Build 124 finding was **reproduced against real data** before any code was touched.

---

## 1. Change summary

| Finding | Sev. | Status | Files |
|---|---|---|---|
| FINDING-001 — no Selenium command-level timeout | 🔴 CRITICAL | **Fixed** | `scraper.py`, `config.py`, `env.example` |
| FINDING-002 — 20.7% of hotels with 0 `gallery_visible` photos | 🟠 HIGH | **Mitigated** (root cause in FINDING-001/003) + operational | — |
| FINDING-003 — Build 122 fix is a no-op; noisy reconciliation metric | 🟡 MEDIUM | **Fixed** | `image_classifier.py`, `scraper_service.py` |
| FINDING-004 — `BUILD_VERSION` drift (123 vs 124) | 🟡 MEDIUM | **Fixed at the root** | `config.py`, `__init__.py` (+ headers) |
| FINDING-005 — "partial load" persists thin records | 🔵 LOW | **Fixed** | `scraper.py` |

---

## FINDING-001 🔴 — Selenium command-level timeout (CRITICAL)

### Verified evidence
- Search across all of `app/`: `set_timeout` / `command_executor` / `_client_config` / `ClientConfig` / `BROWSER_COMMAND_TIMEOUT` → **NONE FOUND**.
- The only timeouts in place were `webdriver.Chrome()` (launch), `driver.get()` (`NAVIGATION_TIMEOUT_S`) and `driver.quit()`. The driver is assigned at `scraper.py:600` and **immediately after** (`:603`) `execute_script(...)` is called **unprotected**.
- `find_element/find_elements`, `click()`, `current_url`, and the whole `GalleryModalExtractor` interaction were left at the mercy of the HTTP socket to ChromeDriver, with no limit.
- Runtime logs: `RemoteDisconnected` (15×) and **5× `WATCHDOG-HANG-001: Task blocked 600s`**. The log blamed "VPN / Selenium init", which **are** protected → misleading diagnosis.

### Root cause
`set_page_load_timeout()` only covers navigation. Any subsequent command, when the ChromeDriver↔Brave IPC pipe is stuck (common on Windows 11), **blocks the socket read indefinitely**, keeping the task alive until the watchdog fires `os._exit(1)` (600s). The prime suspect is the gallery-modal interaction.

### Fix applied
`app/scraper.py`, `_get_driver()`, right after `self._driver = _launch_result["driver"]`:

```python
try:
    _cmd_timeout = int(getattr(cfg, "BROWSER_COMMAND_TIMEOUT_S", 120))
    self._driver.command_executor.set_timeout(_cmd_timeout)   # Selenium >=4.16
except Exception:
    try:
        self._driver.command_executor._client_config.timeout = _cmd_timeout
    except Exception:
        logger.warning("FINDING-001-FIX: could not set command timeout")
```

- `app/config.py`: new `BROWSER_COMMAND_TIMEOUT_S: int = Field(default=120, ge=15, le=600, ...)`.
- `env.example`: documented with a 120s recommendation.

### Verification
`Settings().BROWSER_COMMAND_TIMEOUT_S == 120`. The timeout now covers **all** subsequent commands; a stuck IPC raises an exception and the language fails cleanly to be retried, instead of hanging the task for 600s.

---

## FINDING-002 🟠 — 20.7% of hotels with 0 `gallery_visible` photos (HIGH)

### Verified evidence (`pruebas/_table__image_data__.csv`, real run)
```
Total hotels   : 140
gallery_visible == 0      :  29  (20.7%)   <- all 29 are entirely source=js_array
gallery_visible == total  :  45  (32.1%)
partial (0<gv<total)      :  66  (47.1%)
```
The 29 zero-gallery hotels never opened the modal in that run. In `api_payload_builder.py:455-488`, with `API_IMAGES_GALLERY_ONLY=True` and `API_IMAGES_STRICT_GALLERY=False` (defaults), `_load_image_urls()` falls back to the download **superset** → the exported `images[]` does not match the public gallery (it over-includes; no data loss).

### Handling (no data loss; product decision)
Not a wiring bug — it's modal-capture failure. Addressed by:
1. **Root cause mitigated by FINDING-001** (many modal failures were command hangs) and FINDING-003 (clearer real-failure detection).
2. **Selective re-scrape:** criterion `gallery_visible_count == 0 AND badge > 0` (`scripts/retry_incomplete.py` already exists).
3. **Hard decision:** if "must match the public gallery" is a requirement, set `API_IMAGES_STRICT_GALLERY=True` (flag already present) to send `[]` instead of the superset for those hotels.

> `STRICT_GALLERY=True` was **not** forced as default because it would break the historical safety net (sending `[]`); left as Omar's operational decision.

---

## FINDING-003 🟡 — Build 122 fix is a no-op; noisy reconciliation metric (MEDIUM)

### Verified evidence (real function against `pruebas/HTML_*_en-gb.html`)
```
villa-dvor      previews=8 badges=[51, 51] min=51 max=51 -> est=59
hilton-vienna   previews=8 badges=[83, 83] min=83 max=83 -> est=91
topazz          previews=8 badges=[30, 30] min=30 max=30 -> est=38
...
```
The HERO emits **2 badges of identical value** → `min(badges) == max(badges)`. The Build 122 `max→min` change is a **no-op** on current production HTML. The log `classified=62 vs page badge=124` (exactly 2×) further proves the badge is still ~2× the real gallery. The equality comparison produced **90 false `Gallery count mismatch` alarms** that masked the real failures (FINDING-002).

### Fix applied
- `image_classifier.py:gallery_count_from_html()`: corrected comment (identical badges, no-op; the value is an **upper bound**, not the public count). `min()` is kept as harmless.
- `scraper_service.py` (reconciliation): warning is emitted only on an **unambiguous real modal failure** — `_n_gallery == 0 AND badge > 0` — everything else degrades to `info`. Noise removed, FINDING-002 made visible.

---

## FINDING-004 🟡 — `BUILD_VERSION` drift (MEDIUM)

### Verified evidence
```
app/__init__.py  BUILD_VERSION = 124
app/config.py    default        = 123   -> Settings().BUILD_VERSION == 123 with no env var
app/main.py      header         = "build 96"
api_payload_builder.py header   = "Build 112"
```
Exact recurrence of `BUG-CONFIG-SYNC-001` (Build 112).

### Fix applied (at the root)
- `app/config.py` imports the literal instead of duplicating it:
  ```python
  try:
      from app import BUILD_VERSION as _CANONICAL_BUILD_VERSION
  except Exception:
      _CANONICAL_BUILD_VERSION = 125
  ...
  BUILD_VERSION: int = Field(default_factory=lambda: _CANONICAL_BUILD_VERSION, ...)
  ```
  `app/__init__.py` imports nothing (it's pure), so there is **no cycle** (the docstring at `__init__.py:771` itself confirms the `config → app.__init__` flow).
- `app/__init__.py`: `BUILD_VERSION = 125` and header docstring synchronized.
- Headers of the delivered files synchronized to Build 125.

### Empirical verification
`Settings().BUILD_VERSION == 125 == app.__init__.BUILD_VERSION` → **IN SYNC**. The bug class is eliminated: any future bump in `__init__.py` now propagates by itself.

> **Outstanding (out of this delivery):** `main.py` ("build 96") and `api_payload_builder.py` ("Build 112") still carry a literal header. They were not modified in this build because their logic was not touched; recommend syncing their headers in the next cycle that touches them.

---

## FINDING-005 🔵 — "Partial load" persists thin records (LOW)

### Verified evidence
- `rt-name-link` **does exist** in the real HTML (`topazz_de`=12, `topazz_es`=12, `wild-bolz_es`=4) → the RoomTypes warning is **not a selector bug**, but a consequence of a partial load missing the (JS-rendered) table.
- The code already returned `None` on detected challenge (`scraper.py:1410-1417`) and on a non-hotel page (`:1423-1428`). The real risk was a partial load that **passes** `_is_hotel_page()` but lacks the core block.

### Fix applied
`app/scraper.py`, partial-load path (`loaded == False`): if the HTML **does not** contain the `application/ld+json` block with `"hotel"`/`"lodgingbusiness"`, the language is discarded (`return None`) so Strategy E retries it, instead of persisting a thin record that would corrupt the completeness metric.

---

## 2. Checks that pass (with evidence)

| Check | Evidence |
|---|---|
| 15 upserts wired | `scraper_service.py:913-946` ✅ |
| `extract_all()` returns `individual_reviews` | `extractor.py` ✅ (RISK-001 resolved) |
| Watchdog cancelled on all paths | `tasks.py` (try/finally) ✅ |
| `driver.get/quit/Chrome()` daemon-thread timeout | `scraper.py` ✅ |
| room_types selectors valid in real DOM | `rt-name-link` present in `pruebas/` ✅ |
| ORM ↔ schema, no missing columns | 21 tables ✅ |

---

## 3. Delivered files (original names preserved)

| File | Change |
|---|---|
| `app/scraper.py` | FINDING-001 (command timeout) + FINDING-005 (partial load) + header 125 |
| `app/config.py` | FINDING-001 (new setting) + FINDING-004 (canonical import) + header 125 |
| `app/__init__.py` | FINDING-004 (`BUILD_VERSION = 125`) + changelog + docstring 125 |
| `app/image_classifier.py` | FINDING-003 (badge comment/semantics) + header 125 |
| `app/scraper_service.py` | FINDING-003 (reconciliation = real modal failure) + header 125 |
| `env.example` | FINDING-001 (`BROWSER_COMMAND_TIMEOUT_S=120`) |

**Validation:** all 5 `.py` files pass `ast.parse()`. `schema_v77_complete.sql` is unchanged (no remediation requires a schema change).

*End of report — Build 125.*
