# SCRAPV25 — BookingScraper Pro

## Multilingual Hotel Scraping Platform (Strategy E)

**Repository:** https://github.com/corralejo-htls/scrapv25  
**Version:** v6.0.0 Build 58+  
**Language:** Python  
**Architecture:** Distributed Scraping + Task Queue + Integrity System  
**Source of truth:** https://github.com/corralejo-htls/scrapv25/blob/main/schema_v77_complete.sql
**repository file listings:** https://github.com/corralejo-htls/scrapv25/blob/main/documentations/_path-file.md
# Overview

SCRAPV25 is a distributed web scraping system designed to extract structured hotel data from Booking.com across multiple languages.

The system is built to ensure **data integrity, completeness, and recoverability**, even under partial failures.

It supports:

- Multilingual scraping (EN / ES / DE / IT)
- Distributed task execution with Celery
- Browser automation via ChromeDriver
- Redis/Memurai message broker
- SQL persistence layer
- Intelligent retry system
- Data integrity validation (Strategy E)

---

# Key Feature: Strategy E

## Enhanced State with Conditional Commit

Strategy E is the core improvement of the system.

### Problem it solves

Previously, URLs were marked as `done` even when:

- Only some languages succeeded
- Others failed silently
- Data was partially missing

This caused:

- False completion metrics
- Incomplete datasets
- Silent data corruption

---

## Strategy E Rules

### Completion logic

A URL is only marked as:

```
DONE
```

when:

```
All languages (EN, ES, DE, IT) succeed
```

---

### Partial success handling

If only some languages succeed:

```
STATUS = ERROR (but data is preserved)
```

- Successful languages are kept
- Failed languages are marked for retry
- No data is deleted

---

### Total failure handling

If all languages fail:

```
STATUS = ERROR
→ Full cleanup
→ Full retry required
```

---

### Retry logic

- Retry ONLY failed languages
- Never re-scrape successful ones
- Reduce bandwidth and processing time

---

# Architecture

## High-Level Flow

```text
URL Queue
   ↓
Scraper Service
   ↓
Language Engine (EN / ES / DE / IT)
   ↓
ChromeDriver
   ↓
Booking.com
   ↓
Data Extraction
   ↓
SQL Database
   ↓
Integrity Validation (Strategy E)
   ↓
Retry Engine (if needed)
```

---

## System Components

### Core Services

- Scraper Service (orchestration)
- Language Processor
- Retry Engine
- Validation Engine

---

### Infrastructure

- Celery (task queue)
- Redis / Memurai (broker)
- ChromeDriver (browser automation)
- SQL Database (storage)
- Alembic (migrations)

---

# Data Model

## URL Lifecycle

```text
pending → processing → done / error
```

---

## Language Tracking

Table: `url_language_status`

| Language | Status |
|----------|--------|
| en | done / error |
| es | done / error |
| de | done / error |
| it | done / error |

---

## Hotel Data

Each URL produces:

- hotels
- hotel_descriptions
- hotel_amenities
- hotel_policies
- hotel_legal
- hotel_fine_print
- hotel_property_highlights
- hotel_guest_reviews

Each record is language-specific.

---

# Integrity Model

A URL is considered valid only if:

```
number_of_hotel_records == number_of_enabled_languages
```

Expected:

```
4 languages → 4 records per URL
```

---

## Integrity Check

```sql
SELECT url_id, COUNT(*)
FROM hotels
GROUP BY url_id;
```

---

# Retry System

## Partial Retry

Used when:

- Some languages succeeded
- Some failed

Behavior:

- Retry only missing languages
- Preserve existing data

---

## Full Retry

Used when:

- All languages failed

Behavior:

- Clean previous data
- Retry all languages

---

# Repository Structure

## Root Files

```text
alembic.ini
config.ini
env.example
requirements.txt
requirements-optional.txt

schema_v77_complete.sql

windows_service.py

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
```

---

## Application Layer

```text
app/
├── config.py
├── database.py
├── scraper_service.py
├── logger.py
├── models/
│   ├── url_queue.py
│   ├── hotel.py
│   ├── url_language_status.py
│   ├── hotel_amenities.py
│   ├── hotel_description.py
│   ├── hotel_policy.py
│   └── ...
├── services/
│   ├── scraper_service.py
│   ├── retry_service.py
│   └── validation_service.py
└── repositories/
```

---

## Scripts

```text
scripts/
├── retry_incomplete.py
├── integrity_audit.py
├── cleanup_jobs.py
```

---

## Tests

```text
tests/
├── test_strategy_e.py
├── test_scraper_service.py
├── test_retry_system.py
├── test_integrity.py
```

---

## Documentation

```text
documentations/
├── Strategy_E_Implementation_Guide_EN.md
├── architecture_overview.md
```

---

# Monitoring

The system tracks:

- Completed URLs
- Partial failures
- Total failures
- Integrity score
- Retry efficiency

---

# Technology Stack

- Python
- Celery
- Redis / Memurai
- Selenium / ChromeDriver
- SQL Database
- Alembic
- Windows batch automation

---

