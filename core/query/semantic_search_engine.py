from __future__ import annotations

from typing import Any, Dict, List


def semantic_search(haystack: Dict[str, Any], needle: str, max_hits: int = 50) -> Dict[str, Any]:
    hits: List[Dict[str, str]] = []
    n = needle.lower()

    def walk(obj: Any, path: str = "") -> None:
        if len(hits) >= max_hits:
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj[:max_hits]):
                walk(v, f"{path}[{i}]")
        elif isinstance(obj, str) and n in obj.lower():
            hits.append({"path": path, "match": obj[:120]})

    walk(haystack)
    return {"hits": hits, "count": len(hits), "bounded": len(hits) <= max_hits}
