"""
test_completeness.py — State machine and completeness service tests.
"""

from __future__ import annotations

import pytest


class TestStateMachineTransitions:
    """SCRAP-BUG-034: Only valid state transitions should be allowed."""

    def test_pending_to_processing_allowed(self):
        from app.completeness_service import _is_valid_transition
        assert _is_valid_transition("pending", "processing")

    def test_pending_to_skipped_allowed(self):
        from app.completeness_service import _is_valid_transition
        assert _is_valid_transition("pending", "skipped")

    def test_processing_to_done_allowed(self):
        from app.completeness_service import _is_valid_transition
        assert _is_valid_transition("processing", "done")

    def test_processing_to_error_allowed(self):
        from app.completeness_service import _is_valid_transition
        assert _is_valid_transition("processing", "error")

    def test_processing_to_incomplete_allowed(self):
        from app.completeness_service import _is_valid_transition
        assert _is_valid_transition("processing", "incomplete")

    def test_done_to_pending_rejected(self):
        """Terminal state: done → pending must be rejected."""
        from app.completeness_service import _is_valid_transition
        assert not _is_valid_transition("done", "pending")

    def test_done_to_processing_rejected(self):
        from app.completeness_service import _is_valid_transition
        assert not _is_valid_transition("done", "processing")

    def test_skipped_to_pending_rejected(self):
        from app.completeness_service import _is_valid_transition
        assert not _is_valid_transition("skipped", "pending")

    def test_error_to_pending_allowed(self):
        from app.completeness_service import _is_valid_transition
        assert _is_valid_transition("error", "pending")

    def test_unknown_state_returns_false(self):
        from app.completeness_service import _is_valid_transition
        assert not _is_valid_transition("unknown_state", "done")


class TestVPNManagerValidation:
    """SCRAP-BUG-010: VPN country validation must reject invalid names."""

    def test_valid_country_accepted(self):
        from app.vpn_manager_windows import _validate_country
        assert _validate_country("Spain") == "Spain"
        assert _validate_country("Germany") == "Germany"

    def test_invalid_country_rejected(self):
        from app.vpn_manager_windows import _validate_country
        with pytest.raises(ValueError, match="approved VPN country list"):
            _validate_country("InvalidCountryXYZ")

    def test_injection_attempt_rejected(self):
        """Shell injection via country name must be blocked."""
        from app.vpn_manager_windows import _validate_country
        with pytest.raises(ValueError):
            _validate_country("Spain; rm -rf /")

    def test_empty_country_rejected(self):
        from app.vpn_manager_windows import _validate_country
        with pytest.raises(ValueError):
            _validate_country("")


class TestCircuitBreaker:
    """Circuit breaker atomic state transitions."""

    def test_initially_closed(self):
        from app.vpn_manager_windows import CircuitBreaker
        cb = CircuitBreaker(failure_threshold=3)
        assert not cb.is_open

    def test_opens_after_threshold_failures(self):
        from app.vpn_manager_windows import CircuitBreaker
        cb = CircuitBreaker(failure_threshold=3, reset_timeout_s=3600)
        for _ in range(3):
            cb.record_failure()
        assert cb.is_open

    def test_resets_after_success(self):
        from app.vpn_manager_windows import CircuitBreaker
        cb = CircuitBreaker(failure_threshold=2, reset_timeout_s=3600)
        cb.record_failure()
        cb.record_failure()
        cb.record_success()
        assert not cb.is_open

    def test_try_acquire_returns_false_when_open(self):
        from app.vpn_manager_windows import CircuitBreaker
        cb = CircuitBreaker(failure_threshold=1, reset_timeout_s=3600)
        cb.record_failure()
        assert not cb.try_acquire()

    def test_try_acquire_returns_true_when_closed(self):
        from app.vpn_manager_windows import CircuitBreaker
        cb = CircuitBreaker(failure_threshold=5)
        assert cb.try_acquire()
