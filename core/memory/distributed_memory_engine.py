from __future__ import annotations

from typing import Any, Dict, List


def build_distributed_memory(
    nodes: List[Dict[str, Any]],
) -> Dict[str, Any]:
    merged_nodes = sorted(nodes, key=lambda item: str(item.get("node_id", "")))

    return {
        "nodes": merged_nodes,
        "replication": len(merged_nodes),
        "synchronized": all(item.get("synced", True) for item in merged_nodes),
        "conflicts_resolved": sum(
            int(item.get("conflicts_resolved", 0)) for item in merged_nodes
        ),
        "converged": len(merged_nodes) > 0,
        "bounded": True,
    }
