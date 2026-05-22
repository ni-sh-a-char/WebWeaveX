from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional


def build_runtime_memory(
    runtime_history: Optional[List[Dict[str, Any]]] = None,
    lineage: Optional[List[Dict[str, Any]]] = None,
    semantic_relations: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    runtime_history = list(runtime_history or [])
    lineage = list(lineage or [])
    semantic_relations = list(semantic_relations or [])

    payload = "|".join(
        [
            str(item.get("tick", item.get("step", "")))
            for item in runtime_history
        ]
        + [str(item.get("id", "")) for item in lineage]
    )
    memory_id = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:32]

    from core.memory.stable_memory_hash import stable_memory_hash

    result = {
        "memory_id": memory_id,
        "runtime_history": sorted(
            runtime_history,
            key=lambda item: int(item.get("tick", item.get("step", 0))),
        ),
        "workflow_history": [
            item for item in runtime_history if item.get("kind") == "workflow"
        ],
        "synchronization_history": [
            item for item in runtime_history if item.get("kind") == "sync"
        ],
        "evolution_history": [
            item for item in runtime_history if item.get("kind") == "evolution"
        ],
        "lineage": sorted(lineage, key=lambda item: str(item.get("id", ""))),
        "semantic_relations": sorted(
            semantic_relations,
            key=lambda item: (
                str(item.get("from", "")),
                str(item.get("to", "")),
            ),
        ),
        "bounded": True,
    }
    result["stable_hash"] = stable_memory_hash(result)
    return result
