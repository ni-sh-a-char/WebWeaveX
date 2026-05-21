from core.interaction import close_modal, detect_modals


def test_modal_detection_and_close():
    page = type("Page", (), {})()
    page._test_modals = [
        {"type": "cookie", "selector": "#cookie-accept"}
    ]

    detected = detect_modals(page)

    assert detected["modals"]

    closed = close_modal(page, "#cookie-accept")

    assert closed["closed"] is True
    assert page._test_modals == []
