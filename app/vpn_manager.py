"""
BookingScraper/app/vpn_manager.py
VPN Manager — Platform Abstraction Layer
Windows 11 + Python 3.14.3

[FIX LOW-40-001] Clarified role: this is NOT an orphan file.
  - This module IS imported by scraper_service.py:
      from app.vpn_manager import vpn_manager_factory
  - vpn_manager.py = platform-agnostic facade (this file, 79 lines)
  - vpn_manager_windows.py = Windows-specific NordVPN implementation (763 lines)

[FIX BUG-V11-004 / BUG-V11-008]
scraper_service.py imports `vpn_manager_factory` from this module:
    from app.vpn_manager import vpn_manager_factory

This file was absent from the repository. `vpn_manager_factory` was added to
`vpn_manager_windows.py` in Session 6, but the import expects `app.vpn_manager`
(not `app.vpn_manager_windows`), so the ImportError persisted.

This module is the intended abstraction layer that:
  1. Detects the runtime platform (Windows vs. Linux/macOS).
  2. Delegates to the appropriate platform-specific implementation.
  3. Exposes a single `vpn_manager_factory()` entry point to service layer callers.

DESIGN:
    - Windows 11 → NordVPNManagerWindows  (app/vpn_manager_windows.py)
    - Linux/macOS → raises RuntimeError with a clear message (not yet implemented)
    - All platform logic is isolated here; callers are platform-agnostic.

USAGE (in scraper_service.py):
    from app.vpn_manager import vpn_manager_factory
    manager = vpn_manager_factory(interactive=False)
"""

from __future__ import annotations

import sys
from loguru import logger


def vpn_manager_factory(interactive: bool = False):
    """
    Return a ready-to-use VPN manager for the current platform.

    On Windows 11 delegates to `NordVPNManagerWindows` (singleton pattern).
    The singleton is managed inside `vpn_manager_windows.vpn_manager_factory`
    using a `threading.Lock`, making this function safe to call concurrently.

    Args:
        interactive (bool): If True, the manager may prompt the user for input
            during initial connection (e.g. authentication dialogs). Always
            False in production / daemon contexts. Defaults to False.

    Returns:
        NordVPNManagerWindows: Initialised VPN manager instance.

    Raises:
        RuntimeError: If the current platform has no supported VPN
            implementation.
        ImportError: If the platform-specific module cannot be imported
            (dependency missing, file absent, etc.).
    """
    if sys.platform.startswith("win"):
        # Delegate to the Windows-specific factory (defined in vpn_manager_windows.py).
        # The factory maintains a global singleton so multiple callers share
        # the same NordVPN connection state.
        from app.vpn_manager_windows import vpn_manager_factory as _win_factory
        logger.debug("[vpn_manager] Delegating to Windows NordVPN factory.")
        return _win_factory(interactive=interactive)

    # ── Future platform implementations ─────────────────────────────────────
    # Linux:
    #   from app.vpn_manager_linux import vpn_manager_factory as _linux_factory
    #   return _linux_factory(interactive=interactive)
    #
    # macOS:
    #   from app.vpn_manager_macos import vpn_manager_factory as _macos_factory
    #   return _macos_factory(interactive=interactive)

    raise RuntimeError(
        f"[vpn_manager] No VPN manager implementation available for platform "
        f"'{sys.platform}'. Supported: win32, win64 (Windows 11). "
        "Set VPN_ENABLED=False or provide a platform-specific implementation."
    )
