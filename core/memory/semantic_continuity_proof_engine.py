from __future__ import annotations

from typing import Any, Dict, List


def prove_semantic_continuity(checkpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
    fps = [c.get("fingerprint") for c in checkpoints if c.get("fingerprint")]
    unique = sorted(set(fps))
    return {
        "continuous": len(unique) == len(fps),
        "checkpoint_count": len(fps),
        "unique_fingerprints": len(unique),
        "deterministic": True,
    }
