from __future__ import annotations

from typing import Any, Dict, List


def build_evidence_graph(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, str]] = []
    seen = set()
    for claim in claims or []:
        if not isinstance(claim, dict):
            continue
        cid = str(claim.get("id", ""))
        if not cid or cid in seen:
            continue
        seen.add(cid)
        nodes.append({"id": cid, "kind": "claim", "metadata": {"sources": claim.get("sources", [])}})
        for src in claim.get("sources", []) or []:
            sid = f"source:{src}"
            if sid not in seen:
                seen.add(sid)
                nodes.append({"id": sid, "kind": "source", "metadata": {}})
            edges.append({"from": sid, "to": cid})
    nodes = nodes[:5000]
    allowed = {n["id"] for n in nodes}
    edges = [e for e in sorted(edges, key=lambda x: (x["from"], x["to"])) if e["from"] in allowed and e["to"] in allowed][:20000]
    return {"nodes": nodes, "edges": edges}
