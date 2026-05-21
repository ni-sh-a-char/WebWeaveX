from core.reconstruction.runtime_topology_reconstruction import reconstruct_runtime_topology


def test_topology_consistency():
    graph = {
        "nodes": [{"id": "w1", "type": "worker"}],
        "edges": [{"from": "w1", "to": "n1", "relation": "routes"}],
    }
    workers = [{"worker_id": "w1", "runtime": "browser"}]

    first = reconstruct_runtime_topology(runtime_graph=graph, workers=workers)
    second = reconstruct_runtime_topology(runtime_graph=graph, workers=workers)

    assert first == second
    assert first["reconstructed"] is True
