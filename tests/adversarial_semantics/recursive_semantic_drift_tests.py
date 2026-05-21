from core.documents.document_semantic_ir_engine import build_document_semantic_ir


def test_deterministic_discourse_ir():
    text = "# A\n\n## B\n"
    a = build_document_semantic_ir(text)
    b = build_document_semantic_ir(text)
    assert a["rhetorical"]["unit_count"] == b["rhetorical"]["unit_count"]
