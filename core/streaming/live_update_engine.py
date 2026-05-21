from __future__ import annotations

from typing import Any, Dict, List

from core.streaming.stream_capture_engine import make_stream_event

MAX_UPDATES = 5000


def track_live_runtime_updates(page: Any) -> Dict[str, Any]:
    updates: List[Dict[str, Any]] = []
    events: List[Dict[str, Any]] = []

    if page is not None and hasattr(page, "_test_live_updates"):
        updates = list(page._test_live_updates)[:MAX_UPDATES]

    for index, update in enumerate(updates):
        events.append(
            make_stream_event(
                step=index,
                source="live_update",
                direction=str(update.get("kind", "refresh")),
                payload=str(update.get("payload", "")),
                connection_id=str(update.get("target", "")),
            )
        )

    return {
        "updates": updates,
        "events": events,
        "bounded": True,
    }
