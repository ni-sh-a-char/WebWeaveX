from __future__ import annotations

from typing import Any, Dict, Optional


def reconstruct_runtime_memory(
    memory_ir: Optional[Dict[str, Any]] = None,
    semantic: Optional[Dict[str, Any]] = None,
    lineage: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    memory_ir = memory_ir or {}
    semantic = semantic or {}
    lineage = lineage or {}

    runtime_history = memory_ir.get("runtime_history", {})
    if isinstance(runtime_history, dict):
        history_list = runtime_history.get("runtime_history", [])
    else:
        history_list = runtime_history if isinstance(runtime_history, list) else []

    lineage_body = lineage or memory_ir.get("lineage", {})
    lineage_entries = lineage_body.get("lineage", lineage_body) if isinstance(lineage_body, dict) else lineage_body

    return {
        "semantic_memory": dict(semantic or memory_ir.get("semantic", {})),
        "lineage": sorted(
            lineage_entries if isinstance(lineage_entries, list) else [],
            key=lambda item: str(item.get("id", "")),
        ),
        "continuity": dict(memory_ir.get("knowledge", {})),
        "runtime_graph_memory": dict(memory_ir.get("memory_graphs", {})),
        "synchronization_history": [
            item for item in history_list if item.get("kind") == "sync"
        ],
        "bounded": True,
    }
