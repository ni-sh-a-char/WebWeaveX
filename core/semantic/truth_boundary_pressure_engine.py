from __future__ import annotations

from typing import Any, Dict


def compute_truth_boundary_pressure(truth_bounded: bool, entropy: float) -> Dict[str, Any]:
    pressure = round((0.0 if truth_bounded else 0.5) + entropy * 0.3, 3)
    return {"pressure": min(1.0, pressure), "violation": not truth_bounded}
