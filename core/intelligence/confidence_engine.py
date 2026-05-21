from __future__ import annotations

from typing import Any, Dict


def _ratio(num: int, den: int) -> float:
    if den <= 0:
        return 0.0
    return max(0.0, min(1.0, num / den))


def compute_confidence(result: Dict[str, Any]) -> float:
    content = result.get("content", {})
    deps = result.get("dependencies", {})
    rel = result.get("relationships", {})
    meta = result.get("metadata", {})

    completeness = 1.0 if result.get("raw_text", "") else 0.0
    metadata_score = _ratio(len([k for k,v in meta.items() if v not in (None, "", {}, [])]), max(len(meta), 1))
    dep_score = 1.0 if deps.get("packages") else 0.5
    graph_score = 1.0 if rel else 0.5
    consistency = 1.0 if isinstance(content, dict) and isinstance(deps, dict) and isinstance(rel, dict) else 0.0

    score = (0.25*completeness) + (0.2*metadata_score) + (0.2*dep_score) + (0.2*graph_score) + (0.15*consistency)
    return round(max(0.0, min(1.0, score)), 6)
