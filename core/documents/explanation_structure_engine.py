from __future__ import annotations

from typing import Any, Dict

from core.documents.discourse_causality_engine import model_discourse_causality
from core.documents.argument_semantics_engine import analyze_argument_semantics


def build_explanation_structure(text: str) -> Dict[str, Any]:
    causal = model_discourse_causality(text)
    args = analyze_argument_semantics(text)
    return {
        "explanation_causal": causal.get("causal", []),
        "argument": args,
        "layers": ["lexical", "syntactic", "semantic", "rhetorical", "argumentative"],
    }
