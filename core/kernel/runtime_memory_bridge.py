from __future__ import annotations

from typing import Any, Dict, Optional


def run_memory_phase(
    sources: Optional[Dict[str, Any]] = None,
    tick: int = 0,
    **kwargs: Any,
) -> Dict[str, Any]:
    from core.memory.runtime_memory_orchestrator import run_memory_for_extraction

    return run_memory_for_extraction(
        federated_memory=True,
        sources=sources,
        tick=tick,
        merge_graph=False,
        **{k: v for k, v in kwargs.items() if k in ("memory_path", "memory_key")},
    )
