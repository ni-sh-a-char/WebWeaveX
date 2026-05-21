from core.auth.token_runtime_engine import extract_auth_tokens, inject_auth_tokens


class _MockPage:
    def __init__(self):
        self._test_headers = {}
        self._test_tokens = []


def test_token_injection_and_extraction():
    page = _MockPage()

    tokens = [
        {
            "type": "bearer",
            "value": "abc.def.ghi",
        }
    ]

    inject_auth_tokens(page, tokens)
    page._test_headers["Authorization"] = "Bearer abc.def.ghi"

    extracted = extract_auth_tokens(page)

    assert extracted["tokens"][0]["type"] == "bearer"
