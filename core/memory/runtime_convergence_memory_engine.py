from __future__ import annotations

from typing import Any, Dict, List


def converge_runtime_memory(
    replicas: List[Dict[str, Any]],
) -> Dict[str, Any]:
    if not replicas:
        return {"converged": True, "memory_id": "", "bounded": True}

    base = replicas[0]
    for replica in replicas[1:]:
        if replica.get("memory_id") != base.get("memory_id"):
            return {
                "converged": False,
                "conflict": True,
                "bounded": True,
            }

    return {
        "converged": True,
        "memory_id": base.get("memory_id", ""),
        "replica_count": len(replicas),
        "bounded": True,
    }
