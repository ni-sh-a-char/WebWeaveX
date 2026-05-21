from __future__ import annotations

from typing import Any, Dict, List


def build_conflict_graph(conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
    nodes = []
    edges = []
    seen = set()
    for c in conflicts or []:
        if not isinstance(c, dict):
            continue
        a, b = str(c.get("from", "")), str(c.get("to", ""))
        if not a or not b:
            continue
        for nid in (a, b):
            if nid not in seen:
                seen.add(nid)
                nodes.append({"id": nid, "kind": "claim", "metadata": {"conflict": True}})
        edges.append(
            {
                "from": a,
                "to": b,
                "metadata": {"edge_basis": "contradicted", "evidence": c.get("evidence", [])},
            }
        )
    return {"nodes": sorted(nodes, key=lambda n: n["id"]), "edges": edges}
