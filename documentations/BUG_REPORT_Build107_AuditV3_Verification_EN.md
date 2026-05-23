# BookingScraper Pro v6.0.0 — Verification of Audit v3 & Build 107 Status (EN)

**Repository:** `corralejo-htls/scrapv25` (read-only clone verified OK)
**Verification date:** 2026-05-23
**Document under review:** `BookingScraper_Audit_Report_Build106_EN_v3.md`
**Method:** Every v3 claim re-checked against the actual `pruebas/*.csv` / `*.html` and the
source code. Nothing accepted on the report's word.

---

## 0. Headline

v3 is a clear improvement over v2: it **adopted the Build 107 analysis** — 840 rows / 0
duplicates, the real image composition (large 100% / thumb 93.1% / highres 49.3%, 81 errors),
and the correct root cause (the supplement source never builds `highres_url`). **v3's sole
HIGH-priority finding (P0) is already implemented in Build 107.** A few stale claims from v2
survive in v3 and are refuted again below with data.

---

## 1. Claim-by-Claim Verdict

| v3 item | v3 says | Verified verdict | Evidence |
|---|---|---|---|
| `url_queue` | 141 (140 done, 1 error) | ✅ **Correct** | direct parse |
| `hotels` rows / duplicates | 840 / 0 | ✅ **Correct** (v3 fixed v2's 841 error) | dump = 840, baseline sums 840, 0 `(url_id,language)` dups |
| Image composition + 81 errors | large 11,772 / thumb 10,964 / highres 5,808 / 81 err | ✅ **Correct** | matches `image_downloads` exactly |
| **#1 highres root cause** | supplement never builds highres | ✅ **Correct — and ALREADY FIXED in Build 107** | code review + fix in `extractor.py` |
| **#2 empty categories "Skiing ~1.9%"** | ~1.9%, Skiing group | ❌ **Stale/incorrect** | real 0.71% (475/67,017); only 29/475 are ski-related |
| **#3 `pt` 0-services (pending)** | possible, pending | ❌ **False** | 0 hotel-language pairs have 0 services; `pt`=11,188 |
| Services total | 65,727 | ⚠️ **Stale** | real = **67,017** |
| #4 canceled hotel | external | ✅ **Correct** | `error` state, 6 logs |
| #5 4 hotels not ingested | parser issue | ⚠️ **Count correct, cause wrong** | all 4 pass `load_urls.py` validation → operational drift |
| P1 `NOT NULL` on `service_category` | recommended | ❌ **Unsafe** | breaks recreate-from-schema startup; 94.9% of empties are legit popular-facility items |
| P1 `NOT NULL` on `image_downloads.size_variant` | recommended | ❌ **Wrong** | column is named `category`, intentionally nullable, with a CHECK; `size_variant` does not exist |

---

## 2. v3's P0 Is Already Implemented (Build 107)

v3 recommends (P0) deriving `highres_url` and missing `thumb_url` from `large_url` by swapping
the size segment, reusing the shared `k=` token. **This is exactly `BUG-IMG-DERIVE-001-FIX`,
delivered in Build 107.** The current `app/extractor.py` already:

1. Harvests the `k=` token per `id_photo` from any size segment in the HTML.
2. Supplements it with tokens embedded in JS-source URLs.
3. Derives all three sizes (`max200`, `max1024x768`, `max1280x900`) for every photo.
4. Adds supplement photos with the three sizes pre-built.

### 2.1 Fresh empirical proof on real HTML (post-fix)

| Snapshot | Photos | thumb | large | highres | highres segment correct |
|---|---|---|---|---|---|
| `HTML_1001_Villa-Dvor_Ohrid.html` | 106 | 100% | 100% | **100%** | ✅ `max1280x900` |
| `HTML_78465_wild-&-bolz-eMotel.html` | 24 | 100% | 100% | **100%** | ✅ `max1280x900` |

### 2.2 Projected full-run impact

| Metric | Before | After |
|---|---|---|
| `highres_url` | 5,808 | 11,772 (+5,964) |
| `thumb_url` | 10,964 | 11,772 (+808) |
| `image_downloads` | 28,544 | **35,316** |

This matches v3's own "expected impact after fix" (~35,316), reached through derivation — not
retries.

---

## 3. Refuted / Corrected Items (with data)

### 3.1 Empty `service_category` — not a "Skiing" defect

Real rate is **0.71%** (475 of 67,017), not ~1.9%. Of those 475, only **29** are ski-related.
Cross-referencing against `hotels_popular_services` shows **451 of 475 (94.9%)** are exactly the
"most popular facilities" highlight items (Bar, Free WiFi, Restaurant, Parking, Gym, Spa…),
which Booking.com renders **without** a facility-group header. An empty category there is
**semantically correct**, not a bug. Only 24 items (0.036% of all services) are genuine orphans.

Therefore: **no `NOT NULL` and no invented fallback.** A `NOT NULL` constraint would abort the
fresh DB recreation (`schema` re-run at every startup, no migration), and forcing a category
would contradict Build 103's deliberate move to DOM-verbatim categories. If the downstream API
dislikes empty categories, the clean place to handle it is the export layer (map empty →
"popular"), not the schema. No evidence of API rejection was found.

### 3.2 No language has 0 services

All 140 active hotels have services in all six languages: en 11,012 / es 10,944 / de 11,323 /
it 11,541 / fr 11,009 / **pt 11,188**. Zero hotel-language pairs are empty. v3 Finding #3 can be
closed as **resolved-false**.

### 3.3 `size_variant` does not exist

`ImageDownload` (`app/models.py`) stores the size in a column named **`category`**
(`String(16)`, nullable, `CHECK category IN ('thumb_url','large_url','highres_url')`). After the
Build 107 fix every row is populated anyway, so no constraint change is needed or advisable.

### 3.4 Schema file absence

The `schema_v77_complete.sql` cited as "single source of truth" is **not present** anywhere in
the cloned repository (no `.sql` files exist). The effective schema is `app/models.py`. Any
`schema_v78.sql` recommendation in v3 cannot be applied as written and should target `models.py`
if pursued — but per §3.1/§3.3 none is warranted.

---

## 4. Net Action This Cycle

The only valid actionable finding in v3 (P0 highres/thumb derivation) **is already fixed in
Build 107**. No additional code defect was found that withstands verification. Accordingly, the
delivered files remain the Build 107 set (which implements v3's P0); no no-op build was
manufactured.

| File | State |
|---|---|
| `app/extractor.py` | Contains `BUG-IMG-DERIVE-001-FIX` (v3's P0) — `ast.parse()` OK |
| `app/__init__.py` | `BUILD_VERSION = 107` + changelog — `ast.parse()` OK |
| `app/config.py` | `BUILD_VERSION` default 107 — `ast.parse()` OK |

---

*End of verification — Audit v3 / Build 107 (EN).*
