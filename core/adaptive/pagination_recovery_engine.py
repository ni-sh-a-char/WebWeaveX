from __future__ import annotations

from typing import Any, Dict, List

_NEXT_PATTERNS = [
    "a.next",
    "button.next",
    "[aria-label='Next']",
    "a:has-text('Next')",
]


def recover_pagination_flow(
    broken_selector: str,
    html: str = "",
) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []

    for index, selector in enumerate(_NEXT_PATTERNS):
        if _pattern_matches(selector, html):
            candidates.append({
                "selector": selector,
                "priority": index,
            })

    if not candidates:
        candidates.append({
            "selector": broken_selector,
            "priority": 99,
        })

    active = sorted(candidates, key=lambda item: item["priority"])[0]

    return {
        "original": broken_selector,
        "recovered_selector": active["selector"],
        "candidates": candidates,
        "bounded": True,
    }


def _pattern_matches(selector: str, html: str) -> bool:
    lowered = html.lower()
    if "next" in selector.lower():
        return "next" in lowered
    return selector.strip("#.") in lowered
