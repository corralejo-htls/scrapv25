# Bug Report — BookingScraper Pro v6.0.0 Build 86
**Date:** 2026-04-09  
**Scope:** Full audit of `app/*.py` + `schema_v77_complete.sql`  
**Auditor:** Automated code review (static analysis + cross-reference)

---

## Summary

| ID | Severity | File | Impact |
|----|----------|------|--------|
| BUG-DISPATCH-001 | 🔴 Critical | `app/main.py` | `/scraping/force-now` always raises TypeError |
| BUG-LOAD-URLS-001 | 🔴 Critical | `app/main.py` | `POST /urls/load` raises NameError on any valid URL |
| BUG-VPN-INIT-001 | 🟠 High | `app/scraper_service.py` | NordVPN initialized in interactive mode in all workers |
| BUG-ENABLED-LANGS-001 | 🟠 High | `app/completeness_service.py` | `is_fully_complete()` always returns False |
| BUG-DOUBLE-COMMIT-002 | 🟡 Medium | `app/scraper_service.py` | Redundant DB round-trips in every scraping cycle |
| BUG-VIEW-004 | 🟡 Medium | `schema_v77_complete.sql` | `v_hotels_full` missing fields: `category_code`, `adults`, `children`, `images`, `info` |
| BUG-DEAD-CODE-001 | 🔵 Low | `app/extractor.py` | 170-line duplicate unreachable implementation |

---

## BUG-DISPATCH-001 — Critical: `/scraping/force-now` always fails

**File:** `app/main.py` line 834  
**Root cause:** `ScraperService.dispatch_batch()` is defined with signature `def dispatch_batch(self) -> dict` (no parameters). The endpoint calls it with `service.dispatch_batch(url_ids=payload.url_ids, max_workers=workers)`, which raises `TypeError: dispatch_batch() got an unexpected keyword argument 'url_ids'`.

**Evidence:**
```python
# main.py line 834 — WRONG:
result = service.dispatch_batch(url_ids=payload.url_ids, max_workers=workers)

# scraper_service.py line 235 — actual signature:
def dispatch_batch(self) -> dict:
```

**Impact:** Every call to `POST /scraping/force-now` fails with HTTP 500. Manual scraping trigger is completely non-functional.

**Fix:** Remove kwargs from the call site. `max_workers` is already read from config inside `dispatch_batch()` via `getattr(cfg, "SCRAPER_MAX_WORKERS", 2)`.

```python
result = service.dispatch_batch()
```

---

## BUG-LOAD-URLS-001 — Critical: `POST /urls/load` NameError

**File:** `app/main.py` line 440  
**Root cause:** A dead loop at the start of `load_urls()` references `_valid` (undefined). The variable was renamed to `valid` in a previous refactor but the loop was not updated. When any URL passes validation, Python evaluates `_valid if True else invalid`, raising `NameError: name '_valid' is not defined`.

**Evidence:**
```python
# main.py lines 437-440 — WRONG:
valid, invalid = [], []
for url in payload.urls:
    (_valid if _validate_booking_url(url) else invalid).append(url)  # type: ignore
```

**Note:** The variables `valid` and `invalid` are recomputed from `normalized_urls` immediately after this loop. The loop was entirely redundant AND broken. Removed without loss of functionality.

**Impact:** `POST /urls/load` raises HTTP 500 (`NameError`) whenever at least one Booking.com URL is valid — which is the expected case. Programmatic URL loading via JSON payload is non-functional.

---

## BUG-VPN-INIT-001 — High: NordVPN initialized in interactive mode

**File:** `app/scraper_service.py` lines 200–201  
**Root cause:** `NordVPNManager.__init__` signature is `def __init__(self, interactive: bool = False)`. The factory function passes the entire `cfg` Settings object as the first positional argument: `NordVPNManager(cfg)`. Since `cfg` is a Pydantic Settings instance (truthy), `interactive=True` in all production Celery workers.

**Evidence:**
```python
# scraper_service.py line 201 — WRONG:
return NordVPNManager(cfg)

# vpn_manager_windows.py line 218:
def __init__(self, interactive: bool = False) -> None:
```

**Impact:** `interactive=True` enables prompt-based input in workers (console dialogs, `input()` calls). In headless Celery workers this causes hangs or unexpected behavior. The parameter name `cfg` masked the bug during code review.

**Fix:** `return NordVPNManager()` (use default `interactive=False`).

---

## BUG-ENABLED-LANGS-001 — High: `is_fully_complete()` always returns False

**File:** `app/completeness_service.py` line 104  
**Root cause:** `Settings.ENABLED_LANGUAGES` is declared as `str = "en,es,de,it,fr,pt"`. The method does `languages = required_languages or get_settings().ENABLED_LANGUAGES`, receiving the raw string. When iterating over a string, Python yields individual characters: `'e'`, `'n'`, `','`, `'e'`, `'s'`, etc. The status lookup `statuses.get('e')` never returns `"done"`, so the method always returns `False`.

**Evidence:**
```python
# completeness_service.py line 104 — WRONG:
languages = required_languages or get_settings().ENABLED_LANGUAGES
# → iterates: 'e','n',',','e','s',',','d','e',',','i','t',',','f','r',',','p','t'
```

**Impact:** `is_fully_complete()` can never return `True`, corrupting partial-retry logic and completeness reporting. Used by `retry_incomplete.py` and any caller that checks completion status.

**Fix:** `languages = required_languages or get_settings().ENABLED_LANGUAGES.split(",")`

---

## BUG-DOUBLE-COMMIT-002 — Medium: Redundant `session.commit()` calls

**File:** `app/scraper_service.py`  
**Root cause:** Build 84 fixed the double-commit in `_persist_hotel_data()` (BUG-DOUBLE-COMMIT-001-FIX) but did not extend the fix to four other methods that use `get_db()` as a context manager and also call `session.commit()` explicitly.

**Affected methods:**
| Method | Line |
|--------|------|
| `dispatch_batch()` | 291 |
| `_upsert_lang_status()` | 1361 |
| `_log_scraping_event()` | 1398 |
| `_finalize_url()` | 1423 |
| `_mark_url_error()` | 1428 |

**Impact:** Each call executes two commit round-trips instead of one. At 6 languages × 14 URLs = 84 scraping cycles per batch, approximately 336 redundant commit calls per batch. Increases DB load and connection checkout time.

**Fix:** Remove all `session.commit()` calls inside `with get_db() as session:` blocks. The context manager commits on clean exit.

---

## BUG-VIEW-004 — Medium: `v_hotels_full` view missing columns

**File:** `schema_v77_complete.sql`  
**Root cause:** The `v_hotels_full` view was not updated when `category_code` (Build 82) and `adults/children/images/info` (Build 80) were added to their respective tables.

**Missing fields in `nearby_places` subquery:**
- `category_code` (SMALLINT) — added Build 82 for API integer category codes

**Missing fields in `room_types_detail` subquery:**
- `adults` (SMALLINT)
- `children` (SMALLINT)
- `images` (JSONB)
- `info` (TEXT)

**Impact:** Any consumer of `v_hotels_full` (reporting queries, external tools) receives incomplete data. The API endpoint `GET /hotels/{id}` is not affected (it queries tables directly), but the view used for analytics and direct SQL access is missing these API-required fields.

---

## BUG-DEAD-CODE-001 — Low: Duplicate unreachable implementation in `_extract_nearby_places()`

**File:** `app/extractor.py`  
**Root cause:** A 170-line duplicate of `_extract_nearby_places()` exists after the first `return places` statement. The block was an older version of the method (without `category_code` support) accidentally retained after a merge or partial edit. Python treats the `"""..."""` after `return` as a string literal expression (not a docstring), and all subsequent code is unreachable.

**Impact:** No runtime impact (dead code never executes). High maintenance risk: future developers may edit the dead copy believing it is active, or may be confused about which implementation is canonical.

**Fix:** Remove lines 3262–3428 (the unreachable duplicate block). The active implementation (lines 3096–3261) is complete and includes `category_code` support.

---

## Files Modified

| File | Changes |
|------|---------|
| `app/main.py` | BUG-DISPATCH-001-FIX, BUG-LOAD-URLS-001-FIX |
| `app/scraper_service.py` | BUG-VPN-INIT-001-FIX, BUG-DOUBLE-COMMIT-002-FIX (×5) |
| `app/completeness_service.py` | BUG-ENABLED-LANGS-001-FIX |
| `schema_v77_complete.sql` | BUG-VIEW-004-FIX |
| `app/extractor.py` | BUG-DEAD-CODE-001-FIX |

---

*Generated by automated audit — BookingScraper Pro Build 86*
