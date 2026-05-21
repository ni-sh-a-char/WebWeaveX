from __future__ import annotations

from typing import Any, Dict

from core.evidence.confidence_collapse_engine import apply_confidence_collapse


def apply_recursive_confidence_decay(
    score: float,
    fragility: Dict[str, Any],
    *,
    depth: int = 0,
    closure_count: int = 0,
    drift_pressure: float = 0.0,
    entropy: float = 0.0,
    contradiction_count: int = 0,
    ambiguity_count: int = 0,
    uncertainty_count: int = 0,
) -> Dict[str, Any]:
    base = apply_confidence_collapse(
        score,
        fragility,
        stabilization_count=closure_count,
        decay_pressure=drift_pressure,
        truth_boundary_pressure=depth * 0.05,
        contradiction_count=contradiction_count,
        ambiguity_count=ambiguity_count,
        uncertainty_count=uncertainty_count,
    )
    depth_pen = round(min(0.35, depth * 0.08), 3)
    entropy_pen = round(min(0.2, entropy * 0.25), 3)
    final = round(max(0.0, base["score"] - depth_pen - entropy_pen), 3)
    return {
        **base,
        "score": final,
        "recursive_decay": {"depth_penalty": depth_pen, "entropy_penalty": entropy_pen, "final": final},
        "recursive_pressure": {"depth": depth, "closure": closure_count},
        "recursive_penalties": {"depth": depth_pen, "entropy": entropy_pen},
        "recursive_entropy": {"level": entropy},
        "recursive_instability": {"pressure": drift_pressure},
        "deterministic_inputs": base.get("deterministic_inputs", []) + [f"depth={depth}", f"entropy={entropy}"],
    }
