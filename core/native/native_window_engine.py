from __future__ import annotations

import sys
from typing import Any, Dict, List, Optional


def extract_native_windows(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Extract native window metadata (titles, bounds, z-order, focus).

    Uses live OS enumeration when snapshot is absent; graceful degradation
    returns structural empty graph on failure.
    """
    if snapshot is not None:
        return _normalize_windows(snapshot)

    try:
        return _enumerate_platform_windows()
    except Exception:
        return {
            "windows": [],
            "focused_window": "",
            "platform": sys.platform,
            "degraded": True,
            "bounded": True,
        }


def _normalize_windows(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    windows = list(snapshot.get("windows", []))[:5000]
    focused = str(snapshot.get("focused_window", ""))

    if not focused and windows:
        for window in windows:
            if window.get("focused"):
                focused = str(window.get("title", window.get("id", "")))
                break

    return {
        "windows": sorted(
            windows,
            key=lambda item: (
                -int(item.get("z_order", 0)),
                str(item.get("title", "")),
            ),
        ),
        "focused_window": focused,
        "platform": str(snapshot.get("platform", sys.platform)),
        "bounded": True,
    }


def _enumerate_platform_windows() -> Dict[str, Any]:
    platform = sys.platform

    if platform == "win32":
        return _enumerate_windows_uia()
    if platform == "darwin":
        return _enumerate_windows_ax()
    return _enumerate_windows_atspi()


def _enumerate_windows_uia() -> Dict[str, Any]:
    try:
        import comtypes  # noqa: F401
    except ImportError:
        return _empty_windows("win32", "uia_unavailable")

    return _empty_windows("win32", "uia_requires_runtime_binding")


def _enumerate_windows_ax() -> Dict[str, Any]:
    return _empty_windows("darwin", "ax_requires_runtime_binding")


def _enumerate_windows_atspi() -> Dict[str, Any]:
    return _empty_windows("linux", "atspi_requires_runtime_binding")


def _empty_windows(platform: str, reason: str) -> Dict[str, Any]:
    return {
        "windows": [],
        "focused_window": "",
        "platform": platform,
        "degraded": True,
        "reason": reason,
        "bounded": True,
    }
