from __future__ import annotations

from typing import Any, Dict

from core.documents.argument_graph_engine import build_argument_graph
from core.documents.semantic_transition_engine import model_semantic_transitions


def build_semantic_discourse_graph(text: str) -> Dict[str, Any]:
    arg = build_argument_graph(text)
    trans = model_semantic_transitions(text)
    return {
        "nodes": arg.get("nodes", []),
        "edges": arg.get("edges", []) + trans.get("transitions", []),
        "evidence": ["discourse:argument", "discourse:transition"],
    }
