from __future__ import annotations

from typing import Any, Callable, Dict, List


MAX_PIPELINE_STAGES = 32


def run_semantic_pipeline_stages(
    stages: List[Callable[[Dict[str, Any]], Dict[str, Any]]],
    initial: Dict[str, Any],
) -> Dict[str, Any]:
    state = dict(initial)
    trace: List[str] = []
    for idx, stage in enumerate(stages[:MAX_PIPELINE_STAGES]):
        state = stage(state)
        trace.append(f"stage_{idx}")
    return {"state": state, "trace": trace, "deterministic": True, "bounded": len(trace) <= MAX_PIPELINE_STAGES}
