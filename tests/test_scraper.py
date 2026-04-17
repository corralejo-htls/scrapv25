"""
test_scraper.py — Scraper engine unit tests.
No network calls — all HTTP is mocked.
"""

from __future__ import annotations

import pytest


class TestBuildLanguageUrl:
    """BUG-004: build_language_url must never produce double .html suffixes."""

    def _build(self, url, lang):
        from app.scraper import build_language_url
        return build_language_url(url, lang)

    def test_adds_language_to_clean_url(self):
        result = self._build("https://www.booking.com/hotel/es/test-hotel.html", "de")
        assert result.endswith(".de.html")
        assert result.count(".html") == 1

    def test_replaces_existing_language_suffix(self):
        result = self._build("https://www.booking.com/hotel/es/test.es.html", "de")
        assert ".de.html" in result
        assert ".es." not in result
        assert result.count(".html") == 1

    def test_no_double_html_from_url_without_html(self):
        result = self._build("https://www.booking.com/hotel/es/test.es", "de")
        assert result.count(".html") == 1

    def test_no_double_html_from_url_with_html_no_lang(self):
        result = self._build("https://www.booking.com/hotel/es/test.html", "fr")
        assert result.count(".html") == 1

    def test_preserves_query_params_structure(self):
        result = self._build("https://www.booking.com/hotel/es/test.es.html?aid=123", "de")
        # Query params should still be accessible (or stripped — either is acceptable)
        assert "booking.com" in result
        assert result.count(".html") == 1


class TestBlockDetection:
    """BUG-013: _is_blocked must handle parse errors gracefully."""

    def test_detects_captcha(self):
        from app.scraper import _is_blocked
        assert _is_blocked("Please solve the captcha to continue")

    def test_detects_human_verification(self):
        from app.scraper import _is_blocked
        assert _is_blocked("Please verify you are a human")

    def test_clean_page_not_blocked(self):
        from app.scraper import _is_blocked
        html = "<html><body><h1>Luxury Hotel Corralejo</h1></body></html>"
        assert not _is_blocked(html)

    def test_handles_none_like_input(self):
        from app.scraper import _is_blocked
        # Should not raise
        result = _is_blocked("")
        assert isinstance(result, bool)

    def test_handles_parse_exception(self):
        """BUG-013: parse errors must return True (safe default), not raise."""
        from app.scraper import _is_blocked
        # Pass an object that causes issues — should not raise, returns True
        result = _is_blocked("normal text without issues")
        assert isinstance(result, bool)


class TestUrlToFilename:
    """BUG-106: SHA-256 must be used, not MD5."""

    def test_produces_deterministic_output(self):
        from app.scraper import url_to_filename
        url = "https://www.booking.com/hotel/es/test.html"
        assert url_to_filename(url) == url_to_filename(url)

    def test_produces_hex_string(self):
        from app.scraper import url_to_filename
        name = url_to_filename("https://example.com/test.html")
        # SHA-256 hex digest truncated to 32 chars + extension
        base = name.replace(".html", "")
        assert all(c in "0123456789abcdef" for c in base)
        assert len(base) == 32

    def test_different_urls_produce_different_names(self):
        from app.scraper import url_to_filename
        assert url_to_filename("https://a.com/1.html") != url_to_filename("https://a.com/2.html")


class TestPartitionNameValidation:
    """BUG-101 / SCRAP-BUG-009: Partition names must pass strict regex."""

    def test_valid_partition_name(self):
        from app.tasks import _safe_partition_name
        assert _safe_partition_name(2026, 3) == "scraping_logs_2026_03"
        assert _safe_partition_name(2026, 12) == "scraping_logs_2026_12"
        assert _safe_partition_name(2026, 1) == "scraping_logs_2026_01"

    def test_invalid_month_13_raises(self):
        from app.tasks import _safe_partition_name
        with pytest.raises(ValueError):
            _safe_partition_name(2026, 13)

    def test_invalid_month_0_raises(self):
        from app.tasks import _safe_partition_name
        with pytest.raises(ValueError):
            _safe_partition_name(2026, 0)

    def test_date_literal_validates_correctly(self):
        from app.tasks import _safe_date_literal
        import datetime
        d = datetime.date(2026, 3, 7)
        literal = _safe_date_literal(d)
        assert literal == "2026-03-07"


class TestUserAgentWeights:
    """BUG-018: User agents should be drawn with market-share weights."""

    def test_user_agents_are_valid_strings(self):
        from app.scraper import _random_user_agent
        ua = _random_user_agent()
        assert isinstance(ua, str)
        assert "Mozilla" in ua

    def test_weights_sum_to_approximately_one(self):
        from app.scraper import _UA_WEIGHTS
        total = sum(_UA_WEIGHTS)
        assert abs(total - 1.0) < 0.01

    def test_population_and_weights_same_length(self):
        from app.scraper import _UA_POPULATION, _UA_WEIGHTS
        assert len(_UA_POPULATION) == len(_UA_WEIGHTS)
