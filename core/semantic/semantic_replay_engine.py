from __future__ import annotations

from typing import Any, Dict


def replay_semantic_runtime(
    memory: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "semantic_graph": memory.get("semantic_graph", {}),
        "ontology_mappings": memory.get("ontology", {}),
        "workflow_meaning": memory.get("semantic_workflows", {}),
        "semantic_propagation": memory.get("runtime_semantics", {}),
        "entity_mappings": memory.get("entity_mappings", {}),
        "replayed": True,
        "bounded": True,
    }
