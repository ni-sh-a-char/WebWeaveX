from __future__ import annotations

from typing import Any, Dict, List


ALLOWED_ACTIONS = frozenset({
    "click",
    "focus",
    "type",
    "select",
    "scroll",
})


def perform_native_interaction(
    action: str,
    target: str,
    value: str = "",
    step: int = 0,
) -> Dict[str, Any]:
    normalized = action.lower().strip()

    if normalized not in ALLOWED_ACTIONS:
        return {
            "performed": False,
            "action": normalized,
            "error": "unsupported_action",
            "bounded": True,
        }

    return {
        "performed": True,
        "action": normalized,
        "target": target,
        "value": value,
        "step": step,
        "replay_index": step,
        "bounded": True,
    }


def build_interaction_sequence(
    interactions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    sequence = []
    for index, item in enumerate(interactions[:10000]):
        result = perform_native_interaction(
            action=str(item.get("action", "click")),
            target=str(item.get("target", item.get("selector", ""))),
            value=str(item.get("value", "")),
            step=index,
        )
        sequence.append(result)
    return sequence
