# Bug Report — BUG-VPN-004 + BUG-VPN-005 + BUG-VPN-006

| Field | Value |
|---|---|
| **IDs** | BUG-VPN-004, BUG-VPN-005, BUG-VPN-006 |
| **Title** | Windows UAC dialog during rotation; Brave accumulates nordaccount.com tabs; NordVPN opens system browser inside Selenium session |
| **Severity** | 🔴 Critical — VPN rotation interrupted; scraping session corrupted by browser interference |
| **Build detected** | Build 69 |
| **Build fixed** | Build 70 |
| **Files changed** | `app/vpn_manager_windows.py`, `app/scraper.py`, `app/config.py`, `env.example` |
| **Date** | 2026-04-02 |

---

## 1. Observed Behaviour

### Image 1 — Windows UAC Dialog (BUG-VPN-004)
Windows UAC prompt: **"¿Quieres permitir que esta aplicación haga cambios en el dispositivo?"** for `NordSecurity.NordVpn.DiagnosticsTool.Application`. Appears during every VPN rotation attempt, blocking the desktop.

### Images 2, 4, 5 — Brave Tabs Accumulating (BUG-VPN-005)
Brave browser opens 11+ tabs to `nordaccount.com/login` ("Quick, easy, and secure login with Nord"). One new tab per rotation — 6+ rotations per batch × 2 batches = 12+ tabs.

### Image 3 — DNS Error in Brave (BUG-VPN-005 consequence)
After VPN reconnects, Brave cannot resolve `my.nordaccount.com` (DNS_PROBE_POSSIBLE) because the new VPN tunnel's DNS isn't resolved yet. The tab remains open and breaks browser state.

---

## 2. Root Cause Analysis

### BUG-VPN-004 — DiagnosticsTool UAC prompt

**Location**: All `subprocess.run([nordvpn.exe, ...])` calls in `vpn_manager_windows.py`.

The `nordvpn.exe` CLI spawns child processes including `NordVPN.DiagnosticsTool.exe` when it encounters connection issues or as part of normal telemetry. Without `CREATE_NO_WINDOW`, these child processes inherit a window handle and display GUI elements including UAC dialogs.

```python
# Build 69 (BUGGY):
subprocess.run([self._NORDVPN_EXE, "-c", "-g", country_name],
               capture_output=True, text=True, timeout=60, shell=False)
# → DiagnosticsTool child process inherits console → UAC dialog appears
```

### BUG-VPN-005 — nordaccount.com tabs accumulating

**Location**: `_dismiss_nordvpn_popup()` in `vpn_manager_windows.py`.

The existing implementation used `WScript.Shell.AppActivate('NordVPN')` + SendKeys `{ESC}{TAB}{ENTER}`. The sequence had two failure modes:

**Failure Mode A**: `{TAB}` moves focus to a hyperlink in the NordVPN UI (e.g. "Get help" or "Learn more"). `{ENTER}` clicks that link → NordVPN opens its support center / login page in the system browser (Brave) → tab opens.

**Failure Mode B**: If `AppActivate('NordVPN')` focused the wrong NordVPN window (e.g. the main NordVPN app, not the popup dialog), `{TAB}{ENTER}` navigated the NordVPN GUI to a URL and opened it in Brave.

Evidence: Images show `my.nordaccount.com/support-center/?utm_source=nordvpn-windows&utm_campaign=get_help_support_center` — the exact URL triggered by clicking NordVPN's "Get help" button.

**Accumulation**: Each rotation fires `_dismiss_nordvpn_popup()` twice. With 6 rotations per batch (one per language), and 2 URLs per batch, that's 12–24 dismissal attempts, each with a chance of accidentally clicking a link → 11+ tabs observed in production.

### BUG-VPN-006 — NordVPN browser opens inside Selenium session

**Location**: `_build_chrome_options()` in `scraper.py` (no `--user-data-dir`).

Without a dedicated `--user-data-dir`, Selenium's Brave instance uses the same profile path as the system Brave. When NordVPN opens the system browser, it opens a window in the **same Brave profile** that Selenium is using. This can:
- Add tabs to the Selenium-controlled window
- Interfere with cookie/session state (bkng_lang cookies from previous NordVPN navigation)
- Cause driver.get() to land on an unexpected page

---

## 3. Fix Applied — Build 70

### Fix 1 — CREATE_NO_WINDOW for all nordvpn subprocess calls (BUG-VPN-004)

Added Windows subprocess flags at module level:

```python
import sys as _sys
if _sys.platform == "win32":
    _WIN32_NO_WINDOW: int = subprocess.CREATE_NO_WINDOW
    _WIN32_STARTUPINFO = subprocess.STARTUPINFO()
    _WIN32_STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    _WIN32_STARTUPINFO.wShowWindow = 0  # SW_HIDE
```

Applied to every `subprocess.run()` call targeting `nordvpn.exe` and `powershell`:

```python
subprocess.run(
    [self._NORDVPN_EXE, "-c", "-g", country_name],
    capture_output=True, text=True, timeout=60, shell=False,
    creationflags=_WIN32_NO_WINDOW,     # ← prevents child GUI windows
    startupinfo=_WIN32_STARTUPINFO,     # ← SW_HIDE for the process itself
)
```

Child processes launched by nordvpn.exe (DiagnosticsTool) inherit these flags → their windows are hidden → no UAC dialog appears on the desktop.

### Fix 2 — UI Automation popup dismissal (BUG-VPN-005)

Replaced SendKeys with Windows UI Automation API:

```python
# BEFORE (buggy SendKeys):
"[System.Windows.Forms.SendKeys]::SendWait('{TAB}{ENTER}')"
# → accidentally clicks hyperlinks in NordVPN → browser tabs

# AFTER (precise UI Automation):
$pat = $el.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
$pat.Invoke()   # directly invokes "Cancelar" button — no keyboard simulation
```

The PowerShell script enumerates windows, finds any with 'NordVPN' or 'Pausar' in title, then finds and invokes the 'Cancelar'/'Cancel' button directly. No keyboard simulation → zero accidental link clicks.

Fallback: ESC only (no `{TAB}{ENTER}`) if UI Automation fails.

### Fix 3 — Browser tab cleanup after rotation (BUG-VPN-005)

Added `_close_nordaccount_browser_tabs()` called after every successful `_connect_via_cli()`:

```python
# After VPN connects successfully:
self._close_nordaccount_browser_tabs()
```

Uses UI Automation to find and close any browser windows whose title matches `nordaccount`, `nordvpn.com/support`, `Quick.*secure.*login`, etc.

### Fix 4 — Isolated Brave profile for Selenium (BUG-VPN-006)

New config field `SELENIUM_BRAVE_PROFILE_DIR` (default: `data/brave_profile`).

`scraper.py` now passes `--user-data-dir` to Brave:

```python
brave_profile = getattr(cfg, "SELENIUM_BRAVE_PROFILE_DIR", None)
if brave_profile:
    os.makedirs(brave_profile, exist_ok=True)
    options.add_argument(f"--user-data-dir={brave_profile}")
```

NordVPN opens the system Brave with its DEFAULT profile (e.g. `%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data`) → **completely separate process** from Selenium's `data/brave_profile` → no shared state.

Additional flags added:
```python
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")
options.add_argument("--disable-default-apps")
```

---

## 4. Expected Log After Fix

```
[rotate] VPN: rotating (current=IT)...
[rotate] VPN disconnected.
[dismiss] BUG-VPN-005-FIX: UI Automation found NordVPN dialog → Cancelar clicked
[connect] VPN: connecting to Sweden (SE)...
[connect] VPN connected to Sweden — IP: 31.40.213.85
[cleanup] BUG-VPN-005-FIX: No nordaccount browser tabs found.
[browser] BUG-VPN-006-FIX: Selenium Brave using isolated profile at data/brave_profile
```

No UAC dialogs. No nordaccount.com tabs. Selenium Brave unaffected by NordVPN GUI.

---

## 5. Verification

```
# After running a full batch:
# 1. No UAC dialogs appeared on desktop
# 2. No Brave tabs opened to nordaccount.com or nordvpn.com
# 3. Worker log shows "BUG-VPN-005-FIX: No nordaccount browser tabs found."
# 4. Worker log shows "BUG-VPN-006-FIX: Selenium Brave using isolated profile at data/brave_profile"
```

```sql
-- All URLs scraped in 6 languages:
SELECT url_id, COUNT(DISTINCT language) FROM hotels
GROUP BY url_id HAVING COUNT(DISTINCT language) < 6;
-- Expected: 0 rows
```

---

*BookingScraper Pro — Build 69 → Build 70 — 2026-04-02*
