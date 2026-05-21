from __future__ import annotations

from typing import Any, Dict, Optional


def run_semantic_phase(
    sources: Optional[Dict[str, Any]] = None,
    tick: int = 0,
    **kwargs: Any,
) -> Dict[str, Any]:
    from core.semantic.semantic_orchestrator import run_semantic_for_extraction

    return run_semantic_for_extraction(
        semantic_runtime=True,
        sources=sources,
        tick=tick,
        merge_graph=False,
        **{k: v for k, v in kwargs.items() if k in ("memory_path", "memory_key")},
    )
