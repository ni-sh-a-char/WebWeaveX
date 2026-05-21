from __future__ import annotations

from typing import Any, Dict, List


MAX_SIMULATION = 1000


def simulate_engineering_change(
    changes: List[Dict[str, Any]],
) -> Dict[str, Any]:
    ordered = sorted(
        changes,
        key=lambda x: str(x.get("id")),
    )[:MAX_SIMULATION]
    return {
        "simulated_changes": ordered,
        "simulation_count": len(ordered),
        "bounded": True,
    }
