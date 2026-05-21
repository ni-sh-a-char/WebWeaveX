from __future__ import annotations

from typing import Dict, List


def build_grounded_facts(edges: List[dict], evidence_key: str = "evidence") -> List[Dict[str, object]]:
    facts = []
    for edge in edges or []:
        if not isinstance(edge, dict):
            continue
        f, t = edge.get("from"), edge.get("to")
        if not f or not t:
            continue
        facts.append(
            {
                "subject": str(f),
                "object": str(t),
                "relation": "related_to",
                evidence_key: edge.get(evidence_key, "graph_edge"),
            }
        )
    return sorted(facts, key=lambda x: (x["subject"], x["object"]))
