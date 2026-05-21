from __future__ import annotations

import ast
import re
from typing import Any, Dict, List, Set


def resolve_symbols(source: str, language: str, ast_tree: Dict[str, Any] | None = None) -> Dict[str, List[str]]:
    lang = (language or "text").lower()
    src = source or ""
    classes: Set[str] = set()
    functions: Set[str] = set()
    methods: Set[str] = set()
    interfaces: Set[str] = set()
    traits: Set[str] = set()
    imports: Set[str] = set()
    exports: Set[str] = set()
    decorators: Set[str] = set()

    if lang == "python":
        try:
            tree = ast.parse(src)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.add(node.name)
                    for dec in node.decorator_list:
                        if isinstance(dec, ast.Name):
                            decorators.add(dec.id)
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    functions.add(node.name)
                    for dec in node.decorator_list:
                        if isinstance(dec, ast.Name):
                            decorators.add(dec.id)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                        if alias.asname:
                            exports.add(alias.asname)
                elif isinstance(node, ast.ImportFrom):
                    mod = node.module or ""
                    imports.add(mod)
                    for alias in node.names:
                        name = alias.name
                        if name == "*":
                            exports.add(f"{mod}.*")
                        else:
                            exports.add(alias.asname or name)
        except SyntaxError:
            pass

    if lang != "python" or not classes:
        interfaces.update(re.findall(r"\binterface\s+([A-Za-z_][A-Za-z0-9_]*)", src))
        traits.update(re.findall(r"\btrait\s+([A-Za-z_][A-Za-z0-9_]*)", src))
        classes.update(re.findall(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)", src))
        functions.update(
            re.findall(r"\b(?:def|function|fun|fn)\s+([A-Za-z_][A-Za-z0-9_]*)", src)
        )
        methods.update(re.findall(r"\b(?:public|private|protected)?\s*\w+\s+(\w+)\s*\(", src))

    symbols = classes | functions | methods | interfaces | traits
    return {
        "classes": sorted(classes),
        "functions": sorted(functions),
        "methods": sorted(methods),
        "interfaces": sorted(interfaces),
        "traits": sorted(traits),
        "imports": sorted(i for i in imports if i),
        "exports": sorted(exports),
        "decorators": sorted(decorators),
        "symbols": sorted(symbols),
    }
