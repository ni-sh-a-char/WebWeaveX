from __future__ import annotations

from typing import Any, Dict, List


def compute_uncertainty_pressure(uncertainties: List[str], ambiguities: List[str]) -> Dict[str, Any]:
    count = len(uncertainties) + len(ambiguities)
    pressure = round(min(1.0, count * 0.1), 3)
    return {
        "pressure": pressure,
        "suppress_propagation": pressure >= 0.25,
        "confidence_reduction": round(min(0.3, pressure * 0.35), 3),
        "preserved": True,
    }
