from __future__ import annotations

from typing import Any, Dict, List


def infer_service_interactions(parsed: Dict[str, Any], files: List[str]) -> Dict[str, Any]:
    calls = (parsed or {}).get("calls", {}) or {}
    call_list = calls.get("calls", []) if isinstance(calls, dict) else []
    services = {f for f in files if "docker-compose" in f or "k8s" in f or "deployment" in f}
    interactions = [
        {"from": c.get("caller", ""), "to": c.get("callee", ""), "evidence": ["parser:call_graph"]}
        for c in call_list[:100]
        if isinstance(c, dict) and c.get("caller")
    ]
    return {
        "interactions": interactions,
        "service_files": sorted(services),
        "evidence": ["parser:call_graph"] if interactions else [],
    }
