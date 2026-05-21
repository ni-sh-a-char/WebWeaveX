from __future__ import annotations

from typing import Any, Dict


def compute_recursive_instability_pressure(instability_regions: int, depth: int) -> Dict[str, Any]:
    return {"pressure": round(min(1.0, instability_regions * 0.2 + depth * 0.05), 3)}
