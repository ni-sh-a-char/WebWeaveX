from __future__ import annotations

from typing import Any, Dict, Optional

from core.connectors.docker_connector_engine import extract_docker_runtime


def extract_container_runtime(
    runtime: str = "docker",
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    normalized = runtime.lower()
    snap = snapshot or {}

    try:
        if normalized in ("docker", "podman", "oci"):
            result = extract_docker_runtime(snap)
            result["runtime"] = normalized
            return result
    except Exception:
        pass

    return {
        "runtime": normalized,
        "containers": [],
        "images": [],
        "volumes": [],
        "networks": [],
        "degraded": True,
        "bounded": True,
    }
