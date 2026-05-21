from __future__ import annotations

from typing import Any, Dict, List


_QUEUE: List[Dict[str, Any]] = []


def enqueue_workflow(
    workflow: Dict[str, Any],
) -> Dict[str, Any]:
    entry = {
        "id": str(workflow.get("id", f"wf:{len(_QUEUE)}")),
        "objective": str(workflow.get("objective", "")),
        "priority": int(workflow.get("priority", 0)),
        "workflow": workflow,
    }
    _QUEUE.append(entry)
    _QUEUE.sort(key=lambda item: (item["priority"], item["id"]))
    return {"enqueued": True, "id": entry["id"], "position": _QUEUE.index(entry), "bounded": True}


def dequeue_workflow() -> Dict[str, Any]:
    if not _QUEUE:
        return {"available": False, "workflow": {}, "bounded": True}
    entry = _QUEUE.pop(0)
    return {"available": True, "workflow": entry, "bounded": True}


def peek_workflow_queue() -> List[Dict[str, Any]]:
    return list(_QUEUE)
