from __future__ import annotations

from collections import defaultdict

from typing import Any, Dict, List


class SemanticIndex:

    def __init__(self) -> None:

        self._index: Dict[
            str,
            List[Dict[str, Any]]
        ] = defaultdict(list)

    def add(
        self,
        key: str,
        value: Dict[str, Any],
    ) -> None:

        self._index[key].append(value)

    def search(
        self,
        key: str,
    ) -> List[Dict[str, Any]]:

        return list(
            self._index.get(key, [])
        )
