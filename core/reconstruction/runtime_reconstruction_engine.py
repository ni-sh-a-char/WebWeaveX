from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional


def reconstruct_runtime(
    semantic_ir: Optional[Dict[str, Any]] = None,
    workflow_ir: Optional[Dict[str, Any]] = None,
    synchronization_ir: Optional[Dict[str, Any]] = None,
    execution_ir: Optional[Dict[str, Any]] = None,
    memory_ir: Optional[Dict[str, Any]] = None,
    runtime_graph: Optional[Dict[str, Any]] = None,
    runtime_type: str = "browser",
    tick: int = 0,
) -> Dict[str, Any]:
    canonical = json.dumps(
        {
            "semantic": semantic_ir or {},
            "workflow": workflow_ir or {},
            "sync": synchronization_ir or {},
            "execution": execution_ir or {},
            "memory": memory_ir or {},
            "graph_nodes": len((runtime_graph or {}).get("nodes", [])),
            "runtime_type": runtime_type,
            "tick": tick,
        },
        sort_keys=True,
    )
    runtime_id = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:32]

    return {
        "runtime_id": runtime_id,
        "runtime_type": runtime_type,
        "reconstructed": True,
        "graph_grounded": bool(runtime_graph),
        "bounded": True,
    }
