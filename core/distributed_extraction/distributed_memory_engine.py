from __future__ import annotations

from typing import Any, Dict, List


def merge_distributed_memory(
    memories: List[Dict[str, Any]],
) -> Dict[str, Any]:
    merged: Dict[str, Any] = {
        "workers": [],
        "adaptive": {},
        "streams": [],
        "bounded": True,
    }

    for memory in memories:
        merged["workers"].append(memory.get("worker_id", ""))
        merged["adaptive"].update(memory.get("adaptive", {}))
        merged["streams"].extend(memory.get("streams", []))

    return merged
