"""
BookingScraper Pro v6.0 - Create Tables Script
===============================================
Creates all database tables via SQLAlchemy create_all().
Use this ONLY for development / quick setup.
For production, use install_clean_v46.sql which also creates
triggers, roles, GIN indexes, and partitions.

Usage: python scripts/create_tables.py
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass


def main() -> int:
    try:
        from app.database import engine, test_connection
        from app.models import Base

        print("Testing database connection...")
        test_connection()

        print("Creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
        print()
        print("NOTE: For production, run install_clean_v46.sql instead.")
        print("      It creates triggers, roles, and partitions not handled by create_all().")
        return 0
    except EnvironmentError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
