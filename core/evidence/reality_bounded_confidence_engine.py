from __future__ import annotations

from typing import Any, Dict

from core.evidence.confidence_degradation_engine import apply_confidence_degradation


def apply_reality_bounded_confidence(
    score: float,
    fragility: Dict[str, Any],
    *,
    drift_pressure: float = 0.0,
    continuity_count: int = 0,
    parser_gap: bool = False,
    boundary_pressure: float = 0.0,
    contradiction_count: int = 0,
    ambiguity_count: int = 0,
    uncertainty_count: int = 0,
) -> Dict[str, Any]:
    base = apply_confidence_degradation(
        score,
        fragility,
        contradiction_count=contradiction_count,
        ambiguity_count=ambiguity_count,
        uncertainty_count=uncertainty_count,
        unsupported_expansion_count=continuity_count,
        speculation_count=continuity_count,
        parser_weakness=parser_gap,
    )
    drift_pen = round(min(0.25, drift_pressure * 0.3), 3)
    boundary_pen = round(min(0.2, boundary_pressure * 0.25), 3)
    reality_pen = round(drift_pen + boundary_pen, 3)
    final = round(max(0.0, base["score"] - reality_pen), 3)
    return {
        **base,
        "score": final,
        "reality_penalties": {"drift": drift_pen, "boundary": boundary_pen, "total": reality_pen},
        "stability_penalties": {"continuity": round(min(0.2, continuity_count * 0.08), 3)},
        "drift_penalties": {"amount": drift_pen, "pressure": drift_pressure},
        "boundary_penalties": {"amount": boundary_pen, "pressure": boundary_pressure},
        "deterministic_inputs": base.get("deterministic_inputs", [])
        + [f"drift={drift_pressure}", f"boundary={boundary_pressure}", f"parser_gap={parser_gap}"],
    }
