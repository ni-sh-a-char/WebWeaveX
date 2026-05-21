from __future__ import annotations

from typing import Any, Dict, List

from core.runtime.runtime_state_propagation_engine import propagate_runtime_state

from .schema_types import ExecutionState, RuntimeTransition


def compile_typed_runtime_ir(
    transitions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    typed_transitions: List[RuntimeTransition] = []
    for t in transitions:
        typed_transitions.append(
            RuntimeTransition(
                from_state=str(t.get("from", t.get("from_state", ""))),
                to_state=str(t.get("to", t.get("to_state", ""))),
                transition_type=str(t.get("transition_type", t.get("type", "step"))),
            )
        )
    propagation = propagate_runtime_state(
        [{"from": tr.from_state, "to": tr.to_state} for tr in typed_transitions]
    )
    states = [
        ExecutionState(id=s, state_type="reachable")
        for s in propagation.get("reachable_states", [])
    ]
    return {
        "transitions": typed_transitions,
        "states": states,
        "propagation": propagation,
        "typed": True,
        "deterministic": True,
    }
