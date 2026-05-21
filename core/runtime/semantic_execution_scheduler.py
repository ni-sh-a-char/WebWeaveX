from __future__ import annotations

from typing import Any, Dict, List

from core.runtime.semantic_scheduler import schedule_semantic_tasks


def schedule_execution(tasks: List[Dict[str, Any]], max_tasks: int = 32) -> List[Dict[str, Any]]:
    return schedule_semantic_tasks(tasks, max_tasks=max_tasks)
