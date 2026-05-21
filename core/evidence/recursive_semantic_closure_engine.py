from __future__ import annotations

from typing import Any, Dict, List


def _closure_record(reason: str, depth: int) -> Dict[str, Any]:
    return {
        "reason": reason,
        "recursive_pressure": {"depth": depth, "level": min(1.0, depth * 0.12)},
        "closure_pressure": {"level": 0.8},
        "confidence_decay": {"required": True},
        "entropy_pressure": {"preserve": True},
        "truth_boundary_violation": {"type": "recursive_semantic_closure"},
        "recursive_instability": {"preserved": True},
    }


def detect_recursive_semantic_closure(
    depth: int,
    inferred: Dict[str, Any],
    reconciled: Dict[str, Any],
    evidence: List[str],
) -> Dict[str, Any]:
    suppressed: List[Dict[str, Any]] = []
    if depth >= 2 and reconciled == inferred and len(evidence) < 2:
        suppressed.append(_closure_record("recursive_coherence_closure", depth))
    if depth >= 3 and len(inferred) > len(evidence) + depth:
        suppressed.append(_closure_record("recursive_inference_amplification", depth))
    return {
        "closure_detected": bool(suppressed),
        "suppressed_closures": suppressed,
        "closure_pressure": round(min(1.0, depth * 0.15), 3),
    }
