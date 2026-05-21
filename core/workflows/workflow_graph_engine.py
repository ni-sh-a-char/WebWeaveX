from __future__ import annotations

from typing import Any, Dict, List


def build_workflow_graph(
    objective: Dict[str, Any],
    plan: Dict[str, Any],
    state: Dict[str, Any],
    execution: Dict[str, Any],
    transitions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    obj_name = str(objective.get("objective", "objective"))
    nodes.append({"id": f"objective:{obj_name}", "type": "objective"})

    for step in plan.get("steps", [])[:10000]:
        step_id = str(step.get("id", ""))
        nodes.append({
            "id": step_id,
            "type": "step",
            "runtime": str(step.get("runtime", "")),
        })
        depends_on = str(step.get("depends_on", ""))
        if depends_on:
            edges.append({
                "from": depends_on,
                "to": step_id,
                "relation": "depends_on",
            })
        edges.append({
            "from": f"objective:{obj_name}",
            "to": step_id,
            "relation": "executes",
        })

    for transition in transitions[:10000]:
        edges.append({
            "from": str(transition.get("from", "")),
            "to": str(transition.get("to", "")),
            "relation": "transitions",
        })

    if state.get("retries", 0) > 0:
        nodes.append({"id": "checkpoint:recovery", "type": "checkpoint"})
        edges.append({
            "from": "checkpoint:recovery",
            "to": f"objective:{obj_name}",
            "relation": "recovers",
        })

    nodes.append({
        "id": "semantic:state",
        "type": "semantic_state",
    })

    return {
        "nodes": sorted(nodes, key=lambda item: item["id"]),
        "edges": sorted(
            edges,
            key=lambda item: (
                item.get("from", ""),
                item.get("to", ""),
                item.get("relation", ""),
            ),
        ),
        "bounded": True,
    }
