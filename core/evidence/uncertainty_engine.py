from __future__ import annotations

from typing import Any, Dict, List


def model_uncertainty(
    evidence_count: int,
    ambiguity_count: int,
    contradiction_count: int,
) -> Dict[str, Any]:
    uncertainty = round(min(1.0, 0.2 + ambiguity_count * 0.15 + contradiction_count * 0.2), 3)
    if evidence_count < 2:
        uncertainty = round(min(1.0, uncertainty + 0.3), 3)
    confidence = round(max(0.0, 1.0 - uncertainty), 3)
    return {
        "uncertainty_score": uncertainty,
        "confidence_score": confidence,
        "evidence_count": evidence_count,
        "ambiguity_count": ambiguity_count,
        "contradiction_count": contradiction_count,
        "deterministic_inputs": [
            f"evidence={evidence_count}",
            f"ambiguity={ambiguity_count}",
            f"contradiction={contradiction_count}",
        ],
    }
