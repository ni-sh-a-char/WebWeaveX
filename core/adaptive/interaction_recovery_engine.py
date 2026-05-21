from __future__ import annotations

from typing import Any, Dict, List

from core.adaptive.selector_healing_engine import heal_selector


def recover_interaction_flow(
    interactions: List[Dict[str, Any]],
    dom_nodes: List[Dict[str, Any]],
    html: str = "",
) -> Dict[str, Any]:
    recovered: List[Dict[str, Any]] = []

    for index, action in enumerate(interactions):
        selector = str(action.get("selector", ""))
        healed = heal_selector(selector, dom_nodes, html)

        recovered.append({
            "step": index,
            "original_selector": selector,
            "healed_selector": healed.get("healed_selector", selector),
            "strategy": healed.get("strategy", "primary"),
        })

    return {
        "interactions": recovered,
        "bounded": True,
    }
