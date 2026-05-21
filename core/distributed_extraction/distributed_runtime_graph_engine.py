from __future__ import annotations

from typing import Any, Dict, List


def build_distributed_runtime_graph(
    workers: List[Dict[str, Any]],
    topology: Dict[str, Any],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    for worker in workers:
        worker_id = str(worker.get("worker_id", ""))
        nodes.append({
            "id": worker_id,
            "type": "worker",
            "status": worker.get("status", "idle"),
        })

    topology_nodes = topology.get("nodes", [])
    for node in topology_nodes:
        nodes.append({
            "id": str(node.get("id", "")),
            "type": node.get("type", "runtime"),
        })

    for index in range(len(workers) - 1):
        edges.append({
            "from": str(workers[index].get("worker_id", "")),
            "to": str(workers[index + 1].get("worker_id", "")),
            "relation": "worker_next",
        })

    return {
        "ir": "distributed_runtime_graph",
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "edges": edges,
        "bounded": True,
    }
