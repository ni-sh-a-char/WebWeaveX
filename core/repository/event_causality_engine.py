from __future__ import annotations

from typing import Any, Dict

from core.repository.event_flow_engine import model_event_flow


def model_event_causality(source: str, path: str = "") -> Dict[str, Any]:
    flow = model_event_flow(source, path)
    events = flow.get("events", []) if isinstance(flow.get("events"), list) else []
    causal = [{"cause": events[i], "effect": events[i + 1]} for i in range(max(0, len(events) - 1))]
    return {"causal_chain": causal, "evidence": [flow.get("evidence", "event_topology")], "deterministic": True}
