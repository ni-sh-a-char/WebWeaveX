from core.ingestion.universal_ingestion_engine import (
    detect_input_type,
    ingest_input,
)


def test_detect_pdf():
    assert detect_input_type("a.pdf") == "pdf"


def test_detect_repository():
    assert detect_input_type("main.py") == "repository"


def test_unknown():
    assert detect_input_type("x.abc") == "unknown"


def test_ingest_input():
    result = ingest_input("doc.pdf")
    assert result["input_type"] == "pdf"
    assert result["supported"] is True
    assert result["bounded"] is True
