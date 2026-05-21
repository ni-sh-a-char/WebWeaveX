from __future__ import annotations

import re
from typing import Any, Dict, List

from bs4 import BeautifulSoup

MAX_ANCHORS = 200


def build_semantic_anchor(
    selector: str,
    html: str,
) -> Dict[str, Any]:
    soup = BeautifulSoup(html or "", "html.parser")
    anchors: List[Dict[str, Any]] = []

    for heading in soup.find_all(["h1", "h2", "h3", "label"])[:MAX_ANCHORS]:
        text = heading.get_text(strip=True)
        if text:
            anchors.append({
                "type": heading.name,
                "text": text[:500],
            })

    for node in soup.find_all(True)[:MAX_ANCHORS]:
        aria = node.get("aria-label")
        if aria:
            anchors.append({
                "type": "aria",
                "text": str(aria)[:500],
            })

    token = _selector_token(selector)
    matched = [
        anchor for anchor in anchors
        if token and token in anchor.get("text", "").lower()
    ]

    return {
        "selector": selector,
        "anchors": sorted(anchors, key=lambda item: (item["type"], item["text"])),
        "matched": matched[:20],
        "bounded": True,
    }


def _selector_token(selector: str) -> str:
    match = re.search(r"#([a-zA-Z0-9_-]+)", selector)
    if match:
        return match.group(1).replace("-", " ").lower()
    match = re.search(r"\.([a-zA-Z0-9_-]+)", selector)
    if match:
        return match.group(1).replace("-", " ").lower()
    return selector.strip().lower()
