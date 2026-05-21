from __future__ import annotations

from typing import Any, Dict, List

BUTTON_KEYWORDS = {
    "submit",
    "login",
    "sign in",
    "continue",
}


def detect_ui_components(
    blocks: Dict[str, Any],
) -> Dict[str, Any]:
    components = []

    for block in blocks.get("blocks", []):
        text = block.get("text", "").lower()

        if text in BUTTON_KEYWORDS:
            components.append({
                "type": "button",
                "text": text,
                "bbox": block.get("bbox"),
            })

    return {
        "components": components,
        "bounded": True,
    }
