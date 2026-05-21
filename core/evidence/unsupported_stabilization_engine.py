from __future__ import annotations

from typing import Any, Dict, List


def _stabilization_record(reason: str, evidence_gap: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "reason": reason,
        "reinforcement_pressure": {"level": 0.8},
        "evidence_gap": evidence_gap,
        "semantic_instability": {"preserved": True, "unstable": True},
        "truth_boundary_violation": {"type": "unsupported_stabilization"},
        "confidence_collapse": {"required": True},
    }


def detect_unsupported_stabilization(
    evidence: List[str],
    inferred: Dict[str, Any],
    reconciled: Dict[str, Any],
    *,
    min_evidence: int = 2,
) -> Dict[str, Any]:
    suppressed: List[Dict[str, Any]] = []
    gap = {"required": min_evidence, "actual": len(evidence)}
    if reconciled == inferred and len(evidence) < min_evidence and inferred:
        suppressed.append(_stabilization_record("coherence_stabilization", gap))
    if len(inferred) > len(evidence) + 1:
        suppressed.append(_stabilization_record("inference_confirming_inference", gap))
    return {
        "stabilization_detected": bool(suppressed),
        "suppressed_stabilizations": suppressed,
        "count": len(suppressed),
    }
