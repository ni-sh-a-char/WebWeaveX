from __future__ import annotations

from typing import Any, Dict


def compute_recursive_dependency_pressure(depth: int, interpretation_count: int) -> Dict[str, Any]:
    pressure = round(min(1.0, max(0, depth - 1) * 0.15 + (0.2 if interpretation_count <= 1 else 0)), 3)
    return {"pressure": pressure, "violation": pressure >= 0.3}
