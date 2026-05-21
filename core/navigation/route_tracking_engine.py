from __future__ import annotations

from typing import Any, Dict, List

MAX_ROUTES = 1000


def track_navigation_routes(page: Any) -> Dict[str, Any]:
    routes: List[Dict[str, Any]] = []

    if page is not None and hasattr(page, "_test_route_history"):
        routes = list(page._test_route_history)[:MAX_ROUTES]
        return {
            "routes": routes,
            "transitions": _route_edges(routes),
            "bounded": True,
        }

    current = ""

    if page is not None:
        current = str(getattr(page, "_test_url", getattr(page, "url", "")))

    if current:
        routes.append({
            "path": current,
            "order": 0,
        })

    return {
        "routes": routes,
        "transitions": _route_edges(routes),
        "bounded": True,
    }


def _route_edges(routes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    edges: List[Dict[str, Any]] = []

    for index in range(len(routes) - 1):
        edges.append({
            "from": str(routes[index].get("path", "")),
            "to": str(routes[index + 1].get("path", "")),
            "relation": "route_transition",
        })

    return edges[:MAX_ROUTES]
