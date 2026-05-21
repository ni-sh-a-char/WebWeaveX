from __future__ import annotations

from typing import Any, Dict

from core.ir.document_ir import compile_document_ir
from core.documents.long_range_discourse_engine import analyze_long_range_discourse


def reason_discourse_semantic(text: str) -> Dict[str, Any]:
    ir = compile_document_ir(text)
    long_range = analyze_long_range_discourse(text)
    return {"ir": ir, "long_range": long_range, "explainable": True}
