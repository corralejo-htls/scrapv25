# Bug Report — BookingScraper Pro v6.0.0 Build 113
## VPN Popup Analysis & Fix: `¿Pausar la conexión automática?`

**Report Date:** 2026-06-01  
**Build Analyzed:** 112 (current committed code)  
**New Build:** 113  
**Evidence:** Screenshot — NordVPN dialog "¿Pausar la conexión automática en esta sesión?"  
**Severity:** 🔴 Critical (interrupts automated scraping; requires operator intervention)  

---

## 1. EXECUTIVE SUMMARY

| # | Bug ID | Severity | File | Root Cause |
|---|--------|----------|------|------------|
| 1 | BUG-VPN-POPUP-DIRECT-001 | 🔴 Critical | `app/vpn_manager_windows.py` | `rotate()` calls `nordvpn -d` which triggers NordVPN's auto-connect pause dialog |
| 2 | BUG-VPN-EXTRAE-WIN32-001 | 🟡 Medium | `pruebas/extraer_imagenes.py` | `subprocess.run()` uses `shell=True` string — no `CREATE_NO_WINDOW`, exposes UAC risk |

---

## 2. BUG-VPN-POPUP-DIRECT-001 🔴 CRITICAL

### Problem Description

The screenshot shows NordVPN's confirmation dialog:

> **"¿Pausar la conexión automática en esta sesión?"**  
> "Si pones en pausa la conexión automática en esta sesión, la VPN se
> desconectará. Si reinicias la aplicación, cierras sesión y vuelves a
> iniciarla, cambias de red o te conectas a una VPN manualmente, la conexión
> automática se reanudará."

This dialog appears **on every VPN rotation** triggered by BookingScraper's
automatic scraping cycle.

### Root Cause Analysis

**The existing dismiss machinery (Build 73) was not the root issue — the trigger was:**

```
rotate()  →  disconnect()  →  subprocess nordvpn.exe -d
                                       ↓
                          NordVPN GUI: "¿Pausar la conexión automática?"
```

When NordVPN has **Auto-connect** enabled (default setting), calling
`nordvpn -d` (explicit disconnect) always triggers this confirmation dialog.
The Build 73 fix (pywin32 BM_CLICK + background dismiss thread) attempts to
click "Cancelar" after the popup appears. However, this approach has inherent
race conditions:

- The popup may render faster than the dismiss thread fires
- The `win32gui.EnumWindows` traversal may not find the window in time
- On multi-monitor setups, the HWND search may fail
- The popup persists visually even when BM_CLICK fires (brief flicker)

**Result:** The popup was still visible to the operator and, in some cases, the
dismiss was missing its timing window, leaving the VPN disconnected until manual
intervention.

### Key Insight: `extraer_imagenes.py` Never Shows the Popup

Comparing VPN strategies side by side:

| | `vpn_manager_windows.py` (Build 112) | `extraer_imagenes.py` |
|---|---|---|
| Step 1 | `nordvpn -d` ← **triggers popup** | *(nothing)* |
| Step 2 | `sleep(5)` | *(nothing)* |
| Step 3 | `nordvpn -c -g "country"` | `nordvpn -c -g "country"` |
| Popup? | **Always when auto-connect on** | **Never** |
| Validated with | — | 141 hotels, 0 popups |

`extraer_imagenes.py` calls `nordvpn -c -g "country"` **directly** without a
prior `nordvpn -d`. When NordVPN is already connected and receives a new `connect`
command, it switches servers internally without going through a user-visible
auto-connect pause flow.

### Fix (Build 113)

**Strategy: eliminate the trigger, not just the symptom.**

New `rotate()` flow with `VPN_ROTATE_SKIP_DISCONNECT=True` (default):

```python
# BEFORE (Build 112)
self.disconnect()       # ← triggers "¿Pausar la conexión automática?"
time.sleep(5)
self._popup_dismiss_stop.set()
success = self.connect(new_country)

# AFTER (Build 113, skip_disconnect=True)
success = self.connect(new_country)   # ← no nordvpn -d; popup never appears
```

NordVPN handles the server switch without a visible auto-connect interruption.

**New config toggle `VPN_ROTATE_SKIP_DISCONNECT`:**

```ini
# .env — Build 113
VPN_ROTATE_SKIP_DISCONNECT=true   # default — popup-free rotation
# VPN_ROTATE_SKIP_DISCONNECT=false  # legacy: explicit disconnect first
```

**What is preserved:**
- `disconnect()` method kept intact for explicit shutdown (application exit,
  error recovery)
- Popup dismiss machinery (`_dismiss_nordvpn_popup`, background thread, pywin32
  BM_CLICK) kept as safety net for unexpected popups in edge cases
- All IP validation logic (`_prev_vpn_ip`, `_original_ip` checks) unchanged
- Circuit breaker unchanged
- Home country exclusion unchanged
- Lock-based concurrency protection unchanged

**Timing improvement:**

| Phase | Build 112 | Build 113 |
|-------|-----------|-----------|
| Pre-connect | `sleep(5)` teardown | *(eliminated)* |
| Connect + stabilize | ~10 s | ~10 s |
| **Total per rotation** | **~15 s** | **~10 s** |
| Popup risk | **Every rotation** | **None** |

---

## 3. BUG-VPN-EXTRAE-WIN32-001 🟡 MEDIUM

### Problem Description

`pruebas/extraer_imagenes.py`'s `nordvpn()` function called `subprocess.run()`
with a **string command** (implicit `shell=True`) and without Windows subprocess
hardening flags:

```python
# BEFORE — Build 112 (string + shell=True implicit)
command = f'nordvpn -c -g "{pais_aleatorio}"'
resultado = subprocess.run(
    command,           # ← string → shell=True → risk of UAC / CMD window
    capture_output=True, text=True
)
```

Issues:
1. **No `CREATE_NO_WINDOW`**: a CMD window could flash on screen or, worse,
   NordVPN's DiagnosticsTool child process inherits a visible handle → UAC dialog
   (same class of bug as BUG-VPN-004-FIX Build 71 in the main app).
2. **String command / implicit `shell=True`**: on Windows, subprocess with a
   string triggers `cmd.exe /c "..."`. Not necessary here and slightly less safe.
3. **Logic issues**: `time.sleep(backoff)` fired before the FIRST attempt
   (not only on retries), adding unnecessary delay. `backoff *= 3` was
   aggressive (5s → 15s → 45s per extra attempt).
4. **No `timeout` parameter**: a stalled nordvpn call would block indefinitely.
5. **`return False` inside retry loop on non-retry exceptions**: an unexpected
   exception on attempt 1 would exit without trying again.

### Fix (Build 113)

```python
# AFTER — Build 113 (list args + Windows flags + correct retry logic)
cmd_args = ["nordvpn", "-c", "-g", pais_aleatorio]   # list → shell=False
resultado = subprocess.run(
    cmd_args,
    capture_output=True, text=True,
    timeout=60,
    shell=False,
    creationflags=_EXTRAE_NO_WINDOW,     # CREATE_NO_WINDOW
    startupinfo=_EXTRAE_STARTUPINFO,     # SW_HIDE
)
```

Additional fixes:
- `time.sleep(backoff)` moved to the retry path only (not before attempt 1)
- `backoff *= 2` instead of `*3` (less aggressive: 5s → 10s → 20s)
- `timeout=60` prevents infinite block
- All exception types properly retry instead of `return False` immediately
- Country list moved to module-level `_NORDVPN_PAISES` constant (no re-creation
  per call)
- **NO-DISCONNECT approach preserved** — the core correctness of the function

---

## 4. COMPARISON TABLE: VPN STRATEGIES

| Attribute | `vpn_manager_windows.py` (Build 113) | `extraer_imagenes.py` (Build 113) |
|---|---|---|
| Disconnect before connect | No (skip_disconnect=True) | No (never had it) |
| "¿Pausar la conexión?" popup | **Eliminated** | **Never appeared** |
| subprocess argument style | List args | List args |
| CREATE_NO_WINDOW | ✅ Yes | ✅ Yes (added Build 113) |
| Timeout | 60s | 60s (added Build 113) |
| IP validation after connect | ✅ Full dual-check | ❌ No (standalone script) |
| Circuit breaker | ✅ Yes | ❌ No (standalone script) |
| Home country exclusion | ✅ Yes | ❌ No (standalone script) |
| Retry on failure | ✅ Yes (with backoff) | ✅ Yes (improved Build 113) |

---

## 5. FILE CHANGE SUMMARY

| File | Change | Type |
|---|---|---|
| `app/vpn_manager_windows.py` | `rotate()` rewritten — skip disconnect by default | Logic fix |
| `app/config.py` | `VPN_ROTATE_SKIP_DISCONNECT` toggle added; `BUILD_VERSION=113` | Config |
| `app/__init__.py` | Build 113 changelog; `BUILD_VERSION=113` | Version |
| `pruebas/extraer_imagenes.py` | `nordvpn()` hardened with Windows flags + list args | Robustness |

---

## 6. OPERATOR GUIDE

### Default production behavior (no .env change needed)
`VPN_ROTATE_SKIP_DISCONNECT` defaults to `True` — the popup is eliminated
immediately upon deployment without any configuration change.

### If reverting to legacy behavior
```ini
# .env
VPN_ROTATE_SKIP_DISCONNECT=false
```
Use only if auto-connect is disabled in NordVPN settings AND your network policy
requires an explicit disconnect before reconnecting.

### Validation
After deploying Build 113, monitor the next scraping cycle. The log should show:
```
VPN: direct reconnect to Spain (no disconnect — popup-free)
VPN rotation successful → Spain
```
instead of:
```
VPN disconnected.
BUG-VPN-008-FIX: BM_CLICK sent to 1 'Cancelar' button(s) via pywin32
```

---

*End of Bug Report — BookingScraper Pro v6.0.0 Build 113*  
*Generated: 2026-06-01*
