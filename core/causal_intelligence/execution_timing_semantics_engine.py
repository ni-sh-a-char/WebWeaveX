from __future__ import annotations

from typing import Any, Dict, List


MAX_TIMING = 10000


def analyze_execution_timing(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    event_stream = runtime_ir.get(
        "event_stream",
        {},
    )

    events = sorted(
        list(
            event_stream.get(
                "events",
                [],
            )
            if isinstance(event_stream, dict)
            else []
        ),
        key=lambda x: (
            x.get(
                "timestamp",
                0,
            ),
            str(
                x.get("id")
            ),
        ),
    )

    return {
        "timing_sequence": [
            str(
                e.get("id")
            )
            for e in events[:MAX_TIMING]
        ],
        "bounded": True,
    }
