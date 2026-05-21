from __future__ import annotations

from typing import Any, Callable, Dict, List


def schedule_semantic_tasks(tasks: List[Dict[str, Any]], max_tasks: int = 32) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for t in tasks[:max_tasks]:
        fn: Callable[..., Any] | None = t.get("fn")
        if callable(fn):
            results.append({"id": t.get("id"), "result": fn(), "status": "ok"})
        else:
            results.append({"id": t.get("id"), "status": "skipped"})
    return results
