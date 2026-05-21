from __future__ import annotations

from typing import Any, Dict, List


def expose_ambiguity_visibility(ambiguities: List[str], confidence_score: float) -> Dict[str, Any]:
    pressure = round(min(1.0, len(ambiguities) * 0.12), 3)
    return {
        "visible": bool(ambiguities),
        "count": len(ambiguities),
        "items": sorted(set(str(a) for a in ambiguities)),
        "pressure": pressure,
        "suppress_expansion": pressure >= 0.25,
        "confidence_impact": round(min(0.3, pressure * 0.35), 3),
        "preserved": True,
    }
