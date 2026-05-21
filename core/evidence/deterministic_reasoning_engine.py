from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.evidence_algebra_engine import combine_evidence
from core.evidence.semantic_inference_calculus import infer_from_evidence


def reason_deterministically(
    observed: Dict[str, Any],
    evidence: List[str],
    ambiguities: List[str],
) -> Dict[str, Any]:
    """Single-step deterministic reasoning with explicit inputs."""
    algebra = combine_evidence(evidence)
    inference = infer_from_evidence(observed, evidence, min_evidence=1 if algebra["sufficient"] else 2)
    conservative = bool(ambiguities) or not algebra["sufficient"]
    return {
        "algebra": algebra,
        "inference": inference,
        "conservative": conservative,
        "chain_depth": 1,
        "opaque": False,
        "deterministic_inputs": algebra["deterministic_inputs"] + inference["deterministic_inputs"],
    }
