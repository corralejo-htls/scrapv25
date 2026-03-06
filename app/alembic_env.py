"""
alembic/env.py — Alembic migration environment
BookingScraper Pro | Windows 11

[FIX SEC-001] Credentials are read from app/config.py (which reads from .env).
The sqlalchemy.url placeholder in alembic.ini is intentionally invalid.
This file overrides it at runtime with settings.DATABASE_URL.

Never store database credentials in alembic.ini or any version-controlled file.
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Import application settings — reads DB_* vars from .env
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.config import settings
from app.models import Base  # for autogenerate support

# Alembic Config object (provides access to alembic.ini values)
config = context.config

# [FIX SEC-001] Override the placeholder URL in alembic.ini with
# the live value from settings, which reads DB_PASSWORD from .env.
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Logging setup from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate (--autogenerate flag)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (no live DB connection required)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (live DB connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,   # NullPool: single connection per migration run
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
