from __future__ import annotations

from typing import Any, Dict


def replay_application_runtime(
    memory: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "application_state": memory.get("application_state", {}),
        "workflows": memory.get("workflows", {}),
        "routes": memory.get("navigation_flows", {}),
        "forms": memory.get("forms", {}),
        "action_graphs": memory.get("action_graphs", {}),
        "objectives": memory.get("objectives", []),
        "replayed": True,
        "bounded": True,
    }
