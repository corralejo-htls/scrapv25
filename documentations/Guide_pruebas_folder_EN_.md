# Pruebas Folder Guide

## Overview

The `pruebas` folder contains test data files used for development, debugging, and validation of the BookingScraper Pro application. These files are organized into two main categories: HTML source files downloaded from Booking.com and CSV exports of database tables.

---

## File Structure

### 1. HTML Source Files

All files in `pruebas/_HTML-view-source__*__.md` correspond to the HTML downloaded from Booking.com web pages, for tag review and data extraction.

**Naming Convention:**
```
_HTML-view-source__{hotel-name}_{language}_html__.md
```

**Pattern Breakdown:**
- `hotel-name`: URL-friendly hotel identifier (e.g., `centara-grand-lagoon-maldives`)
- `language`: Language code (e.g., `en-gb`, `es`, `de`, `it`)
- `html`: Indicates HTML content

**Example Files:**

| File | Hotel | Language |
|------|-------|----------|
| `_HTML-view-source__centara-grand-lagoon-maldives_de_html__.md` | Centara Grand Lagoon Maldives | German (de) |
| `_HTML-view-source__centara-grand-lagoon-maldives_en-gb_html__.md` | Centara Grand Lagoon Maldives | English GB (en-gb) |
| `_HTML-view-source__centara-grand-lagoon-maldives_es_html__.md` | Centara Grand Lagoon Maldives | Spanish (es) |
| `_HTML-view-source__centara-grand-lagoon-maldives_it_html__.md` | Centara Grand Lagoon Maldives | Italian (it) |
| `_HTML-view-source__garden-hill-resort-amp-spa_de_html__.md` | Garden Hill Resort & Spa | German (de) |
| `_HTML-view-source__garden-hill-resort-amp-spa_en-gb_html__.md` | Garden Hill Resort & Spa | English GB (en-gb) |
| `_HTML-view-source__garden-hill-resort-amp-spa_es_html__.md` | Garden Hill Resort & Spa | Spanish (es) |
| `_HTML-view-source__garden-hill-resort-amp-spa_it_html__.md` | Garden Hill Resort & Spa | Italian (it) |
| `_HTML-view-source__manaus-hoteis-millennium_en-gb_html__.md` | Manaus Hoteis Millennium | English GB (en-gb) |
| `_HTML-view-source__manaus-hoteis-millennium_es_html__.md` | Manaus Hoteis Millennium | Spanish (es) |
| `_HTML-view-source__the-pink-sands-club_de_html__.md` | The Pink Sands Club | German (de) |
| `_HTML-view-source__the-pink-sands-club_en-gb_html__.md` | The Pink Sands Club | English GB (en-gb) |
| `_HTML-view-source__the-pink-sands-club_es_html__.md` | The Pink Sands Club | Spanish (es) |
| `_HTML-view-source__the-pink-sands-club_it_html__.md` | The Pink Sands Club | Italian (it) |

**Purpose:**
- HTML structure analysis for extractor development
- XPath/CSS selector testing
- Data extraction validation
- Debugging scraping failures
- Language-specific content comparison

---

### 2. Database Table Exports (CSV)

All files in `pruebas/_table__*__.csv` correspond to the data in database tables with the same name.

**Naming Convention:**
```
_table__{table-name}__.csv
```

#### Core Hotel Data Tables

| CSV File | Database Table | Description |
|----------|----------------|-------------|
| `_table__hotels__.csv` | `hotels` | Core hotel information (name, address, rating, coordinates, etc.) |
| `_table__hotels_description__.csv` | `hotels_description` | Hotel descriptions in multiple languages |
| `_table__hotels_amenities__.csv` | `hotels_amenities` | Hotel amenities and facilities |
| `_table__hotels_policies__.csv` | `hotels_policies` | Hotel policies (check-in/out, cancellation, etc.) |
| `_table__hotels_legal__.csv` | `hotels_legal` | Legal information and disclaimers |
| `_table__hotels_fine_print__.csv` | `hotels_fine_print` | Additional terms and conditions |
| `_table__hotels_faqs__.csv` | `hotels_faqs` | Frequently asked questions |
| `_table__hotels_popular_services__.csv` | `hotels_popular_services` | Most popular services offered |
| `_table__hotels_all_services__.csv` | `hotels_all_services` | Complete list of all services |
| `_table__hotels_property_highlights__.csv` | `hotels_property_highlights` | Key property features and highlights |
| `_table__hotels_guest_reviews__.csv` | `hotels_guest_reviews` | Guest reviews and ratings |

#### Image Data Tables

| CSV File | Database Table | Description |
|----------|----------------|-------------|
| `_table__image_data__.csv` | `image_data` | Metadata for downloaded hotel images |
| `_table__image_downloads__.csv` | `image_downloads` | Download tracking and status for images |

#### Queue and Status Tables

| CSV File | Database Table | Description |
|----------|----------------|-------------|
| `_table__url_queue__.csv` | `url_queue` | URLs pending processing and their status |
| `_table__url_language_status__.csv` | `url_language_status` | Per-URL, per-language scraping status |

#### Logging and Monitoring Tables

| CSV File | Database Table | Description |
|----------|----------------|-------------|
| `_table__scraping_logs__.csv` | `scraping_logs` | Detailed scraping activity logs |
| `_table__scraping_logs_default__.csv` | `scraping_logs_default` | Default partition for scraping logs |
| `_table__system_metrics__.csv` | `system_metrics` | System performance metrics |

---

## Usage Examples

### Example 1: Finding Hotel Data

```python
import pandas as pd

# Load hotel data
hotels = pd.read_csv('pruebas/_table__hotels__.csv')

# Find a specific hotel
hotel = hotels[hotels['url_id'] == '3420c869-fd48-4f79-9557-5e185e9e580f']
```

### Example 2: Checking Language Status

```python
# Load language status
lang_status = pd.read_csv('pruebas/_table__url_language_status__.csv')

# Check which languages failed for a URL
failed = lang_status[
    (lang_status['url_id'] == '3420c869-fd48-4f79-9557-5e185e9e580f') &
    (lang_status['status'] == 'error')
]
```

### Example 3: Analyzing HTML Structure

```python
# Read HTML file for analysis
with open('pruebas/_HTML-view-source__centara-grand-lagoon-maldives_en-gb_html__.md', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Use with BeautifulSoup for parsing
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
```

---

## File Count Summary

| Category | Count |
|----------|-------|
| HTML Source Files | 14 |
| Database Table CSVs | 20 |
| **Total Files** | **34** |

---

## Notes

- HTML files are saved in Markdown format (`.md`) for easier viewing in GitHub
- CSV files are UTF-8 encoded and use comma as delimiter
- All files are test data and should not be used in production
- Files are periodically updated as the scraping system evolves
- The `pruebas` folder is excluded from production deployments
