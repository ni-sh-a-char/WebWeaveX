from __future__ import annotations

from typing import Any, Dict, List


def model_evidence_decay(evidence: List[str], *, min_evidence: int = 2) -> Dict[str, Any]:
    incomplete = len(evidence) < min_evidence
    return {
        "decaying": incomplete,
        "incomplete": incomplete,
        "honest_incompleteness": incomplete,
        "evidence_count": len(evidence),
    }
