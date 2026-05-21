from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.interaction import extract_infinite_scroll


class _ScrollPage:
    def __init__(self):
        self._test_html = "<html>start</html>"
        self._test_dom_hash = compute_kaalka_hash(self._test_html)
        self._count = 0

    def _test_scroll(self):
        self._count += 1
        if self._count > 2:
            return
        self._test_html += f"<div>{self._count}</div>"
        self._test_dom_hash = compute_kaalka_hash(self._test_html)


def test_infinite_scroll_bounds():
    result = extract_infinite_scroll(_ScrollPage())

    assert result["scrolls"] <= 100
    assert result["bounded"] is True
