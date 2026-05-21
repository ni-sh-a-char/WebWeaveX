from __future__ import annotations

from typing import Any, Dict, List


def forecast_semantic_resources(
    tasks: List[Dict[str, Any]],
) -> Dict[str, Any]:

    estimate = len(tasks)

    return {
        "cpu_units": estimate,
        "memory_units": estimate * 2,
        "task_count": estimate,
        "bounded": True,
    }
