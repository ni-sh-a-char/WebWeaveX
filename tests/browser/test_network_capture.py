from core.network.network_capture_engine import attach_network_capture


class _FakeRequest:
    def __init__(self, url: str, method: str = "GET", resource_type: str = "document"):
        self.url = url
        self.method = method
        self.resource_type = resource_type


class _FakePage:
    def __init__(self):
        self._handlers = {}

    def on(self, event: str, handler):
        self._handlers[event] = handler

    def emit_request(self, req):
        handler = self._handlers.get("request")
        if handler:
            handler(req)


def test_attach_network_capture():
    page = _FakePage()
    state = attach_network_capture(page)

    page.emit_request(_FakeRequest("https://example.com"))
    page.emit_request(_FakeRequest("https://example.com/app.js", resource_type="script"))

    assert len(state["requests"]) == 2
    assert state["bounded"] is True
