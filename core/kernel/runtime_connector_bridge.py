from __future__ import annotations

from typing import Any, Dict, Optional


def run_connector_phase(
    sources: Optional[Dict[str, Any]] = None,
    tick: int = 0,
    **kwargs: Any,
) -> Dict[str, Any]:
    from core.connectors.live_runtime_orchestrator import run_live_for_extraction

    return run_live_for_extraction(
        live_runtime=True,
        tick=tick,
        merge_graph=False,
        **{k: v for k, v in kwargs.items() if k in ("memory_path", "memory_key", "snapshot")},
    )
