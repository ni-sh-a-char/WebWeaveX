from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.uncertainty_engine import model_uncertainty


def propagate_uncertainty_math(
    evidence_count: int,
    ambiguity_count: int,
    contradiction_count: int,
    parent_uncertainty: float = 0.0,
) -> Dict[str, Any]:
    """Bayesian-style deterministic propagation: U = 1 - (1-U_parent)(1-U_local)."""
    local = model_uncertainty(evidence_count, ambiguity_count, contradiction_count)
    u_local = local["uncertainty_score"]
    u_combined = round(1.0 - (1.0 - parent_uncertainty) * (1.0 - u_local), 3)
    confidence = round(max(0.0, 1.0 - u_combined), 3)
    return {
        **local,
        "uncertainty_score": u_combined,
        "confidence_score": confidence,
        "parent_uncertainty": parent_uncertainty,
        "propagation": "multiplicative_complement",
        "deterministic_inputs": local["deterministic_inputs"]
        + [f"parent={parent_uncertainty}", f"combined={u_combined}"],
    }
