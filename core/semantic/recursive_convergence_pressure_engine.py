from __future__ import annotations

from typing import Any, Dict


def compute_recursive_convergence_pressure(depth: int, diversity_score: float) -> Dict[str, Any]:
    pressure = round(min(1.0, depth * 0.08 + max(0, 0.5 - diversity_score)), 3)
    return {"pressure": pressure, "suppress": pressure >= 0.3}
