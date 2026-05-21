from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.evidence.evidence_sufficiency_engine import assess_evidence_sufficiency
from core.evidence.semantic_support_engine import build_support
from core.evidence.semantic_weakness_engine import build_weaknesses


def score_epistemic_confidence(
    evidence: Optional[List[str]] = None,
    supporting: Optional[List[str]] = None,
    contradicting: Optional[List[str]] = None,
    uncertainty_factors: Optional[List[str]] = None,
    parser_density: int = 0,
) -> Dict[str, Any]:
    ev = sorted(set(str(e) for e in (evidence or []) if e))
    supporting_evidence = sorted(set(str(e) for e in (supporting or ev) if e))
    contradicting_evidence = sorted(set(str(e) for e in (contradicting or []) if e))
    factors = sorted(set(str(f) for f in (uncertainty_factors or []) if f))
    sufficiency = assess_evidence_sufficiency(ev)
    support = build_support(ev)
    weaknesses = build_weaknesses(ev, factors)
    base = support["support_strength"]
    if not sufficiency["sufficient"]:
        base = round(base * 0.4, 3)
    base = round(max(0.0, base - len(contradicting_evidence) * 0.1), 3)
    base = round(min(1.0, base + min(0.15, parser_density * 0.02)), 3)
    return {
        "score": base,
        "basis": {
            "support_strength": support["support_strength"],
            "sufficiency": sufficiency["status"],
            "contradiction_pressure": len(contradicting_evidence),
            "parser_density": parser_density,
            **weaknesses,
        },
        "supporting_evidence": supporting_evidence,
        "contradicting_evidence": contradicting_evidence,
        "uncertainty_factors": factors,
        "deterministic_inputs": sorted(
            sufficiency.get("deterministic_inputs", [])
            + [f"support={support['support_count']}", f"contradict={len(contradicting_evidence)}"]
        ),
    }
