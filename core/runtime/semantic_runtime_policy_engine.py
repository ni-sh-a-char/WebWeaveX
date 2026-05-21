from __future__ import annotations

from typing import Any, Dict


def enforce_runtime_policy(
    state: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "policy_enforced": True,
        "state_size": len(state),
    }
