from core.auth.cookie_runtime_engine import extract_cookies, inject_cookies


class _MockContext:
    def __init__(self):
        self._test_cookies = []

    def cookies(self):
        return list(self._test_cookies)

    def add_cookies(self, cookies):
        self._test_cookies = list(cookies)


def test_cookie_injection():
    context = _MockContext()

    cookies = [
        {
            "name": "sid",
            "value": "abc",
            "domain": "example.com",
            "path": "/",
        }
    ]

    inject_cookies(context, cookies)
    extracted = extract_cookies(context)

    assert extracted["cookies"][0]["name"] == "sid"
