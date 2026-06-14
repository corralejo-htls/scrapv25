"""
alembic_env.py — BookingScraper Pro v48
Alembic migration environment — lazy database URL access.
BUG-111 fix: references the correct migrations/ directory.
"""

from logging.config import fileConfig
from alembic import context
from app.config import get_settings
from app.models import Base

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    cfg = get_settings()
    context.configure(
        url=cfg.database_url_sync,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from sqlalchemy import create_engine
    cfg = get_settings()
    connectable = create_engine(cfg.database_url_sync)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
