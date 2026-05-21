from __future__ import annotations

from typing import Any, Dict, List


def orchestrate_semantic_pipeline(steps: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
    from core.runtime.semantic_pipeline_runtime import run_semantic_pipeline

    return run_semantic_pipeline(steps, context)
