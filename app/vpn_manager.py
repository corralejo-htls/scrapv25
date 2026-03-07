"""
BookingScraper Pro v6.0 - VPN Manager Abstraction Layer
=======================================================
Thin interface over the Windows-specific NordVPN implementation.
Allows future swap-out to a different VPN provider.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class VPNManagerBase(ABC):
    """Abstract interface for VPN management."""

    @abstractmethod
    def connect(self, country: Optional[str] = None) -> bool:
        """Connect VPN; optionally specify country code. Returns success."""

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect VPN. Returns success."""

    @abstractmethod
    def rotate(self) -> bool:
        """Rotate to a new server. Returns success."""

    @abstractmethod
    def get_current_ip(self) -> Optional[str]:
        """Return current public IP, or None on failure."""

    @abstractmethod
    def is_connected(self) -> bool:
        """Return True if VPN is currently active."""


class NullVPNManager(VPNManagerBase):
    """
    No-op VPN manager used when VPN_ENABLED=false.
    Satisfies the interface without any actual VPN operations.
    """

    def connect(self, country: Optional[str] = None) -> bool:
        return True

    def disconnect(self) -> bool:
        return True

    def rotate(self) -> bool:
        return True

    def get_current_ip(self) -> Optional[str]:
        return None

    def is_connected(self) -> bool:
        return False


def vpn_manager_factory(enabled: bool = False) -> VPNManagerBase:
    """
    Return the correct VPN manager based on configuration.
    Avoids importing NordVPN Windows module when VPN is disabled.
    """
    if not enabled:
        return NullVPNManager()
    try:
        from app.vpn_manager_windows import NordVPNManager
        return NordVPNManager()
    except ImportError as exc:
        raise ImportError(
            "vpn_manager_windows module unavailable. "
            "Set VPN_ENABLED=false or ensure pywin32 and NordVPN CLI are installed."
        ) from exc
