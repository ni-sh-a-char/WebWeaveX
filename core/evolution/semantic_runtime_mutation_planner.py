from __future__ import annotations

from typing import Any, Dict


MAX_MUTATIONS = 1000


def plan_runtime_mutation(
    runtime: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "mutation_candidates": sorted(
            runtime.keys()
        )[:MAX_MUTATIONS],
        "bounded": True,
    }
