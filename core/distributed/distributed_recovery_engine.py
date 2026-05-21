from __future__ import annotations

from typing import Any, Dict


def recover_distributed_runtime(
    checkpoint: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "recovered": True,
        "state": checkpoint.get("state", {}),
    }
