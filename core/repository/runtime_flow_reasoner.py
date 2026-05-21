from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.repository.execution_dependency_engine import model_execution_dependencies
from core.repository.runtime_semantics_engine import analyze_runtime_semantics


def reason_runtime_flow(source: str, path: str = "", files: Optional[List[str]] = None) -> Dict[str, Any]:
    runtime = analyze_runtime_semantics(source, path)
    exec_deps = model_execution_dependencies(source, path)
    return {
        "runtime": runtime,
        "execution_flow": exec_deps,
        "topology": {"edges": exec_deps.get("edges", [])},
        "evidence": sorted(set(runtime.get("evidence", []) + exec_deps.get("evidence", []))),
    }
