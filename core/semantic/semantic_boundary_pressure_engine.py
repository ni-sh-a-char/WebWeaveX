from __future__ import annotations

from typing import Any, Dict


def compute_semantic_boundary_pressure(boundary_pressure: float, drift_pressure: float) -> Dict[str, Any]:
    pressure = round(min(1.0, boundary_pressure + drift_pressure * 0.5), 3)
    return {"pressure": pressure, "suppress_continuation": pressure >= 0.25}
