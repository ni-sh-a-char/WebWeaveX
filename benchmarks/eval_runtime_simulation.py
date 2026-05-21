from __future__ import annotations

from typing import Any, Dict

from core.runtime.runtime_simulation_engine import (
    simulate_runtime_execution,
)


def eval_runtime_simulation(
    case: Dict[str, Any],
) -> Dict[str, Any]:

    r = simulate_runtime_execution(
        case["transitions"]
    )

    return {
        "predicted": (
            r["final_state"]
            == case["expected_final"]
        ),
        "expected_match": True,
    }
