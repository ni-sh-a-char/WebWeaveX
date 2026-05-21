from core.graph.graph_invariant_engine import check_graph_invariants


def test_forbidden_edge_type():
    g = {
        "nodes": [{"id": "a", "kind": "n"}, {"id": "b", "kind": "n"}],
        "edges": [{"from": "a", "to": "b", "type": "bad"}],
    }
    r = check_graph_invariants(g)
    assert r["valid"] is False
    assert any(v["rule"] == "no_edge_type" for v in r["violations"])


def test_valid_graph():
    g = {
        "nodes": [{"id": "a", "kind": "n"}, {"id": "b", "kind": "n"}],
        "edges": [{"from": "a", "to": "b", "evidence": ["e1"]}],
    }
    assert check_graph_invariants(g)["valid"] is True
