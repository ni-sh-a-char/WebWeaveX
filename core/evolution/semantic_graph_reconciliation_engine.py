from __future__ import annotations

from typing import Any, Dict, List


def reconcile_semantic_graphs(
    left: Dict[str, Any],
    right: Dict[str, Any],
) -> Dict[str, Any]:
    left_ids = {
        str(n.get("id"))
        for n in left.get("nodes", [])
        if isinstance(n, dict) and n.get("id")
    }
    right_ids = {
        str(n.get("id"))
        for n in right.get("nodes", [])
        if isinstance(n, dict) and n.get("id")
    }
    return {
        "shared": sorted(left_ids & right_ids),
        "left_only": sorted(left_ids - right_ids),
        "right_only": sorted(right_ids - left_ids),
    }
