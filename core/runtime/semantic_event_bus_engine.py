from __future__ import annotations

from collections import deque
from typing import Any, Dict


MAX_EVENTS = 100000


class SemanticEventBus:
    def __init__(self) -> None:
        self._events = deque(maxlen=MAX_EVENTS)

    def publish(
        self,
        event: Dict[str, Any],
    ) -> None:

        self._events.append(event)

    def consume(self) -> Dict[str, Any] | None:
        if not self._events:
            return None

        return self._events.popleft()
