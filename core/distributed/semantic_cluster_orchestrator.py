from __future__ import annotations

from typing import Any, Dict, List


MAX_CLUSTER_NODES = 1024


def orchestrate_semantic_cluster(
    nodes: List[Dict[str, Any]],
) -> Dict[str, Any]:

    bounded = nodes[:MAX_CLUSTER_NODES]

    return {
        "cluster_size": len(bounded),
        "nodes": sorted(
            bounded,
            key=lambda x: str(x.get("id")),
        ),
    }
