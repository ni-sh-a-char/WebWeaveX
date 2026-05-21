from __future__ import annotations

import re


def extract_semantic_diagrams(text: str):
    source = text or ""
    mermaid = re.findall(r"```mermaid\n(.*?)```", source, flags=re.DOTALL)
    plantuml = re.findall(r"```plantuml\n(.*?)```", source, flags=re.DOTALL)
    images = sorted(set(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", source)))
    return {
        "mermaid": sorted({m.strip() for m in mermaid if m.strip()}),
        "plantuml": sorted({p.strip() for p in plantuml if p.strip()}),
        "image_refs": images,
    }
