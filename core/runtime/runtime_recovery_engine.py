from __future__ import annotations

from typing import Any, Dict

from core.runtime.runtime_state_machine_engine import RuntimeStateMachine


def recover_runtime(failed_state: str, evidence: list | None = None) -> Dict[str, Any]:
    sm = RuntimeStateMachine()
    if failed_state != "initialized":
        sm.transition(failed_state, evidence=evidence)
    sm.transition("retrying", evidence=evidence or ["recovery"])
    sm.transition("running", evidence=evidence or ["recovery"])
    return {
        "recovered_state": sm.state,
        "transitions": len(sm.history),
        "deterministic": True,
    }
