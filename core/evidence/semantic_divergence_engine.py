from __future__ import annotations

from typing import Any, Dict, List


def model_semantic_divergence(observed: Dict[str, Any], inferred: Dict[str, Any], ambiguities: List[str]) -> Dict[str, Any]:
    keys = set(observed.keys()) | set(inferred.keys())
    score = round(min(1.0, len(keys) * 0.15 + len(ambiguities) * 0.1), 3)
    return {"divergence_score": score, "preserved": score > 0 or bool(ambiguities), "phase_space_maintained": len(keys) > 1}
