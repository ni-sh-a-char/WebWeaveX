from __future__ import annotations

from typing import Any, Dict

from core.ir.document_ir import compile_document_ir


def query_documents(text: str) -> Dict[str, Any]:
    ir = compile_document_ir(text)
    return {"ir": ir, "claims": ir.get("claims", []), "tutorial_steps": ir.get("tutorial_steps", []), "explainable": True}
