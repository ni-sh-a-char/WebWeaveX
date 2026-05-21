from __future__ import annotations

from typing import Any, Dict, Optional


def create_extraction_worker(
    worker_id: str,
    runtime_state: Optional[Dict[str, Any]] = None,
    identity: Optional[Dict[str, Any]] = None,
    adaptive_runtime: Optional[Dict[str, Any]] = None,
    stream_runtime: Optional[Dict[str, Any]] = None,
    status: str = "idle",
) -> Dict[str, Any]:
    return {
        "worker_id": str(worker_id),
        "runtime_state": dict(runtime_state or {}),
        "identity": dict(identity or {}),
        "adaptive_runtime": dict(adaptive_runtime or {}),
        "stream_runtime": dict(stream_runtime or {}),
        "status": str(status),
        "bounded": True,
    }
