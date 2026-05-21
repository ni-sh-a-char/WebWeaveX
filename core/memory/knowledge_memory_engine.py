from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_knowledge_memory(
    entities: Optional[List[Dict[str, Any]]] = None,
    relations: Optional[List[Dict[str, Any]]] = None,
    topology: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    entities = list(entities or [])
    relations = list(relations or [])
    topology = topology or {}

    return {
        "entities": sorted(entities, key=lambda item: str(item.get("id", ""))),
        "semantic_relations": sorted(
            relations,
            key=lambda item: (
                str(item.get("from", "")),
                str(item.get("to", "")),
                str(item.get("relation", "")),
            ),
        ),
        "runtime_graphs": list(topology.get("graphs", [])),
        "distributed_topology": dict(topology.get("distributed", {})),
        "application_cognition": dict(topology.get("application", {})),
        "operational_structures": list(topology.get("operations", [])),
        "bounded": True,
    }
