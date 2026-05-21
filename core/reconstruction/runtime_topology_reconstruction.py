from __future__ import annotations

from typing import Any, Dict, List, Optional


def reconstruct_runtime_topology(
    runtime_graph: Optional[Dict[str, Any]] = None,
    workers: Optional[List[Dict[str, Any]]] = None,
    connectors: Optional[List[Dict[str, Any]]] = None,
    execution_topology: Optional[Dict[str, Any]] = None,
    sync_topology: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    graph = runtime_graph or {}
    nodes = sorted(graph.get("nodes", []), key=lambda item: str(item.get("id", "")))
    edges = sorted(
        graph.get("edges", []),
        key=lambda item: (
            str(item.get("from", "")),
            str(item.get("to", "")),
            str(item.get("relation", "")),
        ),
    )

    worker_list = sorted(
        workers or [],
        key=lambda item: str(item.get("worker_id", "")),
    )
    connector_list = sorted(
        connectors or [],
        key=lambda item: str(item.get("id", "")),
    )

    return {
        "distributed_workers": worker_list,
        "runtime_graph": {"nodes": nodes, "edges": edges},
        "connector_topology": connector_list,
        "execution_topology": dict(execution_topology or {}),
        "synchronization_topology": dict(sync_topology or {}),
        "reconstructed": True,
        "bounded": True,
    }
