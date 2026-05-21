from __future__ import annotations

from typing import Any, Dict, Optional


def compile_document_runtime_ir(
    structure: Dict[str, Any],
    hierarchy: Dict[str, Any],
    citations: Dict[str, Any],
    references: Dict[str, Any],
    tables: Dict[str, Any],
    knowledge_graph: Dict[str, Any],
    slides: Optional[Dict[str, Any]] = None,
    worksheets: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    slides = slides or {"slides": [], "bounded": True}
    worksheets = worksheets or {"worksheets": [], "bounded": True}

    return {
        "ir": "document_runtime",
        "document_structure": structure,
        "sections": structure.get("sections", []),
        "hierarchy": hierarchy,
        "tables": tables,
        "slides": slides,
        "worksheets": worksheets,
        "citations": citations,
        "references": references,
        "knowledge_graph": knowledge_graph,
        "structure": structure,
        "bounded": True,
    }
