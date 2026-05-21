from __future__ import annotations

from typing import Any, Dict, List


MAX_LINEAGE = 200


def record_semantic_lineage(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    ordered = sorted(entries, key=lambda e: (int(e.get("version", 0)), str(e.get("id", ""))))[:MAX_LINEAGE]
    return {"lineage": ordered, "count": len(ordered), "deterministic": True, "bounded": True}
