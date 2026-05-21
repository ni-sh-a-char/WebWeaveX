from core.causality.distributed_causality_engine import build_distributed_causality


def test_distributed_propagation_stable():
    workers = [
        {"id": "dist:0", "runtime": "distributed", "step": 0, "worker_id": "w1"},
        {"id": "dist:1", "runtime": "distributed", "step": 1, "worker_id": "w2"},
    ]

    first = build_distributed_causality(
        {"workers": [{"id": "w1"}, {"id": "w2"}], "autonomous": True},
        workers,
    )
    second = build_distributed_causality(
        {"workers": [{"id": "w1"}, {"id": "w2"}], "autonomous": True},
        workers,
    )

    assert first == second
    assert first["cluster_synchronization"]["synced"] is True
