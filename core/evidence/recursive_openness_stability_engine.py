from __future__ import annotations

from typing import Any, Dict


def model_recursive_openness_stability(open: bool, depth: int) -> Dict[str, Any]:
    return {
        "stable": open,
        "long_horizon": True,
        "convergence_collapse_blocked": depth >= 3,
        "novelty_exhaustion_blocked": True,
    }
