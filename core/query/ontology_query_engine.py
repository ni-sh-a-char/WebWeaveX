from __future__ import annotations

from typing import Any, Dict, List

from core.ir.knowledge_ir import compile_knowledge_ir


def query_knowledge(entities: List[str], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    ir = compile_knowledge_ir(entities, edges)
    return {"ir": ir, "relations": ir.get("relations", []), "contradictions": ir.get("contradictions", []), "explainable": True}
