from __future__ import annotations

from typing import Any, Dict, List


def diff_ontology_edges(before: List[Dict[str, Any]], after: List[Dict[str, Any]]) -> Dict[str, Any]:
    def key(e):
        return (e.get("from"), e.get("to"))

    bk = {key(e) for e in before if isinstance(e, dict)}
    ak = {key(e) for e in after if isinstance(e, dict)}
    return {"added": len(ak - bk), "removed": len(bk - ak), "stable": len(bk & ak)}
