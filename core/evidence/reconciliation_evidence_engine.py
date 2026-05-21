from __future__ import annotations

from typing import Any, Dict, List


def reconcile_evidence(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_key: Dict[str, List[Dict[str, Any]]] = {}
    for claim in claims or []:
        if not isinstance(claim, dict):
            continue
        key = str(claim.get("key", claim.get("id", "")))
        by_key.setdefault(key, []).append(claim)
    reconciled = []
    conflicts = []
    for key, group in sorted(by_key.items()):
        values = sorted(set(str(c.get("value", "")) for c in group))
        if len(values) > 1:
            conflicts.append({"key": key, "values": values, "claims": len(group)})
        winner = values[0] if values else ""
        reconciled.append({"key": key, "value": winner, "claim_count": len(group)})
    return {
        "reconciled": reconciled,
        "conflicts": conflicts,
        "evidence": ["evidence_reconciliation"],
        "sources": sorted({str(c.get("source", "")) for g in by_key.values() for c in g if c.get("source")}),
        "grounding": {"method": "deterministic_lexicographic_winner"},
        "lineage": {"stage": "reconciliation"},
    }
