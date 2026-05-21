from __future__ import annotations

from typing import Any, Dict, List

MAX_REPLAY_EVENTS = 10000


def replay_stream_events(
    page: Any,
    stream_log: List[Dict[str, Any]],
) -> Dict[str, Any]:
    replayed: List[Dict[str, Any]] = []

    for index, event in enumerate(stream_log[:MAX_REPLAY_EVENTS]):
        if page is not None and hasattr(page, "_test_replay_log"):
            page._test_replay_log.append(dict(event))

        replayed.append({
            "step": index,
            "event": dict(event),
            "replayed": True,
        })

    return {
        "replay": replayed,
        "bounded": True,
    }


def build_stream_timeline(
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    ordered = sorted(
        list(events),
        key=lambda item: (
            int(item.get("timestamp", 0)),
            str(item.get("id", "")),
            str(item.get("source", "")),
        ),
    )

    edges: List[Dict[str, Any]] = []
    previous_id = ""

    for event in ordered:
        event_id = str(event.get("id", ""))
        if previous_id:
            edges.append({
                "from": previous_id,
                "to": event_id,
                "relation": "stream_next",
            })
        previous_id = event_id

    return {
        "events": ordered,
        "edges": edges,
        "bounded": True,
    }
