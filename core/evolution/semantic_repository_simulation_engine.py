from __future__ import annotations

from typing import Any, Dict


MAX_SIMULATION_STEPS = 1000


def simulate_repository_runtime(
    repository_ir: Dict[str, Any],
) -> Dict[str, Any]:

    edges = list(
        repository_ir.get(
            "edges",
            [],
        )
    )

    simulated = edges[
        :MAX_SIMULATION_STEPS
    ]

    return {
        "simulation": simulated,
        "simulation_steps": len(
            simulated
        ),
        "bounded": True,
    }
