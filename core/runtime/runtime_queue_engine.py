from __future__ import annotations

from collections import deque
from typing import Any, Deque, Dict, List


MAX_QUEUE = 1000


class RuntimeQueue:
    def __init__(self, max_size: int = MAX_QUEUE) -> None:
        self._q: Deque[Dict[str, Any]] = deque()
        self._max = max_size

    def enqueue(self, item: Dict[str, Any]) -> bool:
        if len(self._q) >= self._max:
            return False
        self._q.append(item)
        return True

    def dequeue(self) -> Dict[str, Any] | None:
        return self._q.popleft() if self._q else None

    def snapshot(self) -> List[Dict[str, Any]]:
        return list(self._q)
