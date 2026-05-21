from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.application.runtime_goal_engine import build_runtime_goal


def execute_runtime_objective(
    objective: str,
    workflow_graph: Dict[str, Any],
    action_graph: Dict[str, Any],
    navigation: Dict[str, Any],
    adaptive_runtime: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    goal = build_runtime_goal(objective)
    executed: List[Dict[str, Any]] = []

    for index, step in enumerate(goal["steps"]):
        executed.append({
            "step": index,
            "name": step,
            "workflow_nodes": len(workflow_graph.get("nodes", [])),
            "action_nodes": len(action_graph.get("nodes", [])),
            "route": navigation.get("routes", [{}])[0].get("path", ""),
            "adaptive": bool(adaptive_runtime),
            "completed": True,
        })

    return {
        "objective": objective,
        "goal": goal,
        "executed": executed,
        "bounded": True,
    }
