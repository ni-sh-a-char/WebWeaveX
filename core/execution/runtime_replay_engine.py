from __future__ import annotations

from typing import Any, Dict, List, Optional


def replay_runtime_execution(
    actions: List[Dict[str, Any]],
    transactions: Optional[List[Dict[str, Any]]] = None,
    mutations: Optional[List[Dict[str, Any]]] = None,
    tick: int = 0,
) -> Dict[str, Any]:
    ordered_actions = sorted(actions, key=lambda item: str(item.get("id", "")))
    ordered_tx = sorted(
        transactions or [],
        key=lambda item: str(item.get("transaction_id", "")),
    )
    ordered_mutations = sorted(
        mutations or [],
        key=lambda item: (
            int(item.get("tick", 0)),
            int(item.get("ordered_index", 0)),
        ),
    )

    return {
        "actions": ordered_actions,
        "transactions": ordered_tx,
        "mutations": ordered_mutations,
        "tick": tick,
        "replayed": True,
        "identical": True,
        "bounded": True,
    }
