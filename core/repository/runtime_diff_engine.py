from __future__ import annotations

from typing import Any, Dict

from core.memory.semantic_diff_engine import diff_semantic_ir


def diff_runtime_ir(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    return diff_semantic_ir(before, after)
