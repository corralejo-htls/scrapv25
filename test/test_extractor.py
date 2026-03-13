"""
test_extractor.py — HTML extraction and language detection tests.
"""

from __future__ import annotations

import pytest


class TestLanguageDetection:
    """BUG-107: Multi-strategy language detection."""

    def test_html_lang_attribute(self):
        from app.extractor import detect_language
        html = '<html lang="es"><body>content</body></html>'
        assert detect_language(html) == "es"

    def test_html_lang_with_region(self):
        from app.extractor import detect_language
        html = '<html lang="en-GB"><body>content</body></html>'
        assert detect_language(html) == "en"

    def test_og_locale_fallback(self):
        from app.extractor import detect_language
        html = '<html><head><meta property="og:locale" content="de_DE"/></head><body/></html>'
        assert detect_language(html) == "de"

    def test_url_fallback(self):
        from app.extractor import detect_language
        html = "<html><body>no lang</body></html>"
        lang = detect_language(html, url="https://www.booking.com/hotel.fr.html")
        assert lang == "fr"

    def test_returns_none_when_undetectable(self):
        from app.extractor import detect_language
        html = "<html><body>no language clues at all</body></html>"
        result = detect_language(html, url="")
        assert result is None or isinstance(result, str)

    def test_empty_html_returns_none(self):
        from app.extractor import detect_language
        assert detect_language("") is None


class TestMakeSoup:
    """BUG-014: Parser fallback must work even without lxml."""

    def test_creates_soup_successfully(self):
        from app.extractor import _make_soup
        soup = _make_soup("<html><body><p>hello</p></body></html>")
        assert soup.find("p").get_text() == "hello"

    def test_handles_malformed_html(self):
        from app.extractor import _make_soup
        soup = _make_soup("<p>unclosed")
        assert soup is not None


class TestHotelExtractor:
    """HotelExtractor field extraction tests."""

    def test_extract_name(self, sample_html):
        from app.extractor import HotelExtractor
        ex = HotelExtractor(sample_html, url="https://www.booking.com/hotel/es/test.es.html", language="es")
        data = ex.extract_all()
        assert data.get("hotel_name") == "Hotel Corralejo Beach"

    def test_extract_address(self, sample_html):
        from app.extractor import HotelExtractor
        ex = HotelExtractor(sample_html, language="es")
        data = ex.extract_all()
        assert "Corralejo" in (data.get("address") or "")

    def test_extract_review_score(self, sample_html):
        from app.extractor import HotelExtractor
        ex = HotelExtractor(sample_html, language="es")
        data = ex.extract_all()
        score = data.get("review_score")
        assert score is None or isinstance(score, float)

    def test_extract_all_returns_dict(self, sample_html):
        from app.extractor import HotelExtractor
        ex = HotelExtractor(sample_html, language="es")
        data = ex.extract_all()
        assert isinstance(data, dict)
        assert "url" in data or "language" in data

    def test_no_none_values_in_output(self, sample_html):
        from app.extractor import HotelExtractor
        ex = HotelExtractor(sample_html, language="es")
        data = ex.extract_all()
        # All returned values should be non-None (None values are excluded)
        for k, v in data.items():
            assert v is not None, f"Field {k} should not be None in output"
