from __future__ import annotations

from typing import Any, Dict, List


MAX_DISTILLED = 5000


def distill_semantic_knowledge(
    records: List[Dict[str, Any]],
) -> Dict[str, Any]:

    distilled = []

    for record in records[:MAX_DISTILLED]:

        distilled.append(
            sorted(record.keys())
        )

    return {
        "distilled": distilled,
        "bounded": True,
    }
