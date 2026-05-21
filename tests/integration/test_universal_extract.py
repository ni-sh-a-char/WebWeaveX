from webweavex import universal_extract, ingest_input


def test_universal_extract_exists():
    result = universal_extract("x.unknown")

    assert result.get("unsupported") is True


def test_ingest_input_exported():
    result = ingest_input("readme.md")
    assert result["input_type"] == "markdown"


def test_universal_extract_html(tmp_path):
    html_path = tmp_path / "page.html"
    html_path.write_text("<html><body><p>ok</p></body></html>", encoding="utf-8")

    from webweavex import universal_extract

    result = universal_extract(str(html_path))
    assert result["extraction"]["available"] is True
    assert result["bounded"] is True
