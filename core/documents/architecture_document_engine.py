from __future__ import annotations
import re

def extract_architecture_docs(text: str):
    src = text or ""
    sections = [m.group(1).strip() for m in re.finditer(r"^#{1,6}\s+(.+)$", src, flags=re.MULTILINE) if "arch" in m.group(1).lower()]
    return {"architecture_sections": sorted(set(sections))}
