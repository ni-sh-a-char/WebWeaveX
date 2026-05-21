from __future__ import annotations

from typing import Any, Dict, List


def node_ids(graph: Dict[str, Any]) -> List[str]:
    ids: List[str] = []
    for raw in (graph or {}).get("nodes", []) or []:
        if isinstance(raw, dict):
            nid = str(raw.get("id", "")).strip()
        else:
            nid = str(raw or "").strip()
        if nid:
            ids.append(nid)
    return sorted(set(ids))
