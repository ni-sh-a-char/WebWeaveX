from __future__ import annotations

from typing import Any, Dict, List


MAX_SYNTHESIS = 10000


def synthesize_semantic_knowledge(
    records: List[Dict[str, Any]],
) -> Dict[str, Any]:

    synthesized = []

    for record in records[:MAX_SYNTHESIS]:

        synthesized.append(
            {
                "semantic_summary": sorted(
                    record.keys()
                ),
            }
        )

    return {
        "knowledge": synthesized,
        "bounded": True,
    }
