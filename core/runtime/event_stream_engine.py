from __future__ import annotations

from typing import Any, Dict, List


MAX_EVENT_CHAIN = 1000


def reconstruct_event_stream(
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        events[:MAX_EVENT_CHAIN],
        key=lambda x: x.get("timestamp", 0),
    )

    edges = []

    for i in range(len(ordered) - 1):

        edges.append({
            "from": ordered[i].get("id"),
            "to": ordered[i + 1].get("id"),
            "relation": "event_precedes",
        })

    return {
        "events": ordered,
        "edges": edges,
        "bounded": True,
    }
