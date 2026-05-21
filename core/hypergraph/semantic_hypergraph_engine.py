from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


MAX_HYPEREDGES = 10000


def build_semantic_hypergraph(
    nodes: List[Dict[str, Any]],
    relationships: List[Dict[str, Any]],
) -> Dict[str, Any]:

    hyperedges = []

    for rel in relationships[:MAX_HYPEREDGES]:

        members = rel.get(
            "members",
            [],
        )

        if len(members) < 2:
            continue

        hyperedges.append({
            "type": rel.get("type"),
            "members": sorted(members),
        })

    return {
        "nodes": nodes,
        "hyperedges": hyperedges,
        "bounded": True,
    }
