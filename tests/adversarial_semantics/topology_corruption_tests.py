from core.graph.semantic_graph_validator import validate_semantic_graph


def test_corrupt_graph_rejected():
    g = {"nodes": [{"id": "a", "kind": "n"}], "edges": [{"from": "a", "to": "missing", "type": "bad"}]}
    assert validate_semantic_graph(g)["valid"] is False
