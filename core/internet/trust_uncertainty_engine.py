from __future__ import annotations

from typing import Any, Dict

from core.evidence.uncertainty_propagation_math import propagate_uncertainty_math


def model_trust_uncertainty(evidence_count: int, contradiction_count: int, corroboration: int) -> Dict[str, Any]:
    amb = max(0, 2 - corroboration)
    u = propagate_uncertainty_math(evidence_count, amb, contradiction_count)
    return {
        **u,
        "trust_uncertainty": u["uncertainty_score"],
        "contradiction_pressure": min(1.0, contradiction_count * 0.25),
    }
