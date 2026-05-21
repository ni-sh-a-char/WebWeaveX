from __future__ import annotations

from typing import Any, Dict


def detect_recursive_submission(reconciled_eq_inferred: bool, depth: int, evidence_count: int) -> Dict[str, Any]:
    submission = reconciled_eq_inferred and depth >= 2 and evidence_count < 2
    return {"submission": submission, "suppress": submission}
