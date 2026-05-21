from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_runtime_replay(
    actions: Optional[List[Dict[str, Any]]] = None,
    transactions: Optional[List[Dict[str, Any]]] = None,
    timeline: Optional[Dict[str, Any]] = None,
    tick: int = 0,
) -> Dict[str, Any]:
    ordered_actions = sorted(
        actions or [],
        key=lambda item: str(item.get("id", item.get("action_id", ""))),
    )
    ordered_tx = sorted(
        transactions or [],
        key=lambda item: str(item.get("transaction_id", "")),
    )

    chain = [
        {"step": index, "action_id": str(action.get("id", action.get("action_id", ""))), "tick": tick + index}
        for index, action in enumerate(ordered_actions)
    ]

    return {
        "replay_chains": chain,
        "execution_restoration": {"actions": ordered_actions, "transactions": ordered_tx},
        "runtime_continuity": {"tick": tick, "steps": len(chain)},
        "replay_package": {
            "actions": ordered_actions,
            "timeline": timeline.get("timeline", []) if timeline else [],
            "deterministic": True,
        },
        "bounded": True,
    }
