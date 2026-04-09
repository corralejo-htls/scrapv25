"""
completeness_service.py — BookingScraper Pro v48
Fixes applied:
  SCRAP-BUG-023: Race condition fixed — DB operations use SELECT FOR UPDATE.
  SCRAP-BUG-034: Invalid state transitions rejected with explicit guard.
  Platform     : Windows 11 single-node.
"""

from __future__ import annotations

import logging
import uuid
from typing import Dict, List, Optional

from sqlalchemy import text

from app.database import get_db
from app.models import URLLanguageStatus, URLQueue

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Valid state machine transitions
# ---------------------------------------------------------------------------
# SCRAP-BUG-034: state transition table — only these moves are allowed
_VALID_TRANSITIONS: Dict[str, List[str]] = {
    "pending":    ["processing", "skipped"],
    "processing": ["done", "error", "incomplete"],
    "error":      ["pending", "skipped"],
    "incomplete": ["pending", "processing"],
    "done":       [],  # Terminal — no transitions allowed
    "skipped":    [],  # Terminal
}


def _is_valid_transition(current: str, new: str) -> bool:
    """Return True if the state transition is allowed."""
    return new in _VALID_TRANSITIONS.get(current, [])


class CompletenessService:
    """Tracks multi-language scraping completeness per URL."""

    def update_language_status(
        self,
        url_id: uuid.UUID,
        language: str,
        new_status: str,
        error: Optional[str] = None,
    ) -> bool:
        """
        Update the language status for a URL.
        SCRAP-BUG-023 fix: uses SELECT FOR UPDATE to prevent race conditions.
        SCRAP-BUG-034 fix: validates state transition before persisting.
        """
        with get_db() as session:
            # Lock the row during update — prevents concurrent status conflicts
            row = (
                session.query(URLLanguageStatus)
                .filter_by(url_id=url_id, language=language)
                .with_for_update()
                .first()
            )

            if row:
                # Validate transition (SCRAP-BUG-034)
                if not _is_valid_transition(row.status, new_status):
                    logger.warning(
                        "Rejected invalid state transition for url_id=%s lang=%s: %s → %s",
                        url_id, language, row.status, new_status,
                    )
                    return False

                row.status = new_status
                row.last_error = (error or "")[:2000] if error else None
                row.attempts += 1
            else:
                # New record — no current state to validate against
                row = URLLanguageStatus(
                    url_id=url_id,
                    language=language,
                    status=new_status,
                    last_error=(error or "")[:2000] if error else None,
                    attempts=1,
                )
                session.add(row)

        logger.debug("Language status updated: url_id=%s lang=%s status=%s", url_id, language, new_status)
        return True

    def get_url_completeness(self, url_id: uuid.UUID) -> Dict[str, str]:
        """Return language→status mapping for a URL."""
        with get_db() as session:
            rows = (
                session.query(URLLanguageStatus)
                .filter_by(url_id=url_id)
                .all()
            )
        return {r.language: r.status for r in rows}

    def is_fully_complete(self, url_id: uuid.UUID, required_languages: Optional[List[str]] = None) -> bool:
        """Return True if all required languages are in 'done' status."""
        from app.config import get_settings
        # BUG-ENABLED-LANGS-001-FIX (Build 86): ENABLED_LANGUAGES is a comma-separated
        # str (e.g. "en,es,de,it,fr,pt"). Iterating over it directly yielded individual
        # characters. Fixed with .split(",") to produce the correct language list.
        languages = required_languages or get_settings().ENABLED_LANGUAGES.split(",")
        statuses = self.get_url_completeness(url_id)
        return all(statuses.get(lang) == "done" for lang in languages)

    def get_incomplete_urls(self, limit: int = 100) -> List[Dict]:
        """Return URLs that have at least one language not in 'done' status."""
        with get_db() as session:
            rows = (
                session.query(URLLanguageStatus)
                .filter(URLLanguageStatus.status.notin_(["done", "skipped"]))
                .limit(limit)
                .all()
            )
        return [
            {
                "url_id": str(r.url_id),
                "language": r.language,
                "status": r.status,
                "attempts": r.attempts,
            }
            for r in rows
        ]

    def reset_errors_for_retry(self, url_id: uuid.UUID) -> int:
        """Reset errored language statuses back to pending for retry."""
        reset_count = 0
        with get_db() as session:
            rows = (
                session.query(URLLanguageStatus)
                .filter_by(url_id=url_id)
                .filter(URLLanguageStatus.status == "error")
                .with_for_update()
                .all()
            )
            for row in rows:
                if _is_valid_transition(row.status, "pending"):
                    row.status = "pending"
                    row.attempts = 0
                    row.last_error = None
                    reset_count += 1
        return reset_count
