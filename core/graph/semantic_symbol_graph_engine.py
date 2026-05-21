from __future__ import annotations

from typing import Any, Dict, List


MAX_SYMBOLS = 5000


def build_semantic_symbol_graph(
    symbols: List[Dict[str, Any]],
) -> Dict[str, Any]:

    nodes = []

    edges = []

    for i, sym in enumerate(
        symbols[:MAX_SYMBOLS]
    ):

        node_id = sym["name"]

        nodes.append({
            "id": node_id,
            "kind": "symbol",
        })

        refs = sym.get("references", [])

        for ref in refs:

            edges.append({
                "from": node_id,
                "to": ref,
                "relation": "symbol_reference",
            })

    return {
        "nodes": nodes,
        "edges": edges,
        "bounded": True,
    }
