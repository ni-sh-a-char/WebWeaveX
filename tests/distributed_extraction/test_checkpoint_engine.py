from core.distributed_extraction import (
    create_extraction_worker,
    load_distributed_checkpoint,
    save_distributed_checkpoint,
)


def test_checkpoint_recovery(tmp_path):
    checkpoint = {
        "queue": [{"task_id": "t1", "url": "https://example.com", "priority": 0}],
        "workers": [
            create_extraction_worker(
                worker_id="worker_0",
                identity={"profile_id": "default", "fingerprint_hash": "abc"},
            )
        ],
        "tick": 3,
        "bounded": True,
    }

    path = tmp_path / "cluster.enc"
    save_distributed_checkpoint(str(path), checkpoint, "cluster-key")

    loaded = load_distributed_checkpoint(str(path), "cluster-key")

    assert loaded["available"] is True
    assert loaded["checkpoint"]["tick"] == 3
    assert loaded["checkpoint"]["workers"][0]["worker_id"] == "worker_0"
