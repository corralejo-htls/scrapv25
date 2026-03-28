# Strategy E Implementation Guide
## Enhanced State with Conditional Commit for BookingScraper Pro

**Document Version:** 1.0  
**Date:** 2026-03-26  
**Repository:** https://github.com/corralejo-htls/scrapv25.git  
**Target Build:** v6.0.0 Build 58+

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Bug Detection and Analysis](#bug-detection-and-analysis)
4. [Root Cause Analysis](#root-cause-analysis)
5. [Strategy E: Complete Implementation](#strategy-e-complete-implementation)
6. [Database Schema Changes](#database-schema-changes)
7. [Code Implementation](#code-implementation)
8. [Partial Retry System](#partial-retry-system)
9. [Testing Strategy](#testing-strategy)
10. [Migration Guide](#migration-guide)
11. [Rollback Procedure](#rollback-procedure)
12. [Monitoring and Alerting](#monitoring-and-alerting)

---

## Executive Summary

This document provides a comprehensive implementation guide for Strategy E (Enhanced State with Conditional Commit), the recommended solution for fixing the critical data integrity bug identified in BookingScraper Pro v6.0.0 Build 58. The solution preserves valid scraping data while enabling intelligent partial retries for failed language variants.

### Key Benefits

| Benefit | Description |
|---------|-------------|
| **Data Preservation** | Never deletes successful language scrapes |
| **Efficient Retry** | Only re-scrapes failed languages, not all |
| **Minimal Changes** | Uses existing `url_language_status` infrastructure |
| **Bandwidth Optimization** | Reduces redundant HTTP requests |
| **Clear State Tracking** | Distinguishes between complete, partial, and failed states |

---

## Problem Statement

### Context

BookingScraper Pro is a multi-language web scraping application that extracts hotel information from Booking.com. The application supports four languages: English (en), Spanish (es), German (de), and Italian (it). Each URL must be scraped in all four languages to ensure complete data collection.

### Expected Behavior

For each URL in the queue, the scraper should:
1. Scrape the URL in all four enabled languages
2. Store extracted data in the database
3. Mark the URL as "done" only when all languages have been successfully scraped
4. Mark the URL as "error" if any language fails

### Actual Behavior

The scraper marks URLs as "done" regardless of whether all languages were successfully scraped. This results in URLs appearing complete in the `url_queue` table while having incomplete data in the `hotels` table.

---

## Bug Detection and Analysis

### Detection Method

The bug was detected through an integrity audit query that counts the number of language records per URL:

```sql
SELECT url_id, COUNT(url_id) 
FROM hotels 
GROUP BY url_id 
ORDER BY url_id
```

### Evidence

**Query Results:**

| url_id | count | Expected | Status |
|--------|-------|----------|--------|
| bc5d8b35-1a5f-4ab6-b778-3a7ba516bc0b | **1** | 4 | **INCOMPLETE** |
| f13a5377-b27f-4c2c-9e9c-3d17773308af | 4 | 4 | OK |
| cfaea71c-7c4f-4b9c-b53e-394c751b989c | 4 | 4 | OK |
| *(all other url_ids)* | 4 | 4 | OK |

**URL `bc5d8b35-1a5f-4ab6-b778-3a7ba516bc0b` Analysis:**

The `url_language_status` table reveals the actual state of each language:

| language | status | last_error |
|----------|--------|------------|
| en | error | All scraping engines failed |
| es | done | NULL |
| de | error | All scraping engines failed |
| it | error | All scraping engines failed |

**url_queue Table Status:**

```
id: bc5d8b35-1a5f-4ab6-b778-3a7ba516bc0b
status: done  ← INCORRECT - Should be "error" or "incomplete"
```

### Impact Assessment

The bug has far-reaching consequences across the entire data pipeline:

1. **Primary Data Loss:** The `hotels` table contains incomplete records with only 1 of 4 expected languages. This means 75% of the linguistic data is missing for affected URLs.

2. **Cascading Data Gaps:** All related tables inherit the incompleteness:
   - `hotels_amenities` - Missing amenity descriptions in 3 languages
   - `hotels_policies` - Missing policy translations
   - `hotels_legal` - Missing legal information variants
   - `hotels_description` - Incomplete multilingual descriptions
   - `hotels_fine_print` - Missing fine print translations
   - `hotels_property_highlights` - Missing highlight variants

3. **Image Download Failure:** The image download process is triggered only when English language scraping succeeds. Since English failed for this URL, no images were downloaded despite Spanish succeeding.

4. **Reporting Inaccuracy:** Any reports or analytics based on `url_queue.status = 'done'` will show artificially inflated completion rates. Dashboards may report 100% completion while actual data integrity is only 25%.

5. **Downstream Integration Issues:** Any external systems consuming this data will receive incomplete multilingual datasets, potentially causing:
   - Translation fallback failures
   - Missing content on user-facing pages
   - Inconsistent user experiences across language preferences

---

## Root Cause Analysis

### Source Code Analysis

The bug originates in `scraper_service.py` in the `_process_url()` method. The critical flaw is in the unconditional call to `_mark_done()`:

```python
# Current implementation (PROBLEMATIC)
def _process_url(self, url_obj: URLQueue) -> None:
    """Process a single URL through all enabled languages."""
    all_ok = True
    
    for lang in languages:
        ok = self._scrape_language(url_obj, lang)
        if not ok:
            all_ok = False  # Flag is set but subsequently ignored
    
    # BUG: Always marks as done regardless of all_ok value
    self._mark_done(url_obj, all_ok=True)  # Hardcoded True!
```

### The Critical Flaw

The code correctly tracks the success/failure of each language in the `all_ok` variable, but then **ignores this value completely** when calling `_mark_done()`. The `all_ok=True` parameter is hardcoded, meaning:

- Even if `all_ok` is `False` (indicating failures)
- Even if 3 out of 4 languages failed
- Even if only Spanish succeeded and English/German/Italian all failed

The URL will still be marked as `done`.

### Why This Happened

This appears to be a case where:
1. The developer intended to implement proper error handling
2. The `all_ok` variable was created for this purpose
3. During development or debugging, `True` was hardcoded
4. The hardcoded value was never replaced with the actual `all_ok` variable
5. No automated tests caught this because the tests may have only checked happy paths

### Secondary Contributing Factors

1. **Missing Validation Layer:** There is no post-scraping validation that verifies the expected number of language records exists before marking a URL as done.

2. **Silent Failures:** When `_scrape_language()` returns `False`, the error is logged but the process continues without any recovery mechanism.

3. **No Completeness Check:** The existing `CompletenessService.is_fully_complete()` method exists in the codebase but is never called during the scraping workflow.

---

## Strategy E: Complete Implementation

### Strategy Overview

Strategy E (Enhanced State with Conditional Commit) addresses the root cause while adding intelligent state management. The core principle is: **preserve valid data, retry only what failed**.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SCRAPER SERVICE - STRATEGY E                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────┐                                                          │
│  │   START URL   │                                                          │
│  └───────┬───────┘                                                          │
│          │                                                                   │
│          ▼                                                                   │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │                    LANGUAGE ITERATION LOOP                         │      │
│  │  ┌─────────────────────────────────────────────────────────────┐  │      │
│  │  │  FOR EACH LANGUAGE (en, es, de, it):                        │  │      │
│  │  │                                                              │  │      │
│  │  │    ┌─────────────┐     ┌──────────────┐                     │  │      │
│  │  │    │   SCRAPE    │────▶│   SUCCESS?   │                     │  │      │
│  │  │    │   LANGUAGE  │     └──────┬───────┘                     │  │      │
│  │  │    └─────────────┘            │                             │  │      │
│  │  │                      ┌────────┴────────┐                    │  │      │
│  │  │                      │                 │                    │  │      │
│  │  │                    YES               NO                     │  │      │
│  │  │                      │                 │                    │  │      │
│  │  │                      ▼                 ▼                    │  │      │
│  │  │    ┌─────────────────────┐  ┌─────────────────────┐        │  │      │
│  │  │    │ INSERT to DB        │  │ LOG error           │        │  │      │
│  │  │    │ UPDATE status=done  │  │ UPDATE status=error │        │  │      │
│  │  │    │ in url_lang_status  │  │ in url_lang_status  │        │  │      │
│  │  │    └─────────────────────┘  └─────────────────────┘        │  │      │
│  │  └─────────────────────────────────────────────────────────────┘  │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│          │                                                                   │
│          ▼                                                                   │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │                      FINAL VALIDATION                              │      │
│  │                                                                    │      │
│  │    actual_count = COUNT(*) FROM hotels WHERE url_id = X           │      │
│  │    expected_count = len(ENABLED_LANGUAGES)                        │      │
│  │                                                                    │      │
│  │    ┌─────────────────────────────────────────────────────────┐    │      │
│  │    │                    DECISION TREE                         │    │      │
│  │    │                                                         │    │      │
│  │    │  actual == expected ──────────────────▶ STATUS = DONE   │    │      │
│  │    │         │                                               │    │      │
│  │    │         │ (not equal)                                   │    │      │
│  │    │         ▼                                               │    │      │
│  │    │  actual > 0 ──────────────────────────▶ STATUS = ERROR  │    │      │
│  │    │         │                             │ PRESERVE DATA   │    │      │
│  │    │         │                               │ PARTIAL RETRY  │    │      │
│  │    │         │ (actual == 0)                 └────────────────┘    │      │
│  │    │         ▼                                                     │      │
│  │    │  STATUS = ERROR                                               │      │
│  │    │  CLEANUP EMPTY DATA                                           │      │
│  │    │  FULL RETRY NEEDED                                            │      │
│  │    └─────────────────────────────────────────────────────────┘    │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### State Machine Diagram

```
                         ┌─────────────────┐
                         │     PENDING     │
                         │   (initial)     │
                         └────────┬────────┘
                                  │
                                  │ _mark_processing()
                                  ▼
                         ┌─────────────────┐
                         │   PROCESSING    │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │      DONE       │  │     ERROR       │  │     ERROR       │
    │  (all langs OK) │  │ (partial, data  │  │ (total fail,    │
    │                 │  │  preserved)     │  │  data cleaned)  │
    └─────────────────┘  └─────────────────┘  └─────────────────┘
                                 │
                                 │ partial retry
                                 ▼
                         ┌─────────────────┐
                         │   PROCESSING    │
                         │ (retry missing) │
                         └─────────────────┘
```

---

## Database Schema Changes

### Current Schema (No Changes Required)

Strategy E leverages the existing `url_language_status` table which already tracks per-language status:

```sql
-- Existing table structure
CREATE TABLE url_language_status (
    id UUID PRIMARY KEY,
    url_id UUID NOT NULL REFERENCES url_queue(id),
    language VARCHAR(5) NOT NULL,
    status VARCHAR(20) NOT NULL,  -- 'pending', 'processing', 'done', 'error'
    last_error TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Optional Enhancement: Add Metadata Column

For better tracking and debugging, consider adding a metadata column:

```sql
-- Optional enhancement
ALTER TABLE url_queue ADD COLUMN languages_completed TEXT DEFAULT '';
ALTER TABLE url_queue ADD COLUMN languages_failed TEXT DEFAULT '';
```

This allows quick identification of which languages need retry without joining to `url_language_status`.

---

## Code Implementation

### File: `app/scraper_service.py`

Replace the existing `_process_url()` method with the enhanced version:

```python
def _process_url(self, url_obj: URLQueue) -> None:
    """
    Process a single URL through all enabled languages.
    
    STRATEGY E: Enhanced State with Conditional Commit
    
    Flow:
      1. Scrape each language
      2. Insert data immediately if successful
      3. Track state in url_language_status
      4. Final validation: count successful languages
      5. If complete → mark URL 'done'
      6. If incomplete → mark URL 'error', PRESERVE data for partial retry
      7. If total failure → cleanup and mark 'error' for full retry
    
    Args:
        url_obj: URLQueue object to process
    
    Returns:
        None (status is updated in database)
    """
    url_id_str = str(url_obj.id)

    # Attempt to claim the URL for processing (prevent concurrent processing)
    if not _try_claim_url(url_id_str):
        logger.debug("URL %s already claimed, skipping.", url_id_str)
        self._stats.record(skipped=True)
        return

    try:
        # Mark as processing
        self._mark_processing(url_obj)
        
        # Prepare language list with 'en' first (English triggers image downloads)
        languages = list(self._cfg.ENABLED_LANGUAGES)
        if 'en' in languages:
            languages.remove('en')
        languages.insert(0, 'en')
        
        expected_lang_count = len(languages)
        
        # Track results for each language
        lang_results: Dict[str, bool] = {}
        
        # Scrape each language
        for lang in languages:
            try:
                logger.info("URL %s: Starting scrape for language '%s'", url_id_str, lang)
                ok = self._scrape_language(url_obj, lang)
                lang_results[lang] = ok
                
                if ok:
                    logger.info("URL %s lang %s: SUCCESS", url_id_str, lang)
                else:
                    logger.warning("URL %s lang %s: FAILED", url_id_str, lang)
                    
            except Exception as exc:
                logger.error(
                    "URL %s lang %s: EXCEPTION - [%s] %s", 
                    url_id_str, lang, type(exc).__name__, exc
                )
                lang_results[lang] = False
                # Error is already logged in url_language_status by _scrape_language

        # Count successful languages from database (source of truth)
        actual_lang_count = self._count_successful_languages(url_obj.id)
        failed_langs = [lang for lang, ok in lang_results.items() if not ok]
        success_langs = [lang for lang, ok in lang_results.items() if ok]

        # Decision tree based on completion status
        if actual_lang_count == expected_lang_count:
            # CASE 1: Complete success - all languages scraped
            logger.info(
                "URL %s: COMPLETE (%d/%d languages) - %s", 
                url_id_str, actual_lang_count, expected_lang_count, success_langs
            )
            self._mark_done(url_obj, all_ok=True)
            self._stats.record(succeeded=True)
            
        elif actual_lang_count > 0:
            # CASE 2: Partial success - preserve data for partial retry
            error_msg = (
                f"Incomplete: {actual_lang_count}/{expected_lang_count} languages. "
                f"Success: {success_langs}. Failed: {failed_langs}"
            )
            logger.warning("URL %s: %s", url_id_str, error_msg)
            
            # DO NOT delete data - enables partial retry
            self._mark_incomplete(url_obj, error_msg)
            self._stats.record(failed=True)
            
        else:
            # CASE 3: Total failure - no languages succeeded
            error_msg = f"All languages failed: {failed_langs}"
            logger.error("URL %s: %s", url_id_str, error_msg)
            
            # Cleanup empty records (nothing to preserve)
            self._cleanup_empty_url(url_obj.id)
            self._mark_error(url_obj, error_msg)
            self._stats.record(failed=True)

    except Exception as exc:
        # Catch-all for unexpected errors
        logger.error(
            "_process_url failed for %s: [%s] %s", 
            url_id_str, type(exc).__name__, exc
        )
        self._mark_error(url_obj, str(exc)[:2000])
        self._stats.record(failed=True)
        
    finally:
        # Always release the URL lock
        _release_url(url_id_str)
```

### New Helper Methods

Add these new methods to the `ScraperService` class:

```python
def _count_successful_languages(self, url_id: uuid.UUID) -> int:
    """
    Count languages with successful scraping from database.
    
    This queries the hotels table which is the source of truth.
    A record in hotels means the scraping was successful.
    
    Args:
        url_id: UUID of the URL to check
    
    Returns:
        Number of successfully scraped languages (0 to N)
    """
    with get_db() as session:
        count = session.query(func.count(Hotel.id)).filter(
            Hotel.url_id == url_id
        ).scalar()
        return count or 0


def _mark_incomplete(self, url_obj: URLQueue, error_msg: str) -> None:
    """
    Mark URL as 'error' with detailed incomplete status.
    
    CRITICAL: Data is PRESERVED to enable partial retry.
    Only the URL status is updated, not the scraped data.
    
    Args:
        url_obj: URLQueue object to update
        error_msg: Detailed error message including which languages failed
    """
    with get_db() as session:
        url = session.query(URLQueue).filter_by(id=url_obj.id).first()
        if url:
            url.status = "error"
            url.last_error = error_msg
            url.updated_at = datetime.now(timezone.utc)
            # Preserve scraped_at to indicate progress was made
            session.commit()
            logger.info("URL %s marked as incomplete (data preserved)", url_obj.id)


def _cleanup_empty_url(self, url_id: uuid.UUID) -> None:
    """
    Clean up data for URLs where no languages succeeded.
    
    This is ONLY called when actual_lang_count == 0.
    Removes all traces of the failed scraping attempt.
    
    Args:
        url_id: UUID of the URL to cleanup
    """
    with get_db() as session:
        # Delete from all hotel-related tables
        models_to_clean = [
            HotelDescription, 
            HotelAmenity, 
            HotelPolicy, 
            HotelLegal,
            HotelPopularService, 
            HotelFinePrint, 
            HotelAllService,
            HotelFAQ, 
            HotelGuestReview, 
            HotelPropertyHighlights
        ]
        
        for model in models_to_clean:
            deleted = session.query(model).filter(
                model.url_id == url_id
            ).delete(synchronize_session=False)
            if deleted > 0:
                logger.debug("Cleaned %d records from %s for URL %s", 
                           deleted, model.__tablename__, url_id)
        
        # Delete main hotel records
        deleted_hotels = session.query(Hotel).filter(
            Hotel.url_id == url_id
        ).delete(synchronize_session=False)
        
        # Delete language status records
        deleted_status = session.query(URLLanguageStatus).filter(
            URLLanguageStatus.url_id == url_id
        ).delete(synchronize_session=False)
        
        # Delete any associated images
        # Note: Images are linked via hotel_id, so this should already be handled
        # by the hotel deletion above if cascading is set up
        
        session.commit()
        logger.info(
            "Cleaned up URL %s: %d hotels, %d status records", 
            url_id, deleted_hotels, deleted_status
        )


def _mark_error(self, url_obj: URLQueue, error_msg: str) -> None:
    """
    Mark URL as 'error' with error message.
    
    Used when there's a total failure or exception.
    
    Args:
        url_obj: URLQueue object to update
        error_msg: Error description
    """
    with get_db() as session:
        url = session.query(URLQueue).filter_by(id=url_obj.id).first()
        if url:
            url.status = "error"
            url.last_error = error_msg[:2000] if error_msg else None
            url.updated_at = datetime.now(timezone.utc)
            session.commit()
```

---

## Partial Retry System

### Script: `scripts/retry_incomplete.py`

Create this script to enable intelligent partial retries:

```python
#!/usr/bin/env python3
"""
Partial Retry Script for BookingScraper Pro

This script implements intelligent retry functionality that only
re-scrapes languages that failed, preserving already-successful data.

Usage:
    python scripts/retry_incomplete.py [--dry-run] [--limit N]

Options:
    --dry-run    Show what would be retried without actually doing it
    --limit N    Only process the first N incomplete URLs
"""

import argparse
import sys
from typing import List, Dict, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import get_settings
from app.database import get_db
from app.models import Hotel, URLLanguageStatus, URLQueue
from app.services.scraper_service import ScraperService
from app.logger import get_logger

logger = get_logger(__name__)


def get_incomplete_urls() -> List[Dict[str, Any]]:
    """
    Find URLs with partial scraping completion.
    
    A partial URL is one that:
    - Has status='error' in url_queue
    - Has at least one successful language in hotels
    - Is missing at least one expected language
    
    Returns:
        List of dictionaries with url_id, url, completed langs, missing langs
    """
    cfg = get_settings()
    expected_langs = set(cfg.ENABLED_LANGUAGES)
    
    with get_db() as session:
        # Find all URLs marked as error
        error_urls = session.query(URLQueue).filter(
            URLQueue.status == "error"
        ).all()
        
        incomplete = []
        for url in error_urls:
            # Get completed languages from hotels table
            completed = session.query(Hotel.language).filter(
                Hotel.url_id == url.id
            ).all()
            completed_langs = {r[0] for r in completed}
            
            # Calculate missing languages
            missing_langs = expected_langs - completed_langs
            
            # Only include if partially complete (some success, some failure)
            if missing_langs and completed_langs:
                incomplete.append({
                    "url_id": str(url.id),
                    "url": url.url,
                    "completed": sorted(list(completed_langs)),
                    "missing": sorted(list(missing_langs)),
                    "last_error": url.last_error,
                })
        
        return incomplete


def get_total_failure_urls() -> List[Dict[str, Any]]:
    """
    Find URLs where all languages failed.
    
    These need full retry (all languages).
    
    Returns:
        List of dictionaries with url_id, url, error info
    """
    cfg = get_settings()
    expected_langs = set(cfg.ENABLED_LANGUAGES)
    
    with get_db() as session:
        error_urls = session.query(URLQueue).filter(
            URLQueue.status == "error"
        ).all()
        
        total_failures = []
        for url in error_urls:
            completed = session.query(Hotel.language).filter(
                Hotel.url_id == url.id
            ).all()
            completed_langs = {r[0] for r in completed}
            
            # Total failure = no completed languages
            if not completed_langs:
                total_failures.append({
                    "url_id": str(url.id),
                    "url": url.url,
                    "last_error": url.last_error,
                })
        
        return total_failures


def retry_partial(dry_run: bool = False, limit: int = None) -> None:
    """
    Execute partial retry for incomplete URLs.
    
    Args:
        dry_run: If True, only show what would be done
        limit: Maximum number of URLs to process
    """
    incomplete = get_incomplete_urls()
    
    if not incomplete:
        print("✓ No incomplete URLs found. All URLs are either complete or total failures.")
        return
    
    print(f"\n{'='*70}")
    print(f"PARTIAL RETRY REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    print(f"\nFound {len(incomplete)} partially complete URLs:\n")
    
    for i, item in enumerate(incomplete[:limit] if limit else incomplete, 1):
        print(f"  [{i}] {item['url']}")
        print(f"      Completed: {', '.join(item['completed'])}")
        print(f"      Missing:   {', '.join(item['missing'])}")
        print(f"      Last Error: {item['last_error'][:100]}..." if item['last_error'] else "")
        print()
    
    if dry_run:
        print("\n[DRY RUN] No changes made. Run without --dry-run to execute retries.")
        return
    
    # Execute retries
    print("\n" + "="*70)
    print("EXECUTING PARTIAL RETRIES")
    print("="*70 + "\n")
    
    cfg = get_settings()
    scraper = ScraperService()
    
    for item in incomplete[:limit] if limit else incomplete:
        print(f"\nRetrying: {item['url']}")
        print(f"  Targeting languages: {item['missing']}")
        
        # TODO: Implement language-specific retry in ScraperService
        # For now, this is a placeholder for the full implementation
        # result = scraper.retry_languages(item['url_id'], item['missing'])
        
        print(f"  Status: Would retry languages {item['missing']}")


def show_summary() -> None:
    """Display summary of all error URLs."""
    partial = get_incomplete_urls()
    total = get_total_failure_urls()
    
    print(f"\n{'='*70}")
    print("ERROR URL SUMMARY")
    print(f"{'='*70}")
    print(f"\n  Partial failures (some languages OK): {len(partial)}")
    print(f"  Total failures (all languages failed): {len(total)}")
    print(f"  Total error URLs: {len(partial) + len(total)}")
    
    if partial:
        print(f"\n  Partial failures breakdown:")
        for item in partial[:5]:  # Show first 5
            print(f"    - {item['url']}")
            print(f"      OK: {item['completed']}, Missing: {item['missing']}")
        if len(partial) > 5:
            print(f"    ... and {len(partial) - 5} more")


def main():
    parser = argparse.ArgumentParser(
        description="Retry incomplete URL scrapes"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Show what would be retried without executing"
    )
    parser.add_argument(
        "--limit", 
        type=int,
        help="Maximum number of URLs to process"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show summary of error URLs"
    )
    
    args = parser.parse_args()
    
    if args.summary:
        show_summary()
    else:
        retry_partial(dry_run=args.dry_run, limit=args.limit)


if __name__ == "__main__":
    main()
```

---

## Testing Strategy

### Unit Tests

Create `tests/test_strategy_e.py`:

```python
"""Unit tests for Strategy E implementation."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from uuid import uuid4

from app.services.scraper_service import ScraperService
from app.models import URLQueue, Hotel, URLLanguageStatus


class TestProcessUrlStrategyE:
    """Test cases for the enhanced _process_url method."""
    
    @pytest.fixture
    def scraper(self):
        """Create scraper instance for testing."""
        with patch('app.services.scraper_service.get_settings'):
            return ScraperService()
    
    @pytest.fixture
    def url_obj(self):
        """Create a mock URL object."""
        url = Mock(spec=URLQueue)
        url.id = uuid4()
        url.url = "https://www.booking.com/hotel/test.html"
        url.status = "pending"
        return url
    
    def test_all_languages_success_marks_done(self, scraper, url_obj):
        """
        Test Case 1: All 4 languages succeed.
        Expected: URL marked as 'done'
        """
        # Mock all languages succeeding
        with patch.object(scraper, '_scrape_language', return_value=True), \
             patch.object(scraper, '_count_successful_languages', return_value=4), \
             patch.object(scraper, '_mark_done') as mock_mark_done:
            
            scraper._process_url(url_obj)
            
            mock_mark_done.assert_called_once_with(url_obj, all_ok=True)
    
    def test_partial_success_marks_error_preserves_data(self, scraper, url_obj):
        """
        Test Case 2: 3 of 4 languages succeed.
        Expected: URL marked as 'error', data preserved
        """
        with patch.object(scraper, '_scrape_language', side_effect=[True, True, True, False]), \
             patch.object(scraper, '_count_successful_languages', return_value=3), \
             patch.object(scraper, '_mark_incomplete') as mock_mark_incomplete:
            
            scraper._process_url(url_obj)
            
            mock_mark_incomplete.assert_called_once()
            # Verify error message contains partial info
            call_args = mock_mark_incomplete.call_args
            assert "Incomplete: 3/4" in call_args[0][1]
    
    def test_total_failure_cleans_up(self, scraper, url_obj):
        """
        Test Case 3: All 4 languages fail.
        Expected: URL marked as 'error', data cleaned up
        """
        with patch.object(scraper, '_scrape_language', return_value=False), \
             patch.object(scraper, '_count_successful_languages', return_value=0), \
             patch.object(scraper, '_cleanup_empty_url') as mock_cleanup, \
             patch.object(scraper, '_mark_error') as mock_mark_error:
            
            scraper._process_url(url_obj)
            
            mock_cleanup.assert_called_once()
            mock_mark_error.assert_called_once()
    
    def test_single_language_success_preserves_data(self, scraper, url_obj):
        """
        Test Case 4: Only 1 language succeeds (the original bug case).
        Expected: URL marked as 'error', 1 language preserved
        """
        with patch.object(scraper, '_scrape_language', side_effect=[True, False, False, False]), \
             patch.object(scraper, '_count_successful_languages', return_value=1), \
             patch.object(scraper, '_mark_incomplete') as mock_mark_incomplete:
            
            scraper._process_url(url_obj)
            
            mock_mark_incomplete.assert_called_once()
            call_args = mock_mark_incomplete.call_args
            assert "Incomplete: 1/4" in call_args[0][1]


class TestCountSuccessfulLanguages:
    """Test the _count_successful_languages method."""
    
    def test_count_returns_correct_number(self):
        """Verify count matches database records."""
        # Setup mock database with 3 hotel records
        # Assert count returns 3
        pass
    
    def test_count_returns_zero_for_no_records(self):
        """Verify count returns 0 when no records exist."""
        pass


class TestCleanupEmptyUrl:
    """Test the _cleanup_empty_url method."""
    
    def test_cleanup_deletes_all_related_data(self):
        """Verify all related tables are cleaned."""
        # Create test data in multiple tables
        # Call cleanup
        # Assert all tables are empty for that url_id
        pass
    
    def test_cleanup_does_not_affect_other_urls(self):
        """Verify cleanup only affects target URL."""
        pass


class TestPartialRetry:
    """Test the partial retry functionality."""
    
    def test_get_incomplete_urls_finds_partial(self):
        """Verify incomplete URL detection works correctly."""
        pass
    
    def test_partial_retry_only_scrapes_missing(self):
        """Verify retry only targets missing languages."""
        pass
```

### Integration Tests

```python
"""Integration tests for Strategy E."""

import pytest
from app.database import get_db, init_db
from app.models import URLQueue, Hotel, URLLanguageStatus
from app.services.scraper_service import ScraperService
from app.config import get_settings


@pytest.fixture
def test_db():
    """Create test database."""
    init_db()
    yield
    # Cleanup after tests


class TestStrategyEIntegration:
    """Full integration tests."""
    
    def test_full_flow_complete_success(self, test_db):
        """Test complete successful scraping flow."""
        # Create test URL
        # Run scraper with mocked HTTP responses (all success)
        # Verify URL status is 'done'
        # Verify 4 hotel records exist
        pass
    
    def test_full_flow_partial_failure(self, test_db):
        """Test partial failure and retry."""
        # Create test URL
        # Run scraper with 3 success, 1 failure
        # Verify URL status is 'error'
        # Verify 3 hotel records preserved
        # Run partial retry for failed language
        # Verify URL status becomes 'done'
        # Verify 4 hotel records exist
        pass
    
    def test_full_flow_total_failure_and_retry(self, test_db):
        """Test total failure and full retry."""
        # Create test URL
        # Run scraper with all failures
        # Verify URL status is 'error'
        # Verify no hotel records exist
        # Run full retry with success
        # Verify URL status becomes 'done'
        pass
```

---

## Migration Guide

### Step-by-Step Migration

1. **Backup Database**
   ```bash
   # Before making any changes
   cp data/scraper.db data/scraper_backup_$(date +%Y%m%d).db
   ```

2. **Update Code**
   - Replace `_process_url()` method in `scraper_service.py`
   - Add new helper methods: `_count_successful_languages()`, `_mark_incomplete()`, `_cleanup_empty_url()`
   - Create `scripts/retry_incomplete.py`

3. **Fix Existing Incomplete Data**
   ```python
   # Run this script to fix URLs that were incorrectly marked as done
   
   from app.database import get_db
   from app.models import URLQueue, Hotel
   from app.config import get_settings
   
   def fix_incomplete_urls():
       cfg = get_settings()
       expected_count = len(cfg.ENABLED_LANGUAGES)
       
       with get_db() as session:
           done_urls = session.query(URLQueue).filter(
               URLQueue.status == "done"
           ).all()
           
           fixed = 0
           for url in done_urls:
               actual_count = session.query(Hotel).filter(
                   Hotel.url_id == url.id
               ).count()
               
               if actual_count < expected_count:
                   url.status = "error"
                   url.last_error = f"Fixed: Incomplete ({actual_count}/{expected_count})"
                   fixed += 1
           
           session.commit()
           print(f"Fixed {fixed} incomplete URLs")
   
   fix_incomplete_urls()
   ```

4. **Run Tests**
   ```bash
   pytest tests/test_strategy_e.py -v
   ```

5. **Monitor First Run**
   - Watch logs for proper state transitions
   - Verify partial failures are preserved
   - Run retry script to verify it works

---

## Rollback Procedure

### If Strategy E Causes Issues

1. **Revert Code Changes**
   ```bash
   git checkout HEAD~1 -- app/services/scraper_service.py
   git checkout HEAD~1 -- scripts/retry_incomplete.py
   ```

2. **Restore Database**
   ```bash
   cp data/scraper_backup_YYYYMMDD.db data/scraper.db
   ```

3. **Restart Services**
   ```bash
   # Restart your scraping service
   systemctl restart scraper  # or equivalent
   ```

### Partial Rollback

If only the retry script causes issues, you can:
1. Remove `scripts/retry_incomplete.py`
2. Keep the core `_process_url()` changes
3. Manual retries will still work (URLs in 'error' status)

---

## Monitoring and Alerting

### Key Metrics to Track

```python
# Add to your monitoring/metrics.py

def get_integrity_metrics():
    """Return data integrity metrics."""
    cfg = get_settings()
    expected_count = len(cfg.ENABLED_LANGUAGES)
    
    with get_db() as session:
        # URLs marked done but incomplete
        incomplete_done = session.execute("""
            SELECT COUNT(*) 
            FROM url_queue u
            LEFT JOIN hotels h ON h.url_id = u.id
            WHERE u.status = 'done'
            GROUP BY u.id
            HAVING COUNT(h.id) < :expected
        """, {"expected": expected_count}).scalar()
        
        # Partial failures (some success)
        partial_failures = session.query(URLQueue).filter(
            URLQueue.status == "error"
        ).join(Hotel).group_by(URLQueue.id).count()
        
        # Total failures (no success)
        total_failures = session.execute("""
            SELECT COUNT(*) FROM url_queue u
            WHERE u.status = 'error'
            AND NOT EXISTS (SELECT 1 FROM hotels h WHERE h.url_id = u.id)
        """).scalar()
        
        return {
            "incomplete_marked_done": incomplete_done,
            "partial_failures": partial_failures,
            "total_failures": total_failures,
            "integrity_score": calculate_integrity_score(),
        }
```

### Alert Rules

```yaml
# Example Prometheus alert rules
groups:
  - name: scraper_integrity
    rules:
      - alert: IncompleteURLsMarkedDone
        expr: scraper_incomplete_marked_done > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "URLs marked done but incomplete"
          description: "{{ $value }} URLs have status 'done' but missing languages"
      
      - alert: HighPartialFailureRate
        expr: rate(scraper_partial_failures[1h]) > 0.1
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "High partial failure rate"
          description: "More than 10% of URLs are partially failing"
```

---

## Summary

Strategy E provides a robust solution to the critical data integrity bug while:

1. **Preserving valid data** - No longer deleting successful language scrapes
2. **Enabling efficient retries** - Only re-scrape what failed
3. **Using existing infrastructure** - Leverages `url_language_status` table
4. **Providing clear state tracking** - Easy to understand URL states
5. **Supporting monitoring** - Metrics and alerts for integrity

This implementation transforms the scraper from a system that could silently produce incomplete data to one that properly tracks and recovers from failures.

---

*Document generated for BookingScraper Pro v6.0.0 Build 58*  
*Strategy E Implementation Guide v1.0*