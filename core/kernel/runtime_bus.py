from __future__ import annotations

from typing import Any, Dict, List


MAX_BUS_EVENTS = 100_000


def publish_runtime_event(
    bus: List[Dict[str, Any]],
    event_type: str,
    payload: Dict[str, Any],
    tick: int = 0,
) -> Dict[str, Any]:
    events = list(bus)
    events.append({
        "type": event_type,
        "tick": tick,
        "payload": dict(payload),
        "order": len(events),
    })
    events = sorted(events, key=lambda item: (item["tick"], item["order"]))[:MAX_BUS_EVENTS]
    return {"bus": events, "size": len(events), "bounded": True}
