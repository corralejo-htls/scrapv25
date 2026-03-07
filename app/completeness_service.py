"""
BookingScraper Pro v6.0 - Completeness Service
===============================================
Tracks and manages per-language scraping completeness for each URL.

Corrections Applied (v46):
- BUG-022 : MAX_LANG_RETRIES was hardcoded to 1.
            Now read from settings (default 3) so it is configurable via .env.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models import URLLanguageStatus, URLQueue

logger = logging.getLogger(__name__)


def _settings():
    from app.config import get_settings
    return get_settings()


# ─────────────────────────────────────────────────────────────────────────────
class CompletenessService:
    """
    Manages language-level tracking for each URL in the scraping queue.

    Completeness = all ENABLED_LANGUAGES have status='done' for a given url_id.

    BUG-022 FIX: MAX_LANG_RETRIES is read from settings (env var MAX_LANG_RETRIES),
    defaulting to 3. It was previously hardcoded to 1 in this module.
    """

    def __init__(self) -> None:
        cfg = _settings()
        # BUG-022 FIX: configurable via .env
        self._max_retries  = cfg.MAX_LANG_RETRIES
        self._languages    = cfg.ENABLED_LANGUAGES
        logger.debug(
            "CompletenessService init: languages=%s max_retries=%d",
            self._languages, self._max_retries,
        )

    # ── Initialisation ───────────────────────────────────────────────────────

    def initialise_url(self, session: Session, url_id: uuid.UUID) -> list[URLLanguageStatus]:
        """
        Create URLLanguageStatus rows for all enabled languages for a new url_id.
        Idempotent — skips languages that already have a row.
        """
        existing = {
            row.language
            for row in session.query(URLLanguageStatus)
            .filter(URLLanguageStatus.url_id == url_id)
            .all()
        }
        new_rows: list[URLLanguageStatus] = []
        for lang in self._languages:
            if lang not in existing:
                row = URLLanguageStatus(
                    url_id   =url_id,
                    language =lang,
                    status   ="pending",
                )
                session.add(row)
                new_rows.append(row)
        if new_rows:
            session.flush()
            logger.debug("Initialised %d language rows for url_id=%s", len(new_rows), url_id)
        return new_rows

    # ── Status transitions ───────────────────────────────────────────────────

    def mark_processing(self, session: Session, url_id: uuid.UUID, language: str) -> bool:
        """Mark a language status as 'processing'. Returns True on success."""
        row = self._get_row(session, url_id, language)
        if row is None:
            logger.warning("No status row for url_id=%s lang=%s", url_id, language)
            return False
        row.status = "processing"
        row.version_id += 1
        session.flush()
        return True

    def mark_done(self, session: Session, url_id: uuid.UUID, language: str) -> bool:
        """Mark a language as successfully scraped."""
        row = self._get_row(session, url_id, language)
        if row is None:
            return False
        row.status       = "done"
        row.completed_at = datetime.now(timezone.utc)
        row.last_error   = None
        row.version_id  += 1
        session.flush()
        self._maybe_complete_url(session, url_id)
        return True

    def mark_error(self, session: Session, url_id: uuid.UUID, language: str,
                   error: str = "") -> bool:
        """
        Mark a language as errored.
        If retries are exhausted, marks as 'skipped' instead of 'error'
        so the completeness check can still succeed.
        """
        row = self._get_row(session, url_id, language)
        if row is None:
            return False
        row.attempt_count += 1
        row.last_error     = error[:2000] if error else ""
        row.version_id    += 1

        # BUG-022 FIX: use configurable max_retries
        if row.attempt_count >= self._max_retries:
            row.status = "skipped"
            logger.info(
                "url_id=%s lang=%s skipped after %d attempts", url_id, language, row.attempt_count
            )
        else:
            row.status = "error"

        session.flush()
        self._maybe_complete_url(session, url_id)
        return True

    # ── Completeness check ───────────────────────────────────────────────────

    def is_complete(self, session: Session, url_id: uuid.UUID) -> bool:
        """
        Return True if all enabled languages are done or skipped.
        A URL is 'complete' when no language is in pending/processing/error state.
        """
        rows = (
            session.query(URLLanguageStatus)
            .filter(URLLanguageStatus.url_id == url_id)
            .all()
        )
        if not rows:
            return False
        return all(r.status in ("done", "skipped") for r in rows)

    def pending_languages(self, session: Session, url_id: uuid.UUID) -> list[str]:
        """Return list of languages not yet done/skipped for a given URL."""
        rows = (
            session.query(URLLanguageStatus)
            .filter(
                URLLanguageStatus.url_id == url_id,
                URLLanguageStatus.status.in_(["pending", "error"]),
            )
            .all()
        )
        return [r.language for r in rows]

    # ── Helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _get_row(session: Session, url_id: uuid.UUID,
                 language: str) -> Optional[URLLanguageStatus]:
        return (
            session.query(URLLanguageStatus)
            .filter(
                URLLanguageStatus.url_id  == url_id,
                URLLanguageStatus.language == language,
            )
            .first()
        )

    def _maybe_complete_url(self, session: Session, url_id: uuid.UUID) -> None:
        """If all languages are done/skipped, mark the parent URLQueue row as done."""
        if not self.is_complete(session, url_id):
            return
        queue_row = session.query(URLQueue).filter(URLQueue.id == url_id).first()
        if queue_row and queue_row.status != "done":
            queue_row.status       = "done"
            queue_row.completed_at = datetime.now(timezone.utc)
            queue_row.version_id  += 1
            session.flush()
            logger.info("url_id=%s marked done (all languages complete)", url_id)
