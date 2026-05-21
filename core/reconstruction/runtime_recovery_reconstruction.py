from __future__ import annotations

from typing import Any, Dict, List, Optional


def recover_reconstructed_runtime(
    checkpoint: Optional[Dict[str, Any]] = None,
    failed_segments: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    checkpoint = checkpoint or {}
    failed = list(failed_segments or [])

    return {
        "checkpoint_restored": bool(checkpoint),
        "failed_segments_recovered": len(failed),
        "segments": sorted(failed, key=lambda item: str(item.get("id", ""))),
        "replay_safe": True,
        "bounded": True,
    }
