from core.graph.semantic_cycle_analysis_engine import detect_cycles


def test_cycle_bounded_depth():
    edges = [{"from": f"n{i}", "to": f"n{i+1}"} for i in range(60)]
    edges.append({"from": "n59", "to": "n0"})
    g = {"nodes": [{"id": f"n{i}", "kind": "x"} for i in range(60)], "edges": edges}
    r = detect_cycles(g, max_depth=50)
    assert r["bounded"] == 50
