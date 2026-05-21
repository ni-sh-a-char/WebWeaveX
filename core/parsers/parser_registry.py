from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from .ast_engine import parse_ast
from .call_graph_engine import build_call_graph
from .dependency_resolution_engine import resolve_dependencies
from .import_resolution_engine import resolve_imports
from .parser_budget_engine import ParserBudget, enforce_budget
from .parser_recovery_engine import recover_syntax
from .runtime_resolution_engine import resolve_runtime
from .api_resolution_engine import resolve_api_surface
from .framework_resolution_engine import resolve_frameworks
from .semantic_graph_engine import build_semantic_graph
from .symbol_resolution_engine import resolve_symbols
from .parser_output_engine import normalize_parser_output
from .formal_parser_grounding_engine import require_parser_evidence

_EXTENSION_LANGUAGE = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".kt": "kotlin",
    ".go": "go",
    ".rs": "rust",
    ".dart": "dart",
}


class ParserRegistry:
    @staticmethod
    def detect_language(path: str = "", hint: str = "") -> str:
        if hint:
            return hint.lower()
        ext = Path(path).suffix.lower()
        return _EXTENSION_LANGUAGE.get(ext, "text")

    @staticmethod
    def parse(
        source: str,
        path: str = "",
        language_hint: str = "",
        budget: Optional[ParserBudget] = None,
    ) -> Dict[str, object]:
        language = ParserRegistry.detect_language(path=path, hint=language_hint)
        bounded = enforce_budget(source, budget)
        recovered = recover_syntax(bounded, language)
        ast_tree = parse_ast(recovered, language)
        symbols = resolve_symbols(recovered, language, ast_tree=ast_tree)
        calls = build_call_graph(recovered, language)
        imports = resolve_imports(symbols, source_id=path or language)
        deps = resolve_dependencies(recovered, path=path)
        runtime = resolve_runtime(
            deps.get("dependencies", []),
            symbols.get("imports", []),
        )
        frameworks = resolve_frameworks(
            deps.get("dependencies", []),
            symbols.get("imports", []),
            symbols.get("decorators"),
        )
        api_surface = resolve_api_surface(recovered, language, path=path)
        parsed = {
            "language": language,
            "source_id": path or language,
            "ast": ast_tree,
            "symbols": symbols,
            "calls": calls,
            "imports": imports,
            "dependencies": deps,
            "runtime": runtime,
            "frameworks": frameworks,
            "api_surface": api_surface,
        }
        parsed["semantic_graph"] = build_semantic_graph(parsed)
        parsed["evidence"] = {
            "ast": bool(ast_tree.get("nodes")),
            "symbols": bool(symbols.get("symbols")),
            "calls": bool(calls.get("calls")),
            "dependencies": bool(deps.get("dependencies")),
            "tree_sitter": language != "python" and not ast_tree.get("parse_error"),
        }
        if ast_tree.get("parse_error"):
            parsed["evidence"]["parse_error"] = True
        normalized = normalize_parser_output(parsed)
        parsed.update(normalized)
        parsed["parser_grounding"] = require_parser_evidence(parsed)
        return parsed


def parse_source(
    source: str,
    path: str = "",
    language_hint: str = "",
    budget: Optional[ParserBudget] = None,
) -> Dict[str, object]:
    return ParserRegistry.parse(source=source, path=path, language_hint=language_hint, budget=budget)
