from __future__ import annotations

import ast
import re
from typing import Dict, List, Set

_LANG_PATTERNS = {
    "python": [r"\bdef\s+\w+\s*\(", r"\bclass\s+\w+\s*[:(]", r"\bimport\s+\w+"],
    "javascript": [r"\bfunction\s+\w+\s*\(", r"\bconst\s+\w+\s*=", r"\brequire\("],
    "typescript": [r"\binterface\s+\w+", r"\btype\s+\w+\s*=", r"\bimport\s+.+\sfrom\s+"],
    "java": [r"\bpublic\s+class\s+\w+", r"\bpackage\s+\w+[\w.]*\s*;"],
    "kotlin": [r"\bfun\s+\w+\s*\(", r"\bclass\s+\w+", r"\bimport\s+[\w.]+"],
    "dart": [r"\bimport\s+'package:", r"\bclass\s+\w+", r"\bvoid\s+main\s*\("],
    "go": [r"\bpackage\s+\w+", r"\bfunc\s+\w+\s*\("],
    "rust": [r"\bfn\s+\w+\s*\(", r"\buse\s+[\w:]+"],
}


def _sorted(values: Set[str]) -> List[str]:
    return sorted(v for v in values if v)


def extract_semantic_ast(text: str) -> Dict[str, List[str]]:
    source = text or ""
    languages: Set[str] = set()
    for lang, patterns in _LANG_PATTERNS.items():
        if any(re.search(p, source) for p in patterns):
            languages.add(lang)

    symbols: Set[str] = set()
    imports: Set[str] = set()
    classes: Set[str] = set()
    interfaces: Set[str] = set()
    traits: Set[str] = set()
    functions: Set[str] = set()
    methods: Set[str] = set()
    decorators: Set[str] = set()
    annotations: Set[str] = set()
    generics: Set[str] = set()
    exports: Set[str] = set()

    try:
        tree = ast.parse(source)
        languages.add("python")
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.add(node.name)
                symbols.add(node.name)
                decorators.update(ast.unparse(d) for d in node.decorator_list if hasattr(ast, "unparse"))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.add(node.name)
                symbols.add(node.name)
                decorators.update(ast.unparse(d) for d in node.decorator_list if hasattr(ast, "unparse"))
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                imports.add(mod)
                for alias in node.names:
                    symbols.add(alias.name)
    except SyntaxError:
        pass

    classes.update(re.findall(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)", source))
    interfaces.update(re.findall(r"\binterface\s+([A-Za-z_][A-Za-z0-9_]*)", source))
    traits.update(re.findall(r"\btrait\s+([A-Za-z_][A-Za-z0-9_]*)", source))
    functions.update(re.findall(r"\b(?:def|function|fun|fn)\s+([A-Za-z_][A-Za-z0-9_]*)", source))
    methods.update(re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*\)\s*\{", source))
    imports.update(re.findall(r"\bimport\s+([A-Za-z0-9_./:*'-]+)", source))
    imports.update(re.findall(r"\brequire\(['\"]([^'\"]+)['\"]\)", source))
    exports.update(re.findall(r"\bexport\s+(?:default\s+)?(?:class|function|const|let|var)?\s*([A-Za-z_][A-Za-z0-9_]*)", source))
    annotations.update(re.findall(r"@([A-Za-z_][A-Za-z0-9_]*)", source))
    generics.update(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*<([A-Za-z0-9_, ?]+)>", source))
    decorators.update(f"@{x}" for x in annotations)

    symbols.update(classes)
    symbols.update(interfaces)
    symbols.update(traits)
    symbols.update(functions)
    symbols.update(methods)

    return {
        "languages": _sorted(languages),
        "symbols": _sorted(symbols),
        "imports": _sorted(imports),
        "classes": _sorted(classes),
        "interfaces": _sorted(interfaces),
        "traits": _sorted(traits),
        "functions": _sorted(functions),
        "methods": _sorted(methods),
        "decorators": _sorted(decorators),
        "annotations": _sorted(annotations),
        "generics": _sorted(generics),
        "exports": _sorted(exports),
    }
