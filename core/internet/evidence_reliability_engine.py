from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.evidence_weighting_calculus import weight_evidence_calculus


def score_evidence_reliability(evidence: List[str], parser_backed: bool = False) -> Dict[str, Any]:
    w = weight_evidence_calculus(evidence, parser_backed)
    reliability = round(min(1.0, w["total"] / max(1, len(w["weights"] or {}))), 3)
    return {
        "reliability": reliability,
        "weights": w["weights"],
        "deterministic_inputs": w["deterministic_inputs"],
    }
