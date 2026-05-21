from __future__ import annotations

from typing import Any, Dict

from core.repository.runtime_semantics_engine import analyze_runtime_semantics
from core.repository.execution_flow_engine import reconstruct_execution_flow
from core.parsers.parser_registry import parse_source


def analyze_runtime_execution(source: str, path: str = "") -> Dict[str, Any]:
    parsed = parse_source(source, path=path) if source else {}
    runtime = analyze_runtime_semantics(source, path)
    flow = reconstruct_execution_flow(parsed)
    return {
        "runtime": runtime,
        "execution": flow,
        "evidence": sorted(set(runtime.get("evidence", []) + flow.get("evidence", []))),
        "parser_backed": runtime.get("parser_first", False),
    }
