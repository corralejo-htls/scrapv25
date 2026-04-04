# Bug Report — BookingScraper Pro v6.0.0 (Build 75)
**Date:** 2026-04-04
**Origin:** HTML Tag Audit Report review (HTML_Tag_Audit_Report_EN.md)
**Status:** RESOLVED

---

## Audit Report Corrections (NOT implemented)

The following claims in the audit report are **technically incorrect** and were
rejected after cross-checking against the live codebase and schema:

| Audit Claim | Reality | Source |
|---|---|---|
| CloudScraperEngine = primary engine | **Eliminated in Build 63.** Selenium is the sole engine. | `scraper.py` line 281 |
| Extraction flow Step 1 = `CloudScraperEngine.fetch()` | **Does not exist.** Flow starts at `HotelScraper.scrape()` | `scraper_service.py` |
| `hotels_amenities` table | **Deleted in Build 65.** Canonical source is `hotels_popular_services` | `schema_v67_complete.sql` line 23 |
| `hotels_room_types` table | **Does not exist.** `room_types` is a JSONB column in the `hotels` table | `schema_v67_complete.sql` line 181 |
| `.bui-title__text` / `.bui-list__description` classes | **BUI legacy.** Not present in current Booking.com React DOM | DOM audit |
| `div[data-testid="house-rules"] .bui-list__item` | `.bui-list__item` is obsolete BUI class | DOM audit |
| `div[data-testid="checkin-checkout-info"]` | Extractor correctly uses `property-section--policies` | `extractor.py` line ~847 |

---

## AUDIT-HTML-001 — High
**File:** `app/extractor.py`
**Method:** `_extract_all_services()`
**Root cause:** Missing `data-testid="facility-group"` strategy — more precise than regex fallback

### Technical Analysis

After `_expand_facilities()` (BUG-SVC-001-FIX) clicks "See all N facilities",
Booking.com injects the full list as structured `data-testid="facility-group"` blocks.
Each block contains:
- `data-testid="facility-group-icon"` — SVG icon (must be excluded)
- A category header div
- A `<ul><li>` list of individual services

The existing Strategy 2 used `re.compile(r"facilit", re.I)` which also matched
`facility-group-icon`, `facilities-wrapper`, and other sub-elements, causing
duplicated or noisy text captures. `data-testid="facility-group"` is the correct
semantic container and is more stable.

### Fix Applied

**New Strategy 1.5** inserted between Strategy 1 (DOM legacy section) and
Strategy 2 (regex facilit):

```python
# Strategy 1.5: data-testid="facility-group" (AUDIT-HTML-001)
fac_groups = self.soup.find_all(attrs={"data-testid": "facility-group"})
if fac_groups:
    for group in fac_groups:
        # Strip icon element to avoid SVG text noise
        icon_el = group.find(attrs={"data-testid": "facility-group-icon"})
        if icon_el:
            icon_el.extract()
        for li in group.find_all("li"):
            _add(li.get_text(" ", strip=True))
```

**Priority cascade (updated):**

| Strategy | Selector | Trigger |
|---|---|---|
| 0 | Apollo JSON cache | `>= 30` items |
| 1 | `property-section--facilities` | Legacy DOM section |
| **1.5** | `facility-group` (NEW) | Post-expand React blocks |
| 2 | regex `facilit*` | Broad regex fallback |
| 3 | `popular-facilities-wrapper` | Last resort (~10 items) |

---

## STRUCT-018 — High
**File:** `app/extractor.py`
**Method:** `extract_all()` — missing `room_types` key
**Root cause:** `hotels.room_types` (JSONB column) was always NULL — extractor never generated the key

### Technical Analysis

`scraper_service.py` line 585 explicitly reads `data.get("room_types")` and
persists it to `Hotel.room_types` (JSONB, `schema_v67_complete.sql` line 181).
However `extractor.py` never included `"room_types"` in the `extract_all()` dict,
so `data.get("room_types")` always returned `None` → column always NULL for
all 13 URLs × 6 languages.

BUI classes proposed by the audit (`.bui-list__description`, `.bui-title__text`)
were discarded — not present in current Booking.com React DOM.

### Fix Applied

**New method `_extract_room_types()`** added (STRUCT-018), and wired in `extract_all()`:

```python
# extract_all() — new entry
"room_types": self._extract_room_types(),
```

**DOM selectors used (React stable):**

| Field | Selector |
|---|---|
| Block container | `data-testid="room-block"` |
| Room name | `data-testid="room-type-title"` |
| Description | `data-testid="room-description"` |
| Facilities | `data-testid="room-facilities"` → `span` |

**Occupancy fields omitted by design:** `occupancy-max-guests` /
`occupancy-max-children` use SVG icon counts that are unreliable after
`window.stop()` interrupts the page load. Returning `0` consistently would
be worse than omitting the field.

**Output format (per room block):**
```json
[
  {
    "name": "Deluxe Double Room",
    "description": "Spacious room with sea view...",
    "facilities": ["Free WiFi", "Air conditioning", "Flat-screen TV"]
  }
]
```

---

## Fix Verification

| Check | Result |
|---|---|
| `ast.parse(extractor.py)` | PASS |
| `ast.parse(scraper.py)` | PASS |
| Strategy 1.5 inserted | line 1667 ✓ |
| `facility-group-icon` stripped | confirmed ✓ |
| `_extract_room_types()` defined | line 1825 ✓ |
| `room_types` key in `extract_all()` | line 432 ✓ |
| BUI classes absent | confirmed — not used ✓ |

---

## Files Modified

| File | Change |
|---|---|
| `app/extractor.py` | Strategy 1.5 in `_extract_all_services()`; new `_extract_room_types()`; `room_types` key in `extract_all()` |
| `app/scraper.py` | No changes in this session (BUG-SVC-001 already applied in Build 65) |

---

## Cumulative Build 65 → 75 Change Summary

| Bug ID | Severity | File | Change |
|---|---|---|---|
| BUG-SVC-001 | Critical | `scraper.py` | `_expand_facilities()` — click "See all N facilities" |
| BUG-SVC-002 | High | `extractor.py` | Strategy 0 threshold `>= 5` → `>= 30` |
| AUDIT-HTML-001 | High | `extractor.py` | Strategy 1.5: `facility-group` selector |
| STRUCT-018 | High | `extractor.py` | `_extract_room_types()` + wire in `extract_all()` |
