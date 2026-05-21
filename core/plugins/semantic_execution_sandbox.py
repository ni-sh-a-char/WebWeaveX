from __future__ import annotations

from typing import Any, Dict


MAX_SANDBOX_KEYS = 1000


class SemanticExecutionSandbox:
    """Bounded in-memory sandbox — no eval/exec/subprocess."""

    def __init__(self) -> None:
        self._state: Dict[str, Any] = {}

    def put(self, key: str, value: Any) -> bool:
        if key.startswith("__") or len(self._state) >= MAX_SANDBOX_KEYS:
            return False
        self._state[key] = value
        return True

    def get(self, key: str) -> Any:
        return self._state.get(key)

    def snapshot(self) -> Dict[str, Any]:
        return dict(sorted(self._state.items()))
