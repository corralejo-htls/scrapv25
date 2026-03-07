"""
BookingScraper Pro v6.0 - Project Structure Creator
====================================================
Creates all required Windows directories for the application.
Run once after cloning the repository.

Usage: python scripts/create_project_structure.py
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DIRECTORIES = [
    "C:/BookingScraper/images",
    "C:/BookingScraper/data",
    "C:/BookingScraper/exports",
    "C:/BookingScraper/debug",
    "C:/BookingScraper/backups",
    "logs",
    "tests",
    "migrations/versions",
]


def main() -> int:
    print("BookingScraper Pro v6.0 - Creating project structure")
    print(f"Project root: {PROJECT_ROOT}")
    print()

    created  = 0
    existing = 0

    for d in DIRECTORIES:
        path = Path(d) if Path(d).is_absolute() else PROJECT_ROOT / d
        try:
            if path.exists():
                print(f"  EXISTS  : {path}")
                existing += 1
            else:
                path.mkdir(parents=True, exist_ok=True)
                print(f"  CREATED : {path}")
                created += 1
        except OSError as exc:
            print(f"  ERROR   : {path} — {exc}", file=sys.stderr)

    print()
    print(f"Done: {created} created, {existing} already existed")

    # Create .env from .env.example if not present
    env_file = PROJECT_ROOT / ".env"
    env_example = PROJECT_ROOT / ".env.example"
    if not env_file.exists() and env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print(f"\nCreated .env from .env.example — please edit it with your credentials.")
    elif not env_file.exists():
        print("\nWARNING: .env.example not found. Create .env manually.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
