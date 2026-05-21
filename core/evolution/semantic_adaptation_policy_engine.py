from __future__ import annotations

from typing import Any, Dict, List


def enforce_adaptation_policies(
    runtime: Dict[str, Any],
    policies: List[Dict[str, Any]],
) -> Dict[str, Any]:
    allowed = []
    denied = []
    for policy in policies:
        key = policy.get("key")
        if key and key in runtime:
            allowed.append(policy)
        else:
            denied.append(policy)
    return {
        "allowed": allowed,
        "denied": denied,
    }
