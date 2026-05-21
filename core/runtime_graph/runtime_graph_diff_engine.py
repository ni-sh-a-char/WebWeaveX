from __future__ import annotations

from typing import Any, Dict, List, Set


def diff_runtime_graphs(
    left: Dict[str, Any],
    right: Dict[str, Any],
) -> Dict[str, Any]:
    left_ids: Set[str] = {
        str(x.get("id", ""))
        for x in left.get("nodes", [])
    }

    right_ids: Set[str] = {
        str(x.get("id", ""))
        for x in right.get("nodes", [])
    }

    added = sorted(right_ids - left_ids)
    removed = sorted(left_ids - right_ids)

    return {
        "added_nodes": added,
        "removed_nodes": removed,
        "bounded": True,
    }
