from __future__ import annotations

from typing import Any, Dict, List


def compile_interaction_ir(
    interactions: List[Dict[str, Any]],
    navigation_graph: Dict[str, Any],
    modal_states: Dict[str, Any],
    tab_states: Dict[str, Any],
    route_transitions: Dict[str, Any],
    replay_log: Dict[str, Any],
    scroll_runtime: Dict[str, Any] | None = None,
    pagination_runtime: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    return {
        "ir": "interaction_runtime",
        "interactions": list(interactions),
        "navigation_graph": navigation_graph,
        "modal_states": modal_states,
        "tab_states": tab_states,
        "route_transitions": route_transitions,
        "replay_log": replay_log,
        "scroll_runtime": scroll_runtime or {"bounded": True},
        "pagination_runtime": pagination_runtime or {"bounded": True},
        "bounded": True,
    }
