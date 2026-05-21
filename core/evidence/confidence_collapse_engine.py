from __future__ import annotations

from typing import Any, Dict

from core.evidence.reality_bounded_confidence_engine import apply_reality_bounded_confidence


def apply_confidence_collapse(
    score: float,
    fragility: Dict[str, Any],
    *,
    reinforcement_count: int = 0,
    stabilization_count: int = 0,
    decay_pressure: float = 0.0,
    truth_boundary_pressure: float = 0.0,
    contradiction_count: int = 0,
    ambiguity_count: int = 0,
    uncertainty_count: int = 0,
    incompleteness: bool = False,
) -> Dict[str, Any]:
    base = apply_reality_bounded_confidence(
        score,
        fragility,
        drift_pressure=decay_pressure,
        continuity_count=stabilization_count,
        boundary_pressure=truth_boundary_pressure,
        contradiction_count=contradiction_count,
        ambiguity_count=ambiguity_count,
        uncertainty_count=uncertainty_count,
    )
    reinf_pen = round(min(0.3, reinforcement_count * 0.12), 3)
    stab_pen = round(min(0.25, stabilization_count * 0.1), 3)
    incom_pen = 0.08 if incompleteness else 0.0
    collapse = round(reinf_pen + stab_pen + incom_pen, 3)
    final = round(max(0.0, base["score"] - collapse), 3)
    return {
        **base,
        "score": final,
        "collapse_pressure": {"reinforcement": reinf_pen, "stabilization": stab_pen, "incompleteness": incom_pen, "total": collapse},
        "truth_penalties": {"boundary": truth_boundary_pressure, "decay": decay_pressure},
        "instability_penalties": {"amount": stab_pen},
        "reinforcement_penalties": {"amount": reinf_pen, "count": reinforcement_count},
        "deterministic_inputs": base.get("deterministic_inputs", [])
        + [f"reinf={reinforcement_count}", f"stab={stabilization_count}", f"incomplete={incompleteness}"],
    }
