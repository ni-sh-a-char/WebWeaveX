from __future__ import annotations

import re
from typing import Dict, Any


def extract_headings(text: str) -> Dict[str, Any]:
    src = text or ""
    md = [{"level": len(h), "title": t.strip()} for h, t in re.findall(r"^(#{1,6})\s+(.+)$", src, flags=re.MULTILINE)]
    html = [{"level": int(n), "title": t.strip()} for n, t in re.findall(r"<h([1-6])[^>]*>(.*?)</h\1>", src, flags=re.IGNORECASE|re.DOTALL)]
    headings = sorted(md + html, key=lambda x: (x["level"], x["title"]))
    return {"headings": headings}
