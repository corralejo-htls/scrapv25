"""
create_tables.py — Create all database tables via SQLAlchemy.
NOTE: For production use install_clean_v48.sql instead, which also
creates triggers, partitions, indexes, and grants.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import _get_engine
from app.models import Base

if __name__ == "__main__":
    print("Creating tables via SQLAlchemy ORM...")
    engine = _get_engine()
    Base.metadata.create_all(engine)
    print("Done. WARNING: Run install_clean_v48.sql to create triggers and partitions.")
