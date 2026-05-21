from __future__ import annotations

import re


def extract_semantic_tutorials(text: str):
    source = text or ""
    headings = re.findall(r"^(#+)\s+(.+)$", source, flags=re.MULTILINE)
    steps = []
    for hashes, title in headings:
        if len(hashes) <= 3:
            steps.append(title.strip())
    ordered = sorted(set(re.findall(r"^\s*\d+\.\s+(.+)$", source, flags=re.MULTILINE)))
    return {"steps": sorted(set(steps)), "ordered_items": ordered}
