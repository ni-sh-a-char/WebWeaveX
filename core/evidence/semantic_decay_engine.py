from __future__ import annotations

from typing import Any, Dict, List


def model_semantic_decay(
    evidence: List[str],
    inferred: Dict[str, Any],
    stabilization_count: int,
) -> Dict[str, Any]:
    decay_rate = round(min(1.0, (len(inferred) / max(1, len(evidence) + 1)) * 0.2 + stabilization_count * 0.15), 3)
    return {
        "decaying": decay_rate > 0,
        "decay_rate": decay_rate,
        "destabilize_unsupported": len(evidence) < 2,
        "prefer_incomplete": True,
    }
