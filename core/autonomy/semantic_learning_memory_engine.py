from __future__ import annotations

from typing import Any, Dict


class SemanticLearningMemory:
    def __init__(self) -> None:
        self._memory: Dict[str, Dict[str, Any]] = {}

    def learn(
        self,
        key: str,
        state: Dict[str, Any],
    ) -> None:

        self._memory[key] = dict(state)

    def recall(
        self,
        key: str,
    ) -> Dict[str, Any]:

        return dict(
            self._memory.get(key, {})
        )
