from core.distributed_extraction import create_extraction_worker


def test_create_extraction_worker():
    worker = create_extraction_worker(
        worker_id="worker_0",
        identity={"profile_id": "default"},
        status="idle",
    )

    assert worker["worker_id"] == "worker_0"
    assert worker["status"] == "idle"
    assert worker["bounded"] is True
