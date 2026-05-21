from __future__ import annotations

from typing import Any, Dict, List


RELATION_MAP = {
    "organization": "owns",
    "service": "deploys",
    "api": "exposes",
    "metric": "monitors",
    "user": "authenticates",
    "workflow": "triggers",
    "infrastructure": "depends_on",
    "ui_action": "mutates",
}


def build_semantic_graph(
    entities: List[Dict[str, Any]],
    relations: List[Dict[str, Any]],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    for entity in entities[:10000]:
        entity_type = str(entity.get("type", "entity"))
        nodes.append({
            "id": str(entity.get("id", "")),
            "type": entity_type,
            "label": str(entity.get("label", "")),
        })

    for relation in relations[:10000]:
        edges.append({
            "from": str(relation.get("from", "")),
            "to": str(relation.get("to", "")),
            "relation": str(relation.get("relation", "related_to")),
        })

    for entity in entities[:10000]:
        entity_type = str(entity.get("type", ""))
        mapped = RELATION_MAP.get(entity_type)
        if mapped and len(nodes) > 1:
            edges.append({
                "from": str(entity.get("id", "")),
                "to": nodes[0]["id"],
                "relation": mapped,
            })

    if not nodes:
        nodes.append({"id": "semantic:root", "type": "semantic"})

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
