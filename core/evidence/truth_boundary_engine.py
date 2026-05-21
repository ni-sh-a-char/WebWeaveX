from __future__ import annotations

from typing import Any, Dict, List


def model_truth_boundaries(evidence: List[str], *, min_evidence: int = 2) -> Dict[str, Any]:
    bounded = len(evidence) >= min_evidence
    return {
        "truth_bounded": bounded,
        "inference_to_reality_allowed": bounded,
        "coherence_normalization_allowed": False,
        "where_truth_stops": len(evidence),
    }
