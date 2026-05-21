from __future__ import annotations

from typing import Any, Dict, List


MAX_INCIDENT_EVENTS = 10000


def reconstruct_semantic_incident(
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        events,
        key=lambda x: (
            x.get("timestamp", 0),
            str(x.get("id")),
        ),
    )[:MAX_INCIDENT_EVENTS]

    return {
        "incident_path": ordered,
        "bounded": True,
    }
