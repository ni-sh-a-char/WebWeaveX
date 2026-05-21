from __future__ import annotations

from typing import Any, Dict, List


def execute_workflow_plan(
    plan: Dict[str, Any],
    tick: int = 0,
) -> Dict[str, Any]:
    executed: List[Dict[str, Any]] = []

    for index, step in enumerate(plan.get("steps", [])[:10000]):
        executed.append({
            "step_id": str(step.get("id", f"step:{index}")),
            "action": str(step.get("action", "")),
            "runtime": str(step.get("runtime", "browser")),
            "completed": True,
            "tick": tick + index,
            "replay_index": index,
        })

    return {
        "objective": plan.get("objective", ""),
        "executed": executed,
        "completed_count": len(executed),
        "bounded": True,
    }
