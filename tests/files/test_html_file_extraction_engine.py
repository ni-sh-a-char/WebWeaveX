from core.files.html_file_extraction_engine import extract_html_file


def test_extract_html_file(tmp_path):
    html_path = tmp_path / "page.html"
    html_path.write_text(
        "<html><head><title>T</title></head>"
        "<body><h1>Hi</h1><p>Text</p></body></html>",
        encoding="utf-8",
    )

    result = extract_html_file(str(html_path))

    assert result["available"] is True
    assert result["browser_ir"]["ir"] == "browser"
    assert result["semantic"]["title"] == "T"
    assert result["bounded"] is True


def test_html_file_missing():
    result = extract_html_file("missing.html")
    assert result["available"] is False
