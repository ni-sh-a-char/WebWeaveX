from core.graph.graph_invariant_engine import check_graph_invariants


def test_type_field_attack():
    g = {"nodes": [{"id": "a", "kind": "n"}], "edges": [{"from": "a", "to": "b", "type": "x"}]}
    assert check_graph_invariants(g)["valid"] is False
