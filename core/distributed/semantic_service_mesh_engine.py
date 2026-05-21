from __future__ import annotations

from typing import Any, Dict, List


def build_semantic_service_mesh(
    services: List[Dict[str, Any]],
) -> Dict[str, Any]:

    nodes = sorted(
        services,
        key=lambda x: str(x.get("id")),
    )

    links = []

    for idx in range(len(nodes) - 1):
        links.append(
            {
                "from": nodes[idx]["id"],
                "to": nodes[idx + 1]["id"],
            }
        )

    return {
        "nodes": nodes,
        "links": links,
    }
