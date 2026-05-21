from __future__ import annotations

from typing import Any, Dict, Optional


def build_desktop_runtime(
    windows: Dict[str, Any],
    accessibility: Dict[str, Any],
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    window_list = list(windows.get("windows", []))

    active_apps = []
    seen = set()
    for window in window_list:
        app_name = str(window.get("application", window.get("app", "")))
        if app_name and app_name not in seen:
            seen.add(app_name)
            active_apps.append({
                "name": app_name,
                "windows": 1,
            })

    for app in snap.get("active_apps", []):
        name = str(app.get("name", ""))
        if name and name not in seen:
            active_apps.append(app)

    return {
        "active_apps": sorted(active_apps, key=lambda item: item["name"]),
        "runtime_state": {
            "focused_window": windows.get("focused_window", ""),
            "window_count": len(window_list),
        },
        "windows": window_list,
        "tabs": list(snap.get("tabs", [])),
        "dialogs": list(accessibility.get("dialogs", [])),
        "notifications": list(snap.get("notifications", [])),
        "bounded": True,
    }
