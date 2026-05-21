from __future__ import annotations
import re

def extract_diagram_refs(text: str):
    src=text or ''
    refs=sorted(set(re.findall(r"(?:mermaid|plantuml|diagram)[: ]", src, flags=re.IGNORECASE)))
    return {"diagram_references": refs}
