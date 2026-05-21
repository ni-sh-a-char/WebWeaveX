from __future__ import annotations

import re
from urllib.parse import urljoin


def discover_links(base_url: str, text: str):
    src = text or ""
    hrefs = re.findall(r"""href=["']([^"']+)["']""", src, flags=re.IGNORECASE)
    md = re.findall(r"""\[[^\]]+\]\(([^)]+)\)""", src)
    out = []
    for u in hrefs + md:
        full = urljoin(base_url, u)
        if full.startswith("http://") or full.startswith("https://"):
            out.append(full)
    return sorted(set(out))

