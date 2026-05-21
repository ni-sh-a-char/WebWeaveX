from __future__ import annotations

from typing import Any, Dict, List


def federate_runtime_memory(
    memories: List[Dict[str, Any]],
) -> Dict[str, Any]:
    federated_history: List[Dict[str, Any]] = []
    federated_lineage: List[Dict[str, Any]] = []
    federated_relations: List[Dict[str, Any]] = []

    for memory in memories:
        federated_history.extend(memory.get("runtime_history", []))
        federated_lineage.extend(memory.get("lineage", []))
        federated_relations.extend(memory.get("semantic_relations", []))

    return {
        "federated_count": len(memories),
        "runtime_history": sorted(
            federated_history,
            key=lambda item: int(item.get("tick", 0)),
        ),
        "lineage": sorted(federated_lineage, key=lambda item: str(item.get("id", ""))),
        "semantic_relations": sorted(
            federated_relations,
            key=lambda item: (
                str(item.get("from", "")),
                str(item.get("to", "")),
            ),
        ),
        "bounded": True,
    }
