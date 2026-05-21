from __future__ import annotations

from typing import Any, Dict, Optional


def extract_causality_semantics(
    causality_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    causality = causality_result or {}
    inner = causality.get("causality", causality)
    propagation = inner.get("propagation", {})
    alignment = inner.get("alignment", {})

    handoffs = propagation.get("handoffs", [])
    critical_chains = [
        {
            "from": handoff.get("from", ""),
            "to": handoff.get("to", ""),
            "impact": "cross_runtime_propagation",
        }
        for handoff in handoffs[:1000]
    ]

    return {
        "workflow_propagation_meaning": "sequential_runtime_handoff",
        "operational_impact": len(critical_chains),
        "runtime_significance": alignment.get("runtime_count", 0),
        "critical_event_chains": critical_chains,
        "bounded": True,
    }
