# ⚠️ CRITICAL UPDATE — Data Extraction Audit
## Hotel: wild & bolz eMotel (id_externo: 78465)
## Update Date: 2026-05-04

---

## 1. DEVASTATING FINDING: 86.7% of Services Missing

New evidence from the actual Booking.com page screenshot reveals that the scraper is extracting only **13.3%** of available services. This is a **critical data loss bug**.

| Metric | Value |
|--------|-------|
| Actual services on page | ~45 |
| Services in database (EN) | 6 |
| **Missing services** | **~39 (86.7%)** |
| Categories on page | 17 |
| Categories in database | 5 |
| **Missing categories** | **12 (70.6%)** |

---

## 2. What the Actual Page Shows (Screenshot Evidence)

The Booking.com page for wild & bolz eMotel displays **17 distinct categories** with **45+ individual items**:

### Categories Completely Missing from Database:

| Category | Items on Page | Items in DB | Status |
|----------|--------------|-------------|--------|
| **Great for your stay** | 10 (Parking, Private bathroom, Pets allowed, Free WiFi, Free parking, Non-smoking rooms, Flat-screen TV, Shower, Private parking, Lift) | 0 | ✗ MISSING |
| **Private bathroom** | 6 (Toilet paper, Towels, Private bathroom, Toilet, Hairdryer, Shower) | 0 | ✗ MISSING |
| **Bedroom** | 2 (Linen, Wardrobe or closet) | 0 | ✗ MISSING |
| **View** | 1 (Mountain view) | 0 | ✗ MISSING |
| **Room amenities** | 1 (Socket near the bed) | 0 | ✗ MISSING |
| **Pets** | 1 (Pets are allowed. Charges may be applicable.) | 0 | ✗ MISSING |
| **Living Area** | 2 (Seating Area, Desk) | 0 | ✗ MISSING |
| **Media & Technology** | 2 (Flat-screen TV, TV) | 0 | ✗ MISSING |
| **Free parking** | 2 (Electric vehicle charging station, Accessible parking) | 0 | ✗ MISSING |
| **Reception services** | 1 (Invoice provided) | 0 | ✗ MISSING |
| **Safety & security** | 5 (Fire extinguishers, CCTV outside property, CCTV in common areas, Smoke alarms, Key card access) | 0 | ✗ MISSING |
| **Accessibility** | 1 (Upper floors accessible by elevator) | 0 | ✗ MISSING |
| **Languages spoken** | 1 (German) | 0 | ✗ MISSING |

### Categories Partially Captured:

| Category | Items on Page | Items in DB | Missing |
|----------|--------------|-------------|---------|
| **Food & Drink** | 1 (Wine/champagne — Additional charge) | 1 (Wine/champagne) | ⚠️ Detail lost |
| **Internet** | 1 (WiFi is available in all areas and is free of charge.) | 1 (Internet services) | ⚠️ Detail lost |
| **Services** | 3 (Shared lounge/TV area, Vending machine (snacks), Vending machine (drinks)) | 2 (Vending machines only) | ⚠️ Missing 1 item |
| **General** | 5 (Non-smoking throughout, Hardwood or parquet floors, Heating, Lift, Non-smoking rooms) | 1 (Non-smoking rooms only) | ⚠️ Missing 4 items |

---

## 3. What the Database Actually Contains

### EN (English):
```
[Food & Drink]     Wine/champagne
[General]          Non-smoking rooms
[Internet]         Internet services
[Parking]          Parking
[Services]         Vending machine (snacks)
[Services]         Vending machine (drinks)
```
**Total: 6 services**

### ES (Spanish):
```
[Alimentos y bebidas]  Vino / champán
[Aparcamiento]         Parking
[General]              Habitaciones sin humo
[Internet]             Internet
[Servicios]            Máquina expendedora (aperitivos)
[Servicios]            Máquina expendedora (bebidas)
```
**Total: 6 services**

---

## 4. Root Cause: Scraping Wrong Page Section

**Hypothesis:** The scraper is extracting facilities from a **limited section** of the page (likely "Most popular facilities" or a summary widget) instead of the **full facilities block**.

**Evidence:**
1. Only 6 of 45+ services extracted (13.3% coverage)
2. The extracted services are "popular" items (WiFi, parking, vending machines)
3. Detailed room amenities, bathroom features, safety features are all missing
4. The full facility list is in `data-testid="property-facilities-block-container"` which contains 17 categories

**The scraper likely targets:**
- ❌ A limited "highlights" or "popular" section (only ~6 items)
- ❌ Misses the full `property-facilities-block-container` (45+ items)
- ❌ Misses categorized sections with headers like "Private bathroom", "Bedroom", "Safety & security"

---

## 5. Impact Assessment

| Impact Area | Severity | Description |
|-------------|----------|-------------|
| **Data completeness** | **CRITICAL** | 86.7% of facility data is missing |
| **API compatibility** | **CRITICAL** | API consumers expect full facility lists |
| **User experience** | **HIGH** | Guests cannot see full amenity information |
| **Competitive analysis** | **HIGH** | Missing safety, accessibility, room features |
| **Business intelligence** | **MEDIUM** | Incomplete data for analytics |

---

## 6. Updated Recommendations

### Immediate Actions (P0 — Fix Today)

| Action | Description |
|--------|-------------|
| **1. Fix selector target** | Change scraper to target `data-testid="property-facilities-block-container"` instead of limited "popular" section |
| **2. Extract all categories** | Capture all 17 category headers and their associated items |
| **3. Handle nested structure** | The full facility block has nested `<ul>`/`<li>` structures under category headers |
| **4. Re-scrape all hotels** | All previously scraped hotels likely have the same 86% data loss |

### Code Fix Required

The scraper must be updated to:
1. Find the full facilities container (`property-facilities-block-container`)
2. Iterate through all category sections (identified by `<h4>` or similar headers)
3. Extract ALL `<li>` items under each category
4. Store category name + item name for each facility

**Current behavior:** Extracts ~6 "popular" items
**Required behavior:** Extract all ~45 categorized items

---

## 7. Previous Assessment Was Wrong

The initial audit incorrectly concluded that wild & bolz eMotel was "complete" with 0% NULL categories. **This was misleading** — the real issue is that the scraper only captured 13.3% of the data. The "completeness" was an artifact of extracting from a limited section.

**Corrected assessment:**
- vidimo se: Extracted 18/18 services from limited section, but 61% NULL categories
- wild & bolz eMotel: Extracted 6/45 services from limited section, **86.7% data loss**

Both hotels suffer from the same root cause: **the scraper targets the wrong HTML section**.

---

## 8. Appendix: Full Expected vs Actual

### Expected (from Booking.com page):
```
Great for your stay:       Parking, Private bathroom, Pets allowed, Free WiFi, Free parking, Non-smoking rooms, Flat-screen TV, Shower, Private parking, Lift
Private bathroom:          Toilet paper, Towels, Private bathroom, Toilet, Hairdryer, Shower
Bedroom:                   Linen, Wardrobe or closet
View:                      Mountain view
Room amenities:            Socket near the bed
Pets:                      Pets are allowed. Charges may be applicable.
Living Area:               Seating Area, Desk
Media & Technology:        Flat-screen TV, TV
Food & Drink:              Wine/champagne (Additional charge)
Internet:                  WiFi is available in all areas and is free of charge.
Free parking:              Electric vehicle charging station, Accessible parking
Services:                  Shared lounge/TV area, Vending machine (snacks), Vending machine (drinks)
Reception services:        Invoice provided
Safety & security:         Fire extinguishers, CCTV outside property, CCTV in common areas, Smoke alarms, Key card access
General:                   Non-smoking throughout, Hardwood or parquet floors, Heating, Lift, Non-smoking rooms
Accessibility:             Upper floors accessible by elevator
Languages spoken:          German
```

### Actual (from Database):
```
Food & Drink:              Wine/champagne
General:                   Non-smoking rooms
Internet:                  Internet services
Parking:                   Parking
Services:                  Vending machine (snacks), Vending machine (drinks)
```

**Difference: 39 services missing**

---

*Critical Update generated: 2026-05-04*
*Evidence: Booking.com live page screenshot + category list*
