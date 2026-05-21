from __future__ import annotations

from typing import Any, Dict, List


MAX_REPLAY = 10000


def analyze_execution_replay(
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    ordered = sorted(
        events,
        key=lambda x: (
            x.get("timestamp", 0),
            str(x.get("id")),
        ),
    )[:MAX_REPLAY]
    return {
        "replay_sequence": ordered,
        "replay_count": len(ordered),
        "bounded": True,
    }
