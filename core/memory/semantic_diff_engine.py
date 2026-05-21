from __future__ import annotations

from typing import Any, Dict, List


def diff_semantic_ir(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    changes: List[Dict[str, str]] = []
    for key in sorted(set(before.keys()) | set(after.keys())):
        if before.get(key) != after.get(key):
            changes.append({"field": key, "changed": "true"})
    return {"changes": changes, "change_count": len(changes), "deterministic": True}
