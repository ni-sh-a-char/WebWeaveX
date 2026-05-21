from __future__ import annotations

import ast
import re
from typing import Any, Dict


def _py_ast(src: str):
    out = {"symbols": [], "imports": [], "classes": [], "functions": []}
    try:
        tree = ast.parse(src)
    except Exception:
        return out
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            out["imports"].extend([a.name for a in n.names])
        elif isinstance(n, ast.ImportFrom):
            if n.module:
                out["imports"].append(n.module)
        elif isinstance(n, ast.ClassDef):
            out["classes"].append(n.name)
            out["symbols"].append(n.name)
        elif isinstance(n, ast.FunctionDef):
            out["functions"].append(n.name)
            out["symbols"].append(n.name)
    for k in out:
        out[k] = sorted(set(out[k]))
    return out


def _js_like(src: str):
    classes = sorted(set(re.findall(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)", src)))
    funcs = sorted(set(re.findall(r"\bfunction\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", src)))
    imports = sorted(set(re.findall(r"""import\s+.*?from\s+['"]([^'"]+)['"]""", src)))
    interfaces = sorted(set(re.findall(r"\binterface\s+([A-Za-z_][A-Za-z0-9_]*)", src)))
    symbols = sorted(set(classes + funcs + interfaces))
    return {"symbols": symbols, "imports": imports, "classes": classes, "functions": funcs, "interfaces": interfaces}


def _java_kotlin(src: str):
    imports = sorted(set(re.findall(r"\bimport\s+([A-Za-z0-9_.]+)", src)))
    classes = sorted(set(re.findall(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)", src)))
    funcs = sorted(
        set(re.findall(r"\b(?:fun|void|public|private|protected|static)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", src))
    )
    interfaces = sorted(set(re.findall(r"\binterface\s+([A-Za-z_][A-Za-z0-9_]*)", src)))
    symbols = sorted(set(classes + funcs + interfaces))
    return {"symbols": symbols, "imports": imports, "classes": classes, "functions": funcs, "interfaces": interfaces}


def extract_repository_ast(text: str) -> Dict[str, Any]:
    src = text or ""
    py = _py_ast(src)
    js = _js_like(src)
    jv = _java_kotlin(src)
    languages = []
    if py["imports"] or "def " in src:
        languages.append("python")
    if js["imports"] or "function " in src or "class " in src:
        languages.append("javascript_typescript")
    if jv["imports"]:
        languages.append("java_kotlin")
    return {
        "languages": sorted(set(languages)),
        "symbols": sorted(set(py["symbols"] + js["symbols"] + jv["symbols"])),
        "imports": sorted(set(py["imports"] + js["imports"] + jv["imports"])),
        "classes": sorted(set(py["classes"] + js["classes"] + jv["classes"])),
        "functions": sorted(set(py["functions"] + js["functions"] + jv["functions"])),
        "interfaces": sorted(set(js["interfaces"] + jv["interfaces"])),
    }

