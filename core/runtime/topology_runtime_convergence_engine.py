from __future__ import annotations

from typing import Any, Dict


def converge_runtime_and_topology(
    runtime_ir: Dict[str, Any],
    topology_ir: Dict[str, Any],
) -> Dict[str, Any]:

    runtime_services = {
        n["id"]
        for n in runtime_ir.get(
            "distributed_topology",
            {},
        ).get("nodes", [])
    }

    topology_services = {
        n["id"]
        for n in topology_ir.get(
            "nodes",
            []
        )
    }

    aligned = sorted(
        runtime_services & topology_services
    )

    return {
        "aligned_services": aligned,
        "alignment_score": (
            len(aligned)
            / max(1, len(runtime_services))
        ),
    }
