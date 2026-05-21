from core.graph.topology_proof_engine import prove_topology


def test_topology_proof_hubs():
    g = {
        "nodes": [{"id": "a", "kind": "n"}, {"id": "b", "kind": "n"}, {"id": "c", "kind": "n"}],
        "edges": [
            {"from": "a", "to": "b"},
            {"from": "a", "to": "c"},
            {"from": "b", "to": "c"},
        ],
    }
    r = prove_topology(g)
    assert r["proved"] is True
    assert r["max_degree"] >= 2
