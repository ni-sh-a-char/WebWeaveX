from __future__ import annotations

from typing import Any, Dict, List


def build_support(evidence: List[str], extra: List[str] | None = None) -> Dict[str, Any]:
    items = sorted(set(str(e) for e in (evidence or []) + (extra or []) if e))
    return {
        "supporting_evidence": items,
        "support_count": len(items),
        "support_strength": round(min(1.0, 0.15 + len(items) * 0.1), 3),
    }
