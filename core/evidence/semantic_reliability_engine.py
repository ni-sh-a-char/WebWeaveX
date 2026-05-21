from __future__ import annotations

from typing import Any, Dict

from core.evidence.evidence_sufficiency_engine import assess_evidence_sufficiency
from core.evidence.semantic_support_engine import build_support


def score_reliability(evidence: list, ambiguities: list, contradiction_count: int = 0) -> Dict[str, Any]:
    support = build_support(evidence)
    sufficiency = assess_evidence_sufficiency(evidence)
    penalty = min(0.5, contradiction_count * 0.15 + len(ambiguities or []) * 0.1)
    score = round(max(0.0, support["support_strength"] * (1.0 if sufficiency["sufficient"] else 0.5) - penalty), 3)
    return {
        "reliability_score": score,
        "support": support,
        "sufficiency": sufficiency,
        "deterministic_inputs": sufficiency.get("deterministic_inputs", []),
    }
