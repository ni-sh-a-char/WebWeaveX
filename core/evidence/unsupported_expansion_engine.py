from __future__ import annotations

from typing import Any, Dict, List


def detect_unsupported_expansion(
    evidence: List[str],
    expansion_type: str,
    count: int,
) -> Dict[str, Any]:
    suppressed = count > 0 and len(evidence) < 2
    return {
        "expansion_type": expansion_type,
        "count": count,
        "suppressed": suppressed,
        "unsupported_expansions": [f"{expansion_type}:{i}" for i in range(count)] if suppressed else [],
        "reason": "insufficient_evidence" if suppressed else "allowed",
    }
