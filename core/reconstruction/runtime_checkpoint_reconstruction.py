from __future__ import annotations

from typing import Any, Dict, Optional

from core.reconstruction.runtime_snapshot_engine import restore_reconstruction_snapshot


def reconstruct_from_checkpoint(
    checkpoint: Dict[str, Any],
) -> Dict[str, Any]:
    restored = restore_reconstruction_snapshot(checkpoint)
    return {
        "reconstructed_from_checkpoint": True,
        "state": restored.get("state", {}),
        "topology": restored.get("topology", {}),
        "replay_chains": restored.get("replay_chains", []),
        "bounded": True,
    }
