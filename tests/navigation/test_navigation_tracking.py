from core.navigation import track_navigation_routes


def test_navigation_tracking():
    page = type("Page", (), {})()
    page._test_route_history = [
        {"path": "/", "order": 0},
        {"path": "/dashboard", "order": 1},
    ]

    result = track_navigation_routes(page)

    assert len(result["routes"]) == 2
    assert len(result["transitions"]) == 1
