from __future__ import annotations

from typing import Any, Dict

from .python_ast_engine import parse_python_ast
from .symbol_resolution_engine import resolve_symbols
from .control_flow_engine import build_control_flow_graph
from .execution_path_engine import reconstruct_execution_paths


def compile_semantic_ast_ir(code: str) -> Dict[str, Any]:

    ast_ir = parse_python_ast(code)

    symbols = resolve_symbols(ast_ir)

    cfg = build_control_flow_graph(ast_ir)

    execution_paths = reconstruct_execution_paths(cfg)

    return {
        "ast": ast_ir,
        "symbols": symbols,
        "control_flow_graph": cfg,
        "execution_paths": execution_paths,
        "semantic_grounded": True,
        "deterministic": True,
    }
