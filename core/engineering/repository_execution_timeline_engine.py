from __future__ import annotations

from typing import Any, Dict, List


MAX_TIMELINE = 10000


def build_execution_timeline(
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        events,
        key=lambda x: (
            x.get("timestamp", 0),
            str(x.get("id")),
        ),
    )[:MAX_TIMELINE]

    return {
        "timeline": ordered,
        "timeline_size": len(
            ordered
        ),
        "bounded": True,
    }
