from __future__ import annotations

from typing import Dict, List


def merge_sources(sources: List[Dict[str, object]], key: str = "url") -> List[Dict[str, object]]:
    merged: Dict[str, Dict[str, object]] = {}
    for item in sources or []:
        if not isinstance(item, dict):
            continue
        k = str(item.get(key, ""))
        if not k:
            continue
        if k not in merged:
            merged[k] = dict(item)
            continue
        for field, value in item.items():
            if field not in merged[k]:
                merged[k][field] = value
    return [merged[k] for k in sorted(merged)]
