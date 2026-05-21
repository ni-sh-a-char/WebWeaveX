import tempfile
from pathlib import Path

from core.execution.runtime_checkpoint_engine import (
    load_execution_checkpoint,
    save_execution_checkpoint,
)


def test_checkpoint_restore():
    checkpoint = {
        "state": {"browser": {"url": "https://example.com"}},
        "transactions": [],
        "bounded": True,
    }

    with tempfile.TemporaryDirectory() as tmp:
        path = str(Path(tmp) / "execution.checkpoint")
        key = "test-key-phase-x"

        save_execution_checkpoint(path, checkpoint, key)
        first = load_execution_checkpoint(path, key)
        second = load_execution_checkpoint(path, key)

    assert first == second
    assert first["checkpoint"]["state"] == checkpoint["state"]
