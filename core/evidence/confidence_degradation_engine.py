from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.confidence_cap_engine import apply_confidence_caps


def apply_confidence_degradation(
    score: float,
    fragility: Dict[str, Any],
    *,
    contradiction_count: int = 0,
    ambiguity_count: int = 0,
    uncertainty_count: int = 0,
    unsupported_expansion_count: int = 0,
    speculation_count: int = 0,
    parser_weakness: bool = False,
) -> Dict[str, Any]:
    capped = apply_confidence_caps(
        score,
        fragility,
        contradiction_count=contradiction_count,
        ambiguity_count=ambiguity_count,
        unsupported_expansion_count=unsupported_expansion_count,
    )
    spec_penalty = round(min(0.2, speculation_count * 0.1), 3)
    unc_penalty = round(min(0.2, uncertainty_count * 0.06), 3)
    parser_penalty = 0.1 if parser_weakness else 0.0
    degraded = round(max(0.0, capped["score"] - spec_penalty - unc_penalty - parser_penalty), 3)
    degradation = {
        "from_score": score,
        "after_caps": capped["score"],
        "final": degraded,
        "total_reduction": round(max(0.0, score - degraded), 3),
    }
    return {
        **capped,
        "score": degraded,
        "degradation": degradation,
        "uncertainty_penalties": {"amount": unc_penalty, "count": uncertainty_count},
        "speculation_penalties": {"amount": spec_penalty, "count": speculation_count},
        "parser_penalties": {"amount": parser_penalty, "weak": parser_weakness},
        "deterministic_inputs": capped.get("deterministic_inputs", [])
        + [f"spec={speculation_count}", f"unc={uncertainty_count}", f"parser_weak={parser_weakness}"],
    }
