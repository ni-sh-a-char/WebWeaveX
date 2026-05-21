from __future__ import annotations

from typing import Any, Dict


def compile_synchronization_runtime_ir(
    sync: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "synchronization_runtime",
        "snapshot": sync.get("snapshot", {}),
        "delta": sync.get("delta", {}),
        "history": sync.get("history", {}),
        "timeline": sync.get("timeline", {}),
        "convergence": sync.get("convergence", {}),
        "synchronization": sync.get("synchronization", {}),
        "replication": sync.get("replication", {}),
        "continuity": sync.get("continuity", {}),
        "state_graph": sync.get("state_graph", {}),
        "consistency": sync.get("consistency", {}),
        "bounded": True,
    }


def synchronization_runtime_ir_to_graph(
    sync_ir: Dict[str, Any],
) -> Dict[str, Any]:
    graph = sync_ir.get("state_graph", {})
    nodes = list(graph.get("nodes", []))
    edges = list(graph.get("edges", []))

    if not nodes:
        nodes = [{"id": "sync:root", "type": "synchronization"}]

    return {
        "ir": "synchronization_runtime_graph",
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "edges": edges,
        "bounded": True,
    }
