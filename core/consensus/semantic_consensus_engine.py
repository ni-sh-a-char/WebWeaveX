from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


def compute_semantic_consensus(
    votes: List[
        Dict[str, Any]
    ],
) -> Dict[str, Any]:

    counter: Dict[
        str,
        int,
    ] = {}

    for vote in votes:

        value = str(
            vote.get("value")
        )

        counter[value] = (
            counter.get(value, 0)
            + 1
        )

    if not counter:

        return {
            "consensus": None,
        }

    ordered = sorted(
        counter.items(),
        key=lambda item: (
            -item[1],
            item[0],
        ),
    )

    return {
        "consensus": ordered[0][0],
        "votes": ordered,
    }
