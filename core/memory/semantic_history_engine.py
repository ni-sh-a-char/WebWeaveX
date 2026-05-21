from __future__ import annotations

from typing import Any, Dict, List


def record_history(events: List[Dict[str, Any]], max_events: int = 500) -> Dict[str, Any]:
    bounded = events[-max_events:]
    return {"events": bounded, "count": len(bounded), "truncated": len(events) > max_events}
