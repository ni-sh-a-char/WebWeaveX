from __future__ import annotations

from typing import Any, Dict

INPUT_KEYWORDS = {
    "email",
    "password",
    "username",
    "search",
}


def extract_forms(
    blocks: Dict[str, Any],
) -> Dict[str, Any]:
    forms = []

    for block in blocks.get("blocks", []):
        text = block.get("text", "").lower()

        if text in INPUT_KEYWORDS:
            forms.append({
                "field": text,
                "bbox": block.get("bbox"),
            })

    return {
        "forms": forms,
        "bounded": True,
    }
