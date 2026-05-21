from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.internet.probabilistic_trust_engine import compute_probabilistic_trust
from core.ir._base import empty_confidence, empty_lineage

InternetIR = Dict[str, Any]


def compile_internet_ir(url: str, html: str = "", claims: Optional[List[Dict[str, Any]]] = None) -> InternetIR:
    trust = compute_probabilistic_trust(url, corroboration_count=0, html_text=html, claims=claims)
    return {
        "url": url,
        "trust": trust,
        "evidence": trust.get("evidence", []),
        "lineage": empty_lineage("internet_ir"),
        "confidence": {"score": trust.get("trust_score", 0), "basis": trust.get("deterministic_inputs", []), "deterministic": True},
    }
