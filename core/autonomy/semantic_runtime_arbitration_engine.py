from __future__ import annotations

from typing import Any, Dict, List


def arbitrate_semantic_runtime(
    runtimes: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        runtimes,
        key=lambda x: (
            int(x.get("priority", 0)),
            str(x.get("id")),
        ),
    )

    chosen = ordered[0] if ordered else {}

    return {
        "selected_runtime": chosen,
        "runtime_count": len(ordered),
    }
