from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.reconciliation_evidence_engine import reconcile_evidence
from core.semantic.contradiction_preservation_engine import preserve_contradictions


def resolve_contradictions_without_collapse(snippets: List[str]) -> Dict[str, Any]:
    preserved = preserve_contradictions(snippets)
    reconciliation = reconcile_evidence(
        [{"key": "conflict", "value": str(i), "source": f"snippet:{i}"} for i in range(len(snippets or []))]
    )
    return {
        **preserved,
        "resolution": reconciliation,
        "collapsed": False,
        "preserved_interpretations": preserved.get("conflicting_claims", []),
    }
