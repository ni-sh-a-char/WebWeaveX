from core.ocr.ocr_engine import extract_ocr_text


def test_ocr_missing_file():
    result = extract_ocr_text("missing.png")
    assert result["available"] is False
    assert "bounded" in result
