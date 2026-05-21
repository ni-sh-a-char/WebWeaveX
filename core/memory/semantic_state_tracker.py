from __future__ import annotations

from typing import Any, Dict

from core.memory.semantic_memory_engine import SemanticMemory


class SemanticStateTracker:
    def __init__(self, max_entries: int = 128) -> None:
        self.memory = SemanticMemory(max_entries=max_entries)
        self.version = 0

    def commit(self, key: str, state: Dict[str, Any]) -> Dict[str, Any]:
        self.version += 1
        wrapped = {**state, "version": self.version, "lineage": {"stage": "commit", "version": self.version}}
        self.memory.put(key, wrapped, lineage=wrapped.get("lineage"))
        return wrapped

    def current(self, key: str) -> Dict[str, Any]:
        return self.memory.get(key) or {}
