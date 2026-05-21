from __future__ import annotations

from collections import deque

from typing import Any
from typing import Deque
from typing import Dict


MAX_STREAM = 100000


class SemanticStream:

    def __init__(self) -> None:

        self.events: Deque[
            Dict[str, Any]
        ] = deque()

    def push(
        self,
        event: Dict[str, Any],
    ) -> None:

        if len(self.events) >= MAX_STREAM:
            return

        self.events.append(
            event
        )

    def next(self) -> Dict[str, Any]:

        if not self.events:
            return {
                "empty": True,
            }

        return self.events.popleft()
