from __future__ import annotations

from typing import Any, Dict, List


def reconstruct_tutorial_causality(sections: List[Dict[str, Any]]) -> Dict[str, Any]:
    edges = []

    ordered = sorted(
        sections,
        key=lambda s: int(s.get("order", 0)),
    )

    for idx in range(1, len(ordered)):
        previous = ordered[idx - 1]
        current = ordered[idx]

        edges.append(
            {
                "from": previous.get("id"),
                "to": current.get("id"),
                "metadata": {
                    "kind": "tutorial_prerequisite",
                    "basis": "document_order",
                },
            }
        )

    return {
        "tutorial_edges": edges,
        "count": len(edges),
        "deterministic": True,
    }
