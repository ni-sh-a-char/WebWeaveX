from core.query import query_documents, query_repository, query_semantics, semantic_traverse


def test_query_document():
    r = query_documents("# A\n\n## B\n")
    assert "ir" in r
    assert r["explainable"] is True


def test_query_semantics_dispatch():
    r = query_semantics("document", {"text": "# Step\n\nBody"})
    assert r["query_type"] == "document"


def test_bounded_traversal():
    g = {"nodes": [{"id": "a"}], "edges": [{"from": "a", "to": "b"}, {"from": "b", "to": "c"}]}
    r = semantic_traverse(g, "a", max_depth=2)
    assert r["bounded"] is True
