from __future__ import annotations

from typing import Any, Dict, List

MAX_SLIDES = 1000


def extract_presentation_structure(
    slides: List[Dict[str, Any]],
) -> Dict[str, Any]:
    parsed = []

    for idx, slide in enumerate(
        slides[:MAX_SLIDES]
    ):
        parsed.append({
            "slide": idx,
            "title": slide.get("title"),
            "content": slide.get("content"),
        })

    return {
        "slides": parsed,
        "bounded": True,
    }
