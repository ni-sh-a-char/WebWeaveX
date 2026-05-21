from __future__ import annotations

import ast
import re
from typing import Dict, List


def build_semantic_call_graph(text: str) -> Dict[str, List[dict]]:
    source = text or ""
    calls: List[dict] = []
    try:
        tree = ast.parse(source)
        func_stack: List[str] = []

        class Visitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # type: ignore[override]
                func_stack.append(node.name)
                self.generic_visit(node)
                func_stack.pop()

            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # type: ignore[override]
                func_stack.append(node.name)
                self.generic_visit(node)
                func_stack.pop()

            def visit_Call(self, node: ast.Call) -> None:  # type: ignore[override]
                caller = func_stack[-1] if func_stack else "<module>"
                callee = ""
                if isinstance(node.func, ast.Name):
                    callee = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    callee = node.func.attr
                if callee:
                    calls.append({"from": caller, "to": callee})
                self.generic_visit(node)

        Visitor().visit(tree)
    except SyntaxError:
        for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", source):
            name = m.group(1)
            if name not in {"if", "for", "while", "switch", "return"}:
                calls.append({"from": "<module>", "to": name})

    dedup = sorted({(c["from"], c["to"]) for c in calls})
    return {"calls": [{"from": f, "to": t} for f, t in dedup]}
