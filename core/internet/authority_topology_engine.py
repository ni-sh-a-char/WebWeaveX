from __future__ import annotations

from typing import Any, Dict

from core.internet.authority_engine import score_authority


def build_authority_topology(urls: list) -> Dict[str, Any]:
    nodes = []
    edges = []
    for u in urls or []:
        auth = score_authority(u)
        nodes.append({"id": u, "authority": auth.get("authority_score", 0)})
    for i in range(len(nodes) - 1):
        edges.append({"from": nodes[i]["id"], "to": nodes[i + 1]["id"], "relation": "authority_chain"})
    return {"nodes": nodes, "edges": edges}
