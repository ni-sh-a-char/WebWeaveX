from __future__ import annotations

from typing import Any
from typing import Dict


def replicate_semantic_region(
    state: Dict[str, Any],
    replicas: int,
) -> Dict[str, Any]:

    replicated = []

    for i in range(
        max(0, replicas)
    ):

        replicated.append({
            "replica": i,
            "state": dict(state),
        })

    return {
        "replicas": replicated,
    }
