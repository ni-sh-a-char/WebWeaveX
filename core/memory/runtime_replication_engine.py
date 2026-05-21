from __future__ import annotations

from typing import Any, Dict, List


def replicate_runtime_memory(
    source: Dict[str, Any],
    nodes: List[Dict[str, Any]],
) -> Dict[str, Any]:
    replicas: List[Dict[str, Any]] = []

    for index, node in enumerate(nodes[:1000]):
        replicas.append({
            "node_id": str(node.get("node_id", f"node:{index}")),
            "memory_id": str(source.get("memory_id", "")),
            "runtime_history": list(source.get("runtime_history", [])),
            "lineage": list(source.get("lineage", [])),
            "replicated": True,
        })

    return {
        "replicas": replicas,
        "replica_count": len(replicas),
        "bounded": True,
    }
