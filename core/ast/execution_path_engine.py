from __future__ import annotations

from typing import Any, Dict, List


MAX_EXECUTION_PATHS = 100


def reconstruct_execution_paths(
    cfg: Dict[str, Any],
) -> Dict[str, Any]:

    paths: List[List[str]] = []

    nodes = cfg.get("nodes", [])

    for node in nodes[:MAX_EXECUTION_PATHS]:
        paths.append([node["id"]])

    return {
        "paths": paths,
        "path_count": len(paths),
        "bounded": True,
    }
