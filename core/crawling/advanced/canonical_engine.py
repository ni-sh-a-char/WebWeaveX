from __future__ import annotations
import re

def detect_canonical(text: str):
    links=re.findall(r"href=['"]([^'"]+)['"]", text or '', flags=re.IGNORECASE)
    return {"canonical": sorted(set([u for u in links if 'canonical' in (text or '').lower()]))}
