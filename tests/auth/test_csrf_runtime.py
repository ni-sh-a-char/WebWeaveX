from core.auth.csrf_runtime_engine import extract_csrf_tokens


class _MockPage:
    def __init__(self, html: str):
        self._test_html = html
        self._test_headers = {"X-CSRF-Token": "csrf-header-value"}


def test_csrf_extraction():
    page = _MockPage(
        '<html><head>'
        '<meta name="csrf-token" content="meta-token" />'
        '</head><body>'
        '<input name="csrf_token" value="input-token" />'
        '</body></html>'
    )

    result = extract_csrf_tokens(page)

    sources = {item["source"] for item in result["tokens"]}

    assert "meta" in sources
    assert "hidden_input" in sources
    assert "header" in sources
