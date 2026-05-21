from __future__ import annotations

from typing import Any, Dict


def compile_evolution_runtime_ir(
    evolution: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "evolution_runtime",
        "evolution": evolution.get("evolution", {}),
        "selector": evolution.get("selector", {}),
        "workflow": evolution.get("workflow", {}),
        "semantic": evolution.get("semantic", {}),
        "topology": evolution.get("topology", {}),
        "strategy": evolution.get("strategy", {}),
        "repairs": evolution.get("repairs", {}),
        "optimization": evolution.get("optimization", {}),
        "patterns": evolution.get("patterns", {}),
        "lineage": evolution.get("lineage", []),
        "graph": evolution.get("graph", {}),
        "policy": evolution.get("policy", {}),
        "bounded": True,
    }


def evolution_runtime_ir_to_graph(
    evolution_ir: Dict[str, Any],
) -> Dict[str, Any]:
    graph = evolution_ir.get("graph", {})
    nodes = list(graph.get("nodes", []))
    edges = list(graph.get("edges", []))

    if not nodes:
        nodes = [{"id": "evolution:root", "type": "evolution"}]

    return {
        "ir": "evolution_runtime_graph",
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "edges": edges,
        "bounded": True,
    }
