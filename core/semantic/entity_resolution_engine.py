from __future__ import annotations

from typing import Any, Dict, List


def resolve_semantic_entities(
    entities: List[Dict[str, Any]],
) -> Dict[str, Any]:
    canonical: Dict[str, str] = {}
    resolved: List[Dict[str, Any]] = []

    for entity in sorted(entities, key=lambda item: item.get("id", "")):
        label = str(entity.get("label", entity.get("type", ""))).lower().strip()
        canonical_id = canonical.get(label)
        if not canonical_id:
            canonical_id = str(entity.get("id", ""))
            canonical[label] = canonical_id

        resolved.append({
            **entity,
            "canonical_id": canonical_id,
            "resolved": True,
        })

    return {
        "entities": resolved,
        "canonical_map": canonical,
        "bounded": True,
    }
