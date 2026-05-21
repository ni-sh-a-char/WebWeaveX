from __future__ import annotations

from typing import Any, Dict

from core.documents.rhetorical_structure_engine import extract_rhetorical_structure
from core.documents.argument_graph_engine import build_argument_graph


def parse_semantic_discourse(text: str) -> Dict[str, Any]:
    rhet = extract_rhetorical_structure(text)
    arg = build_argument_graph(text)
    return {
        "rhetorical": rhet,
        "argument": arg,
        "transitions": arg.get("edges", []),
        "deterministic_inputs": rhet.get("deterministic_inputs", []) + [f"args={len(arg.get('nodes', []))}"],
    }
