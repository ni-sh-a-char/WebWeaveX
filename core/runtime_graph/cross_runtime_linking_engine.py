from __future__ import annotations

from typing import Any, Dict, List


def link_runtime_entities(
    graph: Dict[str, Any],
) -> Dict[str, Any]:
    nodes = list(graph.get("nodes", []) or [])

    links: List[Dict[str, Any]] = []

    seen = {}

    for node in nodes:
        name = str(
            node.get("name", "")
        ).strip().lower()

        if not name:
            continue

        if name not in seen:
            seen[name] = []

        seen[name].append(node)

    for name, grouped in sorted(seen.items()):
        if len(grouped) < 2:
            continue

        ids = sorted(
            str(x.get("id", ""))
            for x in grouped
        )

        for i in range(len(ids) - 1):
            links.append({
                "from": ids[i],
                "to": ids[i + 1],
                "relation": "same_entity",
            })

    return {
        "entity_links": links[:100000],
        "bounded": True,
    }
