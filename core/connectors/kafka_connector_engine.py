from __future__ import annotations

from typing import Any, Dict, List, Optional


def extract_kafka_runtime(
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    return {
        "stream_type": "kafka",
        "topics": sorted(snap.get("topics", []), key=str),
        "consumers": list(snap.get("consumers", [])),
        "offsets": dict(snap.get("offsets", {})),
        "propagation_state": str(snap.get("state", "stable")),
        "event_lineage": list(snap.get("lineage", [])),
        "degraded": snap.get("degraded", False),
        "bounded": True,
    }
