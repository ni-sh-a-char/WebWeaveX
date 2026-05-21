from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.reconciliation_evidence_engine import reconcile_evidence


def resolve_semantic_claims(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    reconciled = reconcile_evidence(claims)
    resolved = {
        item["key"]: item["value"]
        for item in reconciled.get("reconciled", [])
        if isinstance(item, dict)
    }
    return {
        "resolved": resolved,
        "reconciliation": reconciled,
        "evidence": reconciled.get("evidence", []),
        "sources": reconciled.get("sources", []),
        "grounding": reconciled.get("grounding", {}),
        "lineage": reconciled.get("lineage", {}),
    }
