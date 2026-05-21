from __future__ import annotations

from typing import Any, Dict, List


MAX_OPTIMIZATION_PASSES = 10


def optimize_semantic_ir(
    ir: Dict[str, Any],
) -> Dict[str, Any]:

    optimizations: List[Dict[str, Any]] = []

    if "execution_paths" in ir:

        paths = ir["execution_paths"].get("paths", [])

        deduped = []

        seen = set()

        for p in paths:

            key = tuple(p)

            if key not in seen:
                deduped.append(p)
                seen.add(key)

        optimizations.append({
            "type": "deduplicate_execution_paths",
            "before": len(paths),
            "after": len(deduped),
        })

        ir["execution_paths"]["paths"] = deduped

    return {
        "optimized_ir": ir,
        "optimizations": optimizations[
            :MAX_OPTIMIZATION_PASSES
        ],
        "deterministic": True,
    }
