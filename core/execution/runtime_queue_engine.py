from __future__ import annotations

from typing import Any, Dict, List, Optional

MAX_QUEUE = 100_000


def enqueue_runtime_action(
    queue: List[Dict[str, Any]],
    action: Dict[str, Any],
    priority: int = 0,
) -> Dict[str, Any]:
    updated = list(queue)
    entry = {
        "action": action,
        "priority": priority,
        "order": len(updated),
    }
    updated.append(entry)
    updated = sorted(
        updated,
        key=lambda item: (-int(item.get("priority", 0)), int(item.get("order", 0))),
    )[:MAX_QUEUE]
    return {"queue": updated, "size": len(updated), "bounded": True}


def dequeue_runtime_action(
    queue: List[Dict[str, Any]],
) -> Dict[str, Any]:
    if not queue:
        return {"queue": [], "action": None, "bounded": True}

    ordered = sorted(
        queue,
        key=lambda item: (-int(item.get("priority", 0)), int(item.get("order", 0))),
    )
    head = ordered[0]
    rest = ordered[1:]
    return {
        "queue": rest,
        "action": head.get("action"),
        "bounded": True,
    }
