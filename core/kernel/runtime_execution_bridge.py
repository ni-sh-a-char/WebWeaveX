from __future__ import annotations

from typing import Any, Dict, Optional


def run_execution_phase(
    sources: Optional[Dict[str, Any]] = None,
    runtime: str = "browser",
    tick: int = 0,
    **kwargs: Any,
) -> Dict[str, Any]:
    from core.execution.runtime_execution_orchestrator import run_execution_for_extraction

    return run_execution_for_extraction(
        execution_runtime=True,
        sources=sources,
        runtime=runtime,
        tick=tick,
        merge_graph=False,
        **{k: v for k, v in kwargs.items() if k in (
            "memory_path", "memory_key", "simulate_execution", "rollback_enabled"
        )},
    )
