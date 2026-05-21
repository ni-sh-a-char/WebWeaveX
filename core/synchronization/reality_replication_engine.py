from __future__ import annotations

from typing import Any, Dict, List


def replicate_runtime_reality(
    source: Dict[str, Any],
    workers: List[Dict[str, Any]],
) -> Dict[str, Any]:
    replicas: List[Dict[str, Any]] = []

    for index, worker in enumerate(workers[:1000]):
        replicas.append({
            "worker_id": str(worker.get("worker_id", worker.get("id", f"worker:{index}"))),
            "reality_id": str(source.get("reality_id", "primary")),
            "semantic_state": dict(source.get("semantic_state", {})),
            "runtime_state": dict(source.get("runtime_state", {})),
            "workflows": dict(source.get("workflows", {})),
            "checkpoints": list(source.get("checkpoints", [])),
            "causality_graph": dict(source.get("causality_graph", {})),
            "replicated": True,
        })

    return {
        "replicas": replicas,
        "replica_count": len(replicas),
        "bounded": True,
    }
