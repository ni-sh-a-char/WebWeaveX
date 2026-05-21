from __future__ import annotations

from typing import Any, Dict


def apply_semantic_constraints(bundle: Dict[str, Any], max_depth: int = 20) -> Dict[str, Any]:
    lineage = bundle.get("lineage", {}) or {}
    depth = lineage.get("depth", 0) if isinstance(lineage, dict) else 0
    bounded = depth <= max_depth
    return {**bundle, "constraints": {"max_depth": max_depth, "satisfied": bounded}}
