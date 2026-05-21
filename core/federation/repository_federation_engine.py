from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


def federate_repositories(
    repositories: List[
        Dict[str, Any]
    ],
) -> Dict[str, Any]:

    merged_nodes = []

    for repo in repositories:

        merged_nodes.extend(
            repo.get("nodes", [])
        )

    return {
        "repositories": len(
            repositories
        ),
        "nodes": merged_nodes,
        "federated": True,
    }
