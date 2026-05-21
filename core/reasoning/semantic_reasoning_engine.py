from __future__ import annotations

from typing import Any, Dict


def reason_semantically(domain: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    from core.reasoning.runtime_reasoning_engine import reason_runtime_semantic
    from core.reasoning.discourse_reasoning_engine import reason_discourse_semantic
    from core.reasoning.topology_reasoning_engine import reason_topology_semantic

    dispatch = {
        "runtime": lambda: reason_runtime_semantic(payload.get("source", ""), payload.get("path", "")),
        "discourse": lambda: reason_discourse_semantic(payload.get("text", "")),
        "topology": lambda: reason_topology_semantic(payload.get("graph", {})),
    }
    fn = dispatch.get(domain)
    if not fn:
        return {"error": "unknown_domain", "explainable": True}
    result = fn()
    return {**result, "domain": domain, "deterministic": True}
