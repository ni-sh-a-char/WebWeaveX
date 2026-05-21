from __future__ import annotations

from typing import Dict, List
from urllib.parse import urlparse


def detect_mirrors(urls: List[str]) -> Dict[str, object]:
    paths: Dict[str, List[str]] = {}
    for url in urls or []:
        parsed = urlparse(url)
        key = parsed.path or "/"
        paths.setdefault(key, []).append(url)
    mirrors = [{"path": p, "urls": sorted(u)} for p, u in paths.items() if len(u) > 1]
    return {"mirrors": mirrors, "mirror_count": len(mirrors)}
