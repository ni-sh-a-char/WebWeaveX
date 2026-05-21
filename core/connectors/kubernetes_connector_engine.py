from __future__ import annotations

from typing import Any, Dict, Optional


def extract_kubernetes_runtime(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    return {
        "namespaces": sorted(snap.get("namespaces", ["default"]), key=str),
        "pods": sorted(snap.get("pods", []), key=lambda item: str(item.get("name", item))),
        "deployments": sorted(snap.get("deployments", []), key=lambda item: str(item.get("name", item))),
        "services": list(snap.get("services", [])),
        "ingress": list(snap.get("ingress", [])),
        "topology": dict(snap.get("topology", {})),
        "events": list(snap.get("events", []))[:5000],
        "degraded": snap.get("degraded", False),
        "bounded": True,
    }
