from __future__ import annotations

from typing import Any, Dict

from core.runtime.distributed_topology_engine import (
    build_distributed_topology,
)


def eval_runtime_topology(
    case: Dict[str, Any],
) -> Dict[str, Any]:

    topo = build_distributed_topology(
        case["services"]
    )

    predicted = len(topo["nodes"])

    return {
        "predicted": predicted == case["expected_nodes"],
        "expected_match": True,
    }
