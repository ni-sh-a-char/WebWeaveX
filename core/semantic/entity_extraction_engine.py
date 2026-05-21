from __future__ import annotations

import re
from typing import Any, Dict, List, Optional


ENTITY_PATTERNS = {
    "organization": re.compile(r"\b(inc|corp|llc|ltd|company)\b", re.I),
    "api": re.compile(r"\b(api|endpoint|rest|graphql)\b", re.I),
    "metric": re.compile(r"\b(kpi|metric|latency|throughput|error rate)\b", re.I),
    "user": re.compile(r"\b(user|account|profile|login)\b", re.I),
    "service": re.compile(r"\b(service|microservice|worker|queue)\b", re.I),
    "workflow": re.compile(r"\b(workflow|pipeline|job|task)\b", re.I),
    "infrastructure": re.compile(r"\b(kubernetes|docker|vm|cluster|deploy)\b", re.I),
}


def extract_semantic_entities(
    text: str = "",
    structure: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    structure = structure or {}
    entities: List[Dict[str, Any]] = []
    relations: List[Dict[str, Any]] = []
    entity_index = 0

    for label, pattern in ENTITY_PATTERNS.items():
        if pattern.search(text):
            entity_id = f"entity:{label}:{entity_index}"
            entities.append({
                "id": entity_id,
                "type": label,
                "label": label,
                "source": "pattern",
            })
            entity_index += 1

    for action in structure.get("actions", [])[:5000]:
        entities.append({
            "id": f"entity:ui_action:{entity_index}",
            "type": "ui_action",
            "label": str(action.get("label", action.get("type", ""))),
            "source": "structure",
        })
        entity_index += 1

    for artifact in structure.get("artifacts", [])[:5000]:
        entities.append({
            "id": f"entity:runtime:{entity_index}",
            "type": "runtime_artifact",
            "label": str(artifact),
            "source": "runtime",
        })
        entity_index += 1

    entities = sorted(entities, key=lambda item: item["id"])

    for index in range(1, len(entities)):
        relations.append({
            "from": entities[index - 1]["id"],
            "to": entities[index]["id"],
            "relation": "related_to",
        })

    return {
        "entities": entities,
        "relations": relations,
        "ontology": {},
        "bounded": True,
    }
