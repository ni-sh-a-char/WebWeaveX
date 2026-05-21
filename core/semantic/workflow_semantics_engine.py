from __future__ import annotations

from typing import Any, Dict, List, Optional


def extract_workflow_semantics(
    workflow: Optional[Dict[str, Any]] = None,
    objective: str = "",
) -> Dict[str, Any]:
    workflow = workflow or {}
    nodes = list(workflow.get("nodes", []))
    edges = list(workflow.get("edges", []))

    return {
        "objective": objective,
        "workflow_steps": len(nodes),
        "transitions": len(edges),
        "semantic_intent": objective or "operational_flow",
        "bounded": True,
    }
