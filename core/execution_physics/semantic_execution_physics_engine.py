from __future__ import annotations

from typing import Any, Dict


MAX_PRESSURE = 100000
STABLE_THRESHOLD = 1000


def compute_execution_physics(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    transitions = list(
        runtime_ir.get(
            "transitions",
            [],
        )
    )

    events = list(
        runtime_ir.get(
            "events",
            [],
        )
    )

    pressure = min(
        len(transitions) + len(events),
        MAX_PRESSURE,
    )

    state = (
        "stable"
        if pressure < STABLE_THRESHOLD
        else "unstable"
    )

    return {
        "execution_pressure": pressure,
        "physics_state": state,
        "bounded": True,
    }
