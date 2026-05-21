from core.graph.graph_invariant_engine import check_graph_invariants


def test_large_graph_bounded():
    nodes = [{"id": f"n{i}", "kind": "x"} for i in range(100)]
    edges = [{"from": f"n{i}", "to": f"n{i+1}", "evidence": ["e"]} for i in range(99)]
    r = check_graph_invariants({"nodes": nodes, "edges": edges})
    assert r["edge_count"] == 99
