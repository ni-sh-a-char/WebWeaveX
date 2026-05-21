from __future__ import annotations

from typing import Any, Dict

from core.navigation.route_tracking_engine import track_navigation_routes
from core.navigation.spa_detection_engine import detect_single_page_application


def run_navigation_runtime(page: Any) -> Dict[str, Any]:
    spa = detect_single_page_application(page)
    routes = track_navigation_routes(page)

    return {
        "spa": spa,
        "routes": routes,
        "bounded": True,
    }
