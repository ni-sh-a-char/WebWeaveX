from __future__ import annotations

from typing import Any, Dict, List


def refuse_inference(reasons: List[str], evidence_count: int) -> Dict[str, Any]:
    return {
        "refused": True,
        "reasons": sorted(set(reasons)),
        "evidence_count": evidence_count,
        "message": "cannot_conclude" if evidence_count < 2 else "conclude_with_caution",
    }
