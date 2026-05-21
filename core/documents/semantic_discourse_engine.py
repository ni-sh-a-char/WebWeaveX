from __future__ import annotations

from typing import Any, Dict

from core.documents.discourse_parser_engine import parse_discourse_structure
from core.evidence import structure_cognition


def analyze_semantic_discourse(text: str) -> Dict[str, Any]:
    structure = parse_discourse_structure(text)
    observed = {"lexical": structure["lexical"], "syntactic": structure["syntactic"]}
    inferred = {"discourse": structure["discourse"], "conceptual": structure["conceptual"]}
    return structure_cognition(observed, inferred, {"structure": structure})
