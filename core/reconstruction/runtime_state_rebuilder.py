from __future__ import annotations

from typing import Any, Dict, List, Optional


def rebuild_runtime_state(
    queues: Optional[List[Dict[str, Any]]] = None,
    synchronization: Optional[Dict[str, Any]] = None,
    mutations: Optional[List[Dict[str, Any]]] = None,
    transactions: Optional[List[Dict[str, Any]]] = None,
    memory: Optional[Dict[str, Any]] = None,
    execution_lineage: Optional[List[Dict[str, Any]]] = None,
    workflows: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    ordered_mutations = sorted(
        mutations or [],
        key=lambda item: (
            int(item.get("tick", 0)),
            int(item.get("ordered_index", 0)),
            str(item.get("kind", "")),
        ),
    )
    ordered_transactions = sorted(
        transactions or [],
        key=lambda item: str(item.get("transaction_id", "")),
    )
    ordered_queues = sorted(
        queues or [],
        key=lambda item: (
            -int(item.get("priority", 0)),
            int(item.get("order", 0)),
        ),
    )

    return {
        "queues": ordered_queues,
        "synchronization": dict(synchronization or {}),
        "mutations": ordered_mutations,
        "transactions": ordered_transactions,
        "memory": dict(memory or {}),
        "execution_lineage": sorted(
            execution_lineage or [],
            key=lambda item: str(item.get("id", "")),
        ),
        "workflows": sorted(workflows or [], key=lambda item: str(item.get("id", item.get("objective", "")))),
        "deterministic_order": True,
        "bounded": True,
    }
