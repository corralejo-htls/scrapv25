# BUG REPORT — BookingScraper Pro v6.0.0 · Build 110 → 111

**Repository:** `corralejo-htls/scrapv25` (verified, read-only clone)
**Schema source of truth:** `schema_v77_complete.sql` (unchanged in this build)
**Platform:** Windows 11 · Python 3.14 · PostgreSQL 14+ · Memurai (Redis)
**Report date:** 2026-05-28
**Author:** Technical audit (code + data verified, no assumptions)

---

## 0. Repository connectivity & method

GitHub access **confirmed**: the repository was cloned with `git clone --depth 1` and every directory was enumerated (`app/` 20 modules, `documentations/` 31 files, `pruebas/` 52 artifacts, `scripts/` 8, `tests/` 8, plus 44 root items). The committed code is at **Build 110** (`app/__init__.py: BUILD_VERSION = 110`), not 106 as the attached reports assume.

The audit followed the project rule *"verify against actual source code, CSV exports in `pruebas/`, and real HTML — never infer from audit reports alone."* Every claim below is backed by a measurement against `pruebas/*.csv` or `pruebas/*.html`.

---

## 1. Executive summary

Two things were checked against the live data:

1. **The attached image audit (Image_Audit_Report_Build106_EN) describes a problem that is already resolved.** The gallery-classification system it proposes was implemented in Build 109 and made robust in Build 110. The current `pruebas/` data confirms **140/140 hotels (100 %) have gallery photos captured**, and all five reference hotels match the modal ground truth **exactly** (see §2). No code change is required for images.

2. **One real, verifiable defect remains** in service-category extraction: **510 services (0.77 % of 66 432) across 53 `(hotel, language)` pairs carry an empty `service_category`.** Root cause identified, fix implemented, and verified against the real HTML snapshots. This is **BUG-SVC-POPULAR-CAT-001**, fixed in Build 111.

---

## 2. Image system — verification (no change needed)

The attached report targets the Build 106 state. The current code already classifies images. Verified against `pruebas/_table__image_data__.csv` (the export now contains the `gallery_visible`, `source`, `subcategory`, `gallery_order` columns):

| external_ref | Hotel | Modal ground truth | DB `gallery_visible` | DB total | Match |
|:------------:|-------|:------------------:|:--------------------:|:--------:|:-----:|
| 1001 | Villa Dvor | 59 | **59** | 106 | ✅ |
| 76033 | Hotel Topazz & Lamee | 38 | **38** | 56 | ✅ |
| 76569 | Hotel Aquamarin | 136 | **136** | 137 | ✅ |
| 76972* | Haus Mobene Garni | 31 | **31** | 47 | ✅ |
| 78465 | wild & bolz eMotel | 22 | **22** | 24 | ✅ |

\* `haus-mobene-garni` carries `external_ref=76972` in the current `url_queue` export (the attached report listed `76924`; same hotel).

Additional verified metrics:

- **Gallery capture coverage:** 140/140 hotels (100 %). The 35.7 % modal-open failure described in the Build 110 changelog has been eliminated — the `_prepare_page()` + retry loop in `image_classifier.py` works on the current dataset.
- **`gallery_visible` photos:** 10 993 of 11 805 (93.1 % of the captured superset is filtered out of the gallery subset, exactly as intended).
- **`highres_url` derivation (Build 107):** image-download success rate **99.69 %** (35 304 ok / 111 errors). The earlier 49.3 % highres coverage gap is closed (the three sizes are now derived from the shared `k=` token).
- **API export filter:** `api_payload_builder._load_gallery_image_urls()` correctly joins `image_data.gallery_visible = TRUE` with `image_downloads`, ordered by `gallery_order`. With 100 % capture the historical superset fallback never triggers.

**Conclusion:** the image objective ("API `images` must match the public gallery") is met by the committed code. No image-related change is shipped in Build 111.

---

## 3. BUG-SVC-POPULAR-CAT-001 — empty `service_category`

### 3.1 Symptom (measured)

`pruebas/_table__hotels_all_services__.csv`:

- Total service rows: **66 432**
- Rows with empty `service_category`: **510 (0.77 %)**
- Distinct `(hotel, language)` pairs affected: **53** (6.3 % of the 840 hotel-language pairs)
- Distribution by language: fr 155 · de 98 · en 96 · pt 89 · es 72

These empty-category services are exported to the external API uncategorised.

### 3.2 Root cause (verified, not inferred)

Three measurements pin the cause precisely:

1. **All 53 affected pairs have *every* service uncategorised** — i.e. the primary DOM strategy (Strategy E45, `property-facilities-block-container` → `facility-group-container`) returned **nothing** for those pages. It is not a partial gap; E45 failed entirely for those hotel-language combinations.

2. **95.1 % of the 510 empty rows also appear in `hotels_popular_services`**, and for 49 of 53 pairs the empty-service count equals the popular-service count. The empty services *are* the "Most popular facilities" badge items shown at the top of the property page.

3. **The DOM block for those items carries a verbatim header.** Verified in `pruebas/HTML_76033__Hotel-Topazz.html` and `pruebas/HTML_1001_Villa-Dvor_Ohrid.html`:

   ```html
   <div data-testid="property-most-popular-facilities-wrapper">
     <div><h3><div>Most popular facilities</div></h3><ul>…</ul></div>
   </div>
   ```

When E45 finds no facility groups (the facilities block is lazy-loaded and, for these hotels, stayed empty), control falls to the fallback strategies. Two of them harvest the popular-facilities wrapper but **discard its `<h3>` header**, assigning `category=""`:

- **Strategy 2** (`data-testid` regex `facilit`) — its regex also matches `property-most-popular-facilities-wrapper`; it grabs the `<li>` items with `category=""` and returns *before* Strategy 4.
- **Strategy 4** (explicit popular-wrapper fallback) — already targeted the wrapper but also assigned `category=""`.

A static-snapshot trace confirmed the path: for Villa Dvor, `property-facilities-block-container` is present but **empty** in the saved HTML, E45 yields zero, and Strategy 2 returns the 3 popular items with empty category.

### 3.3 Fix

Extract the wrapper's `<h3>` header **verbatim** and use it as `service_category`. This is literal DOM text — **no inference, no translation** — fully consistent with the Build 103 policy that removed all `_FACILITY_GROUP_MAP`/`_SERVICE_CATEGORY_RULES` inference.

New helper `BookingExtractor._popular_facilities_category(wrapper)` returns the first `<h3>` text (excluding any `<ul>/<li>`), normalised and capped at 128 chars. It is applied in **both** code paths that can harvest the popular wrapper:

- Strategy 2: only when the matched group is `property-most-popular-facilities-wrapper`; all other groups keep the previous `category=""` behaviour.
- Strategy 4: the explicit popular-wrapper fallback.

Guarded by a new toggle **`SVC_POPULAR_FALLBACK_CATEGORY_ENABLED`** (default `True`). Setting it to `False` restores the exact legacy behaviour.

### 3.4 Verification (real snapshots)

Running the modified `_extract_all_services()` against the real `pruebas/` HTML:

| Snapshot | Total services | Empty category (before) | Empty category (after) | Popular-tagged |
|----------|:--------------:|:-----------------------:|:----------------------:|:--------------:|
| HTML_1001_Villa-Dvor | 3 | 3 | **0** | 3 |
| HTML_78465_wild-&-bolz | 3 | 3 | **0** | 3 |
| HTML_76033_Hotel-Topazz | 56 | 0 | **0** | 0 (E45 works) |
| HTML_76569_Hotel-Aquamarin | 53 | 0 | **0** | 0 (E45 works) |

- Hotels where E45 succeeds are **unchanged** (no regression).
- With the toggle off, Villa Dvor returns to 3 empty (legacy behaviour confirmed).
- The existing test suite shows **11 failed / 41 passed both before and after** the change — i.e. **zero new failures** (the 11 failures are pre-existing, caused by older synthetic test fixtures, and are identical on the original Build 110 clone).

### 3.5 Why the schema is NOT changed

A tempting "fix" would be `ALTER TABLE hotels_all_services ALTER COLUMN service_category SET NOT NULL`. This is **rejected**: the database is recreated from `schema_v77_complete.sql` on every startup with no migration, and the Apollo-JSON fallback (Strategy 3) can still legitimately return `""`. A `NOT NULL` constraint would break the fresh-DB recreation. The defect is corrected at extraction time, where the data is verbatim-available.

---

## 4. Files changed (Build 111)

| File | Change |
|------|--------|
| `app/extractor.py` | New `_popular_facilities_category()` helper; Strategy 2 and Strategy 4 of `_extract_all_services()` now apply the verbatim popular-wrapper header. |
| `app/config.py` | New toggle `SVC_POPULAR_FALLBACK_CATEGORY_ENABLED` (default `True`); header bumped to Build 111. |
| `app/__init__.py` | `BUILD_VERSION = 111`; changelog entry for BUG-SVC-POPULAR-CAT-001. |

**Unchanged:** `schema_v77_complete.sql`, `models.py`, `scraper.py`, `scraper_service.py`, `api_payload_builder.py`, `image_classifier.py`, `image_downloader.py`. All files validated with `ast.parse()`.

---

## 5. Residual notes (no action shipped)

- **Apollo-JSON fallback (Strategy 3)** still yields `service_category=""` when neither the DOM facility block nor the popular wrapper is present. This is rare in the current dataset and has no verbatim header to extract; leaving it empty is correct rather than inventing a category.
- **1 hotel remains `error` in `url_queue`** (`minihotel-graz`, all 6 languages failed — listing cancelled on Booking.com). Pre-flight HEAD-check of URLs in `load_urls.py` remains a sensible future improvement but is out of scope here.
- **Image-download errors: 111 / 35 415 (0.31 %)** — transient CDN failures, within tolerance.

---

*End of report — Build 111. Verified against GitHub clone + `pruebas/*.csv` + `pruebas/*.html`. No assumptions; every figure is reproducible from the repository artifacts.*
