from core.browser.universal_web_extraction_engine import extract_web


def test_extract_web_exists():
    result = extract_web("https://example.com")

    assert "bounded" in result


def test_extract_web_structure_when_available():
    result = extract_web("https://example.com")
    if result.get("runtime", {}).get("available"):
        assert "browser_ir" in result
        assert result["browser_ir"]["ir"] == "browser"
        assert "dom" in result
        assert "extraction" in result
