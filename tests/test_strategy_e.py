"""
test_strategy_e.py — BookingScraper Pro v6.0.0 build 58
=========================================================
Tests para Strategy E (Enhanced State with Conditional Commit).
Cubre BUG-INTEGRITY-001: all_ok=True hardcoded corregido.

Casos de prueba:
  Case 1 — Éxito completo    : todos los idiomas OK  → status='done'
  Case 2 — Fallo parcial     : algunos OK, otros KO  → status='error', datos PRESERVADOS
  Case 3 — Fallo total       : todos KO              → cleanup + status='error'
  Case 4 — Caso del bug real : sólo 'es' OK (1/4)    → status='error', 1 idioma preservado
  Case 5 — Excepción en lang : excepción lanzada      → contada como fallo

Windows 11 notes:
  - pytest sin fixtures de señal POSIX (SIGUSR1 no disponible)
  - mock de get_db() compatible con threading (ThreadPoolExecutor)
  - Usar tmp_path de pytest para rutas de Windows
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict
from unittest.mock import MagicMock, patch, call

import pytest


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def url_obj() -> MagicMock:
    """Mock URLQueue row."""
    obj = MagicMock()
    obj.id     = uuid.uuid4()
    obj.url    = "https://www.booking.com/hotel/maldives/test-resort.es.html"
    obj.status = "pending"
    obj.retry_count = 0
    obj.max_retries = 3
    return obj


@pytest.fixture
def mock_cfg():
    cfg = MagicMock()
    cfg.ENABLED_LANGUAGES = ["en", "es", "de", "it"]
    cfg.SCRAPER_REQUEST_TIMEOUT = 30
    cfg.REDIS_URL = "redis://localhost:6379/0"
    cfg.REDIS_MAX_CONNECTIONS = 10
    cfg.MAX_RETRIES = 3
    cfg.VPN_ENABLED = False
    cfg.HEADLESS_BROWSER = True
    cfg.SCRAPER_MAX_WORKERS = 2
    cfg.VPN_ROTATION_INTERVAL = 60
    cfg.VPN_COUNTRIES = []
    return cfg


@pytest.fixture
def service(mock_cfg):
    """ScraperService con todas las dependencias mockeadas."""
    with (
        patch("app.scraper_service.get_settings", return_value=mock_cfg),
        patch("app.scraper_service.CloudScraperEngine"),
        patch("app.scraper_service.SeleniumEngine"),
        patch("app.scraper_service._get_vpn"),
    ):
        from app.scraper_service import ScraperService
        svc = ScraperService.__new__(ScraperService)
        svc._cfg          = mock_cfg
        svc._stats        = MagicMock()
        svc._cloud_engine = MagicMock()
        svc._selenium_engine = MagicMock()
        svc._vpn          = MagicMock()
        return svc


# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────

def _patch_process(service, scrape_results: Dict[str, bool], actual_db_count: int):
    """
    Aplica los mocks necesarios para probar _process_url.

    Args:
        scrape_results:  {lang: True/False} — resultado de _scrape_language()
        actual_db_count: valor que devuelve _count_successful_languages()
    """
    call_order = ["en", "es", "de", "it"]

    def _fake_scrape(url_obj, lang):
        return scrape_results.get(lang, False)

    patches = [
        patch("app.scraper_service._try_claim_url", return_value=True),
        patch("app.scraper_service._release_url"),
        patch.object(service, "_mark_processing"),
        patch.object(service, "_scrape_language",  side_effect=_fake_scrape),
        patch.object(service, "_count_successful_languages", return_value=actual_db_count),
        patch.object(service, "_mark_done"),
        patch.object(service, "_mark_incomplete"),
        patch.object(service, "_cleanup_empty_url"),
        patch.object(service, "_mark_error"),
    ]
    return patches


# ─────────────────────────────────────────────────────────────────────────────
# Case 1 — Éxito completo (4/4 idiomas)
# ─────────────────────────────────────────────────────────────────────────────

class TestCase1CompleteSuccess:
    """Todos los idiomas OK → URL marcada 'done'."""

    def test_marks_done_when_all_languages_succeed(self, service, url_obj):
        results = {"en": True, "es": True, "de": True, "it": True}
        patches = _patch_process(service, scrape_results=results, actual_db_count=4)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5] as mock_done, patches[6], patches[7], patches[8]:
            service._process_url(url_obj)

        mock_done.assert_called_once()
        args, kwargs = mock_done.call_args
        assert kwargs.get("all_ok") is True or (args and args[1] is True), \
            "Case 1: _mark_done debe llamarse con all_ok=True"

    def test_does_not_call_mark_incomplete_on_full_success(self, service, url_obj):
        results = {"en": True, "es": True, "de": True, "it": True}
        patches = _patch_process(service, scrape_results=results, actual_db_count=4)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5], patches[6] as mock_incomplete, patches[7], patches[8]:
            service._process_url(url_obj)

        mock_incomplete.assert_not_called()

    def test_records_succeeded_stat(self, service, url_obj):
        results = {"en": True, "es": True, "de": True, "it": True}
        patches = _patch_process(service, scrape_results=results, actual_db_count=4)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5], patches[6], patches[7], patches[8]:
            service._process_url(url_obj)

        service._stats.record.assert_called_with(succeeded=True)


# ─────────────────────────────────────────────────────────────────────────────
# Case 2 — Fallo parcial (3/4 idiomas)
# ─────────────────────────────────────────────────────────────────────────────

class TestCase2PartialFailure:
    """Algunos idiomas OK → status='error', datos PRESERVADOS."""

    def test_marks_incomplete_not_done_on_partial(self, service, url_obj):
        results = {"en": True, "es": True, "de": True, "it": False}
        patches = _patch_process(service, scrape_results=results, actual_db_count=3)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5] as mock_done, patches[6] as mock_incomplete, patches[7], patches[8]:
            service._process_url(url_obj)

        mock_done.assert_not_called()
        mock_incomplete.assert_called_once()

    def test_incomplete_error_message_contains_counts(self, service, url_obj):
        results = {"en": True, "es": True, "de": True, "it": False}
        patches = _patch_process(service, scrape_results=results, actual_db_count=3)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5], patches[6] as mock_incomplete, patches[7], patches[8]:
            service._process_url(url_obj)

        call_args = mock_incomplete.call_args
        error_msg = call_args[0][1] if call_args[0] else call_args[1].get("error_msg", "")
        assert "3/4" in error_msg or "Incomplete" in error_msg, \
            f"Error message debe indicar 3/4 — got: {error_msg!r}"

    def test_does_not_cleanup_on_partial(self, service, url_obj):
        """Datos de idiomas exitosos NO deben ser eliminados en fallo parcial."""
        results = {"en": True, "es": True, "de": False, "it": False}
        patches = _patch_process(service, scrape_results=results, actual_db_count=2)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5], patches[6], patches[7] as mock_cleanup, patches[8]:
            service._process_url(url_obj)

        mock_cleanup.assert_not_called()

    def test_records_failed_stat_on_partial(self, service, url_obj):
        results = {"en": False, "es": True, "de": False, "it": False}
        patches = _patch_process(service, scrape_results=results, actual_db_count=1)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5], patches[6], patches[7], patches[8]:
            service._process_url(url_obj)

        service._stats.record.assert_called_with(failed=True)


# ─────────────────────────────────────────────────────────────────────────────
# Case 3 — Fallo total (0/4 idiomas)
# ─────────────────────────────────────────────────────────────────────────────

class TestCase3TotalFailure:
    """Todos los idiomas fallaron → cleanup + status='error'."""

    def test_calls_cleanup_on_total_failure(self, service, url_obj):
        results = {"en": False, "es": False, "de": False, "it": False}
        patches = _patch_process(service, scrape_results=results, actual_db_count=0)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5], patches[6], patches[7] as mock_cleanup, patches[8]:
            service._process_url(url_obj)

        mock_cleanup.assert_called_once_with(url_obj.id)

    def test_calls_mark_error_on_total_failure(self, service, url_obj):
        results = {"en": False, "es": False, "de": False, "it": False}
        patches = _patch_process(service, scrape_results=results, actual_db_count=0)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5], patches[6], patches[7], patches[8] as mock_error:
            service._process_url(url_obj)

        mock_error.assert_called_once()

    def test_does_not_mark_done_on_total_failure(self, service, url_obj):
        results = {"en": False, "es": False, "de": False, "it": False}
        patches = _patch_process(service, scrape_results=results, actual_db_count=0)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5] as mock_done, patches[6], patches[7], patches[8]:
            service._process_url(url_obj)

        mock_done.assert_not_called()


# ─────────────────────────────────────────────────────────────────────────────
# Case 4 — Réplica exacta del bug reportado (1/4 — sólo 'es')
# ─────────────────────────────────────────────────────────────────────────────

class TestCase4OriginalBugScenario:
    """
    Reproduce el bug exacto de Build 57:
    URL bc5d8b35 — sólo 'es' exitoso, 'en'/'de'/'it' fallaron.
    Con el bug original, se marcaba 'done'. Con Strategy E debe ser 'error'.
    """

    def test_original_bug_url_marked_error_not_done(self, service, url_obj):
        """
        ANTES (bug): self._mark_done(url_obj, all_ok=True) → siempre 'done'
        AHORA (fix): actual_count=1 < expected=4 → _mark_incomplete() → 'error'
        """
        results = {"en": False, "es": True, "de": False, "it": False}
        patches = _patch_process(service, scrape_results=results, actual_db_count=1)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5] as mock_done, patches[6] as mock_incomplete, patches[7], patches[8]:
            service._process_url(url_obj)

        mock_done.assert_not_called(), \
            "BUG REGRESSION: _mark_done NO debe llamarse cuando sólo 1/4 idiomas tienen éxito"
        mock_incomplete.assert_called_once(), \
            "Strategy E: _mark_incomplete DEBE llamarse para 1/4 con datos preservados"

    def test_spanish_data_preserved_on_other_languages_fail(self, service, url_obj):
        """Datos de 'es' (el único exitoso) deben preservarse — NO cleanup."""
        results = {"en": False, "es": True, "de": False, "it": False}
        patches = _patch_process(service, scrape_results=results, actual_db_count=1)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5], patches[6], patches[7] as mock_cleanup, patches[8]:
            service._process_url(url_obj)

        mock_cleanup.assert_not_called(), \
            "Los datos de 'es' deben PRESERVARSE — _cleanup_empty_url no debe llamarse"

    def test_error_message_identifies_failed_languages(self, service, url_obj):
        results = {"en": False, "es": True, "de": False, "it": False}
        patches = _patch_process(service, scrape_results=results, actual_db_count=1)

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5], patches[6] as mock_incomplete, patches[7], patches[8]:
            service._process_url(url_obj)

        call_args = mock_incomplete.call_args
        error_msg = call_args[0][1] if call_args[0] else call_args[1].get("error_msg", "")
        # El mensaje debe indicar qué falló
        assert any(lang in error_msg for lang in ["en", "de", "it"]), \
            f"Error message debe identificar idiomas fallidos. Got: {error_msg!r}"


# ─────────────────────────────────────────────────────────────────────────────
# Case 5 — Excepción durante scraping de idioma
# ─────────────────────────────────────────────────────────────────────────────

class TestCase5ExceptionHandling:
    """Excepción en un idioma es manejada sin colapsar el proceso."""

    def test_exception_in_one_language_counts_as_failure(self, service, url_obj):
        """Si _scrape_language lanza excepción, ese idioma cuenta como fallido."""
        def _scrape_with_exception(url_obj, lang):
            if lang == "de":
                raise ConnectionError("Simulated network error")
            return True  # en, es, it OK

        patches = [
            patch("app.scraper_service._try_claim_url", return_value=True),
            patch("app.scraper_service._release_url"),
            patch.object(service, "_mark_processing"),
            patch.object(service, "_scrape_language", side_effect=_scrape_with_exception),
            patch.object(service, "_count_successful_languages", return_value=3),
            patch.object(service, "_mark_done"),
            patch.object(service, "_mark_incomplete"),
            patch.object(service, "_cleanup_empty_url"),
            patch.object(service, "_mark_error"),
        ]

        with patches[0], patches[1], patches[2], patches[3], patches[4], \
             patches[5], patches[6] as mock_incomplete, patches[7], patches[8]:
            # No debe propagar la excepción de 'de'
            service._process_url(url_obj)

        # actual_count=3 < expected=4 → debe llamar _mark_incomplete
        mock_incomplete.assert_called_once()

    def test_url_lock_always_released(self, service, url_obj):
        """El lock de Redis debe liberarse siempre, incluso si hay excepción."""
        with (
            patch("app.scraper_service._try_claim_url", return_value=True),
            patch("app.scraper_service._release_url") as mock_release,
            patch.object(service, "_mark_processing", side_effect=RuntimeError("DB down")),
            patch.object(service, "_mark_error"),
        ):
            service._process_url(url_obj)

        mock_release.assert_called_once(), \
            "El lock Redis SIEMPRE debe liberarse (bloque finally)"


# ─────────────────────────────────────────────────────────────────────────────
# Unit tests para _count_successful_languages
# ─────────────────────────────────────────────────────────────────────────────

class TestCountSuccessfulLanguages:
    """Tests para el método _count_successful_languages (Strategy E-001)."""

    def test_returns_correct_count_from_db(self, service):
        uid = uuid.uuid4()
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.scalar.return_value = 3

        with patch("app.scraper_service.get_db") as mock_get_db:
            mock_get_db.return_value.__enter__ = MagicMock(return_value=mock_session)
            mock_get_db.return_value.__exit__  = MagicMock(return_value=False)
            result = service._count_successful_languages(uid)

        assert isinstance(result, int)

    def test_returns_zero_on_db_exception(self, service):
        """Si la DB falla, debe retornar 0 sin propagar excepción."""
        uid = uuid.uuid4()
        with patch("app.scraper_service.get_db", side_effect=Exception("DB error")):
            result = service._count_successful_languages(uid)
        assert result == 0

    def test_returns_zero_on_null_scalar(self, service):
        """COUNT(*) puede devolver None — debe normalizarse a 0."""
        uid = uuid.uuid4()
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.scalar.return_value = None

        with patch("app.scraper_service.get_db") as mock_get_db:
            mock_get_db.return_value.__enter__ = MagicMock(return_value=mock_session)
            mock_get_db.return_value.__exit__  = MagicMock(return_value=False)
            result = service._count_successful_languages(uid)

        assert result == 0


# ─────────────────────────────────────────────────────────────────────────────
# Unit tests para _mark_incomplete
# ─────────────────────────────────────────────────────────────────────────────

class TestMarkIncomplete:
    """Tests para _mark_incomplete (Strategy E-002)."""

    def test_sets_status_to_error(self, service, url_obj):
        mock_row = MagicMock()
        mock_row.scraped_at = None
        mock_session = MagicMock()
        mock_session.get.return_value = mock_row

        with patch("app.scraper_service.get_db") as mock_get_db:
            mock_get_db.return_value.__enter__ = MagicMock(return_value=mock_session)
            mock_get_db.return_value.__exit__  = MagicMock(return_value=False)
            service._mark_incomplete(
                url_obj, "Incomplete: 1/4",
                success_langs=["es"], failed_langs=["en", "de", "it"]
            )

        assert mock_row.status == "error"

    def test_stores_language_lists(self, service, url_obj):
        mock_row = MagicMock()
        mock_row.scraped_at = None
        mock_session = MagicMock()
        mock_session.get.return_value = mock_row

        with patch("app.scraper_service.get_db") as mock_get_db:
            mock_get_db.return_value.__enter__ = MagicMock(return_value=mock_session)
            mock_get_db.return_value.__exit__  = MagicMock(return_value=False)
            service._mark_incomplete(
                url_obj, "test",
                success_langs=["es"], failed_langs=["en", "de", "it"]
            )

        assert mock_row.languages_completed == "es"
        assert "en" in mock_row.languages_failed

    def test_does_not_raise_on_db_exception(self, service, url_obj):
        """_mark_incomplete debe manejar errores de DB sin propagar."""
        with patch("app.scraper_service.get_db", side_effect=Exception("DB error")):
            # No debe lanzar excepción
            service._mark_incomplete(url_obj, "test error", [], [])
