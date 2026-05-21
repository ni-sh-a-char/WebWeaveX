from __future__ import annotations

from typing import Any, Dict

from core.repository.async_runtime_engine import detect_async_runtime


def reason_async_execution(source: str, path: str = "") -> Dict[str, Any]:
    async_r = detect_async_runtime(source, path)
    return {
        "async": async_r,
        "propagation": [{"kind": "await", "count": async_r.get("await_count", 0)}],
        "evidence": async_r.get("evidence", []),
        "parser_backed": async_r.get("parser_backed", False),
    }
