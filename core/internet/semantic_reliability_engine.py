from __future__ import annotations

from typing import Any, Dict, List

from core.internet.evidence_reliability_engine import score_evidence_reliability


def score_semantic_reliability(evidence: List[str], parser_backed: bool = False) -> Dict[str, Any]:
    r = score_evidence_reliability(evidence, parser_backed)
    return {
        **r,
        "reliability_basis": "evidence_weight_calculus",
        "opaque": False,
    }
