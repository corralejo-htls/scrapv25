# BookingScraper Pro v6.0.0 - Recommendations
**Build 58 | March 28, 2026**

---

## Executive Summary

This document provides actionable recommendations to address the issues identified in the comprehensive audit of BookingScraper Pro v6.0.0. Recommendations are organized by priority and include implementation guidance.

---

## Immediate Actions (This Week)

### 1. Fix hotels_fine_print Extraction

**Priority:** 🔴 Critical  
**Effort:** 2-3 hours  
**Impact:** High data quality improvement

**Problem:**
The fine print extraction stores wrapper HTML instead of just the paragraph content.

**Solution:**

```python
# In extractor.py, modify _extract_fine_print() method

def _extract_fine_print(self) -> Optional[str]:
    """
    Extract only the paragraph content from the Fine Print section.
    Returns HTML with only <p> elements, no wrapper containers.
    """
    # ... existing section finding code ...
    
    if not section:
        return None
    
    try:
        # Find all paragraph elements within the section
        paragraphs = section.find_all("p")
        
        if not paragraphs:
            logger.debug("FinePrint: no paragraphs found for lang=%s", self.language)
            return None
        
        # Build content from paragraphs, skipping header/title paragraphs
        content_parts = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            # Skip empty, very short (likely headers), or duplicate title paragraphs
            if len(text) < 10:
                continue
            # Skip paragraphs that look like section titles
            if text.lower() in ["the fine print", "letra pequeña", "a tener en cuenta"]:
                continue
            content_parts.append(str(p))
        
        if not content_parts:
            return None
            
        # Join paragraphs without additional wrappers
        result = "".join(content_parts)
        
        logger.debug(
            "FinePrint extracted for lang=%s: %d paragraphs",
            self.language, len(content_parts)
        )
        return result
        
    except Exception as exc:
        logger.debug("FinePrint parse error for lang=%s: %s", self.language, exc)
        return None
```

**Testing:**
```sql
-- Verify the fix
SELECT url_id, language, LEFT(fp, 100) as preview
FROM hotels_fine_print
WHERE fp NOT LIKE '<p>%';
-- Should return 0 rows
```

---

### 2. Redesign hotels_property_highlights Structure

**Priority:** 🔴 Critical  
**Effort:** 4-6 hours  
**Impact:** Required for data completeness

**Problem:**
The current structure stores only highlight text. Required structure includes category/detail.

**Solution:**

**Step 1: Modify the Model**
```python
# In models.py, update HotelPropertyHighlights class

class HotelPropertyHighlights(Base):
    """
    Property highlights with category/detail structure.
    """
    __tablename__ = "hotels_property_highlights"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    hotel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    url_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    highlight_category: Mapped[str] = mapped_column(
        String(256), nullable=False,
        comment="Category name (e.g., 'Ideal for your stay', 'Bathroom')"
    )
    highlight_detail: Mapped[str] = mapped_column(
        String(512), nullable=False,
        comment="Detail item (e.g., 'Private bathroom', 'Parking')"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    
    __table_args__ = (
        UniqueConstraint("hotel_id", "language", "highlight_category", "highlight_detail",
                        name="uq_hph_hotel_lang_cat_detail"),
        Index("ix_hph_hotel_id", "hotel_id"),
        Index("ix_hph_language", "language"),
        Index("ix_hph_category", "highlight_category"),
    )
```

**Step 2: Update the Extractor**
```python
def _extract_property_highlights(self) -> List[Dict[str, str]]:
    """
    Extract property highlights with category/detail structure.
    Returns list of dicts with 'category' and 'detail' keys.
    """
    highlights = []
    
    # Find the highlights section
    section = self.soup.find(attrs={"data-testid": "property-highlights"})
    if not section:
        return highlights
    
    # Parse category groups
    current_category = ""
    for element in section.find_all(["h3", "h4", "div", "li"]):
        # Check if this is a category header
        if element.name in ["h3", "h4"]:
            current_category = element.get_text(strip=True)
            continue
        
        # Check if this is a detail item
        if element.name == "li":
            detail = element.get_text(strip=True)
            if detail and current_category:
                highlights.append({
                    "category": current_category,
                    "detail": detail
                })
    
    return highlights
```

**Step 3: Update the Service**
```python
def _upsert_property_highlights(
    self, url_obj, lang: str, highlights: List[Dict[str, str]]
) -> None:
    """Upsert property highlights with category/detail structure."""
    if not highlights:
        return
    
    with get_db() as session:
        hotel = session.query(Hotel).filter_by(
            url_id=url_obj.id, language=lang
        ).first()
        
        if not hotel:
            return
        
        # Delete existing
        session.query(HotelPropertyHighlights).filter_by(
            hotel_id=hotel.id, language=lang
        ).delete()
        
        # Insert new
        for item in highlights:
            session.add(HotelPropertyHighlights(
                hotel_id=hotel.id,
                url_id=url_obj.id,
                language=lang,
                highlight_category=item["category"],
                highlight_detail=item["detail"],
            ))
```

---

### 3. Add Extraction Verification

**Priority:** 🔴 Critical  
**Effort:** 2-3 hours  
**Impact:** Prevents data inconsistency

**Solution:**

```python
# In scraper_service.py, modify _process_url() method

def _process_url(self, url_obj: URLQueue) -> None:
    # ... existing code ...
    
    for lang in languages:
        try:
            ok = self._scrape_language(url_obj, lang)
            lang_results[lang] = ok
            
            # NEW: Verify actual DB commit immediately
            if ok:
                actual = self._count_successful_languages(url_obj.id)
                expected = len([l for l, r in lang_results.items() if r])
                if actual != expected:
                    logger.warning(
                        "URL %s lang=%s: DB count mismatch. Expected %d, got %d",
                        url_obj.id, lang, expected, actual
                    )
                    lang_results[lang] = False
                    
        except Exception as lang_exc:
            logger.error("URL %s lang=%s: EXCEPTION %s", 
                        url_obj.id, lang, lang_exc)
            lang_results[lang] = False
    
    # ... rest of method ...
```

---

## Short-term Improvements (Next 2 Weeks)

### 4. Add Fallback Selectors for Property Highlights

**Priority:** 🟠 High  
**Effort:** 3-4 hours

```python
def _extract_property_highlights(self) -> List[Dict[str, str]]:
    """Extract with multiple fallback strategies."""
    
    # Strategy 1: data-testid selectors
    section = self.soup.find(attrs={"data-testid": "property-highlights"})
    
    # Strategy 2: Class patterns
    if not section:
        section = self.soup.find(attrs={
            "class": re.compile(r"property.highlight|propertyHighlight", re.I)
        })
    
    # Strategy 3: Keyword-based detection
    if not section:
        keywords = {
            "en": ["property highlights", "highlights"],
            "es": ["aspectos destacados"],
            # ... more languages
        }
        for kw in keywords.get(self.language, []):
            el = self.soup.find(string=re.compile(kw, re.I))
            if el:
                section = el.find_parent(["div", "section"])
                break
    
    # Strategy 4: Look for common highlight patterns
    if not section:
        # Find containers with lists of amenities
        for container in self.soup.find_all(["div", "section"]):
            lis = container.find_all("li")
            if len(lis) >= 3:  # Likely a highlights section
                return self._parse_highlights_from_container(container)
    
    return self._parse_highlights_from_container(section) if section else []
```

---

### 5. Implement Idempotency Keys

**Priority:** 🟡 Medium  
**Effort:** 4-6 hours

```python
# Add to models.py
class URLLanguageAttempt(Base):
    """Track each processing attempt for idempotency."""
    __tablename__ = "url_language_attempts"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    url_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    language: Mapped[str] = mapped_column(String(10))
    attempt_id: Mapped[str] = mapped_column(String(32))  # UUID for this attempt
    status: Mapped[str] = mapped_column(String(32))  # processing, done, error
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    __table_args__ = (
        UniqueConstraint("url_id", "language", "attempt_id"),
    )

# In scraper_service.py
def _scrape_language(self, url_obj, lang: str) -> bool:
    attempt_id = str(uuid.uuid4())[:8]
    
    # Check for existing successful attempt
    existing = session.query(URLLanguageAttempt).filter_by(
        url_id=url_obj.id, language=lang, status="done"
    ).first()
    
    if existing:
        logger.info("URL %s lang=%s already processed, skipping", 
                   url_obj.id, lang)
        return True
    
    # Record this attempt
    attempt = URLLanguageAttempt(
        id=uuid.uuid4(),
        url_id=url_obj.id,
        language=lang,
        attempt_id=attempt_id,
        status="processing",
        started_at=datetime.now(timezone.utc),
    )
    session.add(attempt)
    session.commit()
    
    try:
        # ... do scraping ...
        attempt.status = "done"
        attempt.completed_at = datetime.now(timezone.utc)
        session.commit()
        return True
    except Exception:
        attempt.status = "error"
        session.commit()
        return False
```

---

### 6. Add Consistency Checks

**Priority:** 🟡 Medium  
**Effort:** 3-4 hours

```python
# Create new file: app/consistency_checker.py

class ConsistencyChecker:
    """Validate data consistency across tables."""
    
    def check_language_consistency(self) -> List[Dict]:
        """Find URLs where hotels count doesn't match satellite tables."""
        with get_db() as session:
            sql = text("""
                SELECT 
                    h.url_id,
                    COUNT(DISTINCT h.language) as hotel_langs,
                    COUNT(DISTINCT ph.language) as highlight_langs
                FROM hotels h
                LEFT JOIN hotels_property_highlights ph 
                    ON h.url_id = ph.url_id
                GROUP BY h.url_id
                HAVING COUNT(DISTINCT h.language) != COUNT(DISTINCT ph.language)
            """)
            return session.execute(sql).fetchall()
    
    def check_orphaned_satellite_records(self) -> List[Dict]:
        """Find satellite records without matching hotel records."""
        with get_db() as session:
            sql = text("""
                SELECT ph.url_id, ph.language
                FROM hotels_property_highlights ph
                LEFT JOIN hotels h 
                    ON ph.url_id = h.url_id AND ph.language = h.language
                WHERE h.id IS NULL
            """)
            return session.execute(sql).fetchall()
    
    def run_all_checks(self) -> Dict:
        """Run all consistency checks and return report."""
        return {
            "language_consistency": self.check_language_consistency(),
            "orphaned_records": self.check_orphaned_satellite_records(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
```

---

## Long-term Enhancements (Next Month)

### 7. Improve Concurrency Handling

**Priority:** 🟡 Medium  
**Effort:** 8-12 hours

```python
# Use PostgreSQL advisory locks
def _acquire_url_lock(self, url_id: str) -> bool:
    """Acquire advisory lock for URL processing."""
    with get_db() as session:
        # PostgreSQL advisory lock
        result = session.execute(
            text("SELECT pg_try_advisory_lock(:lock_id)"),
            {"lock_id": hash(url_id) % 2**31}
        ).scalar()
        return result

def _release_url_lock(self, url_id: str) -> None:
    """Release advisory lock."""
    with get_db() as session:
        session.execute(
            text("SELECT pg_advisory_unlock(:lock_id)"),
            {"lock_id": hash(url_id) % 2**31}
        )
```

---

### 8. Add Comprehensive Metrics

**Priority:** 🟢 Low  
**Effort:** 6-8 hours

```python
# Create new file: app/metrics.py

from dataclasses import dataclass, field
from typing import Dict
from collections import defaultdict

@dataclass
class ExtractionMetrics:
    """Track extraction success rates by field."""
    
    attempts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    successes: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    def record_attempt(self, field: str) -> None:
        self.attempts[field] += 1
    
    def record_success(self, field: str) -> None:
        self.successes[field] += 1
    
    def get_success_rate(self, field: str) -> float:
        attempts = self.attempts.get(field, 0)
        if attempts == 0:
            return 0.0
        return self.successes.get(field, 0) / attempts
    
    def get_report(self) -> Dict:
        return {
            field: {
                "attempts": self.attempts[field],
                "successes": self.successes[field],
                "rate": self.get_success_rate(field),
            }
            for field in self.attempts.keys()
        }

# Global metrics instance
_metrics = ExtractionMetrics()

# In extractor.py
def _extract_fine_print(self) -> Optional[str]:
    _metrics.record_attempt("fine_print")
    result = self._do_extraction()
    if result:
        _metrics.record_success("fine_print")
    return result
```

---

## Implementation Roadmap

| Week | Tasks | Priority |
|------|-------|----------|
| Week 1 | Fix fine_print extraction | 🔴 Critical |
| Week 1 | Redesign property_highlights | 🔴 Critical |
| Week 1 | Add extraction verification | 🔴 Critical |
| Week 2 | Add fallback selectors | 🟠 High |
| Week 2 | Implement idempotency | 🟡 Medium |
| Week 3 | Add consistency checks | 🟡 Medium |
| Week 3 | Improve concurrency | 🟡 Medium |
| Week 4 | Add comprehensive metrics | 🟢 Low |

---

## Success Criteria

After implementing these recommendations:

1. **Data Quality:**
   - 100% of processed URLs have consistent language counts
   - Fine print contains only paragraph content
   - Property highlights include category/detail structure

2. **Reliability:**
   - Zero race conditions in concurrent processing
   - All extraction failures are properly tracked
   - Automatic recovery from partial failures

3. **Observability:**
   - Daily consistency reports
   - Per-field extraction success rates
   - Alerting on data anomalies

---

*Document generated: March 28, 2026*
*Repository: https://github.com/corralejo-htls/scrapv25.git*
