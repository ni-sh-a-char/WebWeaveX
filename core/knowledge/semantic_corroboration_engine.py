from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.corroboration_engine import corroborate_sources


def corroborate_knowledge(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    result = corroborate_sources(claims)
    agreed = sum(1 for c in result.get("corroborated", []) if c.get("agreement"))
    return {
        "corroboration": result,
        "agreement_count": agreed,
        "evidence": ["knowledge_corroboration"],
        "lineage": {"stage": "knowledge_corroboration", "claims": len(claims or [])},
        "deterministic_inputs": [f"claims={len(claims or [])}", f"agreed={agreed}"],
    }
