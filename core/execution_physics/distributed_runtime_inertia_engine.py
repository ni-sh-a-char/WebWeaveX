from __future__ import annotations

from typing import Any, Dict


MAX_INERTIA = 100000


def compute_runtime_inertia(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    momentum = int(
        runtime_ir.get("semantic_momentum", {}).get(
            "runtime_momentum", 0
        )
        if isinstance(runtime_ir.get("semantic_momentum"), dict)
        else runtime_ir.get("runtime_momentum", 0)
    )
    workers = len(
        list(runtime_ir.get("distributed_workers", []) or [])
    )
    inertia = min(
        momentum * max(workers, 1),
        MAX_INERTIA,
    )
    return {
        "runtime_inertia": inertia,
        "worker_count": workers,
        "bounded": True,
    }
