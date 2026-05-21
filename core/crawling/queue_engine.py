from __future__ import annotations

from typing import List, Set


class DeterministicQueue:
    def __init__(self):
        self._items: List[str] = []
        self._seen: Set[str] = set()

    def enqueue(self, url: str) -> bool:
        u = (url or "").strip()
        if not u or u in self._seen:
            return False
        self._items.append(u)
        self._seen.add(u)
        return True

    def dequeue(self) -> str:
        return self._items.pop(0) if self._items else ""

    def peek(self) -> str:
        return self._items[0] if self._items else ""

    def items(self) -> List[str]:
        return list(self._items)

