from core.browser.playwright_runtime import render_page


def test_runtime_exists():
    result = render_page("https://example.com")

    assert "available" in result
    assert "bounded" in result


def test_runtime_missing_playwright_or_error():
    result = render_page("https://example.com")
    if not result.get("available"):
        assert "reason" in result
