#!/usr/bin/env python3
"""AST-based Python (core/) → Dart (lib/src/) port."""
from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "lib" / "src"
MANIFEST = ROOT / "tools" / "convergence" / "manifest_py.txt"


def snake(s: str) -> str:
    return s  # preserve snake_case filenames in Dart


def py_path_to_dart(py_path: str) -> str:
    rel = py_path.removeprefix("core/")
    parts = rel.split("/")
    fname = parts.pop()
    base = fname.replace(".py", "")
    dart_name = f"{base}.dart" if base != "__init__" else "index.dart"
    return "/".join(parts + [dart_name]) if parts else dart_name


def git_show(py_path: str) -> str | None:
    r = subprocess.run(
        ["git", "show", f"origin/python:{py_path}"],
        cwd=ROOT,
        capture_output=True,
    )
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8-sig", errors="replace")


def load_manifest() -> list[str]:
    r = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "origin/python", "--", "core/"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    MANIFEST.write_text(r.stdout, encoding="utf-8")
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip().endswith(".py")]


class DartEmitter:
    def __init__(self, py_path: str, dart_rel: str) -> None:
        self.py_path = py_path
        self.dart_rel = dart_rel.replace("\\", "/")
        self.dart_dir = str(Path(dart_rel).parent).replace("\\", "/")
        self.imports: list[str] = []
        self.body: list[str] = []

    def rel_import(self, mod_parts: list[str]) -> str:
        target = Path("lib/src") / Path(*mod_parts)
        from_dir = Path("lib/src") / self.dart_dir if self.dart_dir not in (".", "") else Path("lib/src")
        rel = os.path.relpath(target, from_dir).replace("\\", "/")
        if not rel.startswith("."):
            rel = "./" + rel
        base = mod_parts[-1]
        file = "index.dart" if base == "__init__" else f"{base}.dart"
        return f"{rel}/{file}"

    def emit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef, indent: int, in_class: bool) -> list[str]:
        pad = "  " * indent
        name = node.name if in_class or node.name.startswith("_") else node.name
        params = []
        for a in node.args.args:
            if a.arg in ("self", "cls"):
                continue
            params.append(f"{a.arg}")
        ret = "Future<dynamic>" if isinstance(node, ast.AsyncFunctionDef) else "dynamic"
        export = "" if in_class or node.name.startswith("_") else ""
        lines = [f"{pad}{export}{'static ' if in_class and export == '' else ''}dynamic {name}({', '.join(params)}) {{"]
        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                val = "null" if stmt.value is None else "/* expr */"
                lines.append(f"{pad}  return {val};")
            elif isinstance(stmt, ast.Pass):
                lines.append(f"{pad}  // pass")
        lines.append(f"{pad}}}")
        return lines

    def convert(self, source: str) -> str:
        tree = ast.parse(source)
        if self.py_path.endswith("__init__.py"):
            lines = [f"// Barrel from {self.py_path}", ""]
            for node in tree.body:
                if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("core."):
                    mod = node.module.split(".")[-1]
                    for alias in node.names:
                        if alias.name != "*":
                            lines.append(f"export '{mod}/{alias.name}.dart';")
            return "\n".join(lines) + "\n"

        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("core."):
                parts = node.module.split(".")[1:]
                self.imports.append(f"import '{self.rel_import(parts)}';")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.body.extend(self.emit_function(node, 0, False))
            elif isinstance(node, ast.ClassDef):
                self.body.append(f"class {node.name} {{")
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        self.body.extend(self.emit_function(item, 1, True))
                self.body.append("}")

        header = [
            f"// Converted from Python: {self.py_path}",
            "// @generated",
            "",
            *self.imports,
            "",
        ]
        return "\n".join(header + self.body) + "\n"


def main() -> int:
    manifest = load_manifest()
    LIB.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    for i, py_path in enumerate(manifest, 1):
        src = git_show(py_path)
        if src is None:
            fail += 1
            continue
        dart_rel = py_path_to_dart(py_path)
        out_path = LIB / dart_rel
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(DartEmitter(py_path, dart_rel).convert(src), encoding="utf-8")
            ok += 1
        except Exception:
            fail += 1
        if i % 200 == 0:
            print(f"  dart progress: {i}/{len(manifest)}")
    print(f"Dart port: {ok} ok, {fail} fail -> {LIB}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
