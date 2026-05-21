from __future__ import annotations

from typing import Any, Dict, List

from core.query.semantic_traversal_engine import traverse_graph


def query_topology(adjacency: Dict[str, List[str]], start: str) -> Dict[str, Any]:
    order = traverse_graph(adjacency, start)
    return {"order": order, "count": len(order), "deterministic": True, "bounded": True}
