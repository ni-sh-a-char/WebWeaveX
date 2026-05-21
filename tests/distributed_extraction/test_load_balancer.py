from core.distributed_extraction import (
    balance_extraction_workloads,
    create_extraction_worker,
)


def test_balance_extraction_workloads():
    workers = [
        create_extraction_worker(worker_id="w0"),
        create_extraction_worker(worker_id="w1"),
    ]
    tasks = [
        {"task_id": "t0", "url": "https://a.com"},
        {"task_id": "t1", "url": "https://b.com"},
        {"task_id": "t2", "url": "https://c.com"},
    ]

    result = balance_extraction_workloads(workers, tasks)

    assert len(result["assignments"]) == 3
    worker_ids = {item["worker_id"] for item in result["assignments"]}
    assert worker_ids == {"w0", "w1"}
