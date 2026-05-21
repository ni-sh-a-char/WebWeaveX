from core.navigation import detect_single_page_application


def test_spa_detection_markers():
    page = type("Page", (), {})()
    page._test_spa_markers = ["react", "history.pushState"]

    result = detect_single_page_application(page)

    assert result["spa"] is True
    assert "react" in result["markers"]
