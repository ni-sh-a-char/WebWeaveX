from core.files.pdf_extraction_engine import extract_pdf_text


def test_pdf_engine_exists():
    result = extract_pdf_text("missing.pdf")

    assert "bounded" in result or result["available"] is False


def test_pdf_missing_file():
    result = extract_pdf_text("missing.pdf")
    assert result["available"] is False
