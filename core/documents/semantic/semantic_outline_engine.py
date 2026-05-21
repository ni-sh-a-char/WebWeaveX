from __future__ import annotations

import re


def extract_semantic_outline(text: str):
    source = text or ""
    headings = []
    for m in re.finditer(r"^(#+)\s+(.+)$", source, flags=re.MULTILINE):
        headings.append({"level": len(m.group(1)), "title": m.group(2).strip()})
    return {"headings": headings, "count": len(headings)}
