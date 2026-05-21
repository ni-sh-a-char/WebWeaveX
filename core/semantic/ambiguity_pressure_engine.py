from __future__ import annotations

from typing import Any, Dict, List


def compute_ambiguity_pressure(ambiguities: List[str]) -> Dict[str, Any]:
    pressure = round(min(1.0, len(ambiguities) * 0.12), 3)
    return {
        "pressure": pressure,
        "suppress_expansion": pressure >= 0.2,
        "confidence_reduction": round(min(0.25, pressure * 0.3), 3),
        "preserved": True,
    }
