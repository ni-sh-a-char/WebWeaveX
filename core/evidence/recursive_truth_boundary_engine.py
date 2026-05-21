from __future__ import annotations

from typing import Any, Dict


def model_recursive_truth_boundaries(depth: int, evidence_count: int, *, min_evidence: int = 2) -> Dict[str, Any]:
    erosion = round(min(1.0, depth * 0.08), 3)
    bounded = evidence_count >= min_evidence and erosion < 0.5
    return {
        "bounded": bounded,
        "depth": depth,
        "erosion": erosion,
        "closure_allowed": False,
        "recursive_lock_in_allowed": False,
    }
