from __future__ import annotations

from typing import Dict, List

from core.parsers.runtime_resolution_engine import resolve_runtime


def infer_runtime_topology(dependencies: List[str], imports: List[str] | None = None) -> Dict[str, object]:
    runtime = resolve_runtime(dependencies, imports or [])
    return {
        "runtimes": runtime.get("runtimes", []),
        "frameworks": runtime.get("frameworks", []),
        "api_indicators": runtime.get("api_indicators", []),
        "evidence": "parser_runtime_resolution",
    }
