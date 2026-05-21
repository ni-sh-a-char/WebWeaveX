from __future__ import annotations

from typing import Any, Dict, List

MAX_QUEUE_SIZE = 10000


def enqueue_extraction(
    queue: List[Dict[str, Any]],
    task: Dict[str, Any],
) -> Dict[str, Any]:
    bounded = list(queue)[:MAX_QUEUE_SIZE]
    task_id = str(task.get("task_id", f"task_{len(bounded)}"))

    entry = {
        "task_id": task_id,
        "url": str(task.get("url", "")),
        "priority": int(task.get("priority", 0)),
        "order": len(bounded),
        "bounded": True,
    }

    bounded.append(entry)
    bounded = sorted(
        bounded,
        key=lambda item: (
            -int(item.get("priority", 0)),
            int(item.get("order", 0)),
            str(item.get("task_id", "")),
        ),
    )

    return {
        "queue": bounded[:MAX_QUEUE_SIZE],
        "enqueued": task_id,
        "bounded": True,
    }


def dequeue_extraction(
    queue: List[Dict[str, Any]],
) -> Dict[str, Any]:
    bounded = sorted(
        list(queue),
        key=lambda item: (
            -int(item.get("priority", 0)),
            int(item.get("order", 0)),
            str(item.get("task_id", "")),
        ),
    )

    if not bounded:
        return {
            "task": None,
            "queue": [],
            "bounded": True,
        }

    task = bounded[0]
    remaining = bounded[1:]

    return {
        "task": task,
        "queue": remaining,
        "bounded": True,
    }
