from core.synchronization.runtime_state_graph_engine import build_runtime_state_graph


def test_state_graph_edges():
    snapshot = {"snapshot_id": "snapshot:0"}
    delta = {
        "delta_id": "delta:0",
        "changes": [{"field": "semantic", "kind": "semantic_change"}],
    }
    convergence = {"converged": True}

    graph = build_runtime_state_graph(snapshot, delta, convergence)

    relations = {edge["relation"] for edge in graph["edges"]}
    assert "mutates" in relations
    assert "converges" in relations
