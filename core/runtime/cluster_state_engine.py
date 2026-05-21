from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


def compute_cluster_state(
    nodes: List[
        Dict[str, Any]
    ],
) -> Dict[str, Any]:

    return {
        "cluster_size": len(
            nodes
        ),
        "node_ids": sorted(
            n.get("id")
            for n in nodes
            if isinstance(n, dict)
            and n.get("id")
        ),
    }
