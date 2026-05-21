from __future__ import annotations

from typing import Any, Dict


def compile_distributed_extraction_ir(
    workers: Dict[str, Any],
    queue: Dict[str, Any],
    topology: Dict[str, Any],
    identities: Dict[str, Any],
    streams: Dict[str, Any],
    adaptive: Dict[str, Any],
    checkpoint: Dict[str, Any],
    recovery: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "distributed_extraction",
        "workers": workers.get("workers", workers),
        "queues": queue.get("queue", queue),
        "runtime_topology": topology.get("topology", topology),
        "identities": identities,
        "streams": streams,
        "adaptive_runtimes": adaptive,
        "checkpoints": checkpoint,
        "recovery_state": recovery,
        "bounded": True,
    }


def distributed_extraction_ir_to_graph(
    distributed_ir: Dict[str, Any],
) -> Dict[str, Any]:
    workers = distributed_ir.get("workers", [])
    nodes = []
    edges = []

    for worker in workers:
        if isinstance(worker, dict):
            node_id = str(worker.get("worker_id", ""))
            nodes.append({
                "id": node_id,
                "type": "worker",
                "name": node_id,
            })

    for index in range(len(nodes) - 1):
        edges.append({
            "from": nodes[index]["id"],
            "to": nodes[index + 1]["id"],
            "relation": "cluster_next",
        })

    return {
        "ir": "distributed_extraction_graph",
        "nodes": nodes,
        "edges": edges,
        "bounded": True,
    }
