from __future__ import annotations

from typing import Any, Dict


def compile_workflow_runtime_ir(
    workflow: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "workflow_runtime",
        "objective": workflow.get("objective", {}),
        "plan": workflow.get("plan", {}),
        "execution": workflow.get("execution", {}),
        "state": workflow.get("state", {}),
        "workflow_graph": workflow.get("workflow_graph", {}),
        "dependencies": workflow.get("dependencies", {}),
        "federation": workflow.get("federation", {}),
        "semantic_alignment": workflow.get("semantic_alignment", {}),
        "recovery": workflow.get("recovery", {}),
        "bounded": True,
    }


def workflow_runtime_ir_to_graph(
    workflow_ir: Dict[str, Any],
) -> Dict[str, Any]:
    graph = workflow_ir.get("workflow_graph", {})
    nodes = list(graph.get("nodes", []))
    edges = list(graph.get("edges", []))

    if not nodes:
        nodes = [{"id": "workflow:root", "type": "workflow"}]

    return {
        "ir": "workflow_runtime_graph",
        "nodes": sorted(nodes, key=lambda item: str(item.get("id", ""))),
        "edges": edges,
        "bounded": True,
    }
