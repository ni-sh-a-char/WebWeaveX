from __future__ import annotations

from typing import Any, Dict, List


def build_workflow_transitions(
    execution: Dict[str, Any],
) -> List[Dict[str, Any]]:
    transitions: List[Dict[str, Any]] = []
    executed = list(execution.get("executed", []))

    for index in range(1, len(executed)):
        transitions.append({
            "from": str(executed[index - 1].get("step_id", "")),
            "to": str(executed[index].get("step_id", "")),
            "relation": "transitions",
        })

    return transitions
