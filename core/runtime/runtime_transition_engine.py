from __future__ import annotations

from typing import Any, Dict, List

from core.runtime.runtime_state_machine_engine import RuntimeStateMachine


def apply_runtime_transitions(
    states: List[str],
    evidence: List[str] | None = None,
) -> Dict[str, Any]:
    sm = RuntimeStateMachine()
    transitions = []
    for nxt in states:
        t = sm.transition(nxt, evidence=evidence)
        transitions.append(
            {
                "previous": t.previous,
                "current": t.current,
                "valid": t.valid,
                "evidence": t.evidence,
            }
        )
    return {
        "final_state": sm.state,
        "transitions": transitions,
        "deterministic": True,
    }
