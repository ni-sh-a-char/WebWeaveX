from __future__ import annotations

from typing import Any, Dict, List

from core.semantic.ambiguity_preservation_engine import preserve_ambiguities


def reason_ambiguity(candidates: List[str], evidence: List[str]) -> Dict[str, Any]:
    preserved = preserve_ambiguities(candidates, evidence)
    return {
        "ambiguities": preserved.get("ambiguities", []),
        "preserved": preserved.get("preserved", False),
        "evidence": preserved.get("evidence", []),
        "lineage": preserved.get("lineage", {}),
        "competing_interpretations": preserved.get("ambiguities", []),
    }
