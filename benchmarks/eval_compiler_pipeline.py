from __future__ import annotations

from typing import Any, Dict

from core.compiler import compile_semantic_pipeline


def eval_compiler_pipeline(case: Dict[str, Any]) -> Dict[str, Any]:
    r = compile_semantic_pipeline({"edges": case.get("edges", [])})
    steps = r.get("execution_plan", {}).get("steps", 0)
    return {
        "predicted": steps == case.get("expected_steps", 0),
        "actual": {"steps": steps},
        "expected": case.get("expected_steps"),
    }
