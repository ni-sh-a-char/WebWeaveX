from __future__ import annotations

from typing import Any, Dict, List


def assess_evidence_sufficiency(evidence: List[str], required: int = 2) -> Dict[str, Any]:
    count = len(evidence or [])
    sufficient = count >= required
    return {
        "sufficient": sufficient,
        "evidence_count": count,
        "required": required,
        "status": "sufficient" if sufficient else "insufficient_evidence",
        "deterministic_inputs": [f"count={count}", f"required={required}"],
    }
