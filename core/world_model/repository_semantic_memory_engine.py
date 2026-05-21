from __future__ import annotations

from typing import Any, Dict


class RepositorySemanticMemory:
    def __init__(self) -> None:
        self._memory: Dict[str, Dict[str, Any]] = {}

    def store(
        self,
        path: str,
        state: Dict[str, Any],
    ) -> None:

        self._memory[path] = dict(state)

    def retrieve(
        self,
        path: str,
    ) -> Dict[str, Any]:

        return dict(
            self._memory.get(path, {})
        )
