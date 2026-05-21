from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


def resolve_dependencies(
    tasks: List[
        Dict[str, Any]
    ],
) -> Dict[str, Any]:

    resolved = []

    unresolved = []

    indexed = []
    for i, task in enumerate(tasks):
        task_id = task.get("id", f"task_{i}")
        indexed.append({**task, "id": task_id})

    known = {t["id"] for t in indexed}

    for task in indexed:

        deps = task.get(
            "depends_on",
            [],
        )

        if all(
            dep in known
            for dep in deps
        ):

            resolved.append(task)

        else:

            unresolved.append(task)

    return {
        "resolved": resolved,
        "unresolved": unresolved,
    }
