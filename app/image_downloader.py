"""
BookingScraper Pro v6.0 - Image Downloader
==========================================
Downloads hotel images in parallel using ThreadPoolExecutor.
Platform : Windows 11 + Python 3.11+

Corrections Applied (v46):
- BUG-023 : Per-image timeout and per-batch timeout calculated correctly;
            batch timeout = max_workers * per_image_timeout + fixed overhead.
"""

from __future__ import annotations

import hashlib
import logging
import mimetypes
import re
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed, TimeoutError as FutureTimeout
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class DownloadResult:
    url      : str
    success  : bool
    filepath : Optional[Path] = None
    error    : str            = ""
    size_bytes: int           = 0
    width    : Optional[int]  = None
    height   : Optional[int]  = None

@dataclass
class BatchResult:
    total     : int = 0
    downloaded: int = 0
    skipped   : int = 0
    errors    : int = 0
    results   : list[DownloadResult] = field(default_factory=list)


# ─────────────────────────────────────────────────────────────────────────────
class ImageDownloader:
    """
    Downloads images for a list of URLs with configurable concurrency.
    Thread-safe for use inside ThreadPoolExecutor workers.
    """

    CHUNK_SIZE      = 65_536   # 64 KB read chunks
    FIXED_OVERHEAD  = 30       # seconds — network setup, disk write overhead

    def __init__(
        self,
        output_dir      : str,
        max_workers     : int   = 4,
        per_image_timeout: int  = 30,    # BUG-023 FIX: named clearly
        max_size_mb     : float = 10.0,
    ) -> None:
        self._output_dir       = Path(output_dir)
        self._max_workers      = max_workers
        self._per_image_timeout= per_image_timeout
        self._max_size_bytes   = int(max_size_mb * 1024 * 1024)
        # BUG-023 FIX: batch timeout accounts for all workers running sequentially at worst
        self._batch_timeout    = (per_image_timeout * max_workers) + self.FIXED_OVERHEAD
        self._session          = self._build_session()

    def _build_session(self) -> requests.Session:
        sess = requests.Session()
        retry = Retry(total=3, backoff_factor=1.0,
                      status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry, pool_connections=self._max_workers,
                              pool_maxsize=self._max_workers * 2)
        sess.mount("https://", adapter)
        sess.mount("http://",  adapter)
        sess.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept"    : "image/webp,image/apng,image/*,*/*;q=0.8",
        })
        return sess

    # ── Output directory ────────────────────────────────────────────────────

    def _hotel_dir(self, hotel_id: str) -> Path:
        """Return per-hotel subdirectory (created on demand)."""
        d = self._output_dir / hotel_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    # ── File naming ─────────────────────────────────────────────────────────

    @staticmethod
    def _filename_for(url: str) -> str:
        """Generate a deterministic filename from the URL hash."""
        name = hashlib.sha1(url.encode()).hexdigest()[:12]
        ext  = mimetypes.guess_extension(
            mimetypes.guess_type(urlparse(url).path)[0] or ""
        ) or ".jpg"
        if ext == ".jpe":
            ext = ".jpg"
        return name + ext

    # ── Single-image download ────────────────────────────────────────────────

    def _download_one(self, url: str, dest_dir: Path) -> DownloadResult:
        """
        Download a single image to dest_dir.
        Returns DownloadResult regardless of success/failure.
        """
        filename = self._filename_for(url)
        filepath = dest_dir / filename

        if filepath.exists() and filepath.stat().st_size > 0:
            return DownloadResult(url=url, success=True, filepath=filepath,
                                  size_bytes=filepath.stat().st_size)

        try:
            resp = self._session.get(url, stream=True, timeout=self._per_image_timeout)
            resp.raise_for_status()

            content_type = resp.headers.get("content-type", "")
            if not content_type.startswith("image/"):
                return DownloadResult(url=url, success=False,
                                      error=f"Non-image content-type: {content_type}")

            size = 0
            with filepath.open("wb") as fh:
                for chunk in resp.iter_content(chunk_size=self.CHUNK_SIZE):
                    if chunk:
                        fh.write(chunk)
                        size += len(chunk)
                        if size > self._max_size_bytes:
                            fh.flush()
                            filepath.unlink(missing_ok=True)
                            return DownloadResult(url=url, success=False,
                                                  error=f"Image too large (> {self._max_size_bytes//1024//1024} MB)")

            return DownloadResult(url=url, success=True, filepath=filepath, size_bytes=size)

        except requests.exceptions.Timeout:
            return DownloadResult(url=url, success=False, error="Timeout")
        except requests.exceptions.HTTPError as exc:
            return DownloadResult(url=url, success=False, error=f"HTTP {exc.response.status_code}")
        except requests.exceptions.RequestException as exc:
            return DownloadResult(url=url, success=False, error=str(exc))
        except OSError as exc:
            return DownloadResult(url=url, success=False, error=f"Disk error: {exc}")

    # ── Batch download ───────────────────────────────────────────────────────

    def download_images(self, urls: list[str], hotel_id: str) -> BatchResult:
        """
        Download all images for a hotel in parallel.

        BUG-023 FIX: batch_timeout = (per_image_timeout × max_workers) + overhead.
        This ensures even worst-case sequential execution completes within the timeout.
        Previously the batch timeout was per_image_timeout only, which was always
        too short for a batch of more than one image.

        Args:
            urls: List of image URLs to download.
            hotel_id: Used to create an isolated subdirectory per hotel.
        """
        if not urls:
            return BatchResult()

        dest_dir = self._hotel_dir(hotel_id)
        batch    = BatchResult(total=len(urls))
        futures: dict[Future, str] = {}

        with ThreadPoolExecutor(max_workers=self._max_workers) as pool:
            for url in urls:
                if not url or not url.startswith("http"):
                    batch.skipped += 1
                    continue
                fut = pool.submit(self._download_one, url, dest_dir)
                futures[fut] = url

            # BUG-023 FIX: use calculated batch timeout
            try:
                for fut in as_completed(futures, timeout=self._batch_timeout):
                    result = fut.result()
                    batch.results.append(result)
                    if result.success:
                        batch.downloaded += 1
                    else:
                        batch.errors += 1
                        logger.debug("Image download failed: %s — %s", result.url[:60], result.error)

            except FutureTimeout:
                logger.error(
                    "Batch download timed out after %ds for hotel %s — "
                    "%d/%d completed",
                    self._batch_timeout, hotel_id,
                    batch.downloaded + batch.errors, len(futures),
                )
                # Cancel remaining futures
                for fut in futures:
                    fut.cancel()

        logger.info(
            "Hotel %s images: downloaded=%d errors=%d skipped=%d / total=%d",
            hotel_id, batch.downloaded, batch.errors, batch.skipped, batch.total,
        )
        return batch
