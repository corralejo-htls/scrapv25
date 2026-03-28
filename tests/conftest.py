"""
conftest.py — Shared pytest fixtures for BookingScraper Pro v49.
Runs without a real database — uses SQLite in-memory for ORM tests.

Fixes applied (v49):
  BUG-TEST-004: SQLite in-memory fixture now coerces PostgreSQL JSONB → JSON
               so ORM model tests work without a real PostgreSQL instance.
"""

from __future__ import annotations

import os
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def _reset_settings():
    """Reset settings singleton between tests to avoid state leakage."""
    from app.config import reset_settings
    reset_settings()
    yield
    reset_settings()


@pytest.fixture()
def mock_env(monkeypatch):
    """Provide a minimal valid environment for settings tests."""
    env = {
        "SECRET_KEY": "test-secret-key-that-is-long-enough-for-validation-purposes",
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_NAME": "test_db",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "REDIS_URL": "redis://localhost:6379/0",
        "VPN_ENABLED": "false",
        "ENABLED_LANGUAGES": "es,en,de",
    }
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    return env


def _make_sqlite_engine():
    """
    Build a SQLite in-memory engine compatible with PostgreSQL JSONB models.

    BUG-TEST-004 fix: SQLite does not support JSONB. Before calling
    create_all(), we walk all table columns and replace JSONB with JSON
    so SQLite can render the DDL without errors.

    This coercion is safe for structural/constraint tests — it only affects
    the in-memory test DB, never the production PostgreSQL schema.
    """
    from sqlalchemy import create_engine, JSON
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.dialects.postgresql import JSONB
    from app.models import Base

    # Coerce JSONB → JSON for all columns across all mapped tables
    for table in Base.metadata.tables.values():
        for col in table.columns:
            if isinstance(col.type, JSONB):
                col.type = JSON()

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture()
def in_memory_db():
    """
    SQLite in-memory session for ORM structure tests.
    Does NOT require PostgreSQL to be running.
    JSONB columns are coerced to JSON for SQLite compatibility.
    """
    from sqlalchemy.orm import sessionmaker

    engine = _make_sqlite_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture()
def mock_redis():
    """Mock Redis client that simulates SET NX and ping."""
    r = MagicMock()
    r.set.return_value = True
    r.ping.return_value = True
    r.delete.return_value = 1
    return r


@pytest.fixture()
def sample_html():
    """Minimal Booking.com-like hotel HTML for extractor tests."""
    return """
    <html lang="es">
    <head>
        <meta property="og:locale" content="es_ES" />
        <title>Hotel Test - Booking.com</title>
    </head>
    <body>
        <h2 data-testid="title">Hotel Corralejo Beach</h2>
        <span data-testid="address">Calle Mayor 1, Corralejo, Fuerteventura</span>
        <div data-testid="review-score">
            <div class="score">8.5</div>
            <span>1,234 reviews</span>
        </div>
        <div data-testid="property-description">
            Beautiful hotel on the beach with stunning ocean views.
        </div>
    </body>
    </html>
    """
