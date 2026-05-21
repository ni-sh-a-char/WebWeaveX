from core.adaptive import recover_pagination_flow


def test_pagination_recovery():
    html = '<a class="next" href="/page/2">Next</a>'

    result = recover_pagination_flow("#old-next", html)

    assert result["recovered_selector"]
    assert "next" in result["recovered_selector"].lower()
