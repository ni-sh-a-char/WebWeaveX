from __future__ import annotations

from typing import Any, Dict, List


MAX_DEPENDENCIES = 10000


def analyze_semantic_dependencies(
    repository_ir: Dict[str, Any],
) -> Dict[str, Any]:

    edges = list(
        repository_ir.get(
            "edges",
            [],
        )
    )

    dependency_map: Dict[str, List[str]] = {}

    for edge in edges[:MAX_DEPENDENCIES]:

        source = str(
            edge.get("from")
        )

        target = str(
            edge.get("to")
        )

        dependency_map.setdefault(
            source,
            []
        ).append(target)

    for source in dependency_map:
        dependency_map[source] = sorted(
            dependency_map[source]
        )

    return {
        "dependency_map": dict(
            sorted(dependency_map.items())
        ),
        "bounded": True,
    }
