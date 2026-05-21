from __future__ import annotations

from typing import Any, Dict, List

from core.streaming.stream_capture_engine import (
    make_stream_event,
    normalize_stream_events,
)

MAX_SSE_EVENTS = 5000


def capture_server_sent_events(page: Any) -> Dict[str, Any]:
    events: List[Dict[str, Any]] = []

    if page is not None and hasattr(page, "_test_sse_events"):
        for index, item in enumerate(page._test_sse_events[:MAX_SSE_EVENTS]):
            events.append(
                make_stream_event(
                    step=index,
                    source="sse",
                    direction="incoming",
                    payload=str(item.get("payload", "")),
                    connection_id=str(item.get("event_type", "message")),
                )
            )

    return {
        "events": normalize_stream_events(events),
        "bounded": True,
    }
