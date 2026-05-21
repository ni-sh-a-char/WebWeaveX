from __future__ import annotations

from typing import Any, Dict, List

from core.runtime.distributed_topology_engine import build_distributed_topology

from .schema_types import SemanticNode, SemanticEdge


def compile_typed_topology_ir(services: List[str]) -> Dict[str, Any]:
    topo = build_distributed_topology(sorted(services))
    nodes: List[SemanticNode] = []
    edges: List[SemanticEdge] = []
    for n in topo.get("nodes", []):
        nodes.append(SemanticNode(id=str(n.get("id", "")), type=str(n.get("type", "service"))))
    for e in topo.get("edges", []):
        edges.append(
            SemanticEdge(
                source=str(e.get("from", "")),
                target=str(e.get("to", "")),
                relation=str(e.get("relation", "distributed_dependency")),
                evidence=["distributed_topology"],
            )
        )
    return {
        "nodes": nodes,
        "edges": edges,
        "topology": topo,
        "typed": True,
        "deterministic": True,
    }
