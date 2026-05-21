from __future__ import annotations

from typing import Any, Dict, List


def model_evidence_boundaries(evidence: List[str], *, min_evidence: int = 2) -> Dict[str, Any]:
    bounded = len(evidence) >= min_evidence
    return {
        "bounded": bounded,
        "evidence_count": len(evidence),
        "min_required": min_evidence,
        "violation": not bounded,
        "where_evidence_stops": len(evidence),
    }
