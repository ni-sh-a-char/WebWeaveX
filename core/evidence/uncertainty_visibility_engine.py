from __future__ import annotations

from typing import Any, Dict, List


def expose_uncertainty_visibility(
    uncertainties: List[str],
    ambiguities: List[str],
    confidence_score: float,
) -> Dict[str, Any]:
    pressure = round(min(1.0, len(uncertainties) * 0.15 + len(ambiguities) * 0.1), 3)
    return {
        "visible": bool(uncertainties or ambiguities),
        "count": len(uncertainties),
        "items": sorted(set(str(u) for u in uncertainties)),
        "pressure": pressure,
        "suppress_propagation": pressure >= 0.3,
        "confidence_impact": round(min(0.35, pressure * 0.4), 3),
        "preserved": True,
    }
