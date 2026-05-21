from __future__ import annotations

from typing import Any, Dict, List

from core.documents.discourse_parser_engine import parse_discourse_structure


def extract_argument_structure(text: str) -> Dict[str, Any]:
    """Map headings to claim/support roles deterministically."""
    structure = parse_discourse_structure(text)
    headings = structure["discourse"].get("headings", [])
    claims: List[Dict[str, str]] = []
    for i, h in enumerate(headings):
        role = "claim" if i == 0 else "support"
        claims.append({"heading": h, "role": role})
    return {
        "claims": claims,
        "structure_type": "heading_argument",
        "deterministic_inputs": [f"claims={len(claims)}"],
    }
