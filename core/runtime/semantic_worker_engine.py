from __future__ import annotations

from typing import Any, Callable, Dict, List


MAX_WORKERS = 16


def run_semantic_workers(
    tasks: List[Dict[str, Any]],
    handler: Callable[[Dict[str, Any]], Dict[str, Any]],
) -> List[Dict[str, Any]]:
    results = []
    for task in tasks[:MAX_WORKERS]:
        results.append(handler(task))
    return sorted(results, key=lambda r: str(r.get("id", "")))
