from __future__ import annotations

from typing import Any, Dict

from core.ir.repository_ir import compile_repository_ir
from core.repository.runtime_state_engine import model_runtime_state


def reason_runtime_semantic(source: str, path: str = "") -> Dict[str, Any]:
    ir = compile_repository_ir(source, path)
    state = model_runtime_state(source, path)
    return {"ir": ir, "state": state, "evidence": ir.get("semantic_evidence", {}), "explainable": True}
