"""
BookingScraper/app/image_downloader.py
Image Download Engine — BookingScraper Pro
Windows 11 + Python 3.14.3

[FIX BUG-V9-002] This module was completely absent from the repository.
scraper_service.py imports ImageDownloader at line 868 inside _download_images(),
causing ModuleNotFoundError for every hotel when DOWNLOAD_IMAGES=True.

CONTRACT:
    dl = ImageDownloader()
    results: List[Path] = dl.download_images(
        url_id:   int,
        img_urls: List[str],
        language: str,
        session:  requests.Session,     # optional — created internally if None
    )

DESIGN:
    - ThreadPoolExecutor for parallel downloads (MAX_IMAGE_WORKERS from settings)
    - JPEG quality and max dimensions from settings (IMAGE_QUALITY, IMAGE_MAX_WIDTH/HEIGHT)
    - Images saved to: settings.IMAGES_PATH / str(url_id) / <language> / <filename>.jpg
    - Idempotent: existing files are skipped (no re-download)
    - Returns list of Path objects for successfully saved images
"""

from __future__ import annotations

import hashlib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

import requests
from loguru import logger

from app.config import settings


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_DOWNLOAD_TIMEOUT  = 15      # seconds per image request
_MAX_REDIRECTS     = 5
_CHUNK_SIZE        = 65_536  # 64 KB streaming chunks
_HEADERS = {
    "User-Agent":      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept":          "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer":         "https://www.booking.com/",
    "sec-fetch-dest":  "image",
    "sec-fetch-mode":  "no-cors",
    "sec-fetch-site":  "cross-site",
}


# ---------------------------------------------------------------------------
# ImageDownloader
# ---------------------------------------------------------------------------
class ImageDownloader:
    """
    Downloads hotel images from a list of URLs and saves them to disk.

    Storage layout:
        <IMAGES_PATH>/<url_id>/<language>/<hash>.jpg

    Usage:
        dl = ImageDownloader()
        saved = dl.download_images(url_id=42, img_urls=[...], language="en")
    """

    def __init__(self) -> None:
        self._quality    = settings.IMAGE_QUALITY      # JPEG quality 1-95
        self._max_w      = settings.IMAGE_MAX_WIDTH
        self._max_h      = settings.IMAGE_MAX_HEIGHT
        self._max_workers = settings.MAX_IMAGE_WORKERS
        self._base_path  = Path(settings.IMAGES_PATH)

    # ──────────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────────

    def download_images(
        self,
        url_id:   int,
        img_urls: List[str],
        language: str = "en",
        session:  Optional[requests.Session] = None,
    ) -> List[Path]:
        """
        Download a list of image URLs and save them to disk.

        Args:
            url_id:    Hotel URL primary key — determines storage subdirectory.
            img_urls:  List of HTTP/HTTPS image URLs to download.
            language:  Language tag used in the subdirectory path.
            session:   Optional requests.Session with auth cookies pre-loaded.
                       If None, a plain session is created internally.

        Returns:
            List[Path]: Paths of successfully saved image files.

        Raises:
            Never — errors are logged and skipped individually.
        """
        if not img_urls:
            return []

        # [FIX C007] Path traversal protection on 'language' and 'url_id' parameters.
        # An attacker controlling language could inject "../../../Windows/System32".
        # Strategy: (1) sanitize to alphanumeric+hyphen only, (2) resolve absolute path,
        # (3) verify the resolved path is inside _base_path (is_relative_to check).
        _safe_lang = "".join(c for c in str(language) if c.isalnum() or c in ("-", "_"))[:10]
        if not _safe_lang:
            _safe_lang = "unknown"
        _safe_uid  = str(int(url_id))  # int() ensures no path characters possible
        save_dir = (self._base_path / _safe_uid / _safe_lang).resolve()
        if not save_dir.is_relative_to(self._base_path.resolve()):
            raise RuntimeError(
                f"[C007] Path traversal attempt blocked: "
                f"url_id={url_id!r} language={language!r} → {save_dir}"
            )
        save_dir.mkdir(parents=True, exist_ok=True)

        own_session = session is None
        if own_session:
            session = requests.Session()
            session.headers.update(_HEADERS)
            session.max_redirects = _MAX_REDIRECTS

        results: List[Path] = []

        # [FIX BUG-16-012] Overall batch timeout prevents the ThreadPoolExecutor
        # from hanging indefinitely when one download stalls beyond _DOWNLOAD_TIMEOUT.
        # Per-request timeout (_DOWNLOAD_TIMEOUT=15s) guards the HTTP read, but
        # network TCP stalls can bypass requests timeouts. The batch timeout is set to
        # (per_image_timeout + 5s buffer) × max_workers to allow all slots to complete
        # their individual timeouts before abandoning the batch.
        _BATCH_TIMEOUT = (_DOWNLOAD_TIMEOUT + 5) * self._max_workers

        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            futures = {
                executor.submit(
                    self._download_one, session, url, save_dir, idx
                ): url
                for idx, url in enumerate(img_urls)
            }
            try:
                for future in as_completed(futures, timeout=_BATCH_TIMEOUT):
                    url = futures[future]
                    try:
                        path = future.result()
                        if path:
                            results.append(path)
                    except Exception as exc:
                        logger.debug(f"[image_downloader] [{url_id}] {url[:80]}: {exc}")
            except TimeoutError:
                pending = sum(1 for f in futures if not f.done())
                logger.warning(
                    f"[image_downloader] [{url_id}] Batch timeout ({_BATCH_TIMEOUT}s): "
                    f"{len(results)} downloaded, {pending} abandoned."
                )
                # Cancel remaining futures — executor.shutdown(wait=False) called by context manager
                for f in futures:
                    f.cancel()

        if own_session:
            session.close()

        logger.info(
            f"[image_downloader] [{url_id}][{language}] "
            f"{len(results)}/{len(img_urls)} images saved → {save_dir}"
        )
        return results

    # ──────────────────────────────────────────────────────────────────────
    # Internal
    # ──────────────────────────────────────────────────────────────────────

    def _download_one(
        self,
        session:  requests.Session,
        url:      str,
        save_dir: Path,
        idx:      int,
    ) -> Optional[Path]:
        """
        Download a single image URL and save it to save_dir.

        Args:
            session:  Shared requests.Session (thread-safe for reads).
            url:      Image URL to fetch.
            save_dir: Target directory for saved file.
            idx:      Index in the original list (used for filename collision
                      resolution when hash collides).

        Returns:
            Path of saved file, or None on failure.
        """
        filename = self._url_to_filename(url, idx)
        dest     = save_dir / filename

        # Idempotent: skip if already downloaded
        if dest.exists() and dest.stat().st_size > 0:
            return dest

        try:
            resp = session.get(url, timeout=_DOWNLOAD_TIMEOUT, stream=True)
            resp.raise_for_status()

            content_type = resp.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                logger.debug(
                    f"[image_downloader] Skipped non-image response "
                    f"({content_type}) for {url[:80]}"
                )
                return None

            # Stream to a temp buffer then process
            raw_bytes = b"".join(resp.iter_content(chunk_size=_CHUNK_SIZE))

            saved = self._save_image(raw_bytes, dest)
            return saved

        except requests.exceptions.Timeout:
            logger.debug(f"[image_downloader] Timeout fetching {url[:80]}")
        except requests.exceptions.HTTPError as exc:
            logger.debug(f"[image_downloader] HTTP {exc.response.status_code} for {url[:80]}")
        except Exception as exc:
            logger.debug(f"[image_downloader] Unexpected error for {url[:80]}: {exc}")

        return None

    def _save_image(self, raw_bytes: bytes, dest: Path) -> Optional[Path]:
        """
        Resize if needed and save as JPEG.

        Falls back to raw bytes save if Pillow is not available.

        Args:
            raw_bytes: Downloaded image bytes.
            dest:      Target file path (.jpg).

        Returns:
            Path on success, None on failure.
        """
        try:
            from PIL import Image
            import io

            # [FIX H008] Integrity checks before processing:
            # 1. Minimum size guard: < 500 bytes is almost certainly not a real image.
            # 2. Image.verify() reads the full file stream to detect corruption and
            #    truncation (partial downloads). Requires re-opening after verify().
            if len(raw_bytes) < 500:
                logger.debug(
                    "[H008] Rejected image: %d bytes is below minimum (likely not an image)",
                    len(raw_bytes),
                )
                return None
            try:
                _probe = Image.open(io.BytesIO(raw_bytes))
                _probe.verify()  # Checks entire byte stream; raises on truncation/corruption
            except Exception as _verify_err:
                logger.debug("[H008] Image integrity check failed: %s", _verify_err)
                return None

            # Re-open after verify() (verify() leaves file pointer at EOF)
            img = Image.open(io.BytesIO(raw_bytes))

            # Convert palette/RGBA to RGB for JPEG compatibility
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")

            # Resize only if exceeds max dimensions (preserve aspect ratio)
            w, h = img.size
            if w > self._max_w or h > self._max_h:
                img.thumbnail((self._max_w, self._max_h), Image.LANCZOS)

            img.save(dest, "JPEG", quality=self._quality, optimize=True)
            return dest

        except ImportError:
            # Pillow not installed — save raw bytes directly
            dest.write_bytes(raw_bytes)
            return dest

        except Exception as exc:
            logger.debug(f"[image_downloader] Error saving {dest.name}: {exc}")
            # Last resort: save raw bytes
            try:
                dest.write_bytes(raw_bytes)
                return dest
            except OSError:
                return None

    @staticmethod
    def _url_to_filename(url: str, idx: int) -> str:
        """
        Derive a stable, filesystem-safe filename from an image URL.

        Uses first 12 chars of MD5 hash of the URL to avoid name collisions
        between hotels sharing the same CDN path structure.

        Args:
            url: Image URL.
            idx: Ordinal index (appended if hash is empty).

        Returns:
            Filename string ending in '.jpg'.
        """
        try:
            path_part = urlparse(url).path
            base = Path(path_part).stem[:40]   # trim to 40 chars max
            url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
            name = f"{base}_{url_hash}.jpg" if base else f"img_{idx:04d}_{url_hash}.jpg"
            # Replace any remaining unsafe chars
            import re
            name = re.sub(r"[^\w.\-]", "_", name)
            return name
        except Exception:
            return f"img_{idx:04d}_{int(time.time())}.jpg"
