from __future__ import annotations

from typing import Any, Dict, Optional


def extract_docker_runtime(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    return {
        "runtime": "docker",
        "containers": list(snap.get("containers", [])),
        "images": sorted(snap.get("images", []), key=str),
        "volumes": list(snap.get("volumes", [])),
        "networks": list(snap.get("networks", [])),
        "states": dict(snap.get("states", {})),
        "health": dict(snap.get("health", {})),
        "degraded": snap.get("degraded", False),
        "bounded": True,
    }
