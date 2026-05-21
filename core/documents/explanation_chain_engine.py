from __future__ import annotations

from typing import Any, Dict

from core.documents.semantic_section_reconstruction_engine import reconstruct_semantic_sections
from core.evidence import structure_cognition


def build_explanation_chains(text: str) -> Dict[str, Any]:
    sections = reconstruct_semantic_sections(text)
    chains = sections.get("reconciled", {}).get("structure", {}).get("explains", [])
    observed = {"section_structure": sections.get("observed", {})}
    inferred = {"chains": chains}
    reconciled = {"what_explains_what": chains}
    return structure_cognition(observed, inferred, reconciled, parsed=None)
