from __future__ import annotations

from typing import Any, Dict, List


MAX_CAUSALITY = 10000


def reconstruct_distributed_causality(
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        events,
        key=lambda x: (
            x.get("timestamp", 0),
            str(x.get("id")),
        ),
    )

    edges = []

    for idx in range(
        len(ordered) - 1
    ):

        edges.append(
            {
                "from": ordered[idx].get("id"),
                "to": ordered[idx + 1].get("id"),
                "relation": "event_precedes",
            }
        )

    return {
        "causality_edges": edges[
            :MAX_CAUSALITY
        ],
        "bounded": True,
    }
