from __future__ import annotations

from typing import Any, Dict

from core.repository.event_topology_engine import infer_event_topology


def model_event_flow(source: str, path: str = "") -> Dict[str, Any]:
    topo = infer_event_topology(source, path=path)
    return {"events": topo.get("events", []), "evidence": topo.get("evidence", ""), "topology": topo}
