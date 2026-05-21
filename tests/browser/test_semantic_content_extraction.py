from core.extraction.semantic_content_extraction_engine import (
    extract_semantic_content,
)


def test_extract_semantic_content():
    html = """
    <h1>Title</h1>
    <p>Paragraph one.</p>
    <a href="/docs">Docs</a>
    """
    result = extract_semantic_content(html)

    assert result["headings"][0]["text"] == "Title"
    assert "Paragraph one." in result["paragraphs"]
    assert "/docs" in result["links"]
    assert result["bounded"] is True
