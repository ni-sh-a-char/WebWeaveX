from core.synchronization.reality_replication_engine import replicate_runtime_reality


def test_replication_consistency():
    source = {
        "reality_id": "primary",
        "semantic_state": {"domain": "analytics"},
        "runtime_state": {"tick": 1},
        "workflows": {"objective": "monitor_metrics"},
        "checkpoints": [],
        "causality_graph": {},
    }
    workers = [{"worker_id": "w1"}, {"worker_id": "w2"}]

    first = replicate_runtime_reality(source, workers)
    second = replicate_runtime_reality(source, workers)

    assert first == second
    assert first["replica_count"] == 2
