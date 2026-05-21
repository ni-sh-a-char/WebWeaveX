from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_native_navigation(
    desktop: Dict[str, Any],
    electron: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    routes: List[Dict[str, Any]] = []

    for app in desktop.get("active_apps", []):
        routes.append({
            "type": "app",
            "path": str(app.get("name", "")),
        })

    if electron:
        for route in electron.get("routes", []):
            routes.append({
                "type": "electron_route",
                "path": str(route),
            })

    return {
        "routes": sorted(routes, key=lambda item: item["path"]),
        "tabs": list(desktop.get("tabs", [])),
        "bounded": True,
    }
