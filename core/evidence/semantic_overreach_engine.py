from __future__ import annotations

from typing import Any, Dict, List


def detect_semantic_overreach(
    evidence: List[str],
    inferred: Dict[str, Any],
    reconciled: Dict[str, Any],
) -> Dict[str, Any]:
    overreach = []
    if reconciled != inferred and len(evidence) < 2:
        overreach.append("reconciled_beyond_evidence")
    if len(inferred) > 0 and len(evidence) < 2:
        overreach.append("inference_expansion")
    if inferred and len(evidence) == 0:
        overreach.append("pure_heuristic_inference")
    return {
        "overreach_detected": bool(overreach),
        "overreach_flags": sorted(set(overreach)),
        "deterministic_inputs": [f"inferred_keys={len(inferred)}", f"evidence={len(evidence)}"],
    }
