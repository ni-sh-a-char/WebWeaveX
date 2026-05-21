from __future__ import annotations

from typing import Any, Dict, List

from core.documents.semantic_section_reconstruction_engine import reconstruct_semantic_sections
from core.evidence import structure_cognition


def reconstruct_semantic_dependencies(text: str) -> Dict[str, Any]:
    sections = reconstruct_semantic_sections(text)
    deps: List[Dict[str, str]] = sections.get("inferred", {}).get("semantic", {}).get("explains", [])
    support = [{"from": d["from"], "to": d["to"], "relation": "explains"} for d in deps if isinstance(d, dict)]
    extends = [{"from": d["to"], "to": d["from"], "relation": "extends"} for d in deps if isinstance(d, dict)]
    observed = {"section_count": len(sections.get("reconciled", {}).get("sections", []))}
    inferred = {"dependencies": support, "extensions": extends}
    reconciled = {"semantic_dependencies": support + extends}
    return structure_cognition(observed, inferred, reconciled, parsed=None)
