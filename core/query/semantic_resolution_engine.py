from __future__ import annotations

from typing import Any, Dict, List

from core.knowledge.entity_resolution_engine import resolve_entities


def semantic_resolve(candidates: List[str], namespace: str = "query") -> Dict[str, Any]:
    return resolve_entities(candidates, namespace)
