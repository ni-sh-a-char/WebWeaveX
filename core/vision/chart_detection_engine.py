from __future__ import annotations

from typing import Any, Dict

CHART_TERMS = {
    "revenue",
    "sales",
    "growth",
    "profit",
}


def detect_charts(
    blocks: Dict[str, Any],
) -> Dict[str, Any]:
    detected = False

    for block in blocks.get("blocks", []):
        text = block.get("text", "").lower()

        if any(term in text for term in CHART_TERMS):
            detected = True
            break

    return {
        "charts": [{
            "detected": detected,
        }],
        "bounded": True,
    }
