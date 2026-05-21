from core.adaptive import recover_modal_runtime


def test_modal_recovery():
    page = type("Page", (), {})()
    page._test_modals = [{"type": "cookie", "selector": "#cookie-accept"}]

    html = '<button id="cookie-accept">Accept</button>'

    result = recover_modal_runtime(page, html)

    assert result["recovered"]
    assert page._test_modals == []
