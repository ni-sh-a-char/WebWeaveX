from core.documents.semantic_discourse_parser import parse_semantic_discourse
from core.documents.document_dependency_graph_engine import build_document_dependency_graph


def test_discourse_parser_layers():
    r = parse_semantic_discourse("# Claim\n\n## Support\n\nText.")
    assert r["rhetorical"]["unit_count"] >= 2
    assert len(r["argument"]["nodes"]) >= 1


def test_dependency_graph():
    g = build_document_dependency_graph("# A\n\n## B\n")
    assert "nodes" in g
