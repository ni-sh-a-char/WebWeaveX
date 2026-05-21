from core.distributed_extraction import (
    create_extraction_worker,
    failover_extraction_runtime,
)


def test_failover_migration():
    checkpoint = {
        "workers": [
            create_extraction_worker(worker_id="worker_dead"),
            create_extraction_worker(worker_id="worker_live"),
        ],
        "queue": [
            {"task_id": "t1", "url": "https://example.com", "priority": 0},
        ],
        "bounded": True,
    }

    result = failover_extraction_runtime(checkpoint, "worker_dead")

    assert result["dead_worker"] == "worker_dead"
    assert result["replacement_worker"].endswith("_migrated")
    assert result["assignments"]
