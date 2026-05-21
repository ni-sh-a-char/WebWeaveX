from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


class SemanticWAL:

    def __init__(self) -> None:

        self.entries: List[
            Dict[str, Any]
        ] = []

    def append(
        self,
        entry: Dict[str, Any],
    ) -> None:

        self.entries.append(entry)

    def replay(self) -> Dict[str, Any]:

        return {
            "entries": list(
                self.entries
            ),
            "count": len(
                self.entries
            ),
        }
