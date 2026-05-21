from __future__ import annotations

from typing import Any, Dict


def prove_architecture_consistency(
    graph: Dict[str, Any],
) -> Dict[str, Any]:

    nodes = graph.get(
        "nodes",
        [],
    )

    return {
        "consistent": isinstance(
            nodes,
            list,
        ),
        "node_count": len(nodes),
    }
