from __future__ import annotations

from typing import Any, Dict, Optional


def extract_cicd_runtime(
    provider: str = "github_actions",
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    return {
        "provider": provider,
        "workflows": list(snap.get("workflows", [])),
        "jobs": list(snap.get("jobs", [])),
        "logs": list(snap.get("logs", []))[:1000],
        "artifacts": list(snap.get("artifacts", [])),
        "failures": list(snap.get("failures", [])),
        "deployment_graph": dict(snap.get("deployment_graph", {})),
        "degraded": snap.get("degraded", False),
        "bounded": True,
    }
