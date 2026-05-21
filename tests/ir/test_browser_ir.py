from core.ir.browser_ir import compile_browser_ir


def test_compile_browser_ir():
    result = compile_browser_ir(
        runtime={"url": "https://example.com"},
        dom={"node_count": 1},
        extraction={"headings": []},
        network={"requests": []},
    )

    assert result["ir"] == "browser"
    assert result["bounded"] is True
