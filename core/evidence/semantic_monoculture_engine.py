from __future__ import annotations

from typing import Any, Dict, List


def _suppression_record(reason: str) -> Dict[str, Any]:
    return {
        "reason": reason,
        "plurality_pressure": {"preserve": True},
        "monoculture_pressure": {"level": 0.9},
        "orthodoxy_pressure": {"level": 0.8},
        "closure_pressure": {"level": 0.7},
        "interpretive_diversity": {"required": True},
        "explanatory_diversity": {"required": True},
    }


def detect_semantic_monoculture(
    interpretations: List[Dict[str, Any]],
    evidence: List[str],
    depth: int,
) -> Dict[str, Any]:
    suppressed: List[Dict[str, Any]] = []
    if len(interpretations) <= 1 and depth >= 2 and len(evidence) < 2:
        suppressed.append(_suppression_record("semantic_monoculture"))
    return {"detected": bool(suppressed), "suppressed": suppressed}
