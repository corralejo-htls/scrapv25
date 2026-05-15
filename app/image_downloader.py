"""
image_downloader.py — BookingScraper Pro v49
Windows 11 compatible image downloader.

Fixes applied:
  BUG-IMG-401    : Query params (k= auth token) were stripped before download →
                   now receives full URLs from scraper.py (fix is in scraper.py).
  BUG-IMG-SCHEMA : Added id_photo and category to ImageDownload records.
  NEW-TABLE-001  : Persist ImageData (photo metadata) alongside download records.
  Platform       : Windows 11 / ThreadPoolExecutor (not ProcessPoolExecutor).
"""

from __future__ import annotations

import hashlib
import logging
import mimetypes
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

from app.config import get_settings
from app.database import get_db
from app.models import ImageData, ImageDownload

logger = logging.getLogger(__name__)

_ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
_MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

# Category ordering for priority download (large is most useful)
_CATEGORY_PRIORITY = {"large_url": 0, "highres_url": 1, "thumb_url": 2}


class ImageDownloader:
    """
    Download hotel images with parallel workers and deduplication.
    Supports the new 3-size category model (thumb_url, large_url, highres_url).
    """

    def __init__(self) -> None:
        self._cfg = get_settings()
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0",
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer": "https://www.booking.com/",
        })

    def download_batch(
        self,
        hotel_id: uuid.UUID,
        image_urls: List[str],
        max_workers: int = 3,
    ) -> Dict[str, bool]:
        """
        Download a batch of plain image URLs (legacy interface).
        Returns {url: success}.
        Used when caller has only flat URL list (no photo metadata).
        """
        results: Dict[str, bool] = {}
        with ThreadPoolExecutor(max_workers=min(max_workers, 4)) as executor:
            futures = {
                executor.submit(self._download_one, hotel_id, url, None, None): url
                for url in image_urls[:300]  # legacy interface; extended cap (Build 90)
            }
            for future in as_completed(futures, timeout=300):
                url = futures[future]
                try:
                    results[url] = future.result()
                except Exception as exc:
                    logger.warning("Image download failed for %s: %s", url, exc)
                    results[url] = False
        return results

    def download_photo_batch(
        self,
        hotel_id: uuid.UUID,
        photos: List[Dict],
        max_workers: int = 3,
    ) -> Dict[str, int]:
        """
        Download all size variants for a list of photo dicts.

        BUG-PHOTO-LIMIT-001-FIX (Build 90):
          Cap raised from 300 (100 photos x 3 sizes) to 900 (300 photos x 3).
          extract_hotel_photos_from_html() now returns up to 270+ photos.
          Timeout scales dynamically with batch size (min 600s).

        Each photo dict contains:
          id_photo, thumb_url, large_url, highres_url,
          alt, orientation, photo_width, photo_height, created

        Saves:
          - One ImageData row per unique id_photo (photo metadata)
          - One ImageDownload row per (id_photo, category) combination

        Returns {id_photo: count_downloaded}
        """
        results: Dict[str, int] = {}

        # Persist ImageData metadata first (one row per unique photo)
        self._upsert_image_data(hotel_id, photos)

        # Build flat list of (url, id_photo, category) download tasks
        tasks: List[Tuple[str, str, str]] = []
        for photo in photos:
            pid = photo.get("id_photo", "")
            if not pid:
                continue
            for cat in ("large_url", "highres_url", "thumb_url"):
                url = photo.get(cat, "")
                if url and "bstatic.com" in url:
                    tasks.append((url, pid, cat))

        # BUG-PHOTO-LIMIT-001-FIX (Build 90): cap raised from 300→900
        # (300 photos × 3 sizes). Previous cap of 300 (100 photos × 3) was
        # calibrated for the 45-photo hotelPhotos JS limit. After the fix,
        # extract_hotel_photos_from_html() returns up to 270+ photos for large
        # hotels. Timeout scaled proportionally: 600 s → 1800 s.
        task_cap = 900
        batch_timeout = max(600, len(tasks) * 3)  # ~3s per download, min 600s
        with ThreadPoolExecutor(max_workers=min(max_workers, 4)) as executor:
            futures = {
                executor.submit(self._download_one, hotel_id, url, pid, cat): (url, pid, cat)
                for url, pid, cat in tasks[:task_cap]
            }
            for future in as_completed(futures, timeout=batch_timeout):
                url, pid, cat = futures[future]
                try:
                    ok = future.result()
                    results[pid] = results.get(pid, 0) + (1 if ok else 0)
                except Exception as exc:
                    logger.warning("Photo download failed %s/%s: %s", pid, cat, exc)
                    results[pid] = results.get(pid, 0)

        downloaded_total = sum(results.values())
        logger.info(
            "download_photo_batch: %d/%d photo-files saved for hotel %s",
            downloaded_total, len(tasks), hotel_id,
        )
        return results

    # ── Private helpers ───────────────────────────────────────────────────────

    def _upsert_image_data(self, hotel_id: uuid.UUID, photos: List[Dict]) -> None:
        """
        Persist ImageData metadata rows (one per unique id_photo).
        NEW-TABLE-001: Creates/updates image_data table records.
        """
        if not photos:
            return
        try:
            with get_db() as session:
                for photo in photos:
                    pid = str(photo.get("id_photo", "")).strip()
                    if not pid:
                        continue
                    existing = (
                        session.query(ImageData)
                        .filter_by(id_photo=pid)
                        .first()
                    )
                    if existing:
                        # Update mutable fields if richer data available
                        if photo.get("alt") and not existing.alt:
                            existing.alt = photo["alt"]
                        if photo.get("orientation") and not existing.orientation:
                            existing.orientation = photo["orientation"]
                        if photo.get("photo_width") and not existing.photo_width:
                            existing.photo_width = photo["photo_width"]
                        if photo.get("photo_height") and not existing.photo_height:
                            existing.photo_height = photo["photo_height"]
                    else:
                        # Parse created timestamp
                        created_ts: Optional[datetime] = None
                        if photo.get("created"):
                            try:
                                created_ts = datetime.fromisoformat(
                                    str(photo["created"]).replace(" ", "T")
                                ).replace(tzinfo=timezone.utc)
                            except (ValueError, AttributeError):
                                pass

                        session.add(ImageData(
                            id_photo=pid,
                            hotel_id=hotel_id,
                            orientation=photo.get("orientation"),
                            photo_width=photo.get("photo_width"),
                            photo_height=photo.get("photo_height"),
                            alt=photo.get("alt"),
                            created_at_photo=created_ts,
                        ))
        except Exception as exc:
            logger.warning("ImageData upsert failed for hotel %s: %s", hotel_id, exc)

    def _download_one(
        self,
        hotel_id: uuid.UUID,
        url: str,
        id_photo: Optional[str],
        category: Optional[str],
    ) -> bool:
        """
        Download a single image URL and persist ImageDownload record.

        BUG-IMG-401 note: url MUST include full query params (k=... auth token).
        The scraper.py fix ensures URLs are passed with params intact.
        """
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
            # Include id_photo and category in filename for easy identification
            if id_photo and category:
                filename = f"{id_photo}_{category[:5]}{ext}"
            else:
                filename = hashlib.sha256(url.encode()).hexdigest()[:24] + ext

            local_path = images_dir / filename
            local_path.write_bytes(data)

            with get_db() as session:
                existing = (
                    session.query(ImageDownload)
                    .filter_by(hotel_id=hotel_id, url=url)
                    .first()
                )
                if existing:
                    existing.local_path = str(local_path)
                    existing.file_size_bytes = len(data)
                    existing.content_type = content_type
                    existing.status = "done"
                    existing.downloaded_at = datetime.now(timezone.utc)
                    if id_photo and not existing.id_photo:
                        existing.id_photo = id_photo
                    if category and not existing.category:
                        existing.category = category
                else:
                    session.add(ImageDownload(
                        hotel_id=hotel_id,
                        id_photo=id_photo,
                        category=category,
                        url=url,
                        local_path=str(local_path),
                        file_size_bytes=len(data),
                        content_type=content_type,
                        status="done",
                        downloaded_at=datetime.now(timezone.utc),
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
                        hotel_id=hotel_id,
                        id_photo=id_photo,
                        category=category,
                        url=url,
                        status="error",
                        error_message=str(exc)[:2000],
                    ))
            return False
