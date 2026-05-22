"""Playwright runtime branches with mocked sync_playwright."""

from core.browser import playwright_runtime as pr


def test_launch_without_playwright(monkeypatch):
    monkeypatch.setattr(pr, "sync_playwright", None)
    out = pr.launch_authenticated_browser()
    assert out.get("available") is False
    assert out.get("reason") == "playwright_missing"


def test_render_page_mock(monkeypatch):
    class _Page:
        url = "https://example.com"

        def content(self):
            return "<html><body>ok</body></html>"

        def title(self):
            return "ok"

        def goto(self, url, wait_until=None, timeout=None):
            self.url = url

        def set_extra_http_headers(self, headers):
            return None

        def evaluate(self, _script):
            return {}

    class _Context:
        def cookies(self):
            return []

        def new_page(self):
            return _Page()

    class _Browser:
        def new_context(self, **kwargs):
            return _Context()

        def close(self):
            return None

    class _PW:
        def start(self):
            return self

        def stop(self):
            return None

        class chromium:
            @staticmethod
            def launch(headless=True):
                return _Browser()

    monkeypatch.setattr(pr, "sync_playwright", lambda: _PW())
    monkeypatch.setattr(pr, "attach_network_capture", lambda page: {"requests": []})
    monkeypatch.setattr(
        pr,
        "persist_authenticated_context",
        lambda ctx, page, session: session,
    )
    out = pr.render_page("https://example.com", session={"headers": {"X": "1"}, "cookies": []})
    assert out.get("available") is True
    assert "html" in out

    auth_out = pr.render_page(
        "https://example.com",
        session={"cookies": [{"name": "s", "value": "1"}]},
        authenticated=True,
        persistent_identity=True,
    )
    assert auth_out.get("available") is True
