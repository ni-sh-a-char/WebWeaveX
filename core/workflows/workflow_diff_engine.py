from __future__ import annotations

from typing import Any, Dict


def diff_workflow_runtime(
    previous: Dict[str, Any],
    current: Dict[str, Any],
) -> Dict[str, Any]:
    prev_steps = {
        str(item.get("step_id", ""))
        for item in previous.get("executed", [])
    }
    curr_steps = {
        str(item.get("step_id", ""))
        for item in current.get("executed", [])
    }

    return {
        "steps_added": sorted(curr_steps - prev_steps),
        "steps_removed": sorted(prev_steps - curr_steps),
        "objective_changed": previous.get("objective") != current.get("objective"),
        "bounded": True,
    }
