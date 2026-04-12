# Image Download Analysis Report — Post Build 90
## Category Comparison: highres_url / large_url / thumb_url vs Manual Audit

**Date:** 2026-04-12  
**Scope:** 14 hotels · 3 download categories · Manual audit comparison  
**Data source:** `image_downloads` table query (attached `image_downloads.md`)  
**Build version:** BookingScraper Pro v6.0.0 Build 90

---

## EXECUTIVE SUMMARY

| Metric | Value | Status |
|--------|-------|--------|
| Total gallery photos (manual audit) | 1,369 | Reference baseline |
| **thumb_url** total | **1,369** | ✅ **Exact match** |
| **large_url** total | **1,639** | ⚠️ +270 extra (non-gallery property photos) |
| **highres_url** total | **607** | ℹ️ Capped at 45/hotel by design |
| Hotels where large = manual | 9/14 | ✅ |
| Hotels where large > manual | 5/14 | ⚠️ Extra non-gallery images |
| Hotels where large < manual | 0/14 | ✅ No deficits |

**Key finding:** `thumb_url` total equals `manual` total exactly (1,369 = 1,369). The `large_url` surplus of 270 comes from non-gallery property images (room photos, exterior shots) that have `large_url` but no `thumb_url` in the HTML.

---

## 1. COMPLETE COMPARISON TABLE

| Ref | Hotel | Manual | highres | large | thumb | L−M | L−H | L−T |
|-----|-------|:------:|:-------:|:-----:|:-----:|:---:|:---:|:---:|
| 1001 | Manaus Hotéis Millennium | 34 | 34 | 34 | 34 | 0 | 0 | 0 |
| 1002 | Colonna Park | 70 | 45 | **95** | 70 | **+25** | +50 | +25 |
| 1003 | Atlântico Rio | 57 | 45 | 57 | 57 | 0 | +12 | 0 |
| 1004 | Golden Beach Resort | 40 | 40 | 40 | 40 | 0 | 0 | 0 |
| 1005 | Garden Hill Resort | 96 | 45 | 96 | 96 | 0 | +51 | 0 |
| 1006 | CB Seychelles | 97 | 45 | 97 | 97 | 0 | +52 | 0 |
| 1007 | Hôtel Le Roy | 144 | 45 | 144 | 144 | 0 | +99 | 0 |
| 1008 | The Island Garden | 38 | 38 | 38 | 38 | 0 | 0 | 0 |
| 1009 | Grace Bay Club | 118 | 45 | **298** | 118 | **+180** | +253 | +180 |
| 1010 | South Bank | 266 | 45 | **273** | 266 | **+7** | +228 | +7 |
| 1011 | Pink Sands Club | 87 | 45 | 87 | 87 | 0 | +42 | 0 |
| 1012 | Niyama Private Islands | 131 | 45 | **142** | 131 | **+11** | +97 | +11 |
| 1013 | Centara Grand Lagoon | 132 | 45 | 132 | 132 | 0 | +87 | 0 |
| 1014 | Villa Dvor | 59 | 45 | **106** | 59 | **+47** | +61 | +47 |
| **TOTAL** | | **1,369** | **607** | **1,639** | **1,369** | **+270** | **+1,032** | **+270** |

**Legend:** L=large · M=manual · H=highres · T=thumb

---

## 2. INTER-CATEGORY DIFFERENCES

### 2.1 large_url vs highres_url — structural cap at 45

**Result: highres_url = min(45, gallery_count) for ALL 14 hotels**

```
highres_url only comes from the hotelPhotos JavaScript array in the static HTML.
Booking.com caps this array at ~45 entries server-side.
Build 90 extended large_url and thumb_url extraction via img tag scanning,
but highres_url (max1280x900) has no equivalent img tags in the static HTML.
```

| Observation | Hotels | Count |
|------------|--------|-------|
| highres = 45 (at cap) | 11 | CB Seychelles, Centara, Colonna, Garden Hill, Grace Bay, Hôtel Le Roy, Niyama, Pink Sands, South Bank, Villa Dvor, Atlântico Rio |
| highres < 45 (total gallery < 45) | 3 | Manaus (34), Island Garden (38), Golden Beach (40) |

**Conclusion:** `highres_url` count is structurally limited and does not represent total photo coverage. It is not a useful completeness metric.

### 2.2 large_url vs thumb_url — non-gallery photos

**5 hotels have `large_url > thumb_url`:**

| Ref | Hotel | large | thumb | Extra large-only | % Extra |
|-----|-------|:-----:|:-----:|:----------------:|:-------:|
| 1009 | Grace Bay Club | 298 | 118 | **180** | 153% |
| 1014 | Villa Dvor | 106 | 59 | **47** | 80% |
| 1002 | Colonna Park | 95 | 70 | **25** | 36% |
| 1012 | Niyama Private Islands | 142 | 131 | **11** | 8% |
| 1010 | South Bank | 273 | 266 | **7** | 3% |

These 270 extra `large_url`-only images are present in the HTML as `max1024x768` img tags but have **no corresponding `max200` (thumbnail) img tag**. They are property-level images embedded in room description blocks, facilities sections, or other non-gallery page elements.

**Important:** `thumb_url` total = 1,369 = manual gallery total. This confirms `thumb_url` is the accurate gallery photo count.

### 2.3 large_url vs manual audit

**9 hotels match exactly, 5 have surplus, 0 have deficit:**

| Category | Hotels | Description |
|----------|--------|-------------|
| ✅ large = manual | 9/14 | Exact match — all gallery photos present |
| ⚠️ large > manual | 5/14 | Scraper found extra non-gallery images |
| ❌ large < manual | 0/14 | No hotel has a download deficit |

---

## 3. HOTEL CLASSIFICATION

### Category A — All three categories equal (3 hotels)
`highres = large = thumb = manual` — hotels with ≤40 total photos; all fit within the 45-photo hotelPhotos JS cap.

| Ref | Hotel | Count |
|-----|-------|:-----:|
| 1001 | Manaus Hotéis Millennium | 34 |
| 1004 | Golden Beach Resort | 40 |
| 1008 | The Island Garden | 38 |

### Category B — highres capped, large = thumb = manual (7 hotels)
Gallery photos all downloaded. `highres_url` at 45 cap because gallery > 45.

| Ref | Hotel | manual | large | highres |
|-----|-------|:------:|:-----:|:-------:|
| 1003 | Atlântico Rio | 57 | 57 | 45 |
| 1005 | Garden Hill Resort | 96 | 96 | 45 |
| 1006 | CB Seychelles | 97 | 97 | 45 |
| 1007 | Hôtel Le Roy | 144 | 144 | 45 |
| 1011 | Pink Sands Club | 87 | 87 | 45 |
| 1013 | Centara Grand Lagoon | 132 | 132 | 45 |

### Category C — large > manual (extra non-gallery images) (5 hotels)

| Ref | Hotel | manual | large | thumb | Extra |
|-----|-------|:------:|:-----:|:-----:|:-----:|
| 1002 | Colonna Park | 70 | 95 | 70 | **+25** |
| 1009 | Grace Bay Club | 118 | 298 | 118 | **+180** |
| 1010 | South Bank | 266 | 273 | 266 | **+7** |
| 1012 | Niyama Private Islands | 131 | 142 | 131 | **+11** |
| 1014 | Villa Dvor | 59 | 106 | 59 | **+47** |

---

## 4. ROOT CAUSE OF large > thumb DISCREPANCY

The Build 90 supplement extraction scans **all** `max1024x768` img URLs in the HTML:

```python
large_pattern = re.compile(
    r'https://cf\.bstatic\.com/xdata/images/hotel/max1024x768/'
    r'(\d+)\.jpg\?k=([^"\'&\\\s]+)'
)
```

This correctly captures **every** `max1024x768` image in the page — including images embedded in:
- Room type blocks (`hotels_room_types` data)
- Facilities photo widgets
- Promotional/featured property images

These images have `large_url` (1024×768) but no `thumb_url` (max200), as Booking.com only provides thumbnails for main gallery photos.

**This is correct behaviour.** The `large_url` count being higher than manual is not a bug — it means the system is capturing more property media than the manual gallery count. The `thumb_url` count is the precise gallery photo count.

---

## 5. API PAYLOAD IMPACT

For the `images` field in the API payload (`_API_.md`), the current `api_payload_builder.py` uses `image_downloads` to populate the array. All three sizes are available; the payload should use `large_url` or `highres_url` as the primary image URL.

**Recommendation:** use `highres_url` where available (first 45 photos, highest quality), fall back to `large_url` for the remaining gallery photos. Filter out `large_url`-only photos without `thumb_url` if gallery-only coverage is required.

---

## 6. VERIFICATION SQL

```sql
-- Identify large_url-only photos (no corresponding thumb_url)
SELECT 
    h.hotel_name,
    COUNT(*) AS large_only_photos
FROM image_downloads id_l
JOIN hotels h ON h.id = id_l.hotel_id AND h.language = 'en'
WHERE id_l.category = 'large_url'
AND NOT EXISTS (
    SELECT 1 FROM image_downloads id_t
    WHERE id_t.hotel_id = id_l.hotel_id
    AND id_t.id_photo = id_l.id_photo
    AND id_t.category = 'thumb_url'
)
GROUP BY h.hotel_name
ORDER BY large_only_photos DESC;

-- Category completeness matrix
SELECT
    h.hotel_name,
    COUNT(CASE WHEN id.category = 'highres_url' THEN 1 END) AS highres,
    COUNT(CASE WHEN id.category = 'large_url'   THEN 1 END) AS large,
    COUNT(CASE WHEN id.category = 'thumb_url'   THEN 1 END) AS thumb
FROM hotels h
JOIN image_downloads id ON id.hotel_id = h.id
WHERE h.language = 'en'
GROUP BY h.hotel_name
ORDER BY h.hotel_name;
```

---

## 7. CONCLUSIONS

1. **`thumb_url` = gallery count = manual audit** — exact match (1,369 total). This is the correct gallery completeness metric.

2. **`highres_url` is structurally capped at 45** per hotel (server-side JS limitation). Not a useful completeness indicator.

3. **`large_url > manual` for 5 hotels** — not a bug. The scraper is capturing additional non-gallery property images (room photos, etc.) that are not counted in the manual gallery audit.

4. **No hotel has a download deficit** (`large_url < manual` in 0 of 14 hotels). Build 90 fix fully resolved the 44.3% completion issue.

5. **The `thumb_url` count is the recommended completeness metric** for API payload image coverage reporting.

---

*Report generated: 2026-04-12 · BookingScraper Pro v6.0.0 Build 90*
