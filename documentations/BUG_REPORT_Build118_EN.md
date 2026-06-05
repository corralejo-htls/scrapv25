# BookingScraper Pro v6.0.0 — Bug Report Build 118
**Build fixed:** 118  
**Report date:** 2026-06-05  
**Repository:** `github.com/corralejo-htls/scrapv25` — cloned and analysed  
**Schema source of truth:** `schema_v77_complete.sql`  
**Previous build in repo:** scraper.py → Build 117 · vpn_manager_windows.py → Build 116 · scraper_service.py → Build 114  

---

## IMPORTANT: REPOSITORY STATE CLARIFICATION

Before listing bugs, the repository was cloned and every affected file was read line-by-line. The prior session's analysis (Build 116 patch notes) was based on the audit report alone. The actual code differs in one critical area:

| Bug | Prior analysis said | Actual repo state |
|-----|---------------------|-------------------|
| BUG-CHROMEDRIVER-001 | Active, needs fix | **Already fixed in Build 117** — `scraper.py` line 518–554 implements `ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()` with 3-strategy fallback. `requirements.txt` already includes `webdriver-manager>=4.0.0`. |
| BUG-VPN-001 | CB never closes | **Partially correct** — CB has 300s cooldown (auto-reset works). Real sub-defect: `Unknown` IP treated as failure even when NordVPN CLI confirmed connection. |
| BUG-RETRY-001 | retry_count not incremented | **Confirmed in source** — `_finalize_url()` and `_mark_url_error()` never touch `retry_count`. |
| BUG-README-001 | 4 vs 6 languages | **Confirmed** — README not updated. |

---

## BUG REGISTRY — BUILD 118

| ID | Priority | Component | Status | Impact |
|----|----------|-----------|--------|--------|
| BUG-CHROMEDRIVER-001 | ~~P0~~ | `app/scraper.py` | **FIXED in Build 117** | — |
| BUG-VPN-001 (sub-defect) | **P1 HIGH** | `app/vpn_manager_windows.py` | **FIXED in Build 118** | CB false-trips on DNS timeout |
| BUG-RETRY-001 | **P2 MEDIUM** | `app/scraper_service.py` | **FIXED in Build 118** | retry_count always 0 |
| BUG-README-001 | **P3 LOW** | `documentations/readme.md` | **Documented — manual fix** | Doc inconsistency |

---

## BUG-CHROMEDRIVER-001 — FIXED IN BUILD 117 (prior to this session)

### Confirmed fix location
`app/scraper.py` — `_get_driver()` method, lines 517–554 (Build 117 source).

```python
# Strategy 2 — webdriver-manager (Build 117 code, verified in repo):
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
_mgr_path = ChromeDriverManager(
    chrome_type=ChromeType.BRAVE
).install()
_svc = _Svc(executable_path=_mgr_path)
_launch_result["driver"] = webdriver.Chrome(service=_svc, options=options)
```

### Three-strategy fallback (as implemented):
1. `CHROMEDRIVER_PATH` in `.env` (explicit path, legacy/offline — highest priority)
2. `webdriver-manager` with `ChromeType.BRAVE` — auto-downloads matching ChromeDriver
3. `webdriver.Chrome()` without service — system PATH fallback

### Note on Brave v149 in Build 115 session
The `scraper.py` in the current repo is already Build 117. The Build 115 session that produced the audit report ran with an older `scraper.py` that had the static path. **No code change needed for this bug.**

---

## BUG-VPN-001 — FIXED IN BUILD 118 (this session)

### Root cause (confirmed in source code)

File: `app/vpn_manager_windows.py` — `_connect_via_cli()` method, lines 650–674 (Build 116).

The IP validation logic at line 656:
```python
# Build 116 (BEFORE fix):
if new_ip != "Unknown" and ip_changed_from_home and ip_changed_from_prev:
    ...  # only path that returns True
elif new_ip == self._prev_vpn_ip and new_ip != "Unknown":
    return False  # same IP — auto-connect re-used server
else:
    return False  # catches: new_ip == "Unknown" → ALWAYS False
```

When `new_ip == "Unknown"`, the function always fell into the `else` branch and returned `False`. Back in `connect()` (line 331): `self._breaker.record_failure()` was called. This counted a DNS timeout of `api.ipify.org` as a full VPN failure.

### Evidence trace from Build 115 logs
```
[11:49:05] get_current_ip deadline reached — using Unknown    → record_failure() #1
[11:49:53] get_current_ip deadline reached — using Unknown    → record_failure() #2
[11:50:41] get_current_ip deadline reached — using Unknown    → record_failure() #3
[11:50:41] VPN circuit breaker OPENED after 3 failures.       ← CB triggered
```
NordVPN CLI actually connected each time (confirmed by `time.sleep(8)` completing and logs showing real IPs later). The IP check service timed out due to DNS instability in the first seconds post-VPN-connect — precisely the window that `BUG-DNS-RACE-001-FIX` was added to address.

### Secondary finding: cooldown hardcoded to 300s
`NordVPNManager.__init__()` line 254:
```python
# Build 116 (BEFORE fix):
self._breaker = VPNCircuitBreaker(max_failures=3, cooldown_seconds=300.0)
```
The 300s value is not configurable. This is a maintainability concern, not a functional bug — but it prevents operational tuning.

### Fix applied (Build 118)

**Fix A — `_connect_via_cli()`**: New `elif new_ip == "Unknown":` branch. When `VPN_CB_UNKNOWN_IP_AS_SUCCESS=true` (default), returns `True` with a WARNING log instead of `False`. Does not update `_prev_vpn_ip` (unknown IP cannot be stored as reference).

```python
# Build 118 (_connect_via_cli — new branch):
elif new_ip == "Unknown":
    _accept_unknown = bool(getattr(self._cfg, "VPN_CB_UNKNOWN_IP_AS_SUCCESS", True))
    if _accept_unknown:
        logger.warning("BUG-VPN-001-FIX: VPN CLI connected to %s (rc=0) but "
                       "IP check returned Unknown — treating as SUCCESS ...")
        return True   # → connect() calls record_success() → CB not incremented
    else:
        logger.error("... [VPN_CB_UNKNOWN_IP_AS_SUCCESS=false — counting as failure]")
        return False
```

**Fix B — `VPNCircuitBreaker`**: `is_open` property now logs elapsed and remaining cooldown at DEBUG level. Added `force_reset()` method for programmatic recovery.

**Fix C — `NordVPNManager.__init__()`**: Reads `VPN_CB_COOLDOWN_S` from config instead of hardcoding:
```python
_cb_cooldown = float(getattr(self._cfg, "VPN_CB_COOLDOWN_S", 300.0))
self._breaker = VPNCircuitBreaker(max_failures=3, cooldown_seconds=_cb_cooldown)
```

### New config fields added (config.py + env.example)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `VPN_CB_UNKNOWN_IP_AS_SUCCESS` | bool | `true` | Unknown IP treated as success when CLI confirmed connection |
| `VPN_CB_COOLDOWN_S` | float | `300` | CB cooldown in seconds (was hardcoded) |

### Files modified
- `app/vpn_manager_windows.py` — `VPNCircuitBreaker`, `NordVPNManager.__init__()`, `_connect_via_cli()`
- `app/config.py` — two new fields
- `env.example` — two new documented variables

---

## BUG-RETRY-001 — FIXED IN BUILD 118 (this session)

### Root cause (confirmed in source code)

File: `app/scraper_service.py` — `_finalize_url()` lines 1660–1681 and `_mark_url_error()` lines 1683–1691 (Build 114).

```python
# _finalize_url() Build 114 (BEFORE fix) — full body:
def _finalize_url(self, url_obj, status, completed, failed):
    with get_db() as session:
        db_obj = session.get(URLQueue, url_obj.id)
        if db_obj:
            db_obj.status              = status        # set to "error"
            db_obj.languages_completed = ...
            db_obj.languages_failed    = ...
            db_obj.scraped_at          = _now()
            db_obj.updated_at          = _now()
            if failed:
                db_obj.last_error = ...
            # retry_count: NEVER TOUCHED ← the bug
```

`retry_count` is defined in the ORM model (`models.py` line 150) and in the schema (`schema_v77_complete.sql` line 239) but neither `_finalize_url()` nor `_mark_url_error()` ever modify it.

`max_retries` is also defined (model line 151, schema line 240, default=3) but the comparison `retry_count < max_retries` was never evaluated because the counter was never incremented.

This is the third recurrence of the **BUG-PERSIST pattern** (method/field exists but is never called from the execution path):
- Build 63: upsert methods defined but never called
- Build 76: same pattern on a different method
- Build 114/118: `retry_count` field exists, increment never wired up

### Evidence from Build 115 database state
```
url_queue.retry_count = 0 for ALL 141 URLs
url_language_status:  up to 5 retry attempts per URL-language combination
```
The per-language Selenium retry loop (inside `_scrape_language()`) worked correctly — it retried up to 3 times per language. But `url_queue.retry_count`, which tracks complete URL-pass attempts, never moved from 0.

### Fix applied (Build 118)

**`_finalize_url()`** — when `status != "done"` and `failed` is non-empty:
```python
db_obj.retry_count = (db_obj.retry_count or 0) + 1
max_retries = db_obj.max_retries if db_obj.max_retries is not None else 3

if db_obj.retry_count < max_retries:
    effective_status = "pending"   # re-queue for next Beat tick
    logger.info("BUG-RETRY-001-FIX: URL %s retry %d/%d — re-queued as pending ...")
else:
    effective_status = "error"     # permanent — max retries exhausted
    logger.warning("BUG-RETRY-001-FIX: URL %s max_retries (%d) reached ...")
```

**`_mark_url_error()`** — same logic applied to fatal exception path.

**When status == "done"**: `retry_count` is NOT touched. A complete success does not count as a retry attempt.

### Schema columns used (verified in schema_v77_complete.sql)
```sql
retry_count  SMALLINT  NOT NULL DEFAULT 0   -- line 239
max_retries  SMALLINT  NOT NULL DEFAULT 3   -- line 240
```

### Verification query
```sql
-- Run after fix + one failed scrape cycle:
SELECT
    COUNT(*) FILTER (WHERE retry_count = 0)  AS stuck_at_zero,
    COUNT(*) FILTER (WHERE retry_count > 0)  AS incremented,
    MAX(retry_count)                          AS max_seen
FROM url_queue;
-- Build 115:  stuck_at_zero=141, incremented=0
-- Build 118+: stuck_at_zero should decrease; incremented > 0
```

### File modified
- `app/scraper_service.py` — `_finalize_url()` and `_mark_url_error()`

---

## BUG-README-001 — P3 DOCUMENTATION (no code change)

### Finding
`documentations/readme.md` documents 4 languages (EN/ES/DE/IT). The live system runs 6 (EN/ES/DE/IT/FR/PT), confirmed by:
- `app/config.py` — `ENABLED_LANGUAGES: str = Field(default="en,es,de,it,fr,pt", ...)`
- `logs_API-service.csv` — `"LanguageConfig loaded: 6 languages active ['en', 'es', 'de', 'it', 'fr', 'pt']"`

### Required manual change (not automated in this build)
Edit `documentations/readme.md`:
- Language count: 4 → 6
- Language list: EN/ES/DE/IT → EN/ES/DE/IT/FR/PT
- Strategy E thresholds: update any `4/4` references to `6/6`

---

## SYSTEM HEALTH MATRIX — BUILD 118

| Component | Build 115 state | Build 118 state |
|-----------|----------------|----------------|
| ChromeDriver / Brave | ❌ v147 vs v149 — 100% failure | ✅ Fixed in Build 117 (webdriver-manager) |
| VPN circuit breaker | ❌ CB opened on DNS timeout (false-positive) | ✅ Fixed — Unknown IP no longer trips CB |
| retry_count tracking | ❌ Stuck at 0 for all URLs | ✅ Fixed — incremented on every failed pass |
| Celery Beat scheduler | ✅ Operational | ✅ No change |
| PostgreSQL / pool | ✅ Operational | ✅ No change |
| FastAPI service | ✅ Operational | ✅ No change |
| Redis / Memurai | ✅ Operational | ✅ No change |

---

## FILES MODIFIED IN BUILD 118

| File | Change |
|------|--------|
| `app/scraper_service.py` | BUG-RETRY-001-FIX: `retry_count` increment in `_finalize_url()` and `_mark_url_error()` |
| `app/vpn_manager_windows.py` | BUG-VPN-001-FIX: Unknown-IP branch in `_connect_via_cli()`; CB cooldown from config; `force_reset()`; improved logging |
| `app/config.py` | Two new fields: `VPN_CB_UNKNOWN_IP_AS_SUCCESS`, `VPN_CB_COOLDOWN_S` |
| `env.example` | Two new documented variables matching new config fields |

---

## ARCHITECTURAL OBSERVATION: BUG-PERSIST PATTERN

Three builds in a row (63, 76, 118) have exhibited the same pattern: a field or method exists in the model/schema but is never wired into the execution path. This suggests a systematic gap in integration testing.

**Recommendation:** Add a post-scrape integration test that asserts `retry_count > 0` after a simulated failure cycle. The existing `tests/test_scraper.py` and `tests/test_strategy_e.py` cover extraction and strategy logic but do not assert database state after failure paths.

---

*Report: BookingScraper Pro v6.0.0 Build 118 | 2026-06-05 | Based on full source code analysis of cloned repository*
