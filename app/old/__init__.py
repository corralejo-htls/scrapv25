"""
BookingScraper Pro v6.0.0 build 54
Platform: Windows 11 + Python 3.14.x

NOTA: NO importar celery_app aqui.
  from app.celery_app import celery_app  ← PROHIBIDO en __init__.py
  Causaria importacion circular: celery_app.py → app.config → app.__init__
  Celery debe referenciarse siempre con notacion explicita:
      python -m celery -A app.celery_app:celery_app <comando>
"""

__version__ = "6.0.0"
__version_info__ = (6, 0, 0)
APP_VERSION = "6.0.0"
BUILD_VERSION = 54
