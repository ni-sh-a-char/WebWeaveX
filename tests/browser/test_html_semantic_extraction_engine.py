from core.browser.html_semantic_extraction_engine import extract_semantic_html


def test_extract_semantic_html():
    html = """
    <html>
      <head><title>Test Page</title></head>
      <body>
        <h1>Hello</h1>
        <a href="https://example.com">link</a>
      </body>
    </html>
    """
    result = extract_semantic_html(html)

    assert result["title"] == "Test Page"
    assert "https://example.com" in result["links"]
    assert result["headings"][0]["text"] == "Hello"
    assert result["bounded"] is True
