from __future__ import annotations

from typing import Any, Dict, List


MAX_PROPAGATION_DEPTH = 50


def propagate_runtime_state(
    transitions: List[Dict[str, Any]],
) -> Dict[str, Any]:

    states = set()

    for t in transitions[:MAX_PROPAGATION_DEPTH]:

        states.add(t["from"])
        states.add(t["to"])

    return {
        "reachable_states": sorted(states),
        "state_count": len(states),
        "bounded": True,
    }
