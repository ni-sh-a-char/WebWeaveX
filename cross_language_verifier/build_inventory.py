"""Phase 1-2: zero-trust inventory + API parity matrix.

Extracts the public API surface from source (no reports trusted):
- Python: ast-parse webweavex/__init__.py __all__ + core/ module/function census
- JavaScript: parse src/index.ts export statements + src/ census
- Dart: parse lib/webweavex.dart export/show directives + lib/ census

Emits inventory_python.json, inventory_javascript.json, inventory_dart.json,
api_parity_matrix.json. camelCase and snake_case are unified for comparison.
"""
import ast
import json
import re
import sys
from pathlib import Path

PY_ROOT = Path(r"C:\Projects\wwx_cert_py")
JS_ROOT = Path(r"C:\Projects\wwx_cert_js")
DART_ROOT = Path(r"C:\Projects\WebWeaveX")


def camel_to_snake(name: str) -> str:
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def python_inventory():
    init = PY_ROOT / "webweavex" / "__init__.py"
    tree = ast.parse(init.read_text(encoding="utf-8"))
    public = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "__all__":
                    public = [ast.literal_eval(e) for e in node.value.elts]
    modules, functions, classes = [], 0, 0
    for p in sorted((PY_ROOT / "core").rglob("*.py")):
        if "__pycache__" in p.parts:
            continue
        modules.append(str(p.relative_to(PY_ROOT)).replace("\\", "/"))
        try:
            t = ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        functions += sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(t))
        classes += sum(isinstance(n, ast.ClassDef) for n in ast.walk(t))
    return {"public_api": sorted(public), "modules": len(modules), "functions": functions,
            "classes": classes, "module_list": modules}


def _js_exports_of(path, seen):
    """Names exported by a TS module, resolving `export *` recursively."""
    if path in seen or not path.exists():
        return set()
    seen.add(path)
    text = path.read_text(encoding="utf-8")
    names = set()
    for m in re.finditer(r"export\s*\{([^}]*)\}", text, re.S):
        for part in m.group(1).split(","):
            part = part.strip()
            if not part:
                continue
            part = re.sub(r"^type\s+", "", part)
            name = part.split(" as ")[-1].strip() if " as " in part else part.split()[0]
            if name:
                names.add(name)
    for m in re.finditer(r"export\s+(?:async\s+)?(?:function|const|class|let|interface|type|enum)\s+(\w+)", text):
        names.add(m.group(1))
    for m in re.finditer(r"export\s*\*\s*from\s*[\"']([^\"']+)[\"']", text):
        rel = m.group(1).replace(".js", ".ts")
        target = (path.parent / rel).resolve()
        if target.is_dir() or not target.suffix:
            target = Path(str(target) + ".ts")
        names |= _js_exports_of(target, seen)
    return names


def js_inventory():
    names = _js_exports_of(JS_ROOT / "src" / "index.ts", set())
    modules, functions = [], 0
    for p in sorted((JS_ROOT / "src").rglob("*.ts")):
        modules.append(str(p.relative_to(JS_ROOT)).replace("\\", "/"))
        t = p.read_text(encoding="utf-8")
        functions += len(re.findall(r"^export\s+(?:async\s+)?function\s+\w+", t, re.M))
    return {"public_api": sorted(names), "modules": len(modules),
            "exported_functions": functions, "module_list": modules}


_DART_DECL = re.compile(
    r"^(?:class|enum|mixin|extension|typedef)\s+(\w+)"
    r"|^(?:const|final|var)\s+(?:\w[\w<>, ?]*\s+)?(\w+)\s*=",
    re.M,
)
_DART_FN = re.compile(
    r"^(?!//)(?:[A-Za-z_][\w<>,\[\]\(\) ?]*?)\s(\w+)\s*(?:<[^>]*>)?\([^;]*?\)\s*"
    r"(?:async\*?\s*)?(?:=>|\{)",
    re.M,
)


def _dart_top_level_names(path):
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    names = set()
    for m in _DART_DECL.finditer(text):
        n = m.group(1) or m.group(2)
        if n and not n.startswith("_"):
            names.add(n)
    for m in _DART_FN.finditer(text):
        n = m.group(1)
        if n and not n.startswith("_") and n not in ("if", "for", "while", "switch", "catch", "return"):
            names.add(n)
    return names


def dart_inventory():
    lib = DART_ROOT / "lib" / "webweavex.dart"
    text = lib.read_text(encoding="utf-8")
    names = set()
    for m in re.finditer(r"export\s+'([^']+)'\s*(?:show\s+([^;]+))?;", text, re.S):
        if m.group(2):
            for n in m.group(2).split(","):
                n = n.strip()
                if n:
                    names.add(n)
        else:
            names |= _dart_top_level_names(DART_ROOT / "lib" / m.group(1))
    modules, functions = [], 0
    for p in sorted((DART_ROOT / "lib").rglob("*.dart")):
        modules.append(str(p.relative_to(DART_ROOT)).replace("\\", "/"))
        t = p.read_text(encoding="utf-8")
        functions += len(re.findall(r"^(?:[A-Za-z_<>,\s\?\(\)\[\]]+?)\s(\w+)\(.*\)\s*(?:async\s*)?\{", t, re.M))
    return {"public_api": sorted(names), "modules": len(modules), "module_list": modules}


def main():
    py = python_inventory()
    js = js_inventory()
    da = dart_inventory()
    json.dump(py, open("inventory_python.json", "w", encoding="utf-8"), indent=1)
    json.dump(js, open("inventory_javascript.json", "w", encoding="utf-8"), indent=1)
    json.dump(da, open("inventory_dart.json", "w", encoding="utf-8"), indent=1)

    py_keys = {camel_to_snake(n): n for n in py["public_api"]}
    js_keys = {camel_to_snake(n): n for n in js["public_api"]}
    da_keys = {camel_to_snake(n): n for n in da["public_api"]}
    all_keys = sorted(set(py_keys) | set(js_keys) | set(da_keys))
    matrix = []
    full = missing_dart = missing_js = missing_py = 0
    for k in all_keys:
        row = {"api": k, "python": py_keys.get(k), "javascript": js_keys.get(k), "dart": da_keys.get(k)}
        row["parity"] = "FULL" if all([row["python"], row["javascript"], row["dart"]]) else "PARTIAL"
        if row["parity"] == "FULL":
            full += 1
        if not row["dart"]:
            missing_dart += 1
        if not row["javascript"]:
            missing_js += 1
        if not row["python"]:
            missing_py += 1
        matrix.append(row)
    summary = {"total_apis": len(all_keys), "full_parity": full,
               "missing_in_dart": missing_dart, "missing_in_javascript": missing_js,
               "missing_in_python": missing_py,
               "python_public": len(py["public_api"]), "js_public": len(js["public_api"]),
               "dart_public": len(da["public_api"])}
    json.dump({"summary": summary, "matrix": matrix},
              open("api_parity_matrix.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
