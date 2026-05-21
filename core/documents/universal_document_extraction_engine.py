from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.documents.document_structure_engine import (
    build_document_structure,
)
from core.documents.document_hierarchy_engine import (
    build_document_hierarchy,
)
from core.documents.citation_extraction_engine import (
    extract_citations,
)
from core.documents.reference_extraction_engine import (
    extract_references,
)
from core.documents.document_table_engine import (
    extract_document_tables,
)
from core.knowledge.document_knowledge_graph_engine import (
    build_document_knowledge_graph,
)
from core.presentation.presentation_extraction_engine import (
    extract_presentation_structure,
)
from core.spreadsheets.spreadsheet_extraction_engine import (
    extract_spreadsheet_structure,
)
from core.ir.document_runtime_ir import (
    compile_document_runtime_ir,
)


def extract_document_runtime(
    text: str,
    slides: Optional[List[Dict[str, Any]]] = None,
    workbook: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    structure = build_document_structure(
        text,
    )

    hierarchy = build_document_hierarchy(
        structure,
    )

    citations = extract_citations(
        text,
    )

    references = extract_references(
        structure,
    )

    tables = extract_document_tables(
        text,
    )

    knowledge_graph = build_document_knowledge_graph(
        structure,
    )

    slide_payload = extract_presentation_structure(
        slides or [],
    )

    worksheet_payload = extract_spreadsheet_structure(
        workbook or {},
    )

    document_ir = compile_document_runtime_ir(
        structure=structure,
        hierarchy=hierarchy,
        citations=citations,
        references=references,
        tables=tables,
        knowledge_graph=knowledge_graph,
        slides=slide_payload,
        worksheets=worksheet_payload,
    )

    return {
        "structure": structure,
        "hierarchy": hierarchy,
        "citations": citations,
        "references": references,
        "tables": tables,
        "slides": slide_payload,
        "worksheets": worksheet_payload,
        "knowledge_graph": knowledge_graph,
        "document_ir": document_ir,
        "bounded": True,
    }
