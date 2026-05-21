from __future__ import annotations

from typing import Any, Dict, List


def detect_mirror_topology(urls: List[str]) -> Dict[str, Any]:
    mirrors = []
    seen = {}
    for u in urls or []:
        key = u.split("//")[-1].split("/")[0] if "//" in u else u
        if key in seen:
            mirrors.append({"original": seen[key], "mirror": u})
        else:
            seen[key] = u
    return {"mirrors": mirrors, "count": len(mirrors)}
