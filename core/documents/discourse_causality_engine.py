from __future__ import annotations

from typing import Any, Dict

from core.documents.explanation_graph_engine import build_explanation_graph


def model_discourse_causality(text: str) -> Dict[str, Any]:
    expl = build_explanation_graph(text)
    causal = [{"cause": e.get("from"), "effect": e.get("to")} for e in expl.get("explains", [])]
    return {"causal": causal, "evidence": expl.get("deterministic_inputs", [])}
