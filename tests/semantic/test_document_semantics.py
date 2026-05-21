from core.semantic.document_semantics_engine import extract_document_semantics


def test_document_api_reference():
    text = "GET /users endpoint request response OpenAPI specification"

    doc = extract_document_semantics(text)

    assert "api_reference" in doc["kinds"]
