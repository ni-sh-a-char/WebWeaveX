from __future__ import annotations

from typing import Any, Dict


MAX_ADAPTATIONS = 1000


def adapt_semantic_runtime(
    runtime: Dict[str, Any],
) -> Dict[str, Any]:
    adaptations = []
    for idx, key in enumerate(
        sorted(runtime.keys())[:MAX_ADAPTATIONS]
    ):
        adaptations.append(
            {
                "key": key,
                "adaptation": "retain",
            }
        )
    return {
        "adaptations": adaptations,
        "adaptation_count": len(adaptations),
        "bounded": True,
    }
