from core.graph.semantic_cycle_analysis_engine import detect_cycles


def test_cycle_abuse_bounded():
    n = 80
    edges = [{"from": f"n{i}", "to": f"n{(i+1)%n}"} for i in range(n)]
    g = {"nodes": [{"id": f"n{i}", "kind": "x"} for i in range(n)], "edges": edges}
    r = detect_cycles(g, max_depth=30)
    assert r["bounded"] == 30
