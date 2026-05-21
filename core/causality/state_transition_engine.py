from __future__ import annotations

from typing import Any, Dict, List


def build_state_transitions(
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    transitions: List[Dict[str, Any]] = []

    for index in range(1, len(events)):
        prev = events[index - 1]
        curr = events[index]
        transitions.append({
            "from_state": str(prev.get("state", prev.get("type", ""))),
            "to_state": str(curr.get("state", curr.get("type", ""))),
            "runtime": str(curr.get("runtime", "")),
            "step": index,
        })

    return {
        "transitions": transitions,
        "count": len(transitions),
        "bounded": True,
    }
