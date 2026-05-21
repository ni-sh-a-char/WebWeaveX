from __future__ import annotations

from concurrent.futures import (
    ThreadPoolExecutor,
)

from typing import Any
from typing import Callable
from typing import Dict
from typing import List


MAX_WORKERS = 8


def execute_concurrently(
    tasks: List[
        Callable[[], Dict[str, Any]]
    ],
) -> Dict[str, Any]:

    results = []

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS,
    ) as executor:

        futures = [
            executor.submit(task)
            for task in tasks
        ]

        for future in futures:

            results.append(
                future.result()
            )

    return {
        "results": results,
        "count": len(results),
    }
