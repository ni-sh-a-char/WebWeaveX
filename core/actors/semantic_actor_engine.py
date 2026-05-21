from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from typing import Any
from typing import Deque
from typing import Dict
from typing import List


MAX_ACTORS = 1000
MAX_MAILBOX = 10000


@dataclass
class SemanticActor:

    actor_id: str

    mailbox: Deque[
        Dict[str, Any]
    ]


class SemanticActorSystem:

    def __init__(self) -> None:

        self.actors: Dict[
            str,
            SemanticActor,
        ] = {}

    def create_actor(
        self,
        actor_id: str,
    ) -> None:

        if len(self.actors) >= MAX_ACTORS:
            return

        self.actors[
            actor_id
        ] = SemanticActor(
            actor_id=actor_id,
            mailbox=deque(),
        )

    def send(
        self,
        actor_id: str,
        message: Dict[str, Any],
    ) -> None:

        actor = self.actors.get(
            actor_id
        )

        if actor is None:
            return

        if len(actor.mailbox) >= MAX_MAILBOX:
            return

        actor.mailbox.append(
            message
        )

    def receive(
        self,
        actor_id: str,
    ) -> Dict[str, Any]:

        actor = self.actors.get(
            actor_id
        )

        if actor is None:
            return {
                "missing": True,
            }

        if not actor.mailbox:
            return {
                "empty": True,
            }

        return actor.mailbox.popleft()
