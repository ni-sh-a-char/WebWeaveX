from __future__ import annotations

from typing import Any, Dict


def compile_runtime_memory_ir(
    memory_payload: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "runtime_memory",
        "memory_graphs": memory_payload.get("graph", {}),
        "semantic_indexes": memory_payload.get("index", {}),
        "lineage": memory_payload.get("lineage", {}),
        "runtime_history": memory_payload.get("runtime", {}),
        "distributed_memory": memory_payload.get("distributed", {}),
        "knowledge": memory_payload.get("knowledge", {}),
        "semantic": memory_payload.get("semantic", {}),
        "bounded": True,
    }


def runtime_memory_ir_to_graph(
    memory_ir: Dict[str, Any],
) -> Dict[str, Any]:
    graph = memory_ir.get("memory_graphs", {})
    nodes = list(graph.get("nodes", []))
    edges = list(graph.get("edges", []))

    if not nodes:
        nodes = [{"id": "memory:root", "type": "memory"}]

    return {
        "ir": "runtime_memory_graph",
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "edges": edges,
        "bounded": True,
    }
