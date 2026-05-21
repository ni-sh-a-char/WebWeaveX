from __future__ import annotations

from typing import Any, Dict, List

from core.repository.runtime_execution_engine import analyze_runtime_execution


def model_runtime_state(source: str, path: str = "") -> Dict[str, Any]:
    ex = analyze_runtime_execution(source, path)
    return {
        "state": "active" if ex.get("parser_backed") else "unknown",
        "dependencies": ex.get("runtime", {}).get("dependencies", []),
        "execution": ex.get("execution", {}),
        "evidence": ex.get("evidence", []),
        "transitions": [{"from": "init", "to": "parsed" if ex.get("parser_backed") else "text"}],
    }
