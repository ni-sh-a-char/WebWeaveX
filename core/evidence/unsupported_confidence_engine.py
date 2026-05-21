from __future__ import annotations

from typing import Any, Dict


def block_unsupported_confidence_escalation(
    score: float,
    evidence_count: int,
    *,
    min_evidence: int = 2,
    max_without_evidence: float = 0.45,
) -> Dict[str, Any]:
    if evidence_count >= min_evidence:
        return {"escalation_blocked": False, "capped_score": score, "reason": None}
    capped = min(score, max_without_evidence)
    return {
        "escalation_blocked": score > capped,
        "capped_score": round(capped, 3),
        "reason": "unsupported_confidence_escalation",
        "evidence_count": evidence_count,
    }
