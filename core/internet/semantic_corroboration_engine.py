from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.corroboration_engine import corroborate_sources


def analyze_semantic_agreement(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    corroboration = corroborate_sources(claims)
    agreed = [c for c in corroboration.get("corroborated", []) if c.get("agreement")]
    return {
        "corroborated": corroboration.get("corroborated", []),
        "agreement_count": len(agreed),
        "evidence": ["semantic_corroboration"],
        "lineage": {"stage": "corroboration", "claims": len(claims or [])},
    }
