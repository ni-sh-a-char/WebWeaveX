from __future__ import annotations

from typing import Any, Dict, List

from core.memory.runtime_federation_engine import federate_runtime_memory
from core.memory.runtime_memory_engine import build_runtime_memory


def merge_runtime_memories(
    memories: List[Dict[str, Any]],
) -> Dict[str, Any]:
    federated = federate_runtime_memory(memories)
    return build_runtime_memory(
        runtime_history=federated.get("runtime_history", []),
        lineage=federated.get("lineage", []),
        semantic_relations=federated.get("semantic_relations", []),
    )
