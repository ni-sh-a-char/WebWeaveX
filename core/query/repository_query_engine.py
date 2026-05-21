from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.ir.repository_ir import compile_repository_ir


def query_repository(source: str = "", path: str = "", files: Optional[List[str]] = None) -> Dict[str, Any]:
    ir = compile_repository_ir(source, path, files)
    return {"ir": ir, "evidence": ir.get("semantic_evidence", {}), "explainable": True, "bounded": True}
