from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_runtime_patterns(
    ui: Optional[Dict[str, Any]] = None,
    workflows: Optional[List[Dict[str, Any]]] = None,
    semantic: Optional[Dict[str, Any]] = None,
    sync_history: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    ui = ui or {}
    workflows = workflows or []
    sync_history = sync_history or []

    return {
        "ui_structures": sorted(ui.keys()) if isinstance(ui, dict) else [],
        "workflow_patterns": [
            str(w.get("objective", w.get("action", "")))
            for w in workflows[:1000]
        ],
        "semantic_layouts": list((semantic or {}).keys())[:100],
        "sync_histories": len(sync_history),
        "bounded": True,
    }
