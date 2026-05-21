from __future__ import annotations

from typing import Any, Dict, List

from core.distributed_extraction.distributed_load_balancer import (
    balance_extraction_workloads,
)


def route_extraction_tasks(
    workers: List[Dict[str, Any]],
    tasks: List[Dict[str, Any]],
) -> Dict[str, Any]:
    return balance_extraction_workloads(workers, tasks)
