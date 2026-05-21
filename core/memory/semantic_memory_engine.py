from __future__ import annotations

from typing import Any, Dict, List, Optional


class SemanticMemory:
    """Bounded deterministic key-value semantic store (legacy kernel API)."""

    def __init__(self, max_entries: int = 256) -> None:
        self.max_entries = max_entries
        self._store: Dict[str, Any] = {}
        self._lineage: Dict[str, Any] = {}

    def put(
        self,
        key: str,
        value: Any,
        lineage: Optional[Dict[str, Any]] = None,
    ) -> None:
        if len(self._store) >= self.max_entries:
            oldest = next(iter(self._store))
            del self._store[oldest]
            self._lineage.pop(oldest, None)
        self._store[key] = value
        if lineage is not None:
            self._lineage[key] = lineage

    def get(self, key: str) -> Any:
        return self._store.get(key)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "keys": sorted(self._store.keys()),
            "count": len(self._store),
            "bounded": len(self._store) <= self.max_entries,
        }


def build_semantic_memory(
    semantic: Optional[Dict[str, Any]] = None,
    history: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    semantic = semantic or {}
    history = history or []
    inner = semantic.get("semantic", semantic)

    concepts = []
    for entity in inner.get("entities", {}).get("entities", []):
        label = str(entity.get("label", entity.get("type", "")))
        if label:
            concepts.append(label)

    return {
        "semantic_convergence": sorted(set(concepts)),
        "recurring_concepts": sorted(set(concepts)),
        "recurring_workflows": [
            str(item.get("objective", ""))
            for item in history
            if item.get("kind") == "workflow"
        ],
        "recurring_structures": sorted(inner.keys()) if isinstance(inner, dict) else [],
        "domain": inner.get("domain", {}).get("domain", ""),
        "bounded": True,
    }
