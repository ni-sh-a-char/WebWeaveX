from core.files.docx_extraction_engine import extract_docx_text


def test_docx_missing_dependency_or_file():
    result = extract_docx_text("missing.docx")
    assert result["available"] is False
    assert "bounded" in result
