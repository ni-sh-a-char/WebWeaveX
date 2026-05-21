from __future__ import annotations

from typing import Any, Dict


def compute_evidence_boundary_pressure(evidence_count: int, min_evidence: int = 2) -> Dict[str, Any]:
    gap = max(0, min_evidence - evidence_count)
    pressure = round(min(1.0, gap * 0.35), 3)
    return {"pressure": pressure, "violation": gap > 0, "gap": gap}
