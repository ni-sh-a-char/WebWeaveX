from __future__ import annotations

from typing import Any, Dict, List


def build_application_transitions(
    states: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    transitions: List[Dict[str, Any]] = []

    for index in range(len(states) - 1):
        src = states[index]
        dst = states[index + 1]

        transitions.append({
            "from": str(src.get("route", "")),
            "to": str(dst.get("route", "")),
            "relation": "transition",
            "order": index,
        })

    return transitions[:10000]
