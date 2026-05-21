from core.interaction import extract_paginated_content


class _PaginationPage:
    def __init__(self):
        self._test_url = "https://example.com/"
        self._clicks = 0

    def click(self, selector):
        self._clicks += 1

    def _test_paginate(self, current_url):
        if current_url.endswith("/page/2"):
            return current_url
        return current_url.rstrip("/") + "/page/2"


def test_pagination_loop_prevention():
    page = _PaginationPage()

    result = extract_paginated_content(page, "a.next")

    urls = [item["url"] for item in result["pages"]]

    assert len(urls) == len(set(urls))
    assert result["loop_prevented"] is True
