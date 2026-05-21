from __future__ import annotations

from typing import Any, Dict, List


_VALID_TRANSITIONS = {
    "idle": ["queued", "simulating"],
    "queued": ["executing", "rolled_back"],
    "executing": ["committed", "rolled_back", "failed"],
    "simulating": ["idle"],
    "committed": ["idle"],
    "rolled_back": ["idle"],
    "failed": ["recovering", "idle"],
    "recovering": ["idle"],
}


def apply_runtime_transition(
    state: str,
    event: str,
) -> Dict[str, Any]:
    current = state if state in _VALID_TRANSITIONS else "idle"
    targets = _VALID_TRANSITIONS.get(current, ["idle"])

    if event == "enqueue" and "queued" in targets:
        next_state = "queued"
    elif event == "execute" and "executing" in targets:
        next_state = "executing"
    elif event == "commit" and "committed" in targets:
        next_state = "committed"
    elif event == "rollback" and "rolled_back" in targets:
        next_state = "rolled_back"
    elif event == "simulate" and "simulating" in targets:
        next_state = "simulating"
    elif event == "fail" and "failed" in targets:
        next_state = "failed"
    elif event == "recover" and "recovering" in targets:
        next_state = "recovering"
    else:
        next_state = targets[0] if targets else "idle"

    return {
        "from": current,
        "to": next_state,
        "event": event,
        "valid": next_state in _VALID_TRANSITIONS,
        "bounded": True,
    }
