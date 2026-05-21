from core.navigation.navigation_runtime_engine import run_navigation_runtime
from core.navigation.route_tracking_engine import track_navigation_routes
from core.navigation.spa_detection_engine import detect_single_page_application

__all__ = [
    "run_navigation_runtime",
    "track_navigation_routes",
    "detect_single_page_application",
]
