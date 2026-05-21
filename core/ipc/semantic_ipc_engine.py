from __future__ import annotations

from collections import deque

from typing import Any
from typing import Dict
from typing import Deque


MAX_MESSAGES = 10000


class SemanticIPC:

    def __init__(self) -> None:

        self.queue: Deque[
            Dict[str, Any]
        ] = deque()

    def send(
        self,
        message: Dict[str, Any],
    ) -> None:

        if len(self.queue) >= MAX_MESSAGES:
            return

        self.queue.append(message)

    def receive(self) -> Dict[str, Any]:

        if not self.queue:

            return {
                "empty": True,
            }

        return self.queue.popleft()
