from __future__ import annotations

from typing import Any, Dict


def compile_application_runtime_ir(
    cognition: Dict[str, Any],
    recovery: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "application_runtime",
        "application_states": [cognition.get("application_state", {})],
        "workflows": cognition.get("workflow", {}),
        "forms": cognition.get("forms", {}),
        "action_graphs": cognition.get("action_graph", {}),
        "dashboard_runtime": cognition.get("dashboard", {}),
        "navigation_semantics": cognition.get("navigation", {}),
        "objectives": cognition.get("memory", {}).get("objectives", []),
        "recovery_state": recovery,
        "execution": cognition.get("execution", {}),
        "bounded": True,
    }


def application_runtime_ir_to_graph(
    application_ir: Dict[str, Any],
) -> Dict[str, Any]:
    workflow = application_ir.get("workflows", {})
    nodes = list(workflow.get("nodes", []))
    edges = list(workflow.get("edges", []))

    if not nodes:
        nodes = [{"id": "application:root", "type": "application"}]

    return {
        "ir": "application_runtime_graph",
        "nodes": nodes,
        "edges": edges,
        "bounded": True,
    }
