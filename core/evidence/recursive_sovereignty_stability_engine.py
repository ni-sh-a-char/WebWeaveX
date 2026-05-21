from __future__ import annotations

from typing import Any, Dict


def model_sovereignty_stability(sovereign: bool, depth: int) -> Dict[str, Any]:
    return {
        "stable": sovereign,
        "long_horizon": True,
        "dependence_loops_blocked": depth >= 2,
        "obedience_loops_blocked": True,
    }
