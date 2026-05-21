from __future__ import annotations

from typing import Any, Dict, List


def corroborate_sources(sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts: Dict[str, int] = {}
    for s in sources or []:
        key = str(s.get("url", s.get("id", "")))
        if key:
            counts[key] = counts.get(key, 0) + 1
    corroborated = [k for k, v in counts.items() if v > 1]
    return {
        "corroboration_count": len(corroborated),
        "sources": len(sources or []),
        "deterministic_inputs": [f"corroborated={len(corroborated)}"],
    }
