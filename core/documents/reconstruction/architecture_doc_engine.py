from __future__ import annotations
import re

def extract_architecture_sections(text: str):
    vals = [m.group(1).strip() for m in re.finditer(r'^#{1,6}\s+(.+)$', text or '', flags=re.MULTILINE) if any(k in m.group(1).lower() for k in ['architecture','design','system'])]
    return {"sections": sorted(set(vals))}
