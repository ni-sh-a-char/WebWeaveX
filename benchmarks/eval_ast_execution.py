from __future__ import annotations

from typing import Any, Dict

from core.ast import compile_semantic_ast_ir


def eval_ast_execution(case: Dict[str, Any]) -> Dict[str, Any]:

    ir = compile_semantic_ast_ir(case["code"])

    predicted = ir["symbols"]["symbol_count"]

    expected = case["expected_symbols"]

    return {
        "predicted": predicted == expected,
        "expected_match": True,
    }
