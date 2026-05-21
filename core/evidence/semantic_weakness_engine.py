from __future__ import annotations

from typing import Any, Dict, List


def build_weaknesses(evidence: List[str], ambiguities: List[str], min_evidence: int = 2) -> Dict[str, Any]:
    weaknesses = []
    if len(evidence) < min_evidence:
        weaknesses.append("insufficient_evidence")
    for a in ambiguities or []:
        weaknesses.append(f"ambiguity:{a}")
    return {
        "weaknesses": sorted(set(weaknesses)),
        "weak_evidence": len(evidence) < min_evidence,
        "weakness_count": len(weaknesses),
    }
