from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


def coordinate_transactions(
    transactions: List[
        Dict[str, Any]
    ],
) -> Dict[str, Any]:

    committed = []

    for tx in transactions:

        committed.append({
            "id": tx.get("id"),
            "committed": True,
        })

    return {
        "transactions": committed,
    }
