from __future__ import annotations

from typing import Any
from typing import Dict

from core.runtime.distributed_routing_engine import (
    route_semantic_tasks,
)


def eval_distributed_semantic(
    case: Dict[str, Any],
) -> Dict[str, Any]:

    r = route_semantic_tasks(
        tasks=case["tasks"],
        nodes=case["nodes"],
    )

    return {
        "predicted": (
            len(r["routes"]) > 0
        ),
        "expected_match": True,
    }
