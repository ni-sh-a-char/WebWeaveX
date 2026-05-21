from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.distributed_extraction.distributed_adaptive_runtime_engine import (
    synchronize_adaptive_runtime,
)
from core.distributed_extraction.distributed_cluster_engine import (
    build_cluster_state,
)
from core.distributed_extraction.distributed_identity_engine import (
    route_browser_identity,
)
from core.distributed_extraction.distributed_monitoring_engine import (
    monitor_extraction_cluster,
)
from core.distributed_extraction.distributed_recovery_engine import (
    recover_distributed_runtime,
)
from core.distributed_extraction.distributed_runtime_graph_engine import (
    build_distributed_runtime_graph,
)
from core.distributed_extraction.distributed_session_engine import (
    route_authenticated_sessions,
)
from core.distributed_extraction.distributed_stream_engine import (
    federate_stream_runtimes,
)
from core.distributed_extraction.extraction_queue_engine import (
    dequeue_extraction,
    enqueue_extraction,
)
from core.distributed_extraction.extraction_scheduler_engine import (
    schedule_extraction_runtime,
)
from core.distributed_extraction.extraction_worker_engine import (
    create_extraction_worker,
)
from core.distributed_extraction.runtime_federation_engine import (
    federate_extraction_runtimes,
)
from core.distributed_extraction.distributed_load_balancer import (
    balance_extraction_workloads,
)


def run_distributed_extraction(
    tasks: List[Dict[str, Any]],
    workers: Optional[List[Dict[str, Any]]] = None,
    checkpoint: Optional[Dict[str, Any]] = None,
    tick: int = 0,
    runtime_graphs: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    checkpoint = dict(checkpoint or {})
    queue = list(checkpoint.get("queue", []))
    worker_list = list(workers or checkpoint.get("workers", []))

    if not worker_list:
        worker_list = [
            create_extraction_worker(
                worker_id="worker_0",
                identity={"profile_id": "default", "fingerprint_hash": "fp0"},
                adaptive_runtime={"memory": {"healed_selectors": {}}},
                stream_runtime={"events": []},
            )
        ]

    for task in tasks:
        queued = enqueue_extraction(queue, task)
        queue = queued["queue"]

    schedule = schedule_extraction_runtime(tasks, tick=tick)
    assignments = balance_extraction_workloads(worker_list, tasks)

    session_routes = route_authenticated_sessions(worker_list)
    identity_routes = route_browser_identity(worker_list)

    adaptive_sync = synchronize_adaptive_runtime(
        [worker.get("adaptive_runtime", {}) for worker in worker_list]
    )

    stream_federation = federate_stream_runtimes(
        [
            {
                "worker_id": worker.get("worker_id"),
                "events": worker.get("stream_runtime", {}).get("events", []),
            }
            for worker in worker_list
        ]
    )

    federation = federate_extraction_runtimes(runtime_graphs or [])
    distributed_graph = build_distributed_runtime_graph(
        worker_list,
        federation.get("topology", {}),
    )

    monitoring = monitor_extraction_cluster(worker_list, queue)
    cluster = build_cluster_state(worker_list, queue)

    next_checkpoint = {
        "queue": queue,
        "workers": worker_list,
        "runtime_graph": distributed_graph,
        "identities": identity_routes.get("routes", []),
        "adaptive_memory": adaptive_sync,
        "stream_runtime": stream_federation,
        "tick": tick + 1,
        "assignments": assignments.get("assignments", []),
        "bounded": True,
    }

    return {
        "workers": worker_list,
        "queue": queue,
        "schedule": schedule,
        "assignments": assignments,
        "session_routes": session_routes,
        "identity_routes": identity_routes,
        "adaptive_sync": adaptive_sync,
        "stream_federation": stream_federation,
        "topology": federation,
        "distributed_graph": distributed_graph,
        "monitoring": monitoring,
        "cluster": cluster,
        "checkpoint": next_checkpoint,
        "bounded": True,
    }
