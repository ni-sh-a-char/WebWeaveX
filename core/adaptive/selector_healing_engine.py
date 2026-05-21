from __future__ import annotations

import re
from typing import Any, Dict, List

from core.adaptive.semantic_anchor_engine import build_semantic_anchor

MAX_CANDIDATES = 100


def heal_selector(
    selector: str,
    dom_nodes: List[Dict[str, Any]],
    html: str = "",
) -> Dict[str, Any]:
    strategies: List[Dict[str, Any]] = []

    anchor = build_semantic_anchor(selector, html)
    if anchor.get("matched"):
        healed = _anchor_to_selector(anchor["matched"][0])
        strategies.append({
            "strategy": "semantic_anchor",
            "selector": healed,
        })

    for node in dom_nodes[:MAX_CANDIDATES]:
        text = str(node.get("text", "")).lower()
        tag = str(node.get("tag", "div"))
        token = _selector_token(selector)

        if token and token in text:
            strategies.append({
                "strategy": "text_anchor",
                "selector": f"{tag}:has-text('{node.get('text', '')[:100]}')",
            })
            break

    for node in dom_nodes[:MAX_CANDIDATES]:
        attrs = node.get("attrs", {})
        if isinstance(attrs, dict):
            for key in sorted(attrs.keys()):
                if key in {"aria-label", "data-testid", "name", "id"}:
                    value = str(attrs[key])
                    strategies.append({
                        "strategy": "attribute_anchor",
                        "selector": f"[{key}='{value[:200]}']",
                    })
                    break
        if strategies:
            break

    if not strategies:
        parent_tag = dom_nodes[0].get("tag", "div") if dom_nodes else "div"
        strategies.append({
            "strategy": "structural_fallback",
            "selector": str(parent_tag),
        })

    healed = strategies[0]

    return {
        "original": selector,
        "healed_selector": healed["selector"],
        "strategy": healed["strategy"],
        "candidates": strategies[:10],
        "bounded": True,
    }


def _selector_token(selector: str) -> str:
    match = re.search(r"#([a-zA-Z0-9_-]+)", selector)
    if match:
        return match.group(1).replace("-", " ").replace("_", " ").lower()
    match = re.search(r"\.([a-zA-Z0-9_-]+)", selector)
    if match:
        return match.group(1).replace("-", " ").replace("_", " ").lower()
    return selector.strip().lower()


def _anchor_to_selector(anchor: Dict[str, Any]) -> str:
    text = str(anchor.get("text", ""))
    anchor_type = str(anchor.get("type", ""))

    if anchor_type == "aria":
        return f"[aria-label='{text[:200]}']"

    return f"{anchor_type}:has-text('{text[:200]}')"
