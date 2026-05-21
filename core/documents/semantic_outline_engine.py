from __future__ import annotations

import re
from typing import Dict, List


def extract_semantic_outline(text: str) -> Dict[str, object]:
    headings: List[Dict[str, str]] = []
    for line in (text or "").splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if match:
            headings.append({"level": str(len(match.group(1))), "title": match.group(2).strip()})
    return {"headings": headings, "heading_count": len(headings)}
