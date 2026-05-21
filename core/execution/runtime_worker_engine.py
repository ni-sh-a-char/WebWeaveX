from __future__ import annotations

from typing import Any, Dict, List


def build_runtime_workers(
    nodes: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    workers: List[Dict[str, Any]] = []
    for index, node in enumerate(nodes[:1000]):
        workers.append({
            "worker_id": str(node.get("worker_id", node.get("node_id", f"worker:{index}"))),
            "runtime": str(node.get("runtime", "browser")),
            "synced": bool(node.get("synced", True)),
            "bounded": True,
        })
    return sorted(workers, key=lambda item: item["worker_id"])
