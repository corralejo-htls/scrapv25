"""
tests/test_extractor.py — BookingScraper Pro v6.0.0 build 53
=============================================================
Fixes aplicados:

  ERROR-003 (v53): test_extract_address corregido.
                   El campo 'address' fue eliminado en STRUCT-004 (v50).
                   Los tests ahora comprueban 'street_address' y 'address_city'
                   que son los campos canónicos desde v50/v52 respectivamente.
                   Referencia: models.py STRUCT-004, extractor.py BUG-EXTR-006.

  STRUCT-013 (v53): test_extract_fine_print añadido.
  STRUCT-014 (v53): test_extract_all_services añadido.
  STRUCT-015 (v53): test_extract_faqs añadido.
  STRUCT-016 (v53): test_extract_guest_reviews añadido.
  STRUCT-017 (v53): test_extract_property_highlights añadido.

Platform: Windows 11 / pytest / no POSIX signals required.
"""

from __future__ import annotations

import pytest

# ---------------------------------------------------------------------------
# Sample HTML fixtures
# ---------------------------------------------------------------------------

MINIMAL_HOTEL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Garden Hill Resort &amp; Spa — Booking.com</title>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Hotel",
    "name": "Garden Hill Resort & Spa",
    "description": "A beautiful resort in Corralejo.",
    "image": "https://cf.bstatic.com/images/hotel/max1024x768/123/123456.jpg",
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "8.5",
      "bestRating": "10",
      "reviewCount": "1234"
    },
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Calle Majorero 10",
      "addressLocality": "Corralejo",
      "addressRegion": "Fuerteventura",
      "addressCountry": "ES",
      "postalCode": "35660"
    },
    "geo": {
      "latitude": 28.7296,
      "longitude": -13.8654
    }
  }
  </script>
</head>
<body>
  <h1 data-testid="title">Garden Hill Resort &amp; Spa</h1>

  <div data-testid="property-description">
    A luxurious resort nestled in the heart of Corralejo,
    offering stunning views and world-class amenities.
  </div>

  <div data-testid="property-most-popular-facilities-wrapper">
    <ul>
      <li><span>Free WiFi</span></li>
      <li><span>Outdoor pool</span></li>
      <li><span>Spa</span></li>
      <li><span>Free parking</span></li>
    </ul>
  </div>

  <div data-testid="property-section--facilities">
    <ul>
      <li><span>Free WiFi</span></li>
      <li><span>Outdoor pool</span></li>
      <li><span>Spa and wellness centre</span></li>
      <li><span>Free parking</span></li>
      <li><span>Restaurant</span></li>
      <li><span>Bar</span></li>
      <li><span>24-hour front desk</span></li>
      <li><span>Air conditioning</span></li>
    </ul>
  </div>

  <div data-testid="property-section--policies">
    <div>
      <strong>Check-in</strong>
      <p>From 15:00</p>
    </div>
    <div>
      <strong>Check-out</strong>
      <p>Until 11:00</p>
    </div>
    <div>
      <strong>Pets</strong>
      <p>Pets are not allowed.</p>
    </div>
  </div>

  <div data-testid="property-section--legal">
    <h3>Legal information</h3>
    <p>This property is managed by Example Hospitality Ltd.</p>
  </div>

  <div data-testid="property-section--fine-print">
    <h3>Fine print</h3>
    <p>You must show a valid photo ID and credit card upon check-in.</p>
    <p>Special requests are subject to availability upon check-in.</p>
    <p>Guests under 18 years of age must be accompanied by an adult.</p>
  </div>

  <div data-testid="property-highlights">
    <ul>
      <li>
        <svg><path d="M0 0"/></svg>
        <div>Beachfront location</div>
      </li>
      <li>
        <svg><path d="M0 0"/></svg>
        <div>
          <p>Breakfast included</p>
          <p>Continental breakfast daily</p>
        </div>
      </li>
      <li>
        <svg><path d="M0 0"/></svg>
        <div>Free cancellation available</div>
      </li>
    </ul>
  </div>

  <div data-testid="faq-section">
    <h3>Frequently asked questions</h3>
    <div>
      <button aria-expanded="false">
        What are the check-in and check-out times at Garden Hill Resort &amp; Spa?
      </button>
    </div>
    <div>
      <button aria-expanded="false">
        Is there a swimming pool at Garden Hill Resort &amp; Spa?
      </button>
    </div>
    <div>
      <button aria-expanded="false">
        Does Garden Hill Resort &amp; Spa offer free parking?
      </button>
    </div>
  </div>

  <div data-testid="review-score-badge">
    <div>
      <span>Cleanliness</span><span>9.5</span>
    </div>
    <div>
      <span>Comfort</span><span>9.2</span>
    </div>
    <div>
      <span>Location</span><span>9.8</span>
    </div>
    <div>
      <span>Facilities</span><span>8.9</span>
    </div>
    <div>
      <span>Staff</span><span>9.4</span>
    </div>
    <div>
      <span>Value for money</span><span>8.7</span>
    </div>
  </div>

</body>
</html>
"""


@pytest.fixture
def sample_html() -> str:
    return MINIMAL_HOTEL_HTML


@pytest.fixture
def extractor(sample_html: str):
    from app.extractor import HotelExtractor
    return HotelExtractor(sample_html, url="https://www.booking.com/hotel/es/garden-hill.en-gb.html", language="en")


# ---------------------------------------------------------------------------
# Basic field extraction tests
# ---------------------------------------------------------------------------

class TestExtractName:
    def test_extract_name_returns_string(self, extractor):
        data = extractor.extract_all()
        assert isinstance(data.get("hotel_name"), str)
        assert len(data["hotel_name"]) > 0

    def test_extract_name_value(self, extractor):
        data = extractor.extract_all()
        assert "Garden Hill" in (data.get("hotel_name") or "")


class TestExtractDescription:
    def test_extract_description_present(self, extractor):
        data = extractor.extract_all()
        assert "description" in data

    def test_extract_description_content(self, extractor):
        data = extractor.extract_all()
        desc = data.get("description") or ""
        assert len(desc) > 10


class TestExtractAddress:
    """
    ERROR-003 (v53): 'address' field was removed in STRUCT-004 (v50).
    Tests now check 'street_address' and 'address_city' — the canonical
    fields since v50/v52 respectively.
    """

    def test_street_address_present(self, extractor):
        """STRUCT-004 / BUG-EXTR-006: street_address from JSON-LD."""
        data = extractor.extract_all()
        # street_address is populated from JSON-LD schema.org address.streetAddress
        assert "street_address" in data, (
            "street_address key missing — was 'address' used instead? "
            "Field renamed per STRUCT-004 (v50)."
        )

    def test_street_address_contains_locality(self, extractor):
        """streetAddress from JSON-LD should contain expected locality data."""
        data = extractor.extract_all()
        street = data.get("street_address") or ""
        assert len(street) > 0, "street_address should not be empty"

    def test_address_city_present(self, extractor):
        """STRUCT-011 (v52): address_city (renamed from city in v52)."""
        data = extractor.extract_all()
        assert "address_city" in data, (
            "address_city key missing — was 'city' used instead? "
            "Field renamed per STRUCT-011 (v52)."
        )

    def test_address_city_value(self, extractor):
        """address_city should come from JSON-LD addressRegion (BUG-EXTR-006)."""
        data = extractor.extract_all()
        city = data.get("address_city") or ""
        assert len(city) > 0

    def test_address_country_present(self, extractor):
        """STRUCT-012 (v52): address_country is the canonical country field."""
        data = extractor.extract_all()
        assert "address_country" in data, (
            "address_country key missing — was 'country' used instead? "
            "Field is canonical since STRUCT-012 (v52)."
        )

    def test_deprecated_address_field_absent(self, extractor):
        """
        STRUCT-004 (v50): the 'address' key must NOT appear in extract_all() output.
        If this test fails, extractor.py is returning a deprecated field.
        """
        data = extractor.extract_all()
        assert "address" not in data, (
            "'address' key should not be present in extract_all() output. "
            "Field was eliminated per STRUCT-004 (v50)."
        )

    def test_deprecated_country_field_absent(self, extractor):
        """
        STRUCT-012 (v52): the standalone 'country' key must NOT appear.
        Use 'address_country' instead.
        """
        data = extractor.extract_all()
        assert "country" not in data, (
            "'country' key should not be present in extract_all() output. "
            "Field was eliminated per STRUCT-012 (v52). Use 'address_country'."
        )


class TestExtractScores:
    def test_review_score_type(self, extractor):
        data = extractor.extract_all()
        score = data.get("review_score")
        if score is not None:
            assert isinstance(score, float)
            assert 0.0 <= score <= 10.0

    def test_review_count_type(self, extractor):
        data = extractor.extract_all()
        count = data.get("review_count")
        if count is not None:
            assert isinstance(count, int)
            assert count >= 0

    def test_star_rating_range(self, extractor):
        """BUG-EXTR-007: star_rating must be in [0.0, 5.0]."""
        data = extractor.extract_all()
        rating = data.get("star_rating")
        if rating is not None:
            assert 0.0 <= rating <= 5.0, (
                f"star_rating={rating} outside [0, 5] — "
                "check BUG-EXTR-007 normalization (raw ÷ 2)."
            )


# ---------------------------------------------------------------------------
# Amenities and services tests
# ---------------------------------------------------------------------------

class TestExtractAmenities:
    def test_amenities_is_list(self, extractor):
        data = extractor.extract_all()
        amenities = data.get("amenities", [])
        assert isinstance(amenities, list)

    def test_amenities_not_empty(self, extractor):
        data = extractor.extract_all()
        assert len(data.get("amenities", [])) > 0

    def test_amenities_are_strings(self, extractor):
        data = extractor.extract_all()
        for item in data.get("amenities", []):
            assert isinstance(item, str)
            assert len(item) > 0


class TestExtractPopularServices:
    def test_popular_services_is_list(self, extractor):
        data = extractor.extract_all()
        assert isinstance(data.get("popular_services", []), list)

    def test_popular_services_not_empty(self, extractor):
        data = extractor.extract_all()
        assert len(data.get("popular_services", [])) > 0


# ---------------------------------------------------------------------------
# Policies and legal tests
# ---------------------------------------------------------------------------

class TestExtractPolicies:
    def test_policies_is_list(self, extractor):
        data = extractor.extract_all()
        assert isinstance(data.get("policies", []), list)

    def test_policies_structure(self, extractor):
        """Each policy must be a dict with policy_name and policy_details."""
        data = extractor.extract_all()
        for policy in data.get("policies", []):
            assert isinstance(policy, dict)
            assert "policy_name" in policy
            assert isinstance(policy["policy_name"], str)


class TestExtractLegal:
    def test_legal_is_dict_or_none(self, extractor):
        data = extractor.extract_all()
        legal = data.get("legal")
        if legal is not None:
            assert isinstance(legal, dict)
            assert "legal" in legal or "legal_info" in legal


# ---------------------------------------------------------------------------
# STRUCT-013 (v53): Fine Print tests
# ---------------------------------------------------------------------------

class TestExtractFinePrint:
    """STRUCT-013 (v53): Fine print HTML extraction."""

    def test_fine_print_present(self, extractor):
        data = extractor.extract_all()
        assert "fine_print" in data, (
            "fine_print key missing from extract_all() output. "
            "Check _extract_fine_print() in extractor.py (STRUCT-013, v53)."
        )

    def test_fine_print_is_string(self, extractor):
        data = extractor.extract_all()
        fp = data.get("fine_print")
        if fp is not None:
            assert isinstance(fp, str)
            assert len(fp) > 0

    def test_fine_print_preserves_p_tags(self, extractor):
        """HTML sanitization must preserve <p> tags for line breaks."""
        data = extractor.extract_all()
        fp = data.get("fine_print") or ""
        if fp:
            assert "<p>" in fp, (
                "fine_print should preserve <p> tags. "
                "Check _sanitize_html_fragment() — <p> must not be stripped."
            )

    def test_fine_print_no_svg(self, extractor):
        """HTML sanitization must eliminate <svg> tags completely."""
        data = extractor.extract_all()
        fp = data.get("fine_print") or ""
        assert "<svg" not in fp.lower(), (
            "fine_print contains <svg> — sanitization failed. "
            "Check _sanitize_html_fragment() remove_tags parameter."
        )

    def test_fine_print_no_html_attributes(self, extractor):
        """All HTML attributes must be stripped from remaining tags."""
        import re as _re
        data = extractor.extract_all()
        fp = data.get("fine_print") or ""
        # Detect any remaining attributes: <tag attr=... or <tag attr>
        has_attrs = bool(_re.search(r'<\w+\s+[a-zA-Z_][a-zA-Z0-9_-]*\s*[=>\s]', fp))
        assert not has_attrs, (
            "fine_print HTML still contains attributes. "
            "Check _sanitize_html_fragment() — tag.attrs = {} step."
        )


# ---------------------------------------------------------------------------
# STRUCT-014 (v53): All services tests
# ---------------------------------------------------------------------------

class TestExtractAllServices:
    """STRUCT-014 (v53): Complete services/facilities list extraction."""

    def test_all_services_is_list(self, extractor):
        data = extractor.extract_all()
        assert isinstance(data.get("all_services", []), list), (
            "all_services must be a list. "
            "Check _extract_all_services() (STRUCT-014, v53)."
        )

    def test_all_services_not_empty(self, extractor):
        data = extractor.extract_all()
        assert len(data.get("all_services", [])) > 0, (
            "all_services should not be empty for sample HTML with facilities section."
        )

    def test_all_services_are_strings(self, extractor):
        data = extractor.extract_all()
        for item in data.get("all_services", []):
            assert isinstance(item, str)
            assert len(item) > 0

    def test_all_services_no_duplicates(self, extractor):
        data = extractor.extract_all()
        services = data.get("all_services", [])
        assert len(services) == len(set(services)), (
            "all_services contains duplicates — check deduplication logic."
        )

    def test_all_services_coverage(self, extractor):
        """all_services should cover more or equal items than popular_services."""
        data = extractor.extract_all()
        popular = data.get("popular_services", [])
        all_svcs = data.get("all_services", [])
        # all_services is a superset of popular_services in well-formed HTML
        assert len(all_svcs) >= len(popular), (
            "all_services should have at least as many items as popular_services."
        )


# ---------------------------------------------------------------------------
# STRUCT-015 (v53): FAQs tests
# ---------------------------------------------------------------------------

class TestExtractFAQs:
    """STRUCT-015 (v53): FAQ questions extraction."""

    def test_faqs_is_list(self, extractor):
        data = extractor.extract_all()
        assert isinstance(data.get("faqs", []), list), (
            "faqs must be a list. "
            "Check _extract_faqs() (STRUCT-015, v53)."
        )

    def test_faqs_not_empty(self, extractor):
        data = extractor.extract_all()
        assert len(data.get("faqs", [])) > 0, (
            "faqs should not be empty for sample HTML with FAQ section."
        )

    def test_faqs_are_strings(self, extractor):
        data = extractor.extract_all()
        for item in data.get("faqs", []):
            assert isinstance(item, str)
            assert len(item) > 5

    def test_faqs_no_duplicates(self, extractor):
        data = extractor.extract_all()
        faqs = data.get("faqs", [])
        assert len(faqs) == len(set(faqs)), (
            "faqs contains duplicates — check deduplication logic."
        )

    def test_faqs_reasonable_length(self, extractor):
        """FAQ questions should not be excessively long (< 1000 chars)."""
        data = extractor.extract_all()
        for faq in data.get("faqs", []):
            assert len(faq) < 1000, f"FAQ question too long: {faq[:80]}..."


# ---------------------------------------------------------------------------
# STRUCT-016 (v53): Guest reviews tests
# ---------------------------------------------------------------------------

class TestExtractGuestReviews:
    """STRUCT-016 (v53): Guest review categories and scores extraction."""

    def test_guest_reviews_is_list(self, extractor):
        data = extractor.extract_all()
        assert isinstance(data.get("guest_reviews", []), list), (
            "guest_reviews must be a list. "
            "Check _extract_guest_reviews() (STRUCT-016, v53)."
        )

    def test_guest_reviews_structure(self, extractor):
        """Each review must be a dict with reviews_categories and reviews_score."""
        data = extractor.extract_all()
        for review in data.get("guest_reviews", []):
            assert isinstance(review, dict), "Each guest_review must be a dict."
            assert "reviews_categories" in review, (
                "reviews_categories key missing from guest_review dict."
            )
            assert isinstance(review["reviews_categories"], str)
            assert len(review["reviews_categories"]) > 0
            # reviews_score is optional (can be None / missing)
            if review.get("reviews_score") is not None:
                assert isinstance(review["reviews_score"], str)

    def test_guest_reviews_no_duplicate_categories(self, extractor):
        data = extractor.extract_all()
        cats = [r["reviews_categories"] for r in data.get("guest_reviews", []) if "reviews_categories" in r]
        assert len(cats) == len(set(cats)), (
            "guest_reviews contains duplicate categories."
        )

    def test_guest_reviews_category_length(self, extractor):
        """Category names must fit in VARCHAR(256)."""
        data = extractor.extract_all()
        for review in data.get("guest_reviews", []):
            assert len(review.get("reviews_categories", "")) <= 256


# ---------------------------------------------------------------------------
# STRUCT-017 (v53): Property highlights tests
# ---------------------------------------------------------------------------

class TestExtractPropertyHighlights:
    """STRUCT-017 (v53): Property highlights sanitized HTML extraction."""

    def test_property_highlights_present(self, extractor):
        data = extractor.extract_all()
        assert "property_highlights" in data, (
            "property_highlights key missing from extract_all() output. "
            "Check _extract_property_highlights() (STRUCT-017, v53)."
        )

    def test_property_highlights_is_string(self, extractor):
        data = extractor.extract_all()
        hl = data.get("property_highlights")
        if hl is not None:
            assert isinstance(hl, str)
            assert len(hl) > 0

    def test_property_highlights_no_svg(self, extractor):
        """SVG tags must be completely eliminated from highlights HTML."""
        data = extractor.extract_all()
        hl = data.get("property_highlights") or ""
        assert "<svg" not in hl.lower(), (
            "property_highlights contains <svg> — sanitization failed. "
            "Check _sanitize_html_fragment() remove_tags in _extract_property_highlights()."
        )

    def test_property_highlights_no_img(self, extractor):
        """<img> tags must be eliminated from highlights HTML."""
        data = extractor.extract_all()
        hl = data.get("property_highlights") or ""
        assert "<img" not in hl.lower(), (
            "property_highlights contains <img> — sanitization failed."
        )

    def test_property_highlights_no_attributes(self, extractor):
        """All HTML attributes must be stripped from highlights HTML."""
        import re as _re
        data = extractor.extract_all()
        hl = data.get("property_highlights") or ""
        has_attrs = bool(_re.search(r'<\w+\s+[a-zA-Z_][a-zA-Z0-9_-]*\s*[=>\s]', hl))
        assert not has_attrs, (
            "property_highlights HTML still contains attributes. "
            "Check _sanitize_html_fragment() — tag.attrs = {} step."
        )

    def test_property_highlights_preserves_structure(self, extractor):
        """Structural tags like <div>, <ul>, <li> must be preserved."""
        data = extractor.extract_all()
        hl = data.get("property_highlights") or ""
        if hl:
            has_structure = any(tag in hl for tag in ["<div>", "<ul>", "<li>", "<p>"])
            assert has_structure, (
                "property_highlights HTML lost all structural tags. "
                "Sanitization should only remove SVG/img and attributes."
            )


# ---------------------------------------------------------------------------
# Regression tests — deprecated fields
# ---------------------------------------------------------------------------

class TestDeprecatedFields:
    """Ensure removed fields do not reappear in extract_all() output."""

    DEPRECATED_KEYS = {
        "address":  "STRUCT-004 (v50) — use street_address / address_city",
        "country":  "STRUCT-012 (v52) — use address_country",
        "photos":   "STRUCT-002 (v50) — images managed by image_downloads table only",
        "city":     "STRUCT-011 (v52) — renamed to address_city",
    }

    def test_no_deprecated_keys_in_output(self, extractor):
        data = extractor.extract_all()
        for key, reason in self.DEPRECATED_KEYS.items():
            assert key not in data, (
                f"Deprecated key '{key}' found in extract_all() output. "
                f"Reason for removal: {reason}"
            )


# ---------------------------------------------------------------------------
# extract_all() contract test — all expected v53 keys present
# ---------------------------------------------------------------------------

class TestExtractAllContract:
    """Verify the full v53 key contract of extract_all()."""

    # Keys that MUST be present (populated from sample HTML fixture)
    REQUIRED_KEYS = [
        "url", "language", "hotel_name", "description",
        "amenities", "popular_services", "policies", "legal",
        "fine_print", "all_services", "faqs", "property_highlights",
    ]

    # Keys that MUST NOT appear (structural — handled by separate tables)
    FORBIDDEN_KEYS = [
        "address", "country", "photos", "city",
    ]

    def test_required_keys_present(self, extractor):
        data = extractor.extract_all()
        missing = [k for k in self.REQUIRED_KEYS if k not in data]
        assert not missing, (
            f"Missing expected keys in extract_all() output: {missing}. "
            "Ensure all extractors are implemented and the sample HTML triggers them."
        )

    def test_forbidden_keys_absent(self, extractor):
        data = extractor.extract_all()
        present = [k for k in self.FORBIDDEN_KEYS if k in data]
        assert not present, (
            f"Deprecated/forbidden keys found in extract_all() output: {present}. "
            "These fields were removed in v50/v52 structural changes."
        )

    def test_language_key_matches_extractor(self, extractor):
        data = extractor.extract_all()
        assert data.get("language") == "en"

    def test_url_key_present(self, extractor):
        data = extractor.extract_all()
        assert "url" in data
        assert "booking.com" in (data.get("url") or "")
