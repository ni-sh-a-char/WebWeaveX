from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.semantic_inference_calculus import infer_from_evidence


def validate_inference(observed: Dict[str, Any], evidence: List[str]) -> Dict[str, Any]:
    r = infer_from_evidence(observed, evidence)
    return {
        "valid": r["allowed"],
        "inference": r,
        "opaque": False,
        "deterministic_inputs": r["deterministic_inputs"],
    }
