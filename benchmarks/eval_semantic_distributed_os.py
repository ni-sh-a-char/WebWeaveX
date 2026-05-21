from __future__ import annotations

from typing import Any
from typing import Dict

from core.consensus.semantic_consensus_engine import (
    compute_semantic_consensus,
)


def eval_semantic_distributed_os(
    case: Dict[str, Any],
) -> Dict[str, Any]:

    r = compute_semantic_consensus(
        case["votes"]
    )

    return {
        "predicted": (
            r["consensus"]
            == "stable"
        ),
        "expected_match": True,
    }
