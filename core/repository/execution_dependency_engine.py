from __future__ import annotations

from typing import Any, Dict, List

from core.repository.execution_flow_engine import reconstruct_execution_flow
from core.parsers.parser_registry import parse_source


def model_execution_dependencies(source: str, path: str = "") -> Dict[str, Any]:
    parsed = parse_source(source, path=path) if source else {}
    flow = reconstruct_execution_flow(parsed)
    edges: List[Dict[str, str]] = []
    prev = None
    for step in flow.get("flow", []):
        call = step.get("call", {}) if isinstance(step.get("call"), dict) else {}
        cur = call.get("callee") or call.get("caller") or ""
        if prev and cur:
            edges.append({"from": str(prev), "to": str(cur), "evidence": ["parser:call_graph"]})
        prev = cur or prev
    return {"edges": edges, "entrypoints": flow.get("entrypoints", []), "evidence": flow.get("evidence", [])}
