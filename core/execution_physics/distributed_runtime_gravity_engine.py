from __future__ import annotations

from typing import Any, Dict


MAX_GRAVITY = 100000


def compute_runtime_gravity(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    topology = runtime_ir.get("distributed_topology", {})
    node_count = len(topology.get("nodes", []))
    edge_count = len(topology.get("edges", []))
    gravity = min(node_count + edge_count, MAX_GRAVITY)
    return {
        "gravity": gravity,
        "node_count": node_count,
        "bounded": True,
    }
