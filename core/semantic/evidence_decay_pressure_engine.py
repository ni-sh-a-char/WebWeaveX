from __future__ import annotations

from typing import Any, Dict


def compute_evidence_decay_pressure(evidence_count: int, min_evidence: int = 2) -> Dict[str, Any]:
    gap = max(0, min_evidence - evidence_count)
    return {"pressure": round(min(1.0, gap * 0.4), 3), "incomplete": gap > 0}
