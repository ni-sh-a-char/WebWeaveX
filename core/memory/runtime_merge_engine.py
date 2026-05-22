from __future__ import annotations

from typing import Any, Dict, List

from core.memory.runtime_federation_engine import federate_runtime_memory
from core.memory.runtime_memory_engine import build_runtime_memory


def merge_runtime_memories(
    memories: List[Dict[str, Any]],
) -> Dict[str, Any]:
    ordered = sorted(
        memories,
        key=lambda m: str(m.get("memory_id", m.get("runtime_id", ""))),
    )
    for mem in ordered:
        history = mem.get("runtime_history", [])
        if isinstance(history, list):
            mem["runtime_history"] = sorted(
                history,
                key=lambda h: (
                    int(h.get("tick", 0)),
                    str(h.get("kind", "")),
                    str(h.get("source", "")),
                ),
            )
    federated = federate_runtime_memory(ordered)
    return build_runtime_memory(
        runtime_history=federated.get("runtime_history", []),
        lineage=federated.get("lineage", []),
        semantic_relations=federated.get("semantic_relations", []),
    )
