"""
vpn_manager.py — VPN abstraction layer.
Returns the appropriate manager based on platform and config.
"""
import sys
from app.config import get_settings

def get_vpn_manager():
    """Factory: return platform-appropriate VPN manager."""
    if sys.platform == "win32":
        from app.vpn_manager_windows import get_vpn_manager as _get
        return _get()
    # Non-Windows: return null manager
    from app.vpn_manager_windows import NullVPNManager
    return NullVPNManager()
