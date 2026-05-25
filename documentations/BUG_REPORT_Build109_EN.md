# BUG REPORT — Build 109
## Image Classification System — Gallery-Visible vs Non-Gallery
### BookingScraper Pro v6.0.0

**Repository:** `corralejo-htls/scrapv25` (read-only — no changes pushed)
**Date:** 2026-05-26
**Bug ID:** BUG-IMG-CLASS-001
**Schema source of truth:** `schema_v77_complete.sql` (DB is always dropped & recreated — **never** migrated)
**Verification:** GitHub clone succeeded; all code, CSV/HTML fixtures in `pruebas/`, and the two attached reports were reviewed against the actual source before any change.

---

## 0. Objectives Audit (the three required procedures)

| # | Required procedure | Met? | Where it happens | How to verify |
|---|--------------------|------|------------------|---------------|
| 1 | Gallery photos are **downloaded** AND **sent to the API** | ✅ | Download: `image_downloader.download_photo_batch()` queues every photo (gallery photos are appended by `PhotoClassifier`). Sent: `api_payload_builder._load_gallery_image_urls()` returns only `gallery_visible=TRUE` ∩ `image_downloads.status='done'`, ordered by `gallery_order`. | Audit SQL §6.1 |
| 2 | API data **matches what the original page shows** | ✅ | `API_IMAGES_GALLERY_ONLY=True` exports only the gallery subset, in `gallery_order`; `scraper_service` logs a **count reconciliation** (classified gallery vs `gallery_count_from_html` "+N photos" badge) to flag any mismatch. | Audit SQL §6.2 + per-hotel table §5 |
| 3 | Non-gallery photos are **downloaded and saved for future use** | ✅ | Same `download_photo_batch()` downloads ALL photos; `image_data` keeps `gallery_visible=FALSE` rows with a `subcategory`; they are **excluded** from the API payload. | Audit SQL §6.3 |

The rest of this report documents the evidence, the design and the validation behind that table.

---

## 1. Executive Summary

The production pipeline (committed at **Build 108**, not 106/103 as the mind map and the attached reports state) stores a **superset** of photos per hotel: every `id_photo` that carries an authenticated `k=` token anywhere in the page HTML. The public gallery — the set a visitor sees in the "see all photos" modal, validated by the user via `pruebas/extraer_imagenes.py` — is a **subset** of that superset.

Build 109 does **not discard** the surplus. It **classifies** every photo:

- `gallery_visible = TRUE` → downloaded **and** exported to the external API (`images[]`).
- `gallery_visible = FALSE` → downloaded **and** retained with a `subcategory`, but **not** exported.

Implemented coordinately across schema, ORM, extractor (scraper), persistence, orchestration, payload builder and configuration, plus a new module `app/image_classifier.py`.

---

## 2. Verified Findings (evidence-based, not inferred)

### 2.1 Current build is 108
`app/__init__.py` → `BUILD_VERSION = 108`. The mind map and both attached reports are stale. This delivery is **Build 109**. The guides referenced in the prompt URL (`Guide_Documentation_BookingScraper_EN.md`, `Guide_pruebas_folder_EN_.md`) **do not exist** in the repo; only `Strategy_E_Implementation_Guide_EN.md` is present.

### 2.2 Gallery identity is NOT derivable from page source
Grep over the **complete** HTML snapshots in `pruebas/` returned **0** occurrences of `gallery-grid-photo-action` and **0** of `GalleryGridViewModal`. The gallery grid is rendered only **after** the opener is clicked. Therefore *which* photos are gallery-visible cannot be read from the HTML the pipeline already has — it must be captured by opening the modal live, exactly as `extraer_imagenes.py` does.

(Note: `HTML_76033__Hotel-Topazz.html`, `HTML_76569__Hotel-Aquamarin.html`, `HTML_76924__haus-mobene-garni.html` are ~29 KB **partial** fragments — header "parte html de la pagina" — unusable for gallery analysis. The complete snapshots are Villa-Dvor, wild&bolz, arlberg, bruecklwirt, trofana.)

### 2.3 The "+N photos" badge yields the exact gallery COUNT (not identity)
`gallery_count = visible_hero_previews + N`. Verified exactly against ground truth: Villa Dvor 8+51=**59**; wild&bolz 8+14=**22**. Implemented as `gallery_count_from_html()` and used for **count reconciliation only** — it cannot identify which photos belong to the gallery, so it does not replace the live modal capture.

### 2.4 The superset source is confirmed
Villa Dvor: unique `id_photo` carrying a `k=` token across the whole HTML = **106** = DB `count_large_url`. The JS `hotelPhotos` array is capped at **45** (all with the generic alt "Gallery image of Villa Dvor in Ohrid"). The remainder comes from the `<img>`/JSON token scan in `extract_hotel_photos_from_html()`.

### 2.5 The legacy `_open_gallery()` is unsuitable
It clicks the **first hotel image** (single-photo viewer) and scrolls the whole page collecting any `bstatic` `<img>`; it never opens the grid modal, which is why `page_source` contains no grid buttons.

### 2.6 Alt-text subcategorization is overstated in the attached spec
The JS-array `alt` is generic, so alt-based subcategorization mostly yields `unknown`. The **reliable** signal is cross-referencing `id_photo` against `hotels_room_types.images` (JSONB). The functional test confirms it: of 47 non-gallery photos, only the 5 cross-referenced as room images were tagged `room`; the other 42 honestly remained `unknown`.

### 2.7 CRITICAL CORRECTION to the attached spec — no migration file
`Image_Classification_System_Spec_EN.md` proposes `migrations/v78_image_classification.sql`. This **contradicts the project architecture**: `schema_v77_complete.sql` states *"NUNCA es una migración"* and the DB is recreated on every startup. **No migration file was produced.** All schema changes were added **directly** to `schema_v77_complete.sql`.

---

## 3. Implemented Design (Build 109)

### 3.1 `app/image_classifier.py` (NEW)
- `GalleryModalExtractor(driver, cfg)` — opens the real grid modal (opener selectors → `GalleryGridViewModal-wrapper` → in-modal scroll 8×1.5 s → collect `button[data-testid^="gallery-grid-photo-action-"]`), deriving `id_photo` from `src` and building all 3 sizes from the shared `k=` token. Mirrors the user-validated `extraer_imagenes.py`. Fault-tolerant: returns `[]` on any failure.
- `NonGallerySubcategorizer(room_image_ids)` — precedence: room cross-ref → `room`; alt regex; dimension < 300 px → `thumbnail`; else `unknown`.
- `PhotoClassifier(driver, cfg)` — merges gallery set + dual-source superset; tags `gallery_visible/source/subcategory/gallery_order`; appends gallery-only photos missed by dual-source (guarantees gallery completeness → Objective 1).
- `gallery_count_from_html()` — the validated "+N photos" count formula (Objective 2 reconciliation).

### 3.2 `schema_v77_complete.sql`
Added to `image_data` (directly — no migration): `gallery_visible BOOLEAN NOT NULL DEFAULT FALSE`, `source VARCHAR(16) ... DEFAULT 'js_array'`, `subcategory VARCHAR(16) ... DEFAULT 'unknown'`, `gallery_order INTEGER NULL`, plus CHECKs, two indexes, and view `v_api_export_images` (gallery-visible ∩ done, ordered).

### 3.3 `app/models.py`
`ImageData` ORM gains the 4 columns with matching `CheckConstraint`s and two `Index` entries (mirrors the SQL).

### 3.4 `app/scraper.py`
- `_capture_gallery_modal(driver, url)` — opens the real grid, stores gallery photos in `self._gallery_photos_by_url[url]`.
- `take_gallery_photos(url)` — pops the per-URL result (race-safe under `SCRAPER_MAX_WORKERS > 1`).
- Invoked **only on the EN pass** (photos are language-independent), gated by `IMAGE_CLASSIFICATION_ENABLED`.

### 3.5 `app/scraper_service.py`
EN photo block runs `PhotoClassifier.classify_all()` with the live gallery set and `_collect_room_image_ids(extracted)`, then logs the **count reconciliation** (Objective 2). Classification failure degrades gracefully to unclassified download.

### 3.6 `app/image_downloader.py`
`_upsert_image_data()` persists `gallery_visible/source/subcategory/gallery_order`. Gallery wins: once TRUE, never downgraded. **All** photos (gallery + non-gallery) are downloaded → Objectives 1 & 3.

### 3.7 `app/api_payload_builder.py`
`images[]` returns **only** gallery-visible URLs, ordered by `gallery_order`, one URL per photo by size priority (highres > large > thumb). Safety net: if a hotel has no gallery photos, logs a warning and falls back to all `done` (never empty) → Objectives 1 & 2.

### 3.8 `app/config.py` + `env.example`
New toggles, documented in `env.example`: `IMAGE_CLASSIFICATION_ENABLED` (True), `API_IMAGES_GALLERY_ONLY` (True), `GALLERY_MODAL_TIMEOUT_S` (25), `GALLERY_MODAL_SCROLL_ITERATIONS` (8), `GALLERY_MODAL_SCROLL_PAUSE_S` (1.5).

### 3.9 `app/__init__.py`
`BUILD_VERSION = 109` + full changelog entry.

---

## 4. Validation Performed

- **`ast.parse()`** — all modified/new Python files pass.
- **ORM load** — `ImageData` maps the 4 new columns, 6 `chk_imgdata_*` constraints and 3 indexes; `source`/`subcategory` CHECK sets are identical across schema, ORM and `image_classifier.py`.
- **Module import** — `api_payload_builder` and `image_classifier` import cleanly.
- **Functional test against real `pruebas/` HTML** (no Selenium needed for the parsing path):

| Check | Result |
|---|---|
| `gallery_count_from_html` Villa Dvor | **59** (expected 59) ✅ |
| `gallery_count_from_html` wild&bolz | **22** (expected 22) ✅ |
| Superset built from HTML | **106** (expected 106) ✅ |
| Classified gallery_visible | **59** ✅ |
| Classified non-gallery | **47** ✅ |
| `room` via room cross-ref | **5** ✅ |
| Non-gallery left `unknown` (honest) | 42 |
| Every gallery photo has `gallery_order` + 3 sizes | ✅ |

Live modal behavior requires a pilot run on the Windows 11 host (Brave + ChromeDriver + NordVPN); Selenium cannot run in this audit environment.

---

## 5. Expected Counts per Audited Hotel (pilot acceptance criteria)

After the pilot run, `image_data` should show these `gallery_visible=TRUE` counts (must equal `_Calidad__images2.csv`). Non-gallery = superset − gallery, all downloaded and retained.

| external_ref | Hotel | Gallery (API) | Superset (DB) | Non-gallery (retained) |
|---|---|---|---|---|
| 1001 | Villa Dvor | 59 | 106 | 47 |
| 76033 | Hotel Topazz & Lamée | 38 | 56 | 18 |
| 76569 | Jagdhof / Aquamarin | 136 | 137 | 1 |
| 76924 | Haus Mobene Garni | 31 | 47 | 16 |
| 78465 | wild & bolz eMotel | 22 | 24 | 2 |

---

## 6. Verification SQL (audit of the three objectives)

### 6.1 Objective 1 — gallery photos downloaded AND exportable
```sql
-- Every gallery-visible photo must have at least one completed download.
SELECT i.hotel_id,
       COUNT(*)                                              AS gallery_photos,
       COUNT(*) FILTER (WHERE d.id_photo IS NOT NULL)        AS with_download
FROM image_data i
LEFT JOIN image_downloads d
       ON d.id_photo = i.id_photo
      AND d.hotel_id = i.hotel_id
      AND d.status = 'done'
WHERE i.gallery_visible = TRUE
GROUP BY i.hotel_id
HAVING COUNT(*) FILTER (WHERE d.id_photo IS NOT NULL) < COUNT(*);  -- 0 rows = OK
```

### 6.2 Objective 2 — API count matches the page (gallery), not the superset
```sql
-- API export count per hotel (what gets sent) — should equal _Calidad__images2.csv.
SELECT hotel_id, COUNT(DISTINCT id_photo) AS api_image_count
FROM v_api_export_images
GROUP BY hotel_id
ORDER BY hotel_id;
```

### 6.3 Objective 3 — non-gallery photos downloaded and saved for future use
```sql
-- Non-gallery inventory retained, by subcategory, with download coverage.
SELECT i.hotel_id, i.subcategory,
       COUNT(*)                                       AS photos,
       COUNT(*) FILTER (WHERE d.status = 'done')      AS downloaded
FROM image_data i
LEFT JOIN image_downloads d
       ON d.id_photo = i.id_photo AND d.hotel_id = i.hotel_id
WHERE i.gallery_visible = FALSE
GROUP BY i.hotel_id, i.subcategory
ORDER BY i.hotel_id, i.subcategory;
```

---

## 7. Risks & Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Gallery opener selectors drift | Empty gallery for some hotels | Multiple opener selectors + hero fallback; payload safety net; count reconciliation warning in logs |
| +~12–15 s per hotel (EN only) | Throughput | EN-pass only; reuses the existing live driver (no second browser, no extra VPN rotation) |
| Modal capture races (`MAX_WORKERS>1`) | Wrong gallery set | Per-URL storage + pop |
| Non-gallery mostly `unknown` | Limited future categorization | Documented honestly; room cross-ref reliable; richer subcategorization deferred |

**Rollback:** `IMAGE_CLASSIFICATION_ENABLED=false` + `API_IMAGES_GALLERY_ONLY=false` → legacy behavior. Zero data loss — the full superset still lands in `image_downloads`.

---

## 8. Windows 11 Deployment Notes
- DB recreated from `schema_v77_complete.sql` at startup — the 4 columns, 2 indexes and view exist from first boot; no migration step.
- Selenium/Brave + ChromeDriver already provisioned; the modal capture reuses that session — no new OS dependency.
- Pilot: run hotels 1001, 76033, 76569, 76924, 78465 and confirm §5 counts via §6 SQL before enabling `API_IMAGES_GALLERY_ONLY` in production.

---

## 9. Files Delivered (original names preserved)

```
Build109/
├── BUG_REPORT_Build109_EN.md
├── BUG_REPORT_Build109_ES.md
├── schema_v77_complete.sql            (schema source of truth — modified)
├── env.example                        (Build 109 toggles documented)
└── app/
    ├── __init__.py                    (BUILD_VERSION = 109 + changelog)
    ├── image_classifier.py            (NEW)
    ├── models.py
    ├── image_downloader.py
    ├── scraper.py
    ├── scraper_service.py
    ├── api_payload_builder.py
    └── config.py
```

*End of report — Build 109.*
