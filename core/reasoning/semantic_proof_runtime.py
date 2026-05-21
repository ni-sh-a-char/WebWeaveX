from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.semantic_proof_engine import prove_semantic_claim


def prove_semantic_claim_runtime(claim: str, evidence: List[str]) -> Dict[str, Any]:
    return prove_semantic_claim(claim, evidence)
