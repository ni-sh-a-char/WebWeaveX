from __future__ import annotations

from typing import Any, Dict

from core.memory.semantic_diff_engine import diff_semantic_ir


def detect_semantic_changes(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    diff = diff_semantic_ir(before, after)
    return {**diff, "has_changes": diff["change_count"] > 0}
