from __future__ import annotations

from typing import Any, Dict, List


def build_application_session_graph(
    states: List[Dict[str, Any]],
) -> Dict[str, Any]:
    nodes = []
    edges = []

    for index, state in enumerate(states):
        route = str(state.get("route", f"route_{index}"))
        nodes.append({"id": route, "type": "session_state"})
        if index > 0:
            edges.append({
                "from": str(states[index - 1].get("route", "")),
                "to": route,
                "relation": "session_progress",
            })

    return {"nodes": nodes, "edges": edges, "bounded": True}
