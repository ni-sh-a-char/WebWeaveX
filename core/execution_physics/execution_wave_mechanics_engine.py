from __future__ import annotations

from typing import Any, Dict, List


MAX_WAVES = 10000


def analyze_execution_waves(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    events = list(
        runtime_ir.get(
            "events",
            [],
        )
    )

    waves: List[Dict[str, Any]] = []

    for idx, event in enumerate(
        events[:MAX_WAVES]
    ):

        waves.append(
            {
                "wave_id": idx,
                "event": str(
                    event.get(
                        "id",
                        "unknown",
                    )
                ),
            }
        )

    return {
        "execution_waves": waves,
        "bounded": True,
    }
