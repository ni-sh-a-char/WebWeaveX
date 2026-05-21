from __future__ import annotations

from typing import Any, Dict


def compute_recursive_boundary_pressure(boundary_erosion: float, depth: int) -> Dict[str, Any]:
    return {"pressure": round(min(1.0, boundary_erosion + depth * 0.06), 3), "violation": boundary_erosion >= 0.3}
