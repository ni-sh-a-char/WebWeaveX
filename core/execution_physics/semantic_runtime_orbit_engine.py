from __future__ import annotations

from typing import Any, Dict, List


MAX_ORBITS = 1000


def compute_runtime_orbits(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    topology = runtime_ir.get("distributed_topology", {})
    nodes = sorted(
        topology.get("nodes", []),
        key=lambda x: str(x.get("id")),
    )[:MAX_ORBITS]
    orbits = [
        {
            "orbit": idx,
            "node": node.get("id"),
        }
        for idx, node in enumerate(nodes)
    ]
    return {
        "orbits": orbits,
        "orbit_count": len(orbits),
        "bounded": True,
    }
