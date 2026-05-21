from __future__ import annotations

from typing import Any, Dict, List

from core.adaptive.selector_healing_engine import heal_selector
from core.adaptive.semantic_anchor_engine import build_semantic_anchor


def build_extraction_fallback_chain(
    primary_selector: str,
    dom_nodes: List[Dict[str, Any]],
    html: str = "",
) -> Dict[str, Any]:
    healed = heal_selector(primary_selector, dom_nodes, html)
    anchor = build_semantic_anchor(primary_selector, html)

    chain = [
        {
            "step": 0,
            "strategy": "primary",
            "selector": primary_selector,
        },
        {
            "step": 1,
            "strategy": "healed_selector",
            "selector": healed.get("healed_selector", primary_selector),
        },
        {
            "step": 2,
            "strategy": "semantic_anchor",
            "selector": (
                anchor["matched"][0]["text"]
                if anchor.get("matched")
                else primary_selector
            ),
        },
        {
            "step": 3,
            "strategy": "structural_traversal",
            "selector": dom_nodes[0].get("tag", "div") if dom_nodes else "div",
        },
        {
            "step": 4,
            "strategy": "text_fallback",
            "selector": "body",
        },
    ]

    return {
        "chain": chain,
        "active": chain[1] if healed.get("healed_selector") else chain[0],
        "bounded": True,
    }
