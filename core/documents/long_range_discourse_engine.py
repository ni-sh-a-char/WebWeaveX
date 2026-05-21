from __future__ import annotations

from typing import Any, Dict

from core.documents.document_semantic_ir_engine import build_document_semantic_ir


def analyze_long_range_discourse(text: str, max_span: int = 5000) -> Dict[str, Any]:
    bounded = (text or "")[:max_span]
    ir = build_document_semantic_ir(bounded)
    return {
        "ir": ir,
        "bounded_chars": len(bounded),
        "long_range_links": ir.get("coreference", {}).get("edges", [])[:50],
        "evidence": ir.get("evidence", []),
    }
