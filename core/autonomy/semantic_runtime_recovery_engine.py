from __future__ import annotations

from typing import Any, Dict


def recover_semantic_runtime(
    snapshot: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "recovered": True,
        "snapshot_keys": sorted(
            snapshot.keys()
        ),
    }
