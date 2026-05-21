from __future__ import annotations

from typing import Any, Dict, List


def build_runtime_memory_graph(
    entities: List[Dict[str, Any]],
    relations: List[Dict[str, Any]],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    for entity in entities[:10000]:
        node_id = str(entity.get("id", entity.get("label", "")))
        if not node_id:
            continue
        nodes.append({
            "id": node_id,
            "type": str(entity.get("type", "entity")),
        })

    for relation in relations[:10000]:
        edges.append({
            "from": str(relation.get("from", "")),
            "to": str(relation.get("to", "")),
            "relation": str(relation.get("relation", "relates_to")),
        })

    if not nodes:
        nodes.append({"id": "memory:root", "type": "memory"})

    return {
        "nodes": sorted(nodes, key=lambda item: item["id"]),
        "edges": sorted(
            edges,
            key=lambda item: (
                item.get("from", ""),
                item.get("to", ""),
                item.get("relation", ""),
            ),
        ),
        "bounded": True,
    }
