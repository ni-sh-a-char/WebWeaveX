from __future__ import annotations

from typing import Any, Dict


def model_semantic_boundaries(inferred: Dict[str, Any], allowed: bool) -> Dict[str, Any]:
    return {
        "inference_allowed": allowed,
        "bounded_inferences": sorted(inferred.keys()) if allowed else [],
        "blocked_inferences": sorted(inferred.keys()) if not allowed else [],
        "where_inference_stops": [] if allowed else sorted(inferred.keys()),
        "reality_bounded": allowed,
    }
