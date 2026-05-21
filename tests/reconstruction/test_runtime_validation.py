import tempfile
from pathlib import Path

from core.reconstruction import run_reconstruction_runtime
from core.reconstruction.runtime_snapshot_engine import load_reconstruction_snapshot, save_reconstruction_snapshot
from core.reconstruction.runtime_validation_engine import validate_reconstructed_runtime


def test_fabrication_validity():
    result = run_reconstruction_runtime(
        sources={"semantic_ir": {"ir": "semantic_runtime"}},
        fabricate=True,
        tick=1,
    )

    validation = result["validation"]
    assert validation["valid"] is True
    assert validation["integrity_score"] == 1.0


def test_checkpoint_restore():
    snapshot = {"state": {"runtime": {"runtime_id": "abc"}}, "bounded": True}

    with tempfile.TemporaryDirectory() as tmp:
        path = str(Path(tmp) / "reconstruction.snapshot")
        key = "test-key-phase-y"

        save_reconstruction_snapshot(path, snapshot, key)
        first = load_reconstruction_snapshot(path, key)
        second = load_reconstruction_snapshot(path, key)

    assert first == second
    assert first["snapshot"]["state"] == snapshot["state"]


def test_validation_engine():
    runtime = {"reconstructed": True, "replay_safe": True}
    result = validate_reconstructed_runtime(runtime=runtime, replay={"replay_chains": [{"step": 0}]})
    assert result["valid"] is True
