from __future__ import annotations

from typing import Any, Dict, List, Optional


def evolve_selector_runtime(
    selectors: Optional[Dict[str, str]] = None,
    healed: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    selectors = selectors or {}
    healed = healed or {}
    evolved: List[Dict[str, Any]] = []

    for original, replacement in sorted(healed.items()):
        evolved.append({
            "original": original,
            "evolved": replacement,
            "strategy": "healed_promotion",
            "fallback": f"[data-evolved='{replacement}']",
        })

    for selector in sorted(selectors.keys()):
        if selector in healed:
            continue
        evolved.append({
            "original": selector,
            "evolved": selectors[selector],
            "strategy": "structural_upgrade",
            "fallback": selectors[selector],
        })

    return {
        "selectors": evolved,
        "count": len(evolved),
        "bounded": True,
    }
