from __future__ import annotations

from core.evidence.reconciliation_evidence_engine import reconcile_evidence


def reconcile_semantic_evidence(claims: list):
    return reconcile_evidence(claims)
