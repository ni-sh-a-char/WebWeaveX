from __future__ import annotations

from typing import Any, Dict, List


MAX_MUTATIONS = 1000


def trace_execution_mutations(
    transitions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    ordered = sorted(
        transitions,
        key=lambda x: (
            str(x.get("from")),
            str(x.get("to")),
        ),
    )[:MAX_MUTATIONS]
    mutations = [
        {
            "mutation_id": idx,
            "from": t.get("from"),
            "to": t.get("to"),
        }
        for idx, t in enumerate(ordered)
    ]
    return {
        "mutations": mutations,
        "mutation_count": len(mutations),
        "bounded": True,
    }
