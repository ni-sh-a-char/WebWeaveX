from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_workflow_state(
    plan: Dict[str, Any],
    execution: Optional[Dict[str, Any]] = None,
    current_step: int = 0,
) -> Dict[str, Any]:
    execution = execution or {}
    executed = list(execution.get("executed", []))
    steps = list(plan.get("steps", []))

    return {
        "current_step": current_step,
        "completed_steps": [
            item["step_id"] for item in executed if item.get("completed")
        ],
        "retries": 0,
        "runtime_state": {
            "objective": plan.get("objective", ""),
            "total_steps": len(steps),
        },
        "extraction_outputs": [],
        "semantic_checkpoints": [],
        "bounded": True,
    }
