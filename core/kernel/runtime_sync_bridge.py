from __future__ import annotations

from typing import Any, Dict, Optional


def run_sync_phase(
    sources: Optional[Dict[str, Any]] = None,
    tick: int = 0,
    **kwargs: Any,
) -> Dict[str, Any]:
    from core.synchronization.runtime_sync_orchestrator import run_sync_for_extraction

    extraction = (sources or {}).get("extraction", {})
    return run_sync_for_extraction(
        synchronized_runtime=True,
        tick=tick,
        browser=extraction.get("browser_ir") or extraction.get("runtime"),
        merge_graph=False,
        **{k: v for k, v in kwargs.items() if k in ("memory_path", "memory_key")},
    )
