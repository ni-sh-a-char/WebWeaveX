from __future__ import annotations
import re

def build_semantic_flow(text: str):
    headings = [m.group(1).strip() for m in re.finditer(r'^#{1,6}\s+(.+)$', text or '', flags=re.MULTILINE)]
    edges = [{"from": headings[i], "to": headings[i+1]} for i in range(max(0, len(headings)-1))]
    return {"nodes": headings, "edges": edges}
