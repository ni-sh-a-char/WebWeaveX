from core.native.native_checkpoint_engine import (
    load_native_checkpoint,
    save_native_checkpoint,
)
from core.native import run_native_cognition


def test_native_checkpoint_deterministic(tmp_path):
    cognition = run_native_cognition(
        runtime="desktop",
        application="vscode",
    )

    path = tmp_path / "native.cp.enc"
    checkpoint = {
        "runtime_state": cognition["native_state"],
        "windows": cognition["windows"],
        "terminals": cognition["terminal"],
        "workflows": cognition["navigation"],
    }

    save_native_checkpoint(str(path), checkpoint, "cp-key")
    first = load_native_checkpoint(str(path), "cp-key")
    second = load_native_checkpoint(str(path), "cp-key")

    assert first == second
    assert first["available"] is True
