from __future__ import annotations

from typing import Any, Dict


def detect_recursive_coherence_inflation(depth: int, closure_pressure: float) -> Dict[str, Any]:
    inflated = depth >= 2 and closure_pressure >= 0.2
    return {"inflated": inflated, "suppress": inflated, "pressure": closure_pressure}
