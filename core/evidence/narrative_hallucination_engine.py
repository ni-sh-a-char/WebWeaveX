from __future__ import annotations

from typing import Any, Dict, List


def detect_narrative_hallucination(
    inferred: Dict[str, Any],
    evidence: List[str],
    parser_grounded: bool,
) -> Dict[str, Any]:
    hallucinated = bool(inferred) and not parser_grounded and len(evidence) < 1
    return {
        "hallucination_risk": hallucinated,
        "suppressed": hallucinated,
        "reason": "narrative_without_parser" if hallucinated else None,
    }
