from __future__ import annotations
import re

def detect_next_links(text: str):
    hrefs=re.findall(r"href=['"]([^'"]+)['"]", text or '', flags=re.IGNORECASE)
    return {"next_pages": sorted(set([h for h in hrefs if 'next' in h.lower() or 'page=' in h.lower()]))}
