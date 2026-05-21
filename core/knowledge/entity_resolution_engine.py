from __future__ import annotations

from typing import Any, Dict, List

from core.knowledge.semantic_identity_resolver import resolve_semantic_identities


def resolve_entities(candidates: List[str], namespace: str = "ontology") -> Dict[str, Any]:
    """Merge duplicate entity strings by deterministic identity hash."""
    ids = resolve_semantic_identities(candidates, namespace)
    clusters: Dict[str, List[str]] = {}
    for ent in ids.get("entities", []):
        clusters.setdefault(ent["id"], []).append(ent["name"])
    return {"clusters": clusters, "entity_count": len(clusters), "evidence": ["ontology:identity_hash"]}
