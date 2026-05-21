from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Optional


def begin_runtime_transaction(
    tick: int = 0,
    checkpoint_id: str = "",
) -> Dict[str, Any]:
    payload = json.dumps({"tick": tick, "checkpoint": checkpoint_id}, sort_keys=True)
    transaction_id = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:32]

    return {
        "transaction_id": transaction_id,
        "actions": [],
        "mutations": [],
        "transitions": [],
        "checkpoints": [checkpoint_id] if checkpoint_id else [],
        "committed": False,
        "rolled_back": False,
        "bounded": True,
    }


def commit_runtime_transaction(
    transaction: Dict[str, Any],
) -> Dict[str, Any]:
    updated = dict(transaction)
    updated["committed"] = True
    updated["rolled_back"] = False
    return updated


def rollback_runtime_transaction(
    transaction: Dict[str, Any],
) -> Dict[str, Any]:
    updated = dict(transaction)
    updated["committed"] = False
    updated["rolled_back"] = True
    updated["actions"] = []
    updated["mutations"] = []
    return updated
