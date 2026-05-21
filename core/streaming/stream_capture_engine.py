from __future__ import annotations

from typing import Any, Dict, List

MAX_STREAM_EVENTS = 10000


def make_stream_event(
    step: int,
    source: str,
    direction: str,
    payload: str,
    connection_id: str,
) -> Dict[str, Any]:
    return {
        "id": f"stream_{step}",
        "timestamp": step,
        "source": str(source),
        "direction": str(direction),
        "payload": str(payload)[:10000],
        "connection_id": str(connection_id),
        "bounded": True,
    }


def normalize_stream_events(
    events: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []

    for index, event in enumerate(events[:MAX_STREAM_EVENTS]):
        normalized.append(
            make_stream_event(
                step=int(event.get("timestamp", index)),
                source=str(event.get("source", "unknown")),
                direction=str(event.get("direction", "incoming")),
                payload=str(event.get("payload", "")),
                connection_id=str(event.get("connection_id", "")),
            )
        )

    return sorted(
        normalized,
        key=lambda item: (
            int(item.get("timestamp", 0)),
            str(item.get("id", "")),
        ),
    )
