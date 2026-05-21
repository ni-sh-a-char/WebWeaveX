from __future__ import annotations

from typing import Any, Dict

from core.query.semantic_traversal_engine import semantic_traverse


def traverse_with_constraints(graph: Dict[str, Any], start: str, max_depth: int = 10) -> Dict[str, Any]:
    return semantic_traverse(graph, start, max_depth=max_depth)
