"""
create_project_structure.py — BookingScraper Pro v48
Crea todos los directorios requeridos para una instalación limpia en Windows 11.
Estructura de directorios EXACTA del proyecto original.
Seguro para ejecutar múltiples veces (idempotente).
"""

from __future__ import annotations

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

DIRECTORIES = [
    # Aplicación
    BASE / "app",
    BASE / "scripts",
    BASE / "tests",
    BASE / "migrations",
    BASE / "migrations" / "versions",
    # Documentación y plantillas
    BASE / "docs",
    BASE / "templates",
    # Logs de aplicación (rotating file handler)
    BASE / "logs",
    BASE / "logs" / "debug",
    # Datos generados en ejecución
    BASE / "data",
    BASE / "data" / "images",        # Imágenes descargadas de hoteles
    BASE / "data" / "exports",       # Exportaciones CSV/JSON
    BASE / "data" / "logs",
    BASE / "data" / "logs" / "debug", # HTML debug del scraper
    # Backups
    BASE / "backups",
]


def main() -> None:
    print(f"Creando directorios bajo: {BASE}")
    created = 0
    for d in DIRECTORIES:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            print(f"  CREADO  {d.relative_to(BASE)}")
            created += 1
        else:
            print(f"  OK      {d.relative_to(BASE)}")

    print(f"\n{created} directorios nuevos creados, {len(DIRECTORIES)-created} ya existían.")


if __name__ == "__main__":
    main()
