from __future__ import annotations

from typing import Any, Dict


def capture_memory_snapshot(
    state: Dict[str, Any],
    tick: int = 0,
) -> Dict[str, Any]:
    return {
        "snapshot_id": f"memory_snapshot:{tick}",
        "tick": tick,
        "state": dict(state),
        "bounded": True,
    }
