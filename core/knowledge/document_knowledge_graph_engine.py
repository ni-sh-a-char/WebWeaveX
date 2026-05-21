from __future__ import annotations

from typing import Any, Dict

MAX_NODES = 10000


def build_document_knowledge_graph(
    structure: Dict[str, Any],
) -> Dict[str, Any]:
    nodes = []
    edges = []

    sections = structure.get(
        "sections",
        [],
    )

    for idx, section in enumerate(sections):
        node_id = f"section_{idx}"

        nodes.append({
            "id": node_id,
            "title": section.get("title"),
        })

        if idx > 0:
            edges.append({
                "from": f"section_{idx - 1}",
                "to": node_id,
                "relation": "next_section",
            })

    return {
        "nodes": nodes[:MAX_NODES],
        "edges": edges[:MAX_NODES],
        "bounded": True,
    }
