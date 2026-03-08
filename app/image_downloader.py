"""
image_downloader.py — BookingScraper Pro v48
Windows 11 compatible image downloader with timeout and path validation.
"""

from __future__ import annotations

import hashlib
import logging
import mimetypes
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests

from app.config import get_settings
from app.database import get_db
from app.models import ImageDownload

logger = logging.getLogger(__name__)

_ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
_MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


class ImageDownloader:
    """Download hotel images with parallel workers and deduplication."""

    def __init__(self) -> None:
        self._cfg = get_settings()
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0",
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        })

    def download_batch(
        self,
        hotel_id: uuid.UUID,
        image_urls: List[str],
        max_workers: int = 3,
    ) -> Dict[str, bool]:
        """Download a batch of images for a hotel. Returns {url: success}."""
        results: Dict[str, bool] = {}

        with ThreadPoolExecutor(max_workers=min(max_workers, 4)) as executor:
            futures = {
                executor.submit(self._download_one, hotel_id, url): url
                for url in image_urls[:100]  # Safety cap
            }
            for future in as_completed(futures, timeout=300):
                url = futures[future]
                try:
                    results[url] = future.result()
                except Exception as exc:
                    logger.warning("Image download failed for %s: %s", url, exc)
                    results[url] = False

        return results

    def _download_one(self, hotel_id: uuid.UUID, url: str) -> bool:
        """Download a single image and persist record."""
        cfg = self._cfg
        images_dir = cfg.IMAGES_DIR / str(hotel_id)
        images_dir.mkdir(parents=True, exist_ok=True)

        try:
            response = self._session.get(
                url,
                timeout=cfg.SCRAPER_REQUEST_TIMEOUT,
                stream=True,
                allow_redirects=True,
            )
            response.raise_for_status()

            content_type = response.headers.get("content-type", "").split(";")[0].strip()
            if content_type not in _ALLOWED_CONTENT_TYPES:
                logger.debug("Skipping image with content-type %s: %s", content_type, url)
                return False

            # Stream-read with size limit
            chunks = []
            total = 0
            for chunk in response.iter_content(chunk_size=8192):
                chunks.append(chunk)
                total += len(chunk)
                if total > _MAX_IMAGE_SIZE_BYTES:
                    logger.warning("Image too large (>10MB), skipping: %s", url)
                    return False

            data = b"".join(chunks)
            ext = mimetypes.guess_extension(content_type) or ".jpg"
            filename = hashlib.sha256(url.encode()).hexdigest()[:24] + ext

            # Windows path: ensure no reserved chars
            local_path = images_dir / filename
            local_path.write_bytes(data)

            # Persist record
            with get_db() as session:
                existing = (
                    session.query(ImageDownload)
                    .filter_by(hotel_id=hotel_id, url=url)
                    .first()
                )
                if existing:
                    existing.local_path = str(local_path)
                    existing.file_size_bytes = len(data)
                    existing.status = "done"
                else:
                    session.add(ImageDownload(
                        hotel_id=hotel_id,
                        url=url,
                        local_path=str(local_path),
                        file_size_bytes=len(data),
                        content_type=content_type,
                        status="done",
                    ))
            return True

        except requests.RequestException as exc:
            logger.warning("Download error for %s: [%s] %s", url, type(exc).__name__, exc)
            with get_db() as session:
                row = session.query(ImageDownload).filter_by(hotel_id=hotel_id, url=url).first()
                if row:
                    row.status = "error"
                    row.error_message = str(exc)[:2000]
                else:
                    session.add(ImageDownload(
                        hotel_id=hotel_id, url=url, status="error",
                        error_message=str(exc)[:2000],
                    ))
            return False
