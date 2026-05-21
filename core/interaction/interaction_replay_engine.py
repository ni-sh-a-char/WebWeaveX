from __future__ import annotations

from typing import Any, Dict, List

from core.interaction.browser_interaction_engine import (
    click_element,
    fill_input,
    hover_element,
    record_interaction,
    select_option,
    wait_for_selector,
)

MAX_REPLAY_ACTIONS = 1000

_ACTION_DISPATCH = {
    "click": lambda page, action: click_element(
        page,
        str(action.get("selector", "")),
    ),
    "fill": lambda page, action: fill_input(
        page,
        str(action.get("selector", "")),
        str(action.get("value", action.get("metadata", {}).get("value", ""))),
    ),
    "select": lambda page, action: select_option(
        page,
        str(action.get("selector", "")),
        str(action.get("value", action.get("metadata", {}).get("value", ""))),
    ),
    "hover": lambda page, action: hover_element(
        page,
        str(action.get("selector", "")),
    ),
    "wait": lambda page, action: wait_for_selector(
        page,
        str(action.get("selector", "")),
    ),
}


def replay_interactions(
    page: Any,
    interaction_log: List[Dict[str, Any]],
) -> Dict[str, Any]:
    replay_log: List[Dict[str, Any]] = []

    for index, action in enumerate(interaction_log[:MAX_REPLAY_ACTIONS]):
        action_type = str(
            action.get("action", action.get("type", ""))
        ).strip()

        handler = _ACTION_DISPATCH.get(action_type)

        if handler is not None:
            handler(page, action)

        replay_log.append({
            "step": index,
            "action": record_interaction(
                action=action_type,
                selector=str(action.get("selector", "")),
                metadata=dict(action.get("metadata", {})),
                step=index,
            ),
            "replayed": True,
        })

    return {
        "replay": replay_log,
        "bounded": True,
    }
