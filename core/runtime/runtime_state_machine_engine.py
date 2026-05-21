from __future__ import annotations

from dataclasses import dataclass
from typing import List

VALID_TRANSITIONS = {
    "initialized": {"scheduled", "failed"},
    "scheduled": {"running", "failed"},
    "running": {"completed", "failed", "retrying"},
    "retrying": {"running", "failed"},
    "completed": set(),
    "failed": set(),
}


@dataclass(frozen=True)
class RuntimeTransition:
    previous: str
    current: str
    valid: bool
    evidence: List[str]


class RuntimeStateMachine:
    def __init__(self) -> None:
        self._history: List[RuntimeTransition] = []
        self._state = "initialized"

    @property
    def state(self) -> str:
        return self._state

    @property
    def history(self) -> List[RuntimeTransition]:
        return list(self._history)

    def transition(
        self,
        next_state: str,
        evidence: List[str] | None = None,
    ) -> RuntimeTransition:
        evidence = sorted(set(evidence or []))

        valid = next_state in VALID_TRANSITIONS.get(self._state, set())

        transition = RuntimeTransition(
            previous=self._state,
            current=next_state,
            valid=valid,
            evidence=evidence,
        )

        self._history.append(transition)

        if valid:
            self._state = next_state

        return transition


__all__ = [
    "RuntimeStateMachine",
    "RuntimeTransition",
    "VALID_TRANSITIONS",
]
