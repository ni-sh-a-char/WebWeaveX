from __future__ import annotations

from typing import Any, Dict, List


def suppress_unsupported_inference(
    evidence: List[str],
    inferred: Dict[str, Any],
    observed: Dict[str, Any],
    min_evidence: int = 2,
) -> Dict[str, Any]:
    unsupported_dims = []
    suppressed = []
    if len(evidence) < min_evidence and inferred:
        unsupported_dims.append("inferred_without_evidence")
        suppressed = sorted(inferred.keys())
    if inferred and not observed:
        unsupported_dims.append("inferred_without_observation")
    return {
        "suppressed": bool(suppressed),
        "unsupported_dimensions": sorted(set(unsupported_dims)),
        "suppressed_keys": suppressed,
        "allowed_inference": len(evidence) >= min_evidence,
    }
