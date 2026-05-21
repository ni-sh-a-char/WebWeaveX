from __future__ import annotations

from typing import Any, Dict, List


def route_semantic_capability(
    capability: str,
    agents: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        agents,
        key=lambda x: str(x.get("id")),
    )

    for agent in ordered:
        if capability in agent.get("capabilities", []):
            return {
                "selected": agent.get("id"),
                "capability": capability,
            }

    return {
        "selected": None,
        "capability": capability,
    }
