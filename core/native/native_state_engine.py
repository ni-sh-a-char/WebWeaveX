from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_native_state(
    runtime: str,
    windows: Dict[str, Any],
    desktop: Dict[str, Any],
    focused_element: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "runtime": runtime,
        "focused_window": windows.get("focused_window", ""),
        "window_count": len(windows.get("windows", [])),
        "active_apps": desktop.get("active_apps", []),
        "dialogs": desktop.get("dialogs", []),
        "notifications": desktop.get("notifications", []),
        "focused_element": focused_element or {},
        "bounded": True,
    }
