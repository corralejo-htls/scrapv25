# SCRAPV25 — BookingScraper Pro

## State-Aware Multilingual Scraping System (Strategy E)

**Repository:** https://github.com/corralejo-htls/scrapv25  
**Version:** v6.0.0 Build 58+  
**Core Concept:** Data Integrity First  
**Architecture:** Python + Celery + Redis/Memurai + SQL + Selenium  
**Architecture Style:** Hybrid (Service + Script-based + Automation Layer)
**Schema Source of Truth:** https://github.com/corralejo-htls/scrapv25/blob/main/schema_v77_complete.sql
**repository file listings:** https://github.com/corralejo-htls/scrapv25/blob/main/documentations/_path-file.csv
**File listings in Windows:** https://github.com/corralejo-htls/scrapv25/blob/main/pruebas/_arbol_.csv

---

# 1. Overview

SCRAPV25 is a distributed scraping system designed to extract structured hotel data from Booking.com across multiple languages.

It is built around **data integrity, retry intelligence, and partial failure recovery**.

The system ensures:

- Multilingual scraping (EN / ES / DE / IT)
- Distributed execution (Celery + scripts)
- State tracking per language
- Partial retry capability
- Zero silent data loss

---

# 2. Core Principle — Strategy E

## Problem Solved

Before Strategy E:
- URLs were marked as `done` even with incomplete language data
- This caused:
  - false completion metrics
  - incomplete datasets
  - silent corruption of analytics

---

## Strategy E Rule

A URL is considered **DONE only if:**

```
ALL languages succeed (EN + ES + DE + IT)
```

Otherwise:
| Condition | System Status | Behavior |
|----------|---------------|----------|
| 4/4 languages OK | DONE | Complete success |
| 1–3/4 languages OK | ERROR | Data preserved |
| 0/4 languages OK | ERROR | Full cleanup |

---

## Key Design Rule
> Never lose valid scraped data

---

# 3. Real System Architecture
```text
URL Queue (DB)
      ↓
app/scraper_service.py
      ↓
Language Processing Engine
      ↓
ChromeDriver (Browser Automation)
      ↓
Booking.com Extraction Layer
      ↓
Database Storage (SQL)
      ↓
Strategy E Validation Layer
      ↓
Retry System (scripts/retry_incomplete.py)
```

---
# 4. Real Repository Structure

## 4.1 Root Level

```text
.gitignore
alembic.ini
config.ini
env.example
languages.json

requirements.txt
requirements-optional.txt

schema_v77_complete.sql

dump.rdb
memurai.conf

windows_service.py
install_chromedriver_helper.py
```

---

## 4.2 Windows Automation Scripts

```text
start_server.bat
stop_server.bat
restart_all.bat

start_celery.bat
start_celery_beat.bat
stop_celery.bat

start_redis.bat

backup_db.bat
create_db.bat
export_data.bat

cleanup_logs.bat
limpiar_cache.bat

verify_system.bat
verify_memurai.bat
show_status.bat
diagnostico_vpn.bat
```

---

## 4.3 Application Core (app/)

The real system logic lives here:

```text
app/
```

### Core modules

- config.py → system configuration
- database.py → DB connection layer
- logger.py → logging system
- windows_service.py → Windows integration

---

### Scraper Engine (CORE)

```text
app/scraper_service.py
```

Responsible for:

- URL processing
- language iteration
- scraping execution
- state management
- Strategy E decision logic

---

### Models Layer

```text
app/models/
```

Entities include:

- url_queue
- hotel
- url_language_status
- hotel_amenities
- hotel_description
- hotel_policy
- hotel_legal
- hotel_fine_print
- hotel_property_highlights
- hotel_guest_review

---

### Services Layer

```text
app/services/
```

Includes:

- scraper_service.py
- retry_service.py
- validation_service.py
- celery_tasks.py

---

### Repositories Layer

```text
app/repositories/
```

Data access abstraction layer (DAO pattern)

---

# 5. Documentation

```text
documentations/
```

Includes:

- Strategy_E_Implementation_Guide_EN.md
- _path-file.csv

---

# 6. Testing & Analysis

```text
pruebas/
```

Contains:

- _arbol_.csv (real repository structure index)

---

# 7. Scripts Layer

```text
scripts/
```

Includes:

- retry_incomplete.py
- integrity_audit.py
- cleanup utilities

---

# 8. Data Model

A URL is valid only when:

```
hotels_records == 4 (one per language)
```

Expected languages:

- EN
- ES
- DE
- IT

---

# 9. Retry System

## Partial Retry

If some languages fail:

```
EN ❌
ES ✅
DE ❌
IT ❌
```

Only failed languages are retried.

---

## Full Retry

If all languages fail:

- Full reprocessing required
- Previous data is cleaned

---

# 10. System Characteristics

- Hybrid architecture (not strictly layered)
- Service-oriented scraping engine
- Batch-driven automation (Windows scripts)
- Strong dependency on scraper_service.py
- External orchestration via Celery + Redis/Memurai

---

