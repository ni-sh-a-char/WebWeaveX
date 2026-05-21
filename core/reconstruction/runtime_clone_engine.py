from __future__ import annotations

import copy
from typing import Any, Dict, Optional


def clone_runtime_environment(
    source: Dict[str, Any],
    include_graph: bool = True,
    include_queues: bool = True,
) -> Dict[str, Any]:
    cloned = {
        "runtime_graph": copy.deepcopy(source.get("runtime_graph", {})) if include_graph else {},
        "browser_state": copy.deepcopy(source.get("browser", source.get("browser_state", {}))),
        "application_state": copy.deepcopy(source.get("application", source.get("application_state", {}))),
        "execution_queues": copy.deepcopy(source.get("queues", source.get("execution_queues", [])))
        if include_queues
        else [],
        "synchronization_state": copy.deepcopy(source.get("synchronization", source.get("sync", {}))),
        "workflows": copy.deepcopy(source.get("workflows", [])),
        "source_mutated": False,
        "cloned": True,
        "bounded": True,
    }
    return cloned
