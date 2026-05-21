from __future__ import annotations

from typing import Any, Dict, List


MAX_SIMULATION_STEPS = 100


def simulate_runtime_execution(
    transitions: List[Dict[str, Any]],
) -> Dict[str, Any]:

    visited = []

    current = None

    for t in transitions[:MAX_SIMULATION_STEPS]:

        current = t["to"]

        visited.append(current)

    return {
        "visited_states": visited,
        "final_state": current,
        "steps": len(visited),
        "bounded": True,
    }
