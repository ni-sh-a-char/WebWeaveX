from core.graph.topology_reasoning_engine import reason_topology


def test_topology_exposes_justification():
    g = {
        "nodes": [{"id": "a", "kind": "n"}, {"id": "b", "kind": "n"}, {"id": "c", "kind": "n"}],
        "edges": [{"from": "a", "to": "b"}, {"from": "b", "to": "c"}],
    }
    r = reason_topology(g)
    assert r["proved"] is True
    assert "justification" in r
    assert "evidence" in r
