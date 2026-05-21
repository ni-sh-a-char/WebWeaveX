from __future__ import annotations

from typing import Any, Dict


def analyze_infrastructure_semantics(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    topology = runtime_ir.get(
        "distributed_topology",
        {},
    )

    nodes = topology.get(
        "nodes",
        [],
    )

    return {
        "service_count": len(
            nodes
        ),
        "infrastructure_semantic": True,
    }
