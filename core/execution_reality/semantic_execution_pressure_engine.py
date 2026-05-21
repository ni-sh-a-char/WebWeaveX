from __future__ import annotations

from typing import Any, Dict


MAX_PRESSURE = 100000


def compute_execution_pressure(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    transitions = list(
        runtime_ir.get(
            "transitions",
            [],
        )
    )

    event_stream = runtime_ir.get(
        "event_stream",
        {},
    )

    events = list(
        event_stream.get(
            "events",
            [],
        )
        if isinstance(event_stream, dict)
        else []
    )

    pressure_score = min(
        len(transitions)
        + len(events),
        MAX_PRESSURE,
    )

    return {
        "pressure_score": pressure_score,
        "bounded": True,
    }
