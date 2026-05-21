from __future__ import annotations

from typing import Any, Dict, List


MAX_REPLAY_EVENTS = 1000


def replay_semantic_events(
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:

    replay_log = []

    for ev in events[:MAX_REPLAY_EVENTS]:

        replay_log.append({
            "event": ev.get("id"),
            "type": ev.get("type"),
        })

    return {
        "replay_log": replay_log,
        "event_count": len(replay_log),
        "bounded": True,
    }
