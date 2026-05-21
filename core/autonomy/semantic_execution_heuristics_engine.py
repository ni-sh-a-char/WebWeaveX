from __future__ import annotations

from typing import Any, Dict


def compute_execution_heuristics(
    runtime_state: Dict[str, Any],
) -> Dict[str, Any]:

    score = len(runtime_state)

    return {
        "heuristic_score": score,
        "stable": score >= 0,
    }
