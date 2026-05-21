from core.distributed_extraction import create_extraction_worker
from core.distributed_extraction.distributed_recovery_engine import (
    recover_distributed_runtime,
)


def test_identity_continuity_on_recovery():
    identity = {"profile_id": "default", "fingerprint_hash": "stable-fp"}
    checkpoint = {
        "workers": [
            create_extraction_worker(
                worker_id="worker_0",
                identity=identity,
            )
        ],
        "queue": [],
        "bounded": True,
    }

    recovered = recover_distributed_runtime(
        checkpoint,
        failed_worker_ids=["worker_0"],
    )

    assert recovered["workers"][0]["identity"] == identity
