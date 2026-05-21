from __future__ import annotations

import ast
import re
from typing import Dict, List, Set, Tuple


def build_call_graph(source: str, language: str) -> Dict[str, List[dict]]:
    lang = (language or "text").lower()
    src = source or ""
    calls: List[dict] = []

    if lang == "python":
        try:
            tree = ast.parse(src)
            fn_stack: List[str] = []

            class Visitor(ast.NodeVisitor):
                def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                    fn_stack.append(node.name)
                    self.generic_visit(node)
                    fn_stack.pop()

                def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
                    fn_stack.append(node.name)
                    self.generic_visit(node)
                    fn_stack.pop()

                def visit_Call(self, node: ast.Call) -> None:
                    caller = fn_stack[-1] if fn_stack else "<module>"
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
            pass

    if not calls and lang != "python":
        skip = {"if", "for", "while", "switch", "return", "new", "typeof"}
        for match in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", src):
            name = match.group(1)
            if name not in skip:
                calls.append({"from": "<module>", "to": name})

    uniq: Set[Tuple[str, str]] = {(c["from"], c["to"]) for c in calls}
    ordered = sorted(uniq, key=lambda x: (x[0], x[1]))
    return {"calls": [{"from": f, "to": t} for f, t in ordered]}
