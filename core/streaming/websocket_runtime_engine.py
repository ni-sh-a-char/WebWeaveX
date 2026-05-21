from __future__ import annotations

from typing import Any, Dict, List

from core.streaming.stream_capture_engine import (
    make_stream_event,
    normalize_stream_events,
)

MAX_FRAMES = 10000
MAX_CONNECTIONS = 1000


def track_websocket_connections(page: Any) -> Dict[str, Any]:
    connections: List[Dict[str, Any]] = []

    if page is not None and hasattr(page, "_test_websocket_connections"):
        connections = list(page._test_websocket_connections)[:MAX_CONNECTIONS]
    elif page is not None and hasattr(page, "_test_websocket_frames"):
        seen = {}
        for frame in page._test_websocket_frames[:MAX_CONNECTIONS]:
            connection_id = str(frame.get("connection_id", ""))
            if connection_id not in seen:
                seen[connection_id] = {
                    "connection_id": connection_id,
                    "url": str(frame.get("url", ""))[:2000],
                    "lifecycle": "open",
                }
        connections = sorted(
            seen.values(),
            key=lambda item: str(item.get("connection_id", "")),
        )

    return {
        "connections": connections,
        "bounded": True,
    }


def capture_websocket_frames(page: Any) -> Dict[str, Any]:
    events: List[Dict[str, Any]] = []

    if page is not None and hasattr(page, "_test_websocket_frames"):
        for index, frame in enumerate(
            page._test_websocket_frames[:MAX_FRAMES]
        ):
            events.append(
                make_stream_event(
                    step=index,
                    source="websocket",
                    direction=str(frame.get("direction", "incoming")),
                    payload=str(frame.get("payload", "")),
                    connection_id=str(frame.get("connection_id", "")),
                )
            )

    return {
        "events": normalize_stream_events(events),
        "bounded": True,
    }
