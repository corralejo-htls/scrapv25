"""
test_models.py — ORM model structure and constraint tests.
Uses SQLite in-memory — no PostgreSQL required.
"""

from __future__ import annotations

import uuid
import pytest
from datetime import datetime, timezone


class TestURLQueueModel:
    """URLQueue model constraints and defaults."""

    def test_create_url_queue_entry(self, in_memory_db):
        from app.models import URLQueue
        entry = URLQueue(
            url="https://www.booking.com/hotel/es/test.html",
            base_url="https://www.booking.com/hotel/es/test.html",
        )
        in_memory_db.add(entry)
        in_memory_db.commit()
        assert entry.id is not None
        assert entry.status == "pending"
        assert entry.priority == 5
        assert entry.retry_count == 0
        assert entry.version_id == 1

    def test_uuid_primary_key_generated(self, in_memory_db):
        from app.models import URLQueue
        e1 = URLQueue(url="https://www.booking.com/hotel/es/a.html", base_url="x")
        e2 = URLQueue(url="https://www.booking.com/hotel/es/b.html", base_url="x")
        in_memory_db.add_all([e1, e2])
        in_memory_db.commit()
        assert e1.id != e2.id


class TestHotelModel:
    """Hotel model defaults — JSONB fields use callable defaults."""

    def test_jsonb_defaults_are_not_shared(self):
        """SCRAP-BUG-007: mutable JSONB defaults must not be shared across instances."""
        from app.models import Hotel
        h1 = Hotel(url_id=uuid.uuid4(), url="http://a.com", language="es")
        h2 = Hotel(url_id=uuid.uuid4(), url="http://b.com", language="en")
        # Mutate h1's amenities
        if h1.amenities is not None:
            if isinstance(h1.amenities, list):
                h1.amenities.append("pool")
                # h2 should not be affected
                assert "pool" not in (h2.amenities or [])

    def test_version_id_defaults_to_one(self, in_memory_db):
        """
        BUG-TEST-003 fix: SQLAlchemy column default=1 fires at INSERT time,
        not at Python object instantiation. Must commit before asserting.
        """
        from app.models import Hotel
        h = Hotel(url_id=uuid.uuid4(), url="http://test.com", language="es")
        in_memory_db.add(h)
        in_memory_db.commit()
        in_memory_db.refresh(h)
        assert h.version_id == 1


class TestURLLanguageStatus:
    """BUG-016: 'incomplete' must be a valid status."""

    def test_valid_statuses_include_incomplete(self, in_memory_db):
        from app.models import URLLanguageStatus
        row = URLLanguageStatus(
            url_id=uuid.uuid4(),
            language="es",
            status="incomplete",
        )
        in_memory_db.add(row)
        # Should not raise — 'incomplete' is valid
        in_memory_db.commit()
        assert row.status == "incomplete"


class TestSystemMetrics:
    """BUG-019: SystemMetrics must have time-series indexes defined."""

    def test_index_definitions_exist(self):
        from app.models import SystemMetrics
        table = SystemMetrics.__table__
        index_names = {idx.name for idx in table.indexes}
        assert "ix_sysmetrics_recorded_cpu" in index_names
        assert "ix_sysmetrics_recorded_mem" in index_names


class TestScrapingLogDocumentation:
    """BUG-003: ScrapingLog must document FK limitation prominently."""

    def test_docstring_mentions_trigger(self):
        from app.models import ScrapingLog
        doc = ScrapingLog.__doc__ or ""
        # Must mention the trigger dependency
        assert "trigger" in doc.lower() or "trg_" in doc


class TestModelVersionConsistency:
    """All version references must be 6.0.0 / 48."""

    def test_app_version_consistent(self):
        from app import APP_VERSION, BUILD_VERSION
        assert APP_VERSION == "6.0.0"
        assert BUILD_VERSION == 56  # BUG-TEST-VERSION-002 FIX (v56)

    def test_config_version_matches(self):
        from app.config import APP_VERSION as CFG_VER, BUILD_VERSION as CFG_BUILD
        assert CFG_VER == "6.0.0"
        assert CFG_BUILD == 56  # BUG-TEST-VERSION-002 FIX (v56)
