from __future__ import annotations

from typing import Any, Dict, List


class SemanticIndex:
    def __init__(self) -> None:
        self._index: Dict[str, List[Dict[str, Any]]] = {}

    def insert(
        self,
        key: str,
        value: Dict[str, Any],
    ) -> None:

        bucket = self._index.setdefault(key, [])

        bucket.append(value)

    def lookup(
        self,
        key: str,
    ) -> List[Dict[str, Any]]:

        return list(self._index.get(key, []))
