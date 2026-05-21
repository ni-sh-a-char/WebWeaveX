from __future__ import annotations

from typing import Any, Dict, List


def analyze_semantic_impact(
    target_file: str,
    graph: Dict[str, Any],
) -> Dict[str, Any]:

    affected = []

    for edge in graph.get("edges", []):

        if edge.get("to") == target_file:

            affected.append(
                edge.get("from")
            )

    return {
        "target": target_file,
        "affected": sorted(
            affected,
        ),
        "impact_size": len(affected),
    }
