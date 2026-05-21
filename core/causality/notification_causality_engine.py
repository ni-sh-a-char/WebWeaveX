from __future__ import annotations

from typing import Any, Dict, List


def track_notification_causality(
    notifications: List[Dict[str, Any]],
    origin_events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    tracked: List[Dict[str, Any]] = []

    origin_id = str(origin_events[-1].get("id", "")) if origin_events else ""

    for index, notification in enumerate(notifications[:5000]):
        if isinstance(notification, dict):
            notification_id = str(notification.get("id", f"notif:{index}"))
            user_interaction = bool(notification.get("interaction"))
        else:
            notification_id = f"notif:{index}"
            user_interaction = False

        tracked.append({
            "notification_id": notification_id,
            "origin_event": origin_id,
            "downstream_workflow": f"workflow:notif:{index}",
            "user_interaction": user_interaction,
            "payload": str(notification),
        })

    return {
        "notifications": tracked,
        "origin_event": origin_id,
        "count": len(tracked),
        "bounded": True,
    }
