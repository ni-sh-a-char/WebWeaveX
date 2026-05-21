from __future__ import annotations

from typing import Dict, Any
from core.documents.section_engine import extract_sections
from core.documents.semantic_structure_engine import extract_structural_blocks
from core.documents.reference_engine import extract_references


def analyze_document(text: str) -> Dict[str, Any]:
    return {
        "sections": extract_sections(text),
        "structure": extract_structural_blocks(text),
        "references": extract_references(text),
    }
