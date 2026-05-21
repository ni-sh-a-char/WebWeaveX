from __future__ import annotations

from typing import Any, Dict, List


MAX_MUTATIONS = 1000


def build_mutation_lineage(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    keys = sorted(runtime_ir.keys())[:MAX_MUTATIONS]
    lineage = [
        {
            "step": idx,
            "key": key,
            "causal_action": "observe",
        }
        for idx, key in enumerate(keys)
    ]
    return {
        "mutation_lineage": lineage,
        "bounded": True,
    }
