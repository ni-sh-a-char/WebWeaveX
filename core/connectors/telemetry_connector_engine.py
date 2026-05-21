from __future__ import annotations

from typing import Any, Dict, Optional


def extract_telemetry_runtime(
    backends: Optional[list] = None,
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    backends = backends or ["opentelemetry", "prometheus", "jaeger"]
    snap = snapshot or {}

    return {
        "backends": sorted(backends),
        "metrics": list(snap.get("metrics", [])),
        "traces": list(snap.get("traces", [])),
        "spans": list(snap.get("spans", []))[:10000],
        "logs": list(snap.get("logs", []))[:10000],
        "distributed_correlations": list(snap.get("correlations", [])),
        "degraded": snap.get("degraded", False),
        "bounded": True,
    }
