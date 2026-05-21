from __future__ import annotations

from typing import Any, Dict


def merge_semantic_states(left: Dict[str, Any], right: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(left)
    for k, v in sorted(right.items()):
        if k not in merged:
            merged[k] = v
        elif merged[k] != v:
            merged[k] = {"left": merged[k], "right": v, "conflict": True}
    return {"state": merged, "deterministic": True}
