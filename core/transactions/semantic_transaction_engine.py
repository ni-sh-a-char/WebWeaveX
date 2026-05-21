from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


class SemanticTransaction:

    def __init__(self) -> None:

        self.operations: List[
            Dict[str, Any]
        ] = []

        self.committed = False

    def add_operation(
        self,
        operation: Dict[str, Any],
    ) -> None:

        if self.committed:
            return

        self.operations.append(
            operation,
        )

    def commit(self) -> Dict[str, Any]:

        self.committed = True

        return {
            "operations": len(
                self.operations
            ),
            "committed": True,
        }

    def rollback(self) -> Dict[str, Any]:

        count = len(
            self.operations
        )

        self.operations.clear()

        return {
            "rolled_back": count,
        }
