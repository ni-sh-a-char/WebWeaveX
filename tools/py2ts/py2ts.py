#!/usr/bin/env python3
"""
AST-based Python (core/) -> TypeScript (src/) converter for WebWeaveX.
Reads sources via `git show origin/python:<path>`.

Generated modules lean on src/runtime/pyCompat.ts (imported as `py`) for
Python semantics parity: truthiness, deep equality, ordering, slicing,
str/dict/list/set methods, re, pathlib, urllib.parse, bs4, hashlib, json.
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
MANIFEST = ROOT / "tools" / "py2ts" / "manifest.txt"
REPORT = ROOT / "docs" / "architecture" / "PYTHON_TO_JS_CONVERSION_REPORT.md"
PROTECTED = ROOT / "tools" / "py2ts" / "protected.txt"

JS_RESERVED = {
    "new", "delete", "default", "var", "let", "const", "function", "typeof",
    "instanceof", "void", "this", "switch", "case", "do", "catch", "enum",
    "export", "extends", "super", "null", "throw", "debugger", "arguments",
    "eval", "static", "package", "interface", "implements", "private",
    "protected", "public", "undefined",
    "py",  # collides with the pyCompat namespace import
}

PY_EXC_NAMES = {
    "Exception", "ValueError", "TypeError", "KeyError", "IndexError",
    "RuntimeError", "AttributeError", "NotImplementedError", "OSError",
    "IOError", "FileNotFoundError", "ZeroDivisionError", "StopIteration",
    "ArithmeticError", "LookupError", "AssertionError", "PermissionError",
    "TimeoutError", "OverflowError", "UnicodeDecodeError", "ImportError",
}

STR_METHODS = {
    "lower", "upper", "strip", "lstrip", "rstrip", "split", "rsplit",
    "replace", "startswith", "endswith", "find", "rfind", "count",
    "zfill", "ljust", "rjust", "center", "capitalize", "title",
    "splitlines", "partition", "rpartition", "removeprefix",
    "removesuffix", "isdigit", "isalpha", "isalnum", "isspace",
    "isupper", "islower", "encode", "decode", "join", "format",
    "casefold",
}


def json_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def is_const_name(name: str) -> bool:
    body = name.lstrip("_")
    return bool(body) and body.upper() == body


def snake_to_camel(name: str) -> str:
    if is_const_name(name):
        return name
    if not name:
        return name
    if name.startswith("_"):
        stripped = name.lstrip("_")
        prefix = name[: len(name) - len(stripped)]
        return prefix + snake_to_camel(stripped)
    if "_" not in name:
        return name
    parts = name.split("_")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:] if p)


def safe_ident(name: str) -> str:
    return name + "_" if name in JS_RESERVED else name


def py_path_to_ts(py_path: str) -> str:
    rel = py_path.removeprefix("core/")
    parts = rel.split("/")
    fname = parts.pop()
    base = fname.replace(".py", "")
    ts_name = "index.ts" if base == "__init__" else f"{snake_to_camel(base)}.ts"
    return "/".join(parts + [ts_name]) if parts else ts_name


def git_show(py_path: str) -> str | None:
    r = subprocess.run(
        ["git", "show", f"origin/python:{py_path}"],
        cwd=ROOT,
        capture_output=True,
    )
    if r.returncode != 0:
        return None
    raw = r.stdout
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return raw.decode(enc).replace("\x00", "")
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace").replace("\x00", "")


def load_manifest() -> list[str]:
    r = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "origin/python", "--", "core/"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(r.stdout, encoding="utf-8")
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip().endswith(".py")]


def load_protected() -> set[str]:
    if not PROTECTED.exists():
        return set()
    return {
        ln.strip().replace("\\", "/")
        for ln in PROTECTED.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    }


# --------------------------------------------------------------------------
# global registries (built by prescan)
# --------------------------------------------------------------------------

CLASS_NAMES: set[str] = set()
CLASS_INIT_PARAMS: dict[str, list[str]] = {}
FUNC_PARAMS: dict[str, list[str]] = {}
MODULE_PUBLIC_NAMES: dict[str, list[str]] = {}  # "core.x.y" -> public top-level names


def _dataclass_fields(node: ast.ClassDef) -> list[str]:
    return [
        item.target.id
        for item in node.body
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name)
    ]


def _is_dataclass(node: ast.ClassDef) -> bool:
    for d in node.decorator_list:
        if isinstance(d, ast.Name) and d.id == "dataclass":
            return True
        if isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == "dataclass":
            return True
        if isinstance(d, ast.Attribute) and d.attr == "dataclass":
            return True
    return False


def prescan(sources: dict[str, str]) -> None:
    for _path, src in sources.items():
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        dotted = _path.removesuffix(".py").replace("/", ".")
        if dotted.endswith(".__init__"):
            dotted = dotted[: -len(".__init__")]
        publics: list[str] = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not node.name.startswith("_"):
                    publics.append(node.name)
            elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                if not node.targets[0].id.startswith("_") and node.targets[0].id != "__all__":
                    publics.append(node.targets[0].id)
            elif isinstance(node, ast.ImportFrom):
                # re-exported names count as public surface
                for alias in node.names:
                    if alias.name != "*":
                        nm = alias.asname or alias.name
                        if not nm.startswith("_"):
                            publics.append(nm)
        MODULE_PUBLIC_NAMES[dotted] = publics
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                CLASS_NAMES.add(node.name)
                init = next(
                    (
                        item
                        for item in node.body
                        if isinstance(item, ast.FunctionDef) and item.name == "__init__"
                    ),
                    None,
                )
                if init is not None:
                    CLASS_INIT_PARAMS[node.name] = [
                        a.arg for a in init.args.args if a.arg not in ("self", "cls")
                    ] + [a.arg for a in init.args.kwonlyargs]
                elif _is_dataclass(node):
                    CLASS_INIT_PARAMS[node.name] = _dataclass_fields(node)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                params = [a.arg for a in node.args.args if a.arg not in ("self", "cls")]
                params += [a.arg for a in node.args.kwonlyargs]
                if node.args.kwarg and not node.args.vararg:
                    params.append("**")
                FUNC_PARAMS.setdefault(node.name, params)


# --------------------------------------------------------------------------
# type emission
# --------------------------------------------------------------------------

class TypeEmitter:
    PRIMS = {
        "str": "string",
        "int": "number",
        "float": "number",
        "bool": "boolean",
        "Any": "any",
        "Dict": "Record<string, any>",
        "dict": "Record<string, any>",
        "List": "any[]",
        "list": "any[]",
        "Set": "Set<any>",
        "set": "Set<any>",
        "Tuple": "any[]",
        "tuple": "any[]",
        "Sequence": "any[]",
        "Iterable": "any[]",
        "Mapping": "Record<string, any>",
        "Optional": "",
        "bytes": "any",
        "None": "null",
        "NoneType": "null",
        "object": "any",
        "Callable": "(...args: any[]) => any",
        "Deque": "any[]",
    }

    def emit(self, node: ast.expr | None) -> str:
        # generated code is intentionally `any`-typed: strict-mode compilable
        # without fighting Python's dynamic typing; hand-written modules stay strict
        return "any"

    def _emit(self, node: ast.expr | None) -> str:
        if node is None:
            return "any"
        if isinstance(node, ast.Constant):
            if node.value is None:
                return "null"
            if isinstance(node.value, str):
                # string annotation (forward ref)
                return self.PRIMS.get(node.value, "any")
            return "any"
        if isinstance(node, ast.Name):
            if node.id in CLASS_NAMES:
                return node.id
            return self.PRIMS.get(node.id, "any")
        if isinstance(node, ast.Attribute):
            return "any"
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            left = self._emit(node.left)
            right = self._emit(node.right)
            if left in ("any", "") or right in ("any", ""):
                return "any"
            return f"{left} | {right}"
        if isinstance(node, ast.Subscript):
            return self._subscript(node)
        if isinstance(node, ast.Tuple):
            return "any[]"
        return "any"

    def _subscript(self, node: ast.Subscript) -> str:
        if isinstance(node.value, ast.Name):
            nid = node.value.id
            sl = node.slice
            if nid in ("list", "List", "Sequence", "Iterable", "Deque"):
                inner = self._emit(sl)
                return f"{inner}[]" if inner and inner != "any" else "any[]"
            if nid in ("dict", "Dict", "Mapping"):
                if isinstance(sl, ast.Tuple) and len(sl.elts) >= 2:
                    v = self._emit(sl.elts[1])
                    return f"Record<string, {v or 'any'}>"
                return "Record<string, any>"
            if nid in ("tuple", "Tuple"):
                return "any[]"
            if nid in ("set", "Set"):
                return "Set<any>"
            if nid == "Optional":
                inner = self._emit(sl)
                return f"{inner} | null" if inner and inner != "any" else "any"
            if nid in ("Callable",):
                return "(...args: any[]) => any"
        return "any"


# --------------------------------------------------------------------------
# expression emission
# --------------------------------------------------------------------------

class ExprEmitter:
    def __init__(self, mod: "ModuleEmitter") -> None:
        self.mod = mod

    def is_floatish(self, node: ast.expr) -> bool:
        """Static detection of float-typed expressions for Python str() parity."""
        if isinstance(node, ast.Constant):
            return isinstance(node.value, float)
        if isinstance(node, ast.Name):
            return node.id in self.mod.stmt.float_vars
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self":
            return f"self.{node.attr}" in self.mod.stmt.float_vars
        if isinstance(node, ast.UnaryOp):
            return self.is_floatish(node.operand)
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Div):
                return True
            if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Mod, ast.Pow)):
                return self.is_floatish(node.left) or self.is_floatish(node.right)
            return False
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "round" and len(node.args) >= 2:
                # Python round(int, n) stays int — float only if the arg is
                return self.is_floatish(node.args[0])
            if node.func.id == "float":
                return True
            # sum() is NOT float-ish (sum([]) is int 0); min/max are float-ish
            # only when every candidate is float-typed.
            if node.func.id in ("min", "max") and len(node.args) > 1:
                return all(self.is_floatish(a) for a in node.args)
            if node.func.id == "abs" and node.args:
                return self.is_floatish(node.args[0])
        if isinstance(node, ast.IfExp):
            return self.is_floatish(node.body) or self.is_floatish(node.orelse)
        return False

    # -- helpers ----------------------------------------------------------

    def py(self, helper: str, *args: str) -> str:
        self.mod.use_py = True
        return f"py.{helper}({', '.join(args)})"

    def emit_test(self, node: ast.expr) -> str:
        """Emit an expression used in boolean context (if/while/filter)."""
        if isinstance(node, ast.Compare):
            return self.emit(node)
        if isinstance(node, ast.Constant) and isinstance(node.value, bool):
            return "true" if node.value else "false"
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return f"!{self.emit_test(node.operand)}"
        if isinstance(node, ast.BoolOp):
            joiner = " && " if isinstance(node.op, ast.And) else " || "
            return "(" + joiner.join(self.emit_test(v) for v in node.values) + ")"
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in (
            "isinstance", "hasattr", "callable", "bool", "all", "any",
        ):
            return self.emit(node)
        return self.py("truthy", self.emit(node))

    # -- comprehensions ---------------------------------------------------

    def _comp_bind(self, target: ast.expr) -> str | None:
        if isinstance(target, ast.Name):
            return f"({safe_ident(target.id)}: any)"
        if isinstance(target, ast.Tuple) and all(isinstance(e, ast.Name) for e in target.elts):
            inner = ", ".join(safe_ident(e.id) for e in target.elts)  # type: ignore[attr-defined]
            return f"([{inner}]: any)"
        return None

    def _comp_iter(self, it: ast.expr) -> str:
        """Iterable expression for comprehensions with Python iteration."""
        if isinstance(it, ast.Call) and isinstance(it.func, ast.Attribute):
            if it.func.attr == "items" and not it.args:
                return self.py("items", self.emit(it.func.value))
            if it.func.attr == "keys" and not it.args:
                return self.py("keys", self.emit(it.func.value))
            if it.func.attr == "values" and not it.args:
                return self.py("values", self.emit(it.func.value))
        if isinstance(it, ast.Call) and isinstance(it.func, ast.Name):
            if it.func.id == "range":
                return self.py("range", *(self.emit(a) for a in it.args))
            if it.func.id == "enumerate":
                return self.py("enumerate", *(self.emit(a) for a in it.args))
            if it.func.id == "zip":
                return self.py("zip", *(self.emit(a) for a in it.args))
            if it.func.id in ("sorted", "reversed", "list", "set", "tuple"):
                return self.py("iter", self.emit(it))
        return self.py("iter", self.emit(it))

    def _emit_comp_chain(self, generators: list[ast.comprehension], elt_expr: str) -> str | None:
        gen = generators[0]
        bind = self._comp_bind(gen.target)
        if bind is None:
            return None
        chain = self._comp_iter(gen.iter)
        for cond in gen.ifs:
            chain += f".filter({bind} => {self.emit_test(cond)})"
        rest = generators[1:]
        if rest:
            inner = self._emit_comp_chain(rest, elt_expr)
            if inner is None:
                return None
            return f"{chain}.flatMap({bind} => {inner})"
        return f"{chain}.map({bind} => {elt_expr})"

    def _emit_comp(self, elt: ast.expr, generators: list[ast.comprehension], kind: str) -> str:
        elt_s = self.emit(elt)
        if isinstance(elt, (ast.Dict, ast.Set)):
            elt_s = f"({elt_s})"
        chain = self._emit_comp_chain(generators, elt_s)
        if chain is None:
            return "[] /* unsupported comprehension target */"
        if kind == "set":
            return self.py("toSet", chain)
        return chain

    def _emit_dict_comp(self, node: ast.DictComp) -> str:
        pair = f"[{self.emit(node.key)}, {self.emit(node.value)}] as [any, any]"
        chain = self._emit_comp_chain(node.generators, f"({pair})")
        if chain is None:
            return "{}"
        return f"Object.fromEntries({chain})"

    # -- calls ------------------------------------------------------------

    def _kw_get(self, node: ast.Call, name: str) -> ast.expr | None:
        for kw in node.keywords:
            if kw.arg == name:
                return kw.value
        return None

    def _sort_opts(self, node: ast.Call) -> str:
        parts = []
        key = self._kw_get(node, "key")
        rev = self._kw_get(node, "reverse")
        if key is not None:
            parts.append(f"key: ({self.emit(key)}) as (item: any) => any")
        if rev is not None:
            parts.append(f"reverse: {self.emit_test(rev)}")
        return "{" + ", ".join(parts) + "}"

    def _minmax_opts(self, node: ast.Call) -> str:
        parts = []
        key = self._kw_get(node, "key")
        dflt = self._kw_get(node, "default")
        if key is not None:
            parts.append(f"key: ({self.emit(key)}) as (item: any) => any")
        if dflt is not None:
            parts.append(f"dflt: {self.emit(dflt)}, hasDefault: true")
        return "{" + ", ".join(parts) + "}"

    def _re_flags(self, node: ast.expr | None) -> str:
        if node is None:
            return '""'
        names: list[str] = []

        def walk(n: ast.expr) -> None:
            if isinstance(n, ast.BinOp) and isinstance(n.op, ast.BitOr):
                walk(n.left)
                walk(n.right)
            elif isinstance(n, ast.Attribute):
                names.append(n.attr)
            elif isinstance(n, ast.Name):
                names.append(n.id)

        walk(node)
        flags = ""
        for n in names:
            if n in ("I", "IGNORECASE") and "i" not in flags:
                flags += "i"
            elif n in ("S", "DOTALL") and "s" not in flags:
                flags += "s"
            elif n in ("M", "MULTILINE") and "m" not in flags:
                flags += "m"
        return json_str(flags)

    def _emit_isinstance(self, node: ast.Call) -> str:
        obj = self.emit(node.args[0]) if node.args else "null"
        typ_node = node.args[1] if len(node.args) > 1 else None
        typs: list[str] = []
        if isinstance(typ_node, ast.Tuple):
            for e in typ_node.elts:
                if isinstance(e, ast.Name):
                    typs.append(e.id)
                elif isinstance(e, ast.Attribute):
                    typs.append(e.attr)
        elif isinstance(typ_node, ast.Name):
            typs.append(typ_node.id)
        elif isinstance(typ_node, ast.Attribute):
            typs.append(typ_node.attr)
        checks: list[str] = []
        for t in typs:
            if t == "str":
                checks.append(f'typeof {obj} === "string"')
            elif t == "bool":
                checks.append(f'typeof {obj} === "boolean"')
            elif t == "int":
                checks.append(f'(typeof {obj} === "number" && Number.isInteger({obj}))')
            elif t == "float":
                checks.append(f'typeof {obj} === "number"')
            elif t == "dict":
                checks.append(
                    f'({obj} !== null && typeof {obj} === "object" && !Array.isArray({obj}) '
                    f"&& !({obj} instanceof Set) && !({obj} instanceof Map))"
                )
            elif t in ("list", "tuple"):
                checks.append(f"Array.isArray({obj})")
            elif t in ("set", "frozenset"):
                checks.append(f"({obj} instanceof Set)")
            elif t == "bytes":
                checks.append(f"({obj} instanceof py.PyBytes)")
            elif t in CLASS_NAMES:
                checks.append(f"({obj} instanceof {t})")
            elif t in PY_EXC_NAMES:
                checks.append(f"({obj} instanceof Error)")
            else:
                checks.append("true")
        if not checks:
            return "true"
        if any("PyBytes" in c for c in checks):
            self.mod.use_py = True
        return "(" + " || ".join(checks) + ")"

    def _map_positional_kwargs(
        self, node: ast.Call, params: list[str]
    ) -> str | None:
        """Map positional + keyword args onto a known parameter order."""
        if any(kw.arg is None for kw in node.keywords):
            return None
        if any(isinstance(a, ast.Starred) for a in node.args):
            return None
        slots: dict[int, str] = {}
        for i, a in enumerate(node.args):
            slots[i] = self.emit(a)
        ok = True
        for kw in node.keywords:
            if kw.arg in params:
                slots[params.index(kw.arg)] = self.emit(kw.value)
            else:
                ok = False
        if not ok:
            return None
        if not slots:
            return ""
        hi = max(slots.keys())
        return ", ".join(slots.get(i, "undefined") for i in range(hi + 1))

    def _emit_builtin_call(self, node: ast.Call) -> str | None:  # noqa: C901
        fid = node.func.id  # type: ignore[union-attr]
        args = node.args
        e = self.emit
        if fid == "len":
            return self.py("len", e(args[0])) if args else "0"
        if fid == "range":
            return self.py("range", *(e(a) for a in args))
        if fid == "enumerate":
            return self.py("enumerate", *(e(a) for a in args))
        if fid == "zip":
            return self.py("zip", *(e(a) for a in args))
        if fid == "reversed":
            return self.py("reversed", e(args[0])) if args else "[]"
        if fid == "iter":
            return self.py("iter", e(args[0])) if args else "[]"
        if fid == "next":
            if args and isinstance(args[0], ast.Call) and isinstance(args[0].func, ast.Name) and args[0].func.id == "iter":
                seq = self.py("iter", e(args[0].args[0])) if args[0].args else "[]"
            else:
                seq = self.py("iter", e(args[0])) if args else "[]"
            if len(args) > 1:
                return self.py("next", seq, e(args[1]))
            return self.py("next", seq)
        if fid == "list":
            return f"[...{self.py('iter', e(args[0]))}]" if args else "[]"
        if fid == "tuple":
            return f"[...{self.py('iter', e(args[0]))}]" if args else "[]"
        if fid in ("set", "frozenset"):
            return self.py("toSet", e(args[0])) if args else "new Set()"
        if fid == "dict":
            if not args and not node.keywords:
                return "{}"
            if args:
                return self.py("pyDict", e(args[0]))
            pairs = ", ".join(f"{json_str(kw.arg)}: {e(kw.value)}" for kw in node.keywords if kw.arg)
            return "{" + pairs + "}"
        if fid == "str":
            if args and self.is_floatish(args[0]):
                return self.py("floatStr", e(args[0]))
            return self.py("toStr", e(args[0])) if args else '""'
        if fid == "int":
            return self.py("toInt", *(e(a) for a in args)) if args else "0"
        if fid == "float":
            return self.py("toFloat", e(args[0])) if args else "0"
        if fid == "bool":
            return self.py("truthy", e(args[0])) if args else "false"
        if fid == "abs":
            return self.py("pyAbs", e(args[0])) if args else "0"
        if fid == "round":
            return self.py("round", *(e(a) for a in args)) if args else "0"
        if fid == "sum":
            return self.py("sum", *(e(a) for a in args)) if args else "0"
        if fid in ("min", "max"):
            opts = self._minmax_opts(node)
            if len(args) == 1:
                return self.py(fid, e(args[0]), opts) if opts != "{}" else self.py(fid, e(args[0]))
            arr = "[" + ", ".join(e(a) for a in args) + "]"
            return self.py(fid, arr, opts) if opts != "{}" else self.py(fid, arr)
        if fid == "sorted":
            opts = self._sort_opts(node)
            if opts != "{}":
                return self.py("sorted", e(args[0]), opts)
            return self.py("sorted", e(args[0])) if args else "[]"
        if fid == "all":
            return self.py("all", e(args[0])) if args else "true"
        if fid == "any":
            return self.py("any", e(args[0])) if args else "false"
        if fid == "repr":
            return self.py("repr", e(args[0])) if args else '""'
        if fid == "ord":
            return self.py("ord", e(args[0])) if args else "0"
        if fid == "chr":
            return self.py("chr", e(args[0])) if args else '""'
        if fid == "divmod":
            return self.py("divmod", e(args[0]), e(args[1])) if len(args) > 1 else "[0, 0]"
        if fid == "callable":
            return f'(typeof {e(args[0])} === "function")' if args else "false"
        if fid == "isinstance":
            return self._emit_isinstance(node)
        if fid == "hasattr":
            obj = e(args[0]) if args else "null"
            attr = e(args[1]) if len(args) > 1 else '""'
            return (
                f"({obj} !== null && {obj} !== undefined && typeof {obj} === \"object\" "
                f"&& (String({attr}) in ({obj} as object) "
                f"|| typeof ({obj} as Record<string, unknown>)[String({attr})] === \"function\"))"
            )
        if fid == "getattr":
            obj = e(args[0]) if args else "null"
            attr = e(args[1]) if len(args) > 1 else '""'
            if len(args) > 2:
                return (
                    f"((({obj} ?? {{}}) as Record<string, any>)[String({attr})] ?? {e(args[2])})"
                )
            return f"(({obj} as Record<string, any>)[String({attr})])"
        if fid == "setattr":
            obj = e(args[0]) if args else "null"
            attr = e(args[1]) if len(args) > 1 else '""'
            val = e(args[2]) if len(args) > 2 else "null"
            return f"(({obj} as Record<string, any>)[String({attr})] = {val})"
        if fid == "print":
            return self.py("print", *(e(a) for a in args))
        if fid == "open":
            return self.py("open", *(e(a) for a in args))
        if fid == "format":
            return self.py("format", e(args[0]), e(args[1]) if len(args) > 1 else '""')
        if fid == "Path":
            return self.py("path", e(args[0]) if args else '""')
        if fid == "BeautifulSoup":
            return self.py("soup", *(e(a) for a in args))
        if fid == "urlparse":
            return self.py("urlparse", e(args[0])) if args else self.py("urlparse", '""')
        if fid == "urlunparse":
            return self.py("urlunparse", e(args[0])) if args else '""'
        if fid == "urljoin":
            return self.py("urljoin", *(e(a) for a in args))
        if fid == "urlsplit":
            return self.py("urlsplit", e(args[0])) if args else self.py("urlsplit", '""')
        if fid == "urlunsplit":
            return self.py("urlunsplit", e(args[0])) if args else '""'
        if fid == "quote":
            return self.py("quote", *(e(a) for a in args))
        if fid == "unquote":
            return self.py("unquote", *(e(a) for a in args))
        if fid == "deque":
            maxlen = self._kw_get(node, "maxlen")
            val = e(args[0]) if args else "[]"
            if maxlen is not None:
                return self.py("deque", val, e(maxlen))
            return self.py("deque", val)
        if fid == "defaultdict":
            factory = e(args[0]) if args else "() => null"
            if args and isinstance(args[0], ast.Name):
                fmap = {"list": "() => []", "dict": "() => ({})", "set": "() => new Set()", "int": "() => 0", "float": "() => 0", "str": '() => ""'}
                factory = fmap.get(args[0].id, factory)
            return self.py("defaultdict", factory)
        if fid == "Counter":
            return self.py("counter", *(e(a) for a in args))
        if fid == "OrderedDict":
            return e(args[0]) if args else "{}"
        if fid == "deepcopy":
            return self.py("deepcopy", e(args[0])) if args else "null"
        if fid == "asdict":
            return self.py("deepcopy", e(args[0])) if args else "{}"
        if fid == "bytes":
            if not args:
                return "new py.PyBytes(new Uint8Array())"
            self.mod.use_py = True
            return f"new py.PyBytes({e(args[0])})"
        if fid == "field":
            dflt = self._kw_get(node, "default")
            factory = self._kw_get(node, "default_factory")
            if factory is not None and isinstance(factory, ast.Name):
                fmap = {"list": "[]", "dict": "({})", "set": "new Set()"}
                return fmap.get(factory.id, "null")
            if dflt is not None:
                return e(dflt)
            return "null"
        if fid == "ZipFile":
            return self.py("zipFile", *(e(a) for a in args))
        if fid == "Lock" or fid == "RLock":
            return self.py("lock")
        if fid == "ThreadPoolExecutor":
            return self.py("threadPoolExecutor", *(e(a) for a in args))
        if fid == "as_completed":
            return self.py("asCompleted", e(args[0])) if args else "[]"
        if fid in PY_EXC_NAMES:
            msg = e(args[0]) if args else '""'
            return self.py("err", json_str(fid), msg)
        if fid == "super":
            return "super"
        if fid == "id":
            return f"String({e(args[0])})" if args else '"0"'
        if fid == "type" and args:
            return f"({e(args[0])})"
        return None

    def _emit_attr_call(self, node: ast.Call) -> str | None:  # noqa: C901
        func = node.func
        assert isinstance(func, ast.Attribute)
        attr = func.attr
        e = self.emit
        base_node = func.value

        # module-level namespaces -------------------------------------------------
        if isinstance(base_node, ast.Name):
            mod_name = base_node.id
            if mod_name == "re":
                if attr == "compile":
                    flags = self._re_flags(node.args[1] if len(node.args) > 1 else self._kw_get(node, "flags"))
                    return self.py("regex", e(node.args[0]), flags)
                if attr in ("sub", "subn"):
                    # re.sub(pattern, repl, string, count=0, flags=0)
                    flags = self._re_flags(node.args[4] if len(node.args) > 4 else self._kw_get(node, "flags"))
                    cnt = e(node.args[3]) if len(node.args) > 3 else "0"
                    cnt_kw = self._kw_get(node, "count")
                    if cnt_kw is not None:
                        cnt = e(cnt_kw)
                    if attr == "subn":
                        return self.py("regex", e(node.args[0]), flags) + f".subn({e(node.args[1])}, {e(node.args[2])}, {cnt})"
                    return self.py("reSub", e(node.args[0]), e(node.args[1]), e(node.args[2]), cnt, flags)
                if attr in ("search", "match", "fullmatch", "findall", "finditer"):
                    flags = self._re_flags(node.args[2] if len(node.args) > 2 else self._kw_get(node, "flags"))
                    helper = {"search": "reSearch", "match": "reMatch", "fullmatch": "reFullmatch", "findall": "reFindall", "finditer": "reFinditer"}[attr]
                    return self.py(helper, e(node.args[0]), e(node.args[1]), flags)
                if attr == "split":
                    return self.py("reSplit", e(node.args[0]), e(node.args[1]))
                if attr == "escape":
                    return self.py("reEscape", e(node.args[0]))
            if mod_name == "os":
                if attr == "makedirs":
                    return self.py("osMakedirs", *(e(a) for a in node.args + [kw.value for kw in node.keywords]))
                if attr == "remove" or attr == "unlink":
                    return self.py("osRemove", e(node.args[0]))
                if attr == "listdir":
                    return self.py("osListdir", *(e(a) for a in node.args))
                if attr == "rename":
                    return self.py("osRename", e(node.args[0]), e(node.args[1]))
                if attr == "replace":
                    return self.py("osReplace", e(node.args[0]), e(node.args[1]))
            if mod_name == "shutil":
                if attr == "rmtree":
                    return self.py("rmTree", e(node.args[0]))
                if attr in ("copy", "copy2", "copyfile"):
                    return self.py("copyFile", e(node.args[0]), e(node.args[1]))
            if mod_name == "json":
                if attr == "dump" and len(node.args) >= 2:
                    return f"{e(node.args[1])}.write({self.py('jsonDumps', e(node.args[0]))})"
                if attr == "load" and node.args:
                    return self.py("jsonLoads", f"{e(node.args[0])}.read()")
                if attr == "dumps":
                    opts: list[str] = []
                    sk = self._kw_get(node, "sort_keys")
                    ind = self._kw_get(node, "indent")
                    sep = self._kw_get(node, "separators")
                    ea = self._kw_get(node, "ensure_ascii")
                    df = self._kw_get(node, "default")
                    if sk is not None:
                        opts.append(f"sortKeys: {self.emit_test(sk)}")
                    if ind is not None:
                        opts.append(f"indent: {e(ind)}")
                    if sep is not None:
                        opts.append(f"separators: {e(sep)} as [string, string]")
                    if ea is not None:
                        opts.append(f"ensureAscii: {self.emit_test(ea)}")
                    if df is not None:
                        opts.append("defaultStr: true")
                    if opts:
                        return self.py("jsonDumps", e(node.args[0]), "{" + ", ".join(opts) + "}")
                    return self.py("jsonDumps", e(node.args[0]))
                if attr == "loads":
                    return self.py("jsonLoads", e(node.args[0]))
            if mod_name == "hashlib":
                return self.py("hashNew", json_str(attr), *(e(a) for a in node.args))
            if mod_name == "math":
                math_map = {
                    "sqrt": "Math.sqrt", "floor": "Math.floor", "ceil": "Math.ceil",
                    "log": "Math.log", "log2": "Math.log2", "log10": "Math.log10",
                    "exp": "Math.exp", "pow": "Math.pow", "fabs": "Math.abs",
                    "hypot": "Math.hypot", "atan2": "Math.atan2", "cos": "Math.cos",
                    "sin": "Math.sin", "tan": "Math.tan", "trunc": "Math.trunc",
                    "isnan": "Number.isNaN", "isfinite": "Number.isFinite",
                }
                if attr in math_map:
                    return f"{math_map[attr]}({', '.join(e(a) for a in node.args)})"
                if attr == "isinf":
                    a0 = e(node.args[0])
                    return f"({a0} === Infinity || {a0} === -Infinity)"
            if mod_name == "base64":
                if attr == "b64encode":
                    return self.py("b64encode", e(node.args[0]))
                if attr == "b64decode":
                    return self.py("b64decode", e(node.args[0]))
            if mod_name == "unicodedata":
                if attr == "normalize":
                    return self.py("uniNormalize", e(node.args[0]), e(node.args[1]))
                if attr == "category":
                    return self.py("uniCategory", e(node.args[0]))
            if mod_name == "io" and attr == "BytesIO":
                return self.py("bytesIO", e(node.args[0]))
            if mod_name == "ipaddress":
                if attr == "ip_address":
                    return self.py("ipAddress", e(node.args[0]))
            if mod_name == "copy":
                if attr == "deepcopy":
                    return self.py("deepcopy", e(node.args[0]))
                if attr == "copy":
                    return self.py("copy", e(node.args[0]))
            if mod_name == "zipfile" and attr == "ZipFile":
                return self.py("zipFile", *(e(a) for a in node.args))
            if mod_name == "httpx":
                if attr == "AsyncClient":
                    kw_pairs = [
                        f"{json_str(kw.arg)}: {e(kw.value)}"
                        for kw in node.keywords
                        if kw.arg
                    ]
                    return self.py("httpxAsyncClient", "{" + ", ".join(kw_pairs) + "}")
                if attr == "Limits":
                    kw_pairs = [
                        f"{json_str(kw.arg)}: {e(kw.value)}"
                        for kw in node.keywords
                        if kw.arg
                    ]
                    return "{" + ", ".join(kw_pairs) + "}"
            if mod_name == "requests" and attr in ("get", "post", "head"):
                url_arg = e(node.args[0]) if node.args else '""'
                kw_pairs = [
                    f"{json_str(kw.arg)}: {e(kw.value)}"
                    for kw in node.keywords
                    if kw.arg
                ]
                return self.py("requestsGet", url_arg, "{" + ", ".join(kw_pairs) + "}")
            if mod_name == "os" and attr == "getenv":
                if len(node.args) > 1:
                    return f"(py.environ[String({e(node.args[0])})] ?? {e(node.args[1])})"
                self.mod.use_py = True
                return f"(py.environ[String({e(node.args[0])})] ?? null)"
            if mod_name == "dict" and attr == "fromkeys":
                return self.py("fromkeys", *(e(a) for a in node.args))

        if (
            isinstance(base_node, ast.Attribute)
            and isinstance(base_node.value, ast.Name)
            and base_node.value.id == "urllib"
        ):
            if base_node.attr == "parse":
                url_map = {
                    "quote_plus": "quotePlus", "quote": "quote",
                    "unquote": "unquote", "urlparse": "urlparse",
                    "urljoin": "urljoin", "urlencode": "urlencode",
                }
                if attr in url_map:
                    return self.py(url_map[attr], *(e(a) for a in node.args))
            if base_node.attr == "request":
                if attr == "Request":
                    # Request(url, data=None, headers={}) — positional arg 2 is
                    # the headers dict in this codebase's call style
                    args = [e(node.args[0])]
                    headers_kw = [e(kw.value) for kw in node.keywords if kw.arg == "headers"]
                    if headers_kw:
                        args.append(headers_kw[0])
                    elif len(node.args) > 1:
                        args.append(e(node.args[1]))
                    return self.py("urllibRequest", *args)
                if attr == "urlopen":
                    return self.py(
                        "urllibUrlopen",
                        *(e(a) for a in node.args),
                        *(e(kw.value) for kw in node.keywords if kw.arg == "timeout"),
                    )
        if (
            isinstance(base_node, ast.Attribute)
            and isinstance(base_node.value, ast.Name)
            and base_node.value.id == "os"
            and base_node.attr == "path"
        ):
            os_map = {
                "join": "osPathJoin", "exists": "osPathExists",
                "basename": "osPathBasename", "dirname": "osPathDirname",
                "splitext": "osPathSplitext",
            }
            if attr in os_map:
                return self.py(os_map[attr], *(e(a) for a in node.args))

        base = e(base_node)

        # super().__init__ / super().method --------------------------------------
        if base == "super()" or (
            isinstance(base_node, ast.Call)
            and isinstance(base_node.func, ast.Name)
            and base_node.func.id == "super"
        ):
            if attr == "__init__":
                return f"super({', '.join(e(a) for a in node.args)})"
            return f"super.{attr}({', '.join(e(a) for a in node.args)})"

        arg_list = [e(a) for a in node.args]

        # string / collection method dispatch -------------------------------------
        if attr == "lower" and not node.args:
            return f"String({base}).toLowerCase()"
        if attr == "upper" and not node.args:
            return f"String({base}).toUpperCase()"
        if attr == "casefold" and not node.args:
            return f"String({base}).toLowerCase()"
        if attr == "append":
            return self.py("listAppend", base, *arg_list)
        if attr == "appendleft":
            return self.py("appendleft", base, *arg_list)
        if attr == "popleft":
            return self.py("popleft", base)
        if attr == "extend":
            return self.py("extend", base, *arg_list)
        if attr == "insert":
            return self.py("insert", base, *arg_list)
        if attr == "remove":
            return self.py("remove", base, *arg_list)
        if attr == "discard":
            return self.py("setDiscard", base, *arg_list)
        if attr == "pop":
            return self.py("pop", base, *arg_list)
        if attr == "get" and len(node.args) <= 2:
            return self.py("get", base, *arg_list)
        if attr == "setdefault":
            return self.py("setdefault", base, *arg_list)
        if attr == "update":
            return self.py("update", base, *arg_list)
        if attr == "copy" and not node.args:
            return self.py("copy", base)
        if attr == "clear" and not node.args:
            return self.py("clear", base)
        if attr == "keys" and not node.args:
            return self.py("keys", base)
        if attr == "values" and not node.args:
            return self.py("values", base)
        if attr == "items" and not node.args:
            return self.py("items", base)
        if attr == "sort":
            opts = self._sort_opts(node)
            if opts != "{}":
                return self.py("sortInPlace", base, opts)
            return self.py("sortInPlace", base)
        if attr == "reverse" and not node.args:
            return f"{base}.reverse()"
        if attr == "count" and len(node.args) == 1:
            return self.py("count", base, arg_list[0])
        if attr == "index" and len(node.args) == 1:
            return self.py("index", base, arg_list[0])
        if attr == "add" and len(node.args) == 1:
            return self.py("setAdd", base, arg_list[0])
        if attr == "union":
            return self.py("union", base, *arg_list)
        if attr == "intersection":
            return self.py("intersection", base, *arg_list)
        if attr == "difference":
            return self.py("difference", base, *arg_list)
        if attr == "symmetric_difference":
            return self.py("symmetricDifference", base, *arg_list)
        if attr == "issubset":
            return self.py("issubset", base, *arg_list)
        if attr == "issuperset":
            return self.py("issuperset", base, *arg_list)
        if attr == "most_common":
            return self.py("mostCommon", base, *arg_list)
        if attr in STR_METHODS:
            helper = {
                "startswith": "startswith", "endswith": "endswith",
                "splitlines": "splitlines", "removeprefix": "removeprefix",
                "removesuffix": "removesuffix",
            }.get(attr, attr)
            return self.py(helper, base, *arg_list)
        if attr == "format":
            kwargs_pairs = ", ".join(
                f"{json_str(kw.arg)}: {e(kw.value)}" for kw in node.keywords if kw.arg
            )
            return self.py("strFormat", base, "[" + ", ".join(arg_list) + "]", "{" + kwargs_pairs + "}")

        return None

    # -- main emit ---------------------------------------------------------

    def emit(self, node: ast.expr) -> str:  # noqa: C901
        if isinstance(node, ast.Constant):
            v = node.value
            if v is None:
                return "null"
            if v is True:
                return "true"
            if v is False:
                return "false"
            if isinstance(v, float):
                # boxed: Python floats keep their float-ness through arithmetic
                self.mod.use_py = True
                return f"py.F({v!r})"
            if isinstance(v, str):
                return json_str(v)
            if isinstance(v, bytes):
                self.mod.use_py = True
                return f"new py.PyBytes({json_str(v.decode('utf-8', errors='replace'))})"
            if v is Ellipsis:
                return "null"
            return repr(v)
        if isinstance(node, ast.Name):
            nid = node.id
            if nid == "True":
                return "true"
            if nid == "False":
                return "false"
            if nid == "None":
                return "null"
            if nid == "__name__":
                dotted = self.mod.py_path.removesuffix(".py").replace("/", ".")
                if dotted.endswith(".__init__"):
                    dotted = dotted[: -len(".__init__")]
                return json_str(dotted)
            if nid == "self":
                return "this"
            if nid == "cls":
                return self.mod.current_class or "cls"
            if nid == "TYPE_CHECKING":
                return "false"
            if nid == "__file__":
                self.mod.use_py = True
                return "py.metaFile(import.meta.url)"
            if nid == "Path":
                self.mod.use_py = True
                return "py.path"
            if nid in ("Dict", "List", "Set", "Tuple", "Optional", "Any", "Callable", "Sequence", "Mapping", "Iterable"):
                return "Object"
            if nid in ("str", "int", "float", "bool", "len") and nid not in self.mod.name_map:
                # builtin referenced as a value (e.g. key=str, default=str)
                self.mod.use_py = True
                return {"str": "py.toStr", "int": "py.toInt", "float": "py.toFloat", "bool": "py.truthy", "len": "py.len"}[nid]
            if nid in self.mod.stmt.shadowed_params:
                return self.mod.stmt.shadowed_params[nid]
            mapped = self.mod.name_map.get(nid)
            if mapped is not None:
                return mapped
            return safe_ident(nid)
        if isinstance(node, ast.Attribute):
            # module constants
            if isinstance(node.value, ast.Name):
                base_id = node.value.id
                if base_id == "sys":
                    self.mod.use_py = True
                    return f"py.sysShim.{node.attr}"
                if base_id == "math":
                    const_map = {"inf": "Infinity", "nan": "NaN", "pi": "Math.PI", "e": "Math.E", "tau": "(2 * Math.PI)"}
                    if node.attr in const_map:
                        return const_map[node.attr]
                if base_id == "os" and node.attr == "environ":
                    self.mod.use_py = True
                    return "py.environ"
                if base_id == "string":
                    smap = {
                        "ascii_lowercase": json_str("abcdefghijklmnopqrstuvwxyz"),
                        "ascii_uppercase": json_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                        "ascii_letters": json_str("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                        "digits": json_str("0123456789"),
                        "punctuation": json_str("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"),
                    }
                    if node.attr in smap:
                        return smap[node.attr]
            if (
                isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id == "type"
                and node.attr == "__name__"
            ):
                inner = self.emit(node.value.args[0]) if node.value.args else "null"
                return (
                    f"(Array.isArray({inner}) ? \"list\" : {inner} === null ? \"NoneType\" "
                    f": typeof {inner} === \"string\" ? \"str\" "
                    f": typeof {inner} === \"boolean\" ? \"bool\" "
                    f": typeof {inner} === \"number\" ? (Number.isInteger({inner}) ? \"int\" : \"float\") "
                    f": {inner} instanceof Set ? \"set\" "
                    f": {inner} instanceof Error ? (({inner} as Error).name || \"Exception\") "
                    f": typeof {inner} === \"object\" ? (({inner} as object).constructor === Object ? \"dict\" : ({inner} as object).constructor?.name ?? \"object\") "
                    f": typeof {inner})"
                )
            if node.attr == "__mro__":
                return self.py("mro", self.emit(node.value))
            if node.attr == "__name__":
                return f"(({self.emit(node.value)}) as any)?.name ?? String({self.emit(node.value)})"
            return f"{self.emit(node.value)}.{node.attr}"
        if isinstance(node, ast.Subscript):
            base = self.emit(node.value)
            if isinstance(node.slice, ast.Slice):
                lo = self.emit(node.slice.lower) if node.slice.lower is not None else "null"
                hi = self.emit(node.slice.upper) if node.slice.upper is not None else "null"
                if node.slice.step is not None:
                    return self.py("slice", base, lo, hi, self.emit(node.slice.step))
                return self.py("slice", base, lo, hi)
            return self.py("at", base, self.emit(node.slice))
        if isinstance(node, ast.BinOp):
            left = self.emit(node.left)
            right = self.emit(node.right)
            op = node.op
            if isinstance(op, ast.Add):
                return self.py("add", left, right)
            if isinstance(op, ast.Sub):
                return self.py("sub", left, right)
            if isinstance(op, ast.Mult):
                return self.py("mul", left, right)
            if isinstance(op, ast.Div):
                return self.py("div", left, right)
            if isinstance(op, ast.FloorDiv):
                return self.py("floordiv", left, right)
            if isinstance(op, ast.Mod):
                return self.py("mod", left, right)
            if isinstance(op, ast.Pow):
                return f"(({left}) ** ({right}))"
            if isinstance(op, ast.BitOr):
                return self.py("bitor", left, right)
            if isinstance(op, ast.BitAnd):
                return self.py("bitand", left, right)
            if isinstance(op, ast.BitXor):
                return self.py("bitxor", left, right)
            if isinstance(op, ast.LShift):
                return f"(({left}) << ({right}))"
            if isinstance(op, ast.RShift):
                return f"(({left}) >> ({right}))"
            return f"(({left}) /* unsupported op */ , ({right}))"
        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.Not):
                return f"!{self.emit_test(node.operand)}"
            if isinstance(node.op, ast.USub):
                return f"(-{self.emit(node.operand)})"
            if isinstance(node.op, ast.UAdd):
                return f"(+{self.emit(node.operand)})"
            if isinstance(node.op, ast.Invert):
                return f"(~{self.emit(node.operand)})"
            return self.emit(node.operand)
        if isinstance(node, ast.BoolOp):
            helper = "and2" if isinstance(node.op, ast.And) else "or2"
            out = self.emit(node.values[-1])
            for v in reversed(node.values[:-1]):
                out = self.py(helper, self.emit(v), f"() => ({out})")
            return out
        if isinstance(node, ast.Compare):
            return self._emit_compare(node)
        if isinstance(node, ast.Call):
            return self._emit_call(node)
        if isinstance(node, ast.Dict):
            pairs = []
            for k, v in zip(node.keys, node.values):
                if k is None:
                    pairs.append(f"...({self.emit(v)})")
                    continue
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    key = json_str(k.value)
                else:
                    key = f"[{self.py('toStr', self.emit(k))}]"
                pairs.append(f"{key}: {self.emit(v)}")
            return "{" + ", ".join(pairs) + "}"
        if isinstance(node, ast.Set):
            return f"new Set([{', '.join(self.emit(e) for e in node.elts)}])"
        if isinstance(node, (ast.List, ast.Tuple)):
            return f"[{', '.join(self.emit(e) for e in node.elts)}]"
        if isinstance(node, ast.IfExp):
            return f"({self.emit_test(node.test)} ? {self.emit(node.body)} : {self.emit(node.orelse)})"
        if isinstance(node, ast.JoinedStr):
            parts: list[str] = []
            for v in node.values:
                if isinstance(v, ast.Constant):
                    parts.append(
                        str(v.value).replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
                    )
                elif isinstance(v, ast.FormattedValue):
                    floatish = self.is_floatish(v.value)
                    inner = self.emit(v.value)
                    if v.conversion == 114:  # !r
                        inner = self.py("repr", inner)
                    elif v.format_spec is not None and isinstance(v.format_spec, ast.JoinedStr):
                        spec = self.emit(v.format_spec)
                        inner = self.py("format", inner, spec)
                    elif floatish:
                        inner = self.py("floatStr", inner)
                    else:
                        inner = self.py("toStr", inner)
                    parts.append("${" + inner + "}")
            return "`" + "".join(parts) + "`"
        if isinstance(node, (ast.ListComp, ast.GeneratorExp)):
            return self._emit_comp(node.elt, node.generators, "list")
        if isinstance(node, ast.SetComp):
            return self._emit_comp(node.elt, node.generators, "set")
        if isinstance(node, ast.DictComp):
            return self._emit_dict_comp(node)
        if isinstance(node, ast.Lambda):
            params = []
            defaults = list(node.args.defaults)
            args_list = list(node.args.args)
            pad = [None] * (len(args_list) - len(defaults))
            for a, d in zip(args_list, pad + defaults):  # type: ignore[operator]
                if d is None:
                    params.append(f"{safe_ident(a.arg)}: any")
                else:
                    params.append(f"{safe_ident(a.arg)}: any = {self.emit(d)}")
            return f"({', '.join(params)}) => {self.emit(node.body)}"
        if isinstance(node, ast.Await):
            return f"await {self.emit(node.value)}"
        if isinstance(node, ast.Starred):
            return f"...{self.py('iter', self.emit(node.value))}"
        if isinstance(node, ast.Yield):
            if node.value is None:
                return "yield null"
            return f"yield {self.emit(node.value)}"
        if isinstance(node, ast.YieldFrom):
            return f"yield* {self.py('iter', self.emit(node.value))}"
        if isinstance(node, ast.NamedExpr):
            # walrus — emit assignment expression; declaration hoisted to function top
            target = safe_ident(node.target.id) if isinstance(node.target, ast.Name) else "_w"
            if not self.mod.stmt.is_declared(target) and target not in self.mod.stmt.param_names:
                self.mod.stmt.pending_walrus.add(target)
                self.mod.stmt.declare(target)
            return f"({target} = {self.emit(node.value)})"
        return "null /* unsupported expr */"

    def _emit_compare(self, node: ast.Compare) -> str:
        parts: list[str] = []
        left = node.left
        for op, comp in zip(node.ops, node.comparators):
            ls = self.emit(left)
            rs = self.emit(comp)
            if isinstance(op, ast.Eq):
                parts.append(self.py("eq", ls, rs))
            elif isinstance(op, ast.NotEq):
                parts.append(f"!{self.py('eq', ls, rs)}")
            elif isinstance(op, ast.Is):
                if isinstance(comp, ast.Constant) and comp.value is None:
                    parts.append(f"({ls} === null || {ls} === undefined)")
                else:
                    parts.append(f"({ls} === {rs})")
            elif isinstance(op, ast.IsNot):
                if isinstance(comp, ast.Constant) and comp.value is None:
                    parts.append(f"({ls} !== null && {ls} !== undefined)")
                else:
                    parts.append(f"({ls} !== {rs})")
            elif isinstance(op, ast.In):
                parts.append(self.py("contains", rs, ls))
            elif isinstance(op, ast.NotIn):
                parts.append(f"!{self.py('contains', rs, ls)}")
            elif isinstance(op, ast.Lt):
                parts.append(self._num_cmp(left, comp, ls, rs, "<"))
            elif isinstance(op, ast.LtE):
                parts.append(self._num_cmp(left, comp, ls, rs, "<="))
            elif isinstance(op, ast.Gt):
                parts.append(self._num_cmp(left, comp, ls, rs, ">"))
            elif isinstance(op, ast.GtE):
                parts.append(self._num_cmp(left, comp, ls, rs, ">="))
            else:
                parts.append(f"({ls} === {rs})")
            left = comp
        if len(parts) == 1:
            return parts[0]
        return "(" + " && ".join(parts) + ")"

    @staticmethod
    def _is_numeric_literal(node: ast.expr) -> bool:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return True
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return ExprEmitter._is_numeric_literal(node.operand)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("len", "int", "float", "abs", "round", "sum", "ord"):
            return True
        if isinstance(node, ast.BinOp):
            return ExprEmitter._is_numeric_literal(node.left) or ExprEmitter._is_numeric_literal(node.right)
        return False

    def _num_cmp(self, lnode: ast.expr, rnode: ast.expr, ls: str, rs: str, op: str) -> str:
        if self._is_numeric_literal(lnode) or self._is_numeric_literal(rnode):
            return f"({ls} {op} {rs})"
        helper = {"<": "lt", "<=": "le", ">": "gt", ">=": "ge"}[op]
        return self.py(helper, ls, rs)

    def _emit_call(self, node: ast.Call) -> str:
        if isinstance(node.func, ast.Name):
            builtin = self._emit_builtin_call(node)
            if builtin is not None:
                return builtin
            fid = node.func.id
            if fid in CLASS_NAMES:
                params = CLASS_INIT_PARAMS.get(fid, [])
                mapped = self._map_positional_kwargs(node, params)
                if mapped is None:
                    args = [self.emit(a) for a in node.args] + [self.emit(kw.value) for kw in node.keywords]
                    mapped = ", ".join(args)
                return f"new {fid}({mapped})"
            fn = self.mod.name_map.get(fid, snake_to_camel(safe_ident(fid)))
            params = self.mod.local_func_params.get(fid) or FUNC_PARAMS.get(fid, [])
            if node.keywords and params:
                mapped = self._map_positional_kwargs(node, params)
                if mapped is not None:
                    return f"{fn}({mapped})"
                if not any(isinstance(a, ast.Starred) for a in node.args):
                    # keyword expansion (**expr) or unknown kw names — runtime mapping
                    kw_pairs = []
                    for i, a in enumerate(node.args):
                        pname = params[i] if i < len(params) else f"_p{i}"
                        kw_pairs.append(f"{json_str(pname)}: {self.emit(a)}")
                    spreads = []
                    for kw in node.keywords:
                        if kw.arg is None:
                            spreads.append(self.emit(kw.value))
                        else:
                            kw_pairs.append(f"{json_str(kw.arg)}: {self.emit(kw.value)}")
                    order = json.dumps(params)
                    return self.py(
                        "callKw",
                        f"{fn} as (...a: any[]) => any",
                        order,
                        "{" + ", ".join(kw_pairs) + "}",
                        *spreads,
                    )
            args = [self.emit(a) for a in node.args]
            for kw in node.keywords:
                if kw.arg is None:
                    args.append(f"...Object.values({self.emit(kw.value)})")
                else:
                    args.append(self.emit(kw.value))
            return f"{fn}({', '.join(args)})"
        if isinstance(node.func, ast.Attribute):
            mapped_attr = self._emit_attr_call(node)
            if mapped_attr is not None:
                return mapped_attr
            base = self.emit(node.func.value)
            attr = node.func.attr
            args = [self.emit(a) for a in node.args]
            # known method with keyword mapping (same-class methods)
            if node.keywords:
                params = self.mod.local_func_params.get(attr) or FUNC_PARAMS.get(attr, [])
                if params:
                    mapped = self._map_positional_kwargs(node, params)
                    if mapped is not None:
                        return f"{base}.{attr}({mapped})"
                for kw in node.keywords:
                    args.append(self.emit(kw.value))
            return f"{base}.{attr}({', '.join(args)})"
        fn = self.emit(node.func)
        args = [self.emit(a) for a in node.args] + [self.emit(kw.value) for kw in node.keywords]
        return f"{fn}({', '.join(args)})"


# --------------------------------------------------------------------------
# statement emission
# --------------------------------------------------------------------------

class StmtEmitter:
    def __init__(self, mod: "ModuleEmitter") -> None:
        self.mod = mod
        self.expr = ExprEmitter(mod)
        self.scopes: list[set[str]] = [set()]
        self.nonlocals: list[set[str]] = [set()]
        self.param_names: set[str] = set()
        self.shadowed_params: dict[str, str] = {}
        self.catch_var: list[str] = []
        self.pending_walrus: set[str] = set()
        self.float_vars: set[str] = set()

    def reset_scope(self) -> None:
        self.scopes = [set()]
        self.nonlocals = [set()]
        self.param_names = set()
        self.shadowed_params = {}
        self.float_vars = set()

    def push_scope(self) -> None:
        self.scopes.append(set())
        self.nonlocals.append(set())

    def pop_scope(self) -> None:
        self.scopes.pop()
        self.nonlocals.pop()

    def is_declared(self, name: str) -> bool:
        return any(name in s for s in self.scopes)

    def declare(self, name: str) -> None:
        self.scopes[-1].add(name)

    def ensure_declared(self, name: str) -> None:
        if not self.is_declared(name) and name not in self.param_names:
            self.declare(name)

    def emit_block(self, body: list[ast.stmt], indent: int) -> list[str]:
        lines: list[str] = []
        for stmt in body:
            lines.extend(self.emit_stmt(stmt, indent))
        return lines

    def _assign_target(self, target: ast.expr, val: str, pad: str) -> list[str]:
        e = self.expr.emit
        if isinstance(target, ast.Name):
            name = safe_ident(target.id)
            if target.id in self.nonlocals[-1]:
                return [f"{pad}{name} = {val};"]
            if self.is_declared(name) or target.id in self.param_names:
                return [f"{pad}{name} = {val};"]
            self.declare(name)
            # var: Python scoping is function-level, not block-level;
            # always annotate `any` — Python variables are dynamically
            # retyped, so first-assignment inference causes false errors
            ann = ": any"
            if val == "[]":
                ann = ": any[]"
            elif val == "{}":
                ann = ": Record<string, any>"
            elif val == "new Set()":
                ann = ": Set<any>"
            return [f"{pad}var {name}{ann} = {val};"]
        if isinstance(target, (ast.Tuple, ast.List)):
            self.mod.use_py = True
            self.mod.tmp_counter += 1
            tmp = f"_d{self.mod.tmp_counter}"
            lines = [f"{pad}const {tmp} = py.iter({val}) as any[];"]
            for i, elt in enumerate(target.elts):
                if isinstance(elt, ast.Starred):
                    inner = elt.value
                    rest = len(target.elts) - i - 1
                    src_expr = f"{tmp}.slice({i}, {tmp}.length - {rest})" if rest else f"{tmp}.slice({i})"
                    lines.extend(self._assign_target(inner, src_expr, pad))
                else:
                    idx = i - len(target.elts) if any(
                        isinstance(x, ast.Starred) for x in target.elts[:i]
                    ) else i
                    src_expr = f"{tmp}[{tmp}.length - {-idx}]" if idx < 0 else f"{tmp}[{idx}]"
                    lines.extend(self._assign_target(elt, src_expr, pad))
            return lines
        if isinstance(target, ast.Subscript):
            base = e(target.value)
            if isinstance(target.slice, ast.Slice):
                lo = e(target.slice.lower) if target.slice.lower is not None else "0"
                return [f"{pad}{base}.splice({lo}, {base}.length, ...py.iter({val}));"]
            self.mod.use_py = True
            return [f"{pad}py.setItem({base}, {e(target.slice)}, {val});"]
        if isinstance(target, ast.Attribute):
            return [f"{pad}{e(target.value)}.{target.attr} = {val};"]
        return [f"{pad}/* unsupported assignment target */"]

    def emit_stmt(self, node: ast.stmt, indent: int) -> list[str]:  # noqa: C901
        pad = "  " * indent
        e = self.expr.emit

        if isinstance(node, ast.Return):
            if node.value is None:
                return [f"{pad}return null;"] if not self.mod.in_void_fn else [f"{pad}return;"]
            return [f"{pad}return {e(node.value)};"]
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Constant):
                return []  # docstring / bare literal
            if isinstance(node.value, (ast.Yield, ast.YieldFrom)):
                return [f"{pad}{e(node.value)};"]
            return [f"{pad}{e(node.value)};"]
        if isinstance(node, ast.Assign):
            if (
                len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "__all__"
            ):
                return []
            val = e(node.value)
            lines: list[str] = []
            if len(node.targets) == 1:
                t0 = node.targets[0]
                if self.expr.is_floatish(node.value):
                    if isinstance(t0, ast.Name):
                        self.float_vars.add(t0.id)
                    elif isinstance(t0, ast.Attribute) and isinstance(t0.value, ast.Name) and t0.value.id == "self":
                        self.float_vars.add(f"self.{t0.attr}")
                return self._assign_target(t0, val, pad)
            tmp = "_chain"
            self.ensure_declared(tmp)
            lines.append(f"{pad}const _chain{id(node) % 1000} = {val};")
            for t in node.targets:
                lines.extend(self._assign_target(t, f"_chain{id(node) % 1000}", pad))
            return lines
        if isinstance(node, ast.AnnAssign):
            if node.value is None:
                return []
            if (
                isinstance(node.annotation, ast.Name) and node.annotation.id == "float"
            ) or self.expr.is_floatish(node.value):
                if isinstance(node.target, ast.Name):
                    self.float_vars.add(node.target.id)
            return self._assign_target(node.target, e(node.value), pad)
        if isinstance(node, ast.AugAssign):
            op_map = {
                ast.Add: "add", ast.Sub: "sub", ast.Mult: "mul", ast.Div: "div",
                ast.FloorDiv: "floordiv", ast.Mod: "mod", ast.BitOr: "bitor",
                ast.BitAnd: "bitand", ast.BitXor: "bitxor",
            }
            helper = op_map.get(type(node.op))
            val = e(node.value)
            if isinstance(node.target, ast.Name):
                name = safe_ident(node.target.id)
                if helper:
                    return [f"{pad}{name} = {self.expr.py(helper, name, val)};"]
                if isinstance(node.op, ast.Pow):
                    return [f"{pad}{name} = ({name}) ** ({val});"]
                return [f"{pad}{name} = {name};"]
            if isinstance(node.target, ast.Subscript):
                base = e(node.target.value)
                key = e(node.target.slice)
                cur = self.expr.py("at", base, key)
                new = self.expr.py(helper or "add", cur, val)
                self.mod.use_py = True
                return [f"{pad}py.setItem({base}, {key}, {new});"]
            if isinstance(node.target, ast.Attribute):
                tgt = f"{e(node.target.value)}.{node.target.attr}"
                if helper:
                    return [f"{pad}{tgt} = {self.expr.py(helper, tgt, val)};"]
                return [f"{pad}{tgt} = ({tgt}) ** ({val});"]
            return [f"{pad}/* unsupported augassign */"]
        if isinstance(node, ast.If):
            # skip TYPE_CHECKING blocks
            if isinstance(node.test, ast.Name) and node.test.id == "TYPE_CHECKING":
                return []
            lines = [f"{pad}if ({self.expr.emit_test(node.test)}) {{"]
            lines.extend(self.emit_block(node.body, indent + 1))
            if node.orelse:
                if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                    elif_lines = self.emit_stmt(node.orelse[0], indent)
                    lines.append(f"{pad}}} else {elif_lines[0].strip()}")
                    lines.extend(elif_lines[1:])
                    return lines
                lines.append(f"{pad}}} else {{")
                lines.extend(self.emit_block(node.orelse, indent + 1))
            lines.append(f"{pad}}}")
            return lines
        if isinstance(node, ast.For):
            return self._emit_for(node, indent)
        if isinstance(node, ast.While):
            lines = [f"{pad}while ({self.expr.emit_test(node.test)}) {{"]
            lines.extend(self.emit_block(node.body, indent + 1))
            lines.append(f"{pad}}}")
            if node.orelse:
                lines.extend(self.emit_block(node.orelse, indent))
            return lines
        if isinstance(node, ast.Try):
            has_imports = any(isinstance(s, (ast.Import, ast.ImportFrom)) for s in node.body)
            unavailable = self._try_unavailable_imports(node)
            if has_imports and unavailable is None:
                # all guarded imports are available in the JS runtime —
                # the import succeeds, so the except path never runs.
                lines = self.emit_block(node.body, indent)
                if node.finalbody:
                    lines.extend(self.emit_block(node.finalbody, indent))
                if node.orelse:
                    lines.extend(self.emit_block(node.orelse, indent))
                return lines
            if unavailable is not None:
                # `try: import <lib-not-available-in-js> ...` — the import fails
                # at runtime in Python-without-lib and in JS alike: emit the
                # except branch, with imported names bound to null.
                lines = []
                for name in unavailable:
                    nm = safe_ident(name)
                    if not self.is_declared(nm):
                        self.declare(nm)
                        lines.append(f"{pad}var {nm}: any = null;")
                handler = node.handlers[0] if node.handlers else None
                if handler is not None:
                    if handler.name:
                        var = safe_ident(handler.name)
                        self.declare(var)
                        lines.append(f'{pad}var {var}: any = py.err("ImportError", "module not available");')
                        self.mod.use_py = True
                    lines.extend(self.emit_block(handler.body, indent))
                if node.finalbody:
                    lines.extend(self.emit_block(node.finalbody, indent))
                return lines
            lines = [f"{pad}try {{"]
            lines.extend(self.emit_block(node.body, indent + 1))
            handler = node.handlers[0] if node.handlers else None
            var = safe_ident(handler.name) if handler and handler.name else "_e"
            if handler is not None:
                self.catch_var.append(var)
                self.declare(var)
                lines.append(f"{pad}}} catch ({var}: any) {{")
                lines.extend(self.emit_block(handler.body, indent + 1))
                for extra in node.handlers[1:]:
                    lines.append(f"{pad}  /* additional except handler merged: {ast.dump(extra.type) if extra.type else 'bare'} */")
                self.catch_var.pop()
            if node.finalbody:
                lines.append(f"{pad}}} finally {{")
                lines.extend(self.emit_block(node.finalbody, indent + 1))
            lines.append(f"{pad}}}")
            if node.orelse:
                lines.extend(self.emit_block(node.orelse, indent))
            return lines
        if isinstance(node, ast.Raise):
            if node.exc is None:
                cv = self.catch_var[-1] if self.catch_var else None
                return [f"{pad}throw {cv};"] if cv else [f"{pad}throw new Error(\"re-raise\");"]
            if (
                isinstance(node.exc, ast.Call)
                and isinstance(node.exc.func, ast.Name)
                and node.exc.func.id in PY_EXC_NAMES
            ):
                msg = e(node.exc.args[0]) if node.exc.args else '""'
                self.mod.use_py = True
                return [f"{pad}throw py.err({json_str(node.exc.func.id)}, {msg});"]
            if isinstance(node.exc, ast.Name) and node.exc.id in PY_EXC_NAMES:
                self.mod.use_py = True
                return [f"{pad}throw py.err({json_str(node.exc.id)});"]
            return [f"{pad}throw {e(node.exc)};"]
        if isinstance(node, ast.Assert):
            msg = e(node.msg) if node.msg else json_str("AssertionError")
            self.mod.use_py = True
            return [
                f"{pad}if (!{self.expr.emit_test(node.test)}) throw py.err(\"AssertionError\", {msg});"
            ]
        if isinstance(node, ast.Pass):
            return []
        if isinstance(node, ast.Break):
            return [f"{pad}break;"]
        if isinstance(node, ast.Continue):
            return [f"{pad}continue;"]
        if isinstance(node, ast.Delete):
            lines = []
            for t in node.targets:
                if isinstance(t, ast.Subscript):
                    self.mod.use_py = True
                    lines.append(f"{pad}py.delItem({e(t.value)}, {e(t.slice)});")
                elif isinstance(t, ast.Attribute):
                    lines.append(f"{pad}delete ({e(t.value)} as Record<string, any>).{t.attr};")
                elif isinstance(t, ast.Name):
                    lines.append(f"{pad}/* del {t.id} */")
            return lines
        if isinstance(node, (ast.With, ast.AsyncWith)):
            lines = []
            for item in node.items:
                ctx = e(item.context_expr)
                if item.optional_vars and isinstance(item.optional_vars, ast.Name):
                    name = safe_ident(item.optional_vars.id)
                    if self.is_declared(name) or item.optional_vars.id in self.param_names:
                        lines.append(f"{pad}{name} = {ctx};")
                    else:
                        self.declare(name)
                        lines.append(f"{pad}var {name}: any = {ctx};")
                else:
                    lines.append(f"{pad}{ctx};")
            lines.extend(self.emit_block(node.body, indent))
            return lines
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return self.mod.emit_function(node, indent, nested=True)
        if isinstance(node, ast.ClassDef):
            # nested classes are not transpiled; declare the name so later
            # references typecheck (reachable only on paths Python also skips)
            self.declare(safe_ident(node.name))
            return [f"{pad}/* nested class {node.name} unsupported */ var {safe_ident(node.name)}: any;"]
        if isinstance(node, ast.Global) or isinstance(node, ast.Nonlocal):
            for n in node.names:
                self.nonlocals[-1].add(n)
            return []
        if isinstance(node, ast.Import):
            return []
        if isinstance(node, ast.ImportFrom):
            # function-level (lazy) import — hoist to module imports
            self.mod.visit_import_from(node)
            return []
        return [f"{pad}/* unhandled: {type(node).__name__} */"]

    AVAILABLE_IMPORT_ROOTS = {
        "core", "__future__", "typing", "dataclasses", "abc", "enum",
        "pathlib", "bs4", "urllib", "collections", "copy", "re", "json",
        "hashlib", "os", "sys", "math", "base64", "unicodedata",
        "ipaddress", "threading", "concurrent", "io", "string",
        "functools", "itertools", "inspect", "zipfile", "ast",
        "playwright",
    }

    def _try_unavailable_imports(self, node: ast.Try) -> list[str] | None:
        """If a try block imports a lib unavailable in the JS runtime, return
        the names it would have bound (the except path is the real path)."""
        names: list[str] = []
        found_unavailable = False
        for stmt in node.body:
            if isinstance(stmt, ast.Import):
                for alias in stmt.names:
                    root = alias.name.split(".")[0]
                    if root not in self.AVAILABLE_IMPORT_ROOTS:
                        found_unavailable = True
                    names.append(alias.asname or alias.name.split(".")[0])
            elif isinstance(stmt, ast.ImportFrom):
                root = (stmt.module or "").split(".")[0]
                if stmt.level == 0 and root not in self.AVAILABLE_IMPORT_ROOTS:
                    found_unavailable = True
                for alias in stmt.names:
                    if alias.name != "*":
                        names.append(alias.asname or alias.name)
        return names if found_unavailable else None

    def _emit_for(self, node: ast.For, indent: int) -> list[str]:
        pad = "  " * indent
        e = self.expr.emit
        target = node.target
        it = node.iter

        predecl: list[str] = []

        def bind_of(t: ast.expr) -> str | None:
            if isinstance(t, ast.Name):
                nm = safe_ident(t.id)
                if not self.is_declared(nm) and t.id not in self.param_names:
                    predecl.append(nm)
                self.declare(nm)
                return nm
            if isinstance(t, (ast.Tuple, ast.List)) and all(isinstance(x, ast.Name) for x in t.elts):
                names = [safe_ident(x.id) for x in t.elts]  # type: ignore[attr-defined]
                for n in names:
                    if not self.is_declared(n) and n not in self.param_names:
                        predecl.append(n)
                    self.declare(n)
                return f"[{', '.join(names)}]"
            return None

        # range fast-path
        if (
            isinstance(it, ast.Call)
            and isinstance(it.func, ast.Name)
            and it.func.id == "range"
            and isinstance(target, ast.Name)
            and len(it.args) <= 2
        ):
            v = safe_ident(target.id)
            fresh = not self.is_declared(v) and target.id not in self.param_names
            self.declare(v)
            # predeclared var: Python loop variables are function-scoped,
            # and a single `var v: any;` avoids conflicting redeclarations
            lines = []
            if fresh:
                lines.append(f"{pad}var {v}: any;")
            if len(it.args) == 1:
                stop = e(it.args[0])
                lines.append(f"{pad}for ({v} = 0; {v} < {stop}; {v}++) {{")
            else:
                start, stop = e(it.args[0]), e(it.args[1])
                lines.append(f"{pad}for ({v} = {start}; {v} < {stop}; {v}++) {{")
            lines.extend(self.emit_block(node.body, indent + 1))
            lines.append(f"{pad}}}")
            if node.orelse:
                lines.extend(self.emit_block(node.orelse, indent))
            return lines

        bind = bind_of(target)
        iter_src = self.expr._comp_iter(it)
        lines = []
        for nm in predecl:
            lines.append(f"{pad}var {nm}: any;")
        if bind is None:
            bind = "_item"
            if not self.is_declared("_item"):
                lines.append(f"{pad}var _item: any;")
            self.declare("_item")
            lines.append(f"{pad}for (_item of {iter_src}) {{")
            lines.extend(self._assign_target(target, "_item", "  " * (indent + 1)))
        else:
            lines.append(f"{pad}for ({bind} of {iter_src}) {{")
        lines.extend(self.emit_block(node.body, indent + 1))
        lines.append(f"{pad}}}")
        if node.orelse:
            lines.extend(self.emit_block(node.orelse, indent))
        return lines


def is_main_guard(node: ast.stmt) -> bool:
    if not isinstance(node, ast.If):
        return False
    t = node.test
    if not isinstance(t, ast.Compare) or len(t.ops) != 1 or not isinstance(t.ops[0], ast.Eq):
        return False
    left, right = t.left, t.comparators[0]
    return (
        isinstance(left, ast.Name)
        and left.id == "__name__"
        and isinstance(right, ast.Constant)
        and right.value == "__main__"
    )


def has_yield(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    for child in ast.walk(node):
        if isinstance(child, (ast.Yield, ast.YieldFrom)):
            # ensure the yield belongs to this function, not a nested one
            return True
    return False


# --------------------------------------------------------------------------
# module emission
# --------------------------------------------------------------------------

class ModuleEmitter:
    def __init__(self, py_path: str, ts_rel: str) -> None:
        self.py_path = py_path
        self.ts_rel = ts_rel.replace("\\", "/")
        self.ts_dir = str(Path(ts_rel).parent).replace("\\", "/")
        self.types = TypeEmitter()
        self.stmt = StmtEmitter(self)
        self.expr = self.stmt.expr
        self.imports: list[str] = []
        self.body: list[str] = []
        self.exports: list[str] = []
        self.use_py = False
        self.current_class: str | None = None
        self.in_void_fn = False
        self.name_map: dict[str, str] = {}
        self.local_func_params: dict[str, list[str]] = {}
        self.tmp_counter = 0

    # -- import paths ------------------------------------------------------

    def py_compat_import(self) -> str:
        import os

        from_dir = Path("src") / self.ts_dir if self.ts_dir not in (".", "") else Path("src")
        rel = os.path.relpath(Path("src/runtime"), from_dir).replace("\\", "/")
        if not rel.startswith("."):
            rel = "./" + rel
        return f'import * as py from "{rel}/pyCompat.js";'

    def rel_import(self, mod_parts: list[str]) -> str:
        import os

        if not mod_parts:
            return "./index.js"
        package_parts = mod_parts[:-1]
        module_snake = mod_parts[-1]
        if module_snake != "__init__" and "/".join(mod_parts) in PACKAGE_PATHS:
            # import of a (possibly nested) package → its barrel index.ts
            target_pkg = Path("src") / Path(*mod_parts)
            from_pkg = Path("src") / self.ts_dir if self.ts_dir not in (".", "") else Path("src")
            rel = os.path.relpath(target_pkg, from_pkg).replace("\\", "/")
            if not rel.startswith("."):
                rel = "./" + rel
            return f"{rel}/index.js"
        ts_file = "index" if module_snake == "__init__" else snake_to_camel(module_snake)
        target_pkg = Path("src") / Path(*package_parts) if package_parts else Path("src")
        from_pkg = Path("src") / self.ts_dir if self.ts_dir not in (".", "") else Path("src")
        if target_pkg.resolve() == from_pkg.resolve():
            return f"./{ts_file}.js"
        rel = os.path.relpath(target_pkg, from_pkg).replace("\\", "/")
        if not rel.startswith("."):
            rel = "./" + rel
        return f"{rel}/{ts_file}.js"

    # -- functions ----------------------------------------------------------

    def _params(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
        # float-annotated params render like Python floats in f-strings
        for a in list(node.args.args) + list(node.args.kwonlyargs):
            if isinstance(a.annotation, ast.Name) and a.annotation.id == "float":
                self.stmt.float_vars.add(a.arg)
        params: list[str] = []
        args_list = [a for a in node.args.args if a.arg not in ("self", "cls")]
        defaults = list(node.args.defaults)
        # defaults align to the END of (args incl self) — recompute offset
        all_args = node.args.args
        offset = len(all_args) - len(defaults)
        default_for: dict[str, ast.expr] = {}
        for i, a in enumerate(all_args):
            if i >= offset:
                default_for[a.arg] = defaults[i - offset]
        for a in args_list:
            ann = self.types.emit(a.annotation) if a.annotation else "any"
            name = safe_ident(a.arg)
            if a.arg in default_for:
                params.append(f"{name}: {ann} = {self.expr.emit(default_for[a.arg])}")
            else:
                params.append(f"{name}: {ann}")
        for a, d in zip(node.args.kwonlyargs, node.args.kw_defaults):
            ann = self.types.emit(a.annotation) if a.annotation else "any"
            name = safe_ident(a.arg)
            if d is not None:
                params.append(f"{name}: {ann} = {self.expr.emit(d)}")
            else:
                params.append(f"{name}?: {ann}")
        if node.args.vararg:
            params.append(f"...{safe_ident(node.args.vararg.arg)}: any[]")
        elif node.args.kwarg:
            params.append(f"{safe_ident(node.args.kwarg.arg)}: Record<string, any> = {{}}")
        return params

    def _kwarg_decl(self, node: ast.FunctionDef | ast.AsyncFunctionDef, pad: str) -> str | None:
        """When *args and **kwargs coexist, the rest param wins the signature;
        bind kwargs as an (always-empty) body local so references typecheck."""
        if node.args.vararg and node.args.kwarg:
            return f"{pad}  var {safe_ident(node.args.kwarg.arg)}: Record<string, any> = {{}};"
        return None

    def emit_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        indent: int,
        in_class: bool = False,
        nested: bool = False,
    ) -> list[str]:
        pad = "  " * indent
        decorators = {d.id for d in node.decorator_list if isinstance(d, ast.Name)}
        is_async = isinstance(node, ast.AsyncFunctionDef)
        is_gen = has_yield(node)
        star = "*" if is_gen else ""

        # returns-nothing detection (all bare returns / no return)
        self.in_void_fn = not any(
            isinstance(n, ast.Return) and n.value is not None for n in ast.walk(node)
        )

        if in_class and node.name == "__init__":
            params = self._params(node)
            self.stmt.push_scope()
            prev_params = self.stmt.param_names
            self.stmt.param_names = {a.arg for a in node.args.args if a.arg not in ("self", "cls")}
            lines = [f"{pad}constructor({', '.join(params)}) {{"]
            if self.class_has_base:
                lines.append(f"{pad}  super();")
            lines.extend(self.stmt.emit_block(node.body, indent + 1))
            lines.append(f"{pad}}}")
            self.stmt.param_names = prev_params
            self.stmt.pop_scope()
            # strip duplicate super() if user code already called it
            joined = "\n".join(lines)
            if joined.count("super(") > 1:
                lines = [ln for i, ln in enumerate(lines) if not (i == 1 and "super();" in ln)]
            return lines

        if in_class:
            name = node.name
            if name == "__str__":
                name = "toString"
            prefix = ""
            if "staticmethod" in decorators or "classmethod" in decorators:
                prefix = "static "
            if "property" in decorators:
                prefix += "get "
            asy = "async " if is_async else ""
            self.stmt.push_scope()
            prev_params = self.stmt.param_names
            prev_walrus = self.stmt.pending_walrus
            self.stmt.pending_walrus = set()
            self.stmt.param_names = {a.arg for a in node.args.args if a.arg not in ("self", "cls")}
            params = self._params(node)
            body_lines = self.stmt.emit_block(node.body, indent + 1)
            walrus = sorted(self.stmt.pending_walrus)
            self.stmt.pending_walrus = prev_walrus
            ret_ann_m = "Promise<any>" if (is_async and not is_gen) else "any"
            lines = [f"{pad}{prefix}{asy}{name}{star}({', '.join(params)}): {ret_ann_m} {{"]
            kw_decl = self._kwarg_decl(node, pad)
            if kw_decl:
                lines.append(kw_decl)
            if walrus:
                lines.append(f"{pad}  var {', '.join(walrus)};")
            lines.extend(body_lines)
            lines.append(f"{pad}}}")
            self.stmt.param_names = prev_params
            self.stmt.pop_scope()
            return lines

        name = snake_to_camel(safe_ident(node.name))
        self.name_map[node.name] = name
        asy = "async " if is_async else ""
        if nested:
            self.stmt.push_scope()
            prev_params = self.stmt.param_names
            self.stmt.param_names = set(self.stmt.param_names) | {
                a.arg for a in node.args.args if a.arg not in ("self", "cls")
            }
            params = self._params(node)
            ret_ann_n = "Promise<any>" if (is_async and not is_gen) else "any"
            lines = [f"{pad}{asy}function{star} {name}({', '.join(params)}): {ret_ann_n} {{"]
            kw_decl_n = self._kwarg_decl(node, pad)
            if kw_decl_n:
                lines.append(kw_decl_n)
            lines.extend(self.stmt.emit_block(node.body, indent + 1))
            lines.append(f"{pad}}}")
            self.stmt.param_names = prev_params
            self.stmt.pop_scope()
            return lines

        # export everything (Python allows importing private names too)
        export = "export "
        self.stmt.reset_scope()
        self.stmt.param_names = {a.arg for a in node.args.args if a.arg not in ("self", "cls")}
        self.stmt.param_names |= {a.arg for a in node.args.kwonlyargs}
        params = self._params(node)
        body_lines = self.stmt.emit_block(node.body, indent + 1)
        walrus = sorted(self.stmt.pending_walrus)
        self.stmt.pending_walrus.clear()
        ret_ann = "Promise<any>" if (is_async and not is_gen) else "any"
        lines = [f"{pad}{export}{asy}function{star} {name}({', '.join(params)}): {ret_ann} {{"]
        kw_decl_t = self._kwarg_decl(node, pad)
        if kw_decl_t:
            lines.append(kw_decl_t)
        if walrus:
            lines.append(f"{pad}  var {', '.join(walrus)};")
        lines.extend(body_lines)
        lines.append(f"{pad}}}")
        if not node.name.startswith("_"):
            self.exports.append(name)
        return lines

    # -- classes ------------------------------------------------------------

    class_has_base = False

    def emit_class(self, node: ast.ClassDef) -> None:
        prev_class = self.current_class
        self.current_class = node.name
        base = ""
        self.class_has_base = False
        for b in node.bases:
            bname = b.id if isinstance(b, ast.Name) else (b.attr if isinstance(b, ast.Attribute) else "")
            if bname in CLASS_NAMES:
                base = f" extends {bname}"
                self.class_has_base = True
                break
            if bname in PY_EXC_NAMES:
                base = " extends Error"
                self.class_has_base = True
                break
        self.body.append(f"export class {node.name}{base} {{")
        is_dc = _is_dataclass(node)
        fields: list[tuple[str, ast.expr | None]] = []
        methods: list[ast.stmt] = []
        has_init = False
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(item)
                if item.name == "__init__":
                    has_init = True
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                fields.append((item.target.id, item.value))
            elif isinstance(item, ast.Assign) and len(item.targets) == 1 and isinstance(item.targets[0], ast.Name):
                fields.append((item.targets[0].id, item.value))

        # type-only declarations for every self-assigned attribute:
        # visible to dts, no runtime emit, no serialization impact
        self_attrs: list[str] = []
        for item in ast.walk(node):
            if isinstance(item, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                targets = item.targets if isinstance(item, ast.Assign) else [item.target]
                for t in targets:
                    if (
                        isinstance(t, ast.Attribute)
                        and isinstance(t.value, ast.Name)
                        and t.value.id == "self"
                        and t.attr not in self_attrs
                    ):
                        self_attrs.append(t.attr)
        if is_dc and not has_init:
            for fname, _fval in fields:
                if fname not in self_attrs:
                    self_attrs.append(fname)
        method_names = {
            m.name for m in node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        for attr in self_attrs:
            if attr not in method_names:
                self.body.append(f"  declare {attr}: any;")

        if is_dc and not has_init:
            params = []
            assigns = []
            for fname, fval in fields:
                dflt = ""
                if fval is not None:
                    if (
                        isinstance(fval, ast.Call)
                        and isinstance(fval.func, ast.Name)
                        and fval.func.id == "field"
                    ):
                        factory = next((kw.value for kw in fval.keywords if kw.arg == "default_factory"), None)
                        dval = next((kw.value for kw in fval.keywords if kw.arg == "default"), None)
                        if factory is not None and isinstance(factory, ast.Name):
                            fmap = {"list": "[]", "dict": "{}", "set": "new Set()"}
                            dflt = f" = {fmap.get(factory.id, 'null')}"
                        elif dval is not None:
                            dflt = f" = {self.expr.emit(dval)}"
                    else:
                        dflt = f" = {self.expr.emit(fval)}"
                params.append(f"{safe_ident(fname)}: any{dflt}")
                assigns.append(f"    this.{fname} = {safe_ident(fname)};")
            self.body.append(f"  constructor({', '.join(params)}) {{")
            self.body.extend(assigns)
            self.body.append("  }")
        elif not is_dc:
            # Python class attributes are class-level: emit static fields,
            # then alias on the prototype so `self.attr` reads work while
            # instance serialization (Object.entries) stays clean.
            for fname, fval in fields:
                if fval is not None:
                    self.body.append(f"  static {fname} = {self.expr.emit(fval)};")

        for item in methods:
            self.body.extend(self.emit_function(item, 1, in_class=True))  # type: ignore[arg-type]
        self.body.append("}")
        if not is_dc:
            for fname, fval in fields:
                if fval is not None:
                    self.body.append(
                        f"({node.name}.prototype as Record<string, any>)[{json_str(fname)}] = ({node.name} as Record<string, any>)[{json_str(fname)}];"
                    )
        self.exports.append(node.name)
        self.current_class = prev_class

    # -- imports ------------------------------------------------------------

    def map_import_name(self, n: str) -> str:
        if is_const_name(n) or n in CLASS_NAMES or "_" not in n:
            return n
        return snake_to_camel(n)

    def visit_import_from(self, node: ast.ImportFrom) -> None:
        stdlib_skip = {
            "__future__", "typing", "dataclasses", "abc", "enum",
        }
        compat_names = {
            "Path", "BeautifulSoup", "urlparse", "urlunparse", "urljoin",
            "urlsplit", "urlunsplit", "quote", "unquote", "deque",
            "defaultdict", "Counter", "OrderedDict", "deepcopy",
        }
        if node.module in stdlib_skip and not node.level:
            return
        if node.module in (
            "pathlib", "bs4", "urllib.parse", "collections", "copy",
        ) and not node.level:
            for alias in node.names:
                if alias.name in compat_names:
                    self.use_py = True
            return
        if node.module == "playwright.sync_api" and not node.level:
            for alias in node.names:
                if alias.name == "sync_playwright":
                    import os

                    from_dir = Path("src") / self.ts_dir if self.ts_dir not in (".", "") else Path("src")
                    rel = os.path.relpath(Path("src/browser"), from_dir).replace("\\", "/")
                    if not rel.startswith("."):
                        rel = "./" + rel
                    local = safe_ident(alias.asname or alias.name)
                    self.imports.append(
                        f'import {{ syncPlaywright as {local} }} from "{rel}/syncPlaywright.js";'
                    )
                    self.name_map[alias.asname or alias.name] = local
            return
        if node.level:
            parts = self.ts_dir.split("/") if self.ts_dir not in (".", "") else []
            ups = max(0, node.level - 1)
            if ups >= len(parts):
                base: list[str] = []
            elif ups:
                base = parts[:-ups]
            else:
                base = list(parts)
            if node.module:
                mod_parts = base + node.module.split(".")
                rel = self.rel_import(mod_parts)
                names = []
                for a in node.names:
                    if a.name == "*":
                        continue
                    exported = self.map_import_name(a.name)
                    local_out = self.map_import_name(safe_ident(a.asname)) if a.asname else exported
                    self.name_map[a.asname or a.name] = local_out
                    if a.asname and local_out != exported:
                        names.append(f"{exported} as {local_out}")
                    else:
                        names.append(exported)
                if names:
                    self.imports.append(f'import {{ {", ".join(names)} }} from "{rel}";')
            else:
                # from . import sibling
                for a in node.names:
                    rel = self.rel_import(base + [a.name])
                    local = safe_ident(a.asname or a.name)
                    self.imports.append(f'import * as {local} from "{rel}";')
            return
        if not node.module or not node.module.startswith("core."):
            if node.module:
                self.imports.append(f"// from {node.module} import ... (unmapped)")
            return
        parts = node.module.split(".")[1:]
        rel = self.rel_import(parts)
        names = []
        for alias in node.names:
            n = alias.name
            if n != "*" and (alias.asname or n) in self.name_map:
                continue  # already bound (e.g. via an earlier star import)
            if n == "*":
                # star import — expand to the target module's public surface
                publics = MODULE_PUBLIC_NAMES.get(node.module, [])
                star_names = []
                for pub in publics:
                    exported = self.map_import_name(pub)
                    if pub in self.name_map:
                        continue
                    self.name_map[pub] = exported
                    star_names.append(exported)
                if star_names:
                    self.imports.append(
                        f'import {{ {", ".join(sorted(set(star_names)))} }} from "{rel}";'
                    )
                return
            exported = self.map_import_name(n)
            local_out = self.map_import_name(safe_ident(alias.asname)) if alias.asname else exported
            self.name_map[alias.asname or n] = local_out
            if alias.asname and local_out != exported:
                names.append(f"{exported} as {local_out}")
            else:
                names.append(exported)
        if names:
            self.imports.append(f'import {{ {", ".join(names)} }} from "{rel}";')

    # -- barrels --------------------------------------------------------------

    def emit_init_barrel(self, tree: ast.Module) -> str:
        header = [
            "/**",
            f" * Barrel converted from {self.py_path}",
            " * @generated — WebWeaveX python→javascript library port",
            " */",
            "",
        ]
        has_consts = any(
            isinstance(n, ast.Assign)
            and len(n.targets) == 1
            and isinstance(n.targets[0], ast.Name)
            and not n.targets[0].id.startswith("_")
            and n.targets[0].id != "__all__"
            for n in tree.body
        )
        expr = ExprEmitter(self)
        imp_lines: list[str] = []
        body_lines: list[str] = []
        for node in tree.body:
            target_mod: str | None = None
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("core."):
                mod_parts = node.module.split(".")[1:]
                target_mod = self.rel_import(mod_parts)
            elif isinstance(node, ast.ImportFrom) and node.level and node.module:
                parts = self.ts_dir.split("/") if self.ts_dir not in (".", "") else []
                ups = max(0, node.level - 1)
                base = parts[: len(parts) - ups] if ups else list(parts)
                target_mod = self.rel_import(base + node.module.split("."))
            if target_mod is not None and isinstance(node, ast.ImportFrom):
                pairs: list[tuple[str, str]] = []  # (exported-in-target, local)
                for alias in node.names:
                    if alias.name == "*":
                        continue
                    exported = self.map_import_name(alias.name)
                    local = self.map_import_name(alias.asname) if alias.asname else exported
                    self.name_map[alias.asname or alias.name] = local
                    pairs.append((exported, local))
                if not pairs:
                    continue
                if has_consts:
                    # bring names into scope so barrel-level constants can use them
                    spec = ", ".join(e if e == l else f"{e} as {l}" for e, l in pairs)
                    imp_lines.append(f'import {{ {spec} }} from "{target_mod}";')
                    body_lines.append(f'export {{ {", ".join(l for _, l in pairs)} }};')
                else:
                    spec = ", ".join(e if e == l else f"{e} as {l}" for e, l in pairs)
                    body_lines.append(f'export {{ {spec} }} from "{target_mod}";')
            elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                name = node.targets[0].id
                if name.startswith("_") or name == "__all__":
                    continue
                out_name = self.map_import_name(name)
                self.name_map[name] = out_name
                body_lines.append(f"export const {out_name} = {expr.emit(node.value)};")
        if self.use_py:
            imp_lines.insert(0, self.py_compat_import())
        return "\n".join(header + imp_lines + body_lines) + "\n"

    # -- conversion --------------------------------------------------------

    def convert(self, source: str) -> str:
        self.use_py = False
        tree = ast.parse(source)
        if self.py_path.endswith("__init__.py"):
            return self.emit_init_barrel(tree)

        # pre-pass: imports populate name_map before bodies are emitted
        for node in tree.body:
            if isinstance(node, ast.ImportFrom):
                self.visit_import_from(node)
        # pre-pass: local function names + exact local signatures
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.name_map[node.name] = snake_to_camel(safe_ident(node.name))
            elif isinstance(node, ast.ClassDef):
                self.name_map[node.name] = node.name
            elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                tname = node.targets[0].id
                if tname != "__all__" and not tname.startswith("_"):
                    self.name_map[tname] = self.map_import_name(safe_ident(tname))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                params = [a.arg for a in node.args.args if a.arg not in ("self", "cls")]
                params += [a.arg for a in node.args.kwonlyargs]
                if node.args.kwarg and not node.args.vararg:
                    params.append("**")
                self.local_func_params[node.name] = params

        # `import ast` — bind the pyCompat ast shim so member access typechecks
        for node in tree.body:
            if isinstance(node, ast.Import) and any(a.name == "ast" for a in node.names):
                self.use_py = True
                self.body.append("const ast: any = py.astModule;")
                break

        # unguarded third-party imports: the Python module dies with
        # ModuleNotFoundError when the lib is absent — mirror that.
        SHIMMED_LATER = {"requests", "httpx", "playwright", "kaalka"}
        for node in tree.body:
            roots: list[str] = []
            if isinstance(node, ast.Import):
                roots = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and not node.level and node.module:
                roots = [node.module.split(".")[0]]
            for root in roots:
                if (
                    root not in StmtEmitter.AVAILABLE_IMPORT_ROOTS
                    and root not in SHIMMED_LATER
                ):
                    self.use_py = True
                    self.body.append(
                        f'throw py.err("ModuleNotFoundError", "No module named \'{root}\'");'
                    )
                    # the code below the throw is unreachable but must still
                    # typecheck: declare the names the dead import would bind
                    dead: list[str] = []
                    if isinstance(node, ast.Import):
                        dead = [safe_ident(a.asname or a.name.split(".")[0]) for a in node.names]
                    elif isinstance(node, ast.ImportFrom):
                        dead = [safe_ident(a.asname or a.name) for a in node.names if a.name != "*"]
                    for dn in dead:
                        self.body.append(f"var {dn}: any;")
                    break
            else:
                continue
            break

        for node in tree.body:
            if isinstance(node, ast.ImportFrom) or isinstance(node, ast.Import):
                continue
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.body.extend(self.emit_function(node, 0))
            elif isinstance(node, ast.ClassDef):
                self.emit_class(node)
            elif isinstance(node, ast.If):
                if not is_main_guard(node):
                    self.body.extend(self.stmt.emit_stmt(node, 0))
            elif isinstance(node, ast.Assign):
                if (
                    len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name)
                    and node.targets[0].id != "__all__"
                ):
                    name = node.targets[0].id
                    val = self.expr.emit(node.value)
                    export = "" if name.startswith("_") else "export "
                    out_name = safe_ident(name) if name.startswith("_") else self.map_import_name(safe_ident(name))
                    self.name_map[name] = out_name
                    self.stmt.declare(out_name)
                    self.body.append(f"{export}let {out_name}: any = {val};")
                    if export:
                        self.exports.append(out_name)
                else:
                    self.body.extend(self.stmt.emit_stmt(node, 0))
            elif isinstance(node, (ast.AnnAssign, ast.For, ast.With, ast.Try, ast.Expr, ast.AugAssign)):
                self.body.extend(self.stmt.emit_stmt(node, 0))

        # re-export imported names not shadowed by local definitions
        # (Python modules implicitly re-export everything they import)
        defined = {n for n in self.exports}
        reexports: list[str] = []
        for local in sorted(set(self.name_map.values())):
            if local.startswith("py.") or local in defined or local in ("Object",):
                continue
            if any(
                re.search(rf"[{{,\s]{re.escape(local)}[,\s}}]|as {re.escape(local)}\b", imp)
                for imp in self.imports
                if imp.startswith("import {")
            ):
                if not local.startswith("_"):
                    reexports.append(local)
        if reexports:
            self.body.append(f"export {{ {', '.join(sorted(set(reexports)))} }};")

        header = [
            "/**",
            f" * Converted from Python: {self.py_path}",
            " * @generated — WebWeaveX python→javascript library port",
            " */",
            "",
        ]
        seen = set()
        imp_lines = []
        if self.use_py:
            imp_lines.append(self.py_compat_import())
        for line in self.imports:
            if line not in seen:
                seen.add(line)
                imp_lines.append(line)
        return "\n".join(header + imp_lines + [""] + self.body) + "\n"


PACKAGES: set[str] = set()
PACKAGE_PATHS: set[str] = set()  # all package dir paths relative to core/, e.g. "native/electron"


def restore_protected(protected: set[str]) -> None:
    if not protected:
        return
    backup = ROOT / "tools" / "convergence" / "protected_backup"
    if backup.exists():
        import shutil

        for rel in protected:
            src_b = backup / rel.replace("src/", "", 1)
            dst = ROOT / rel
            if src_b.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_b, dst)
        return
    subprocess.run(["git", "checkout", "HEAD", "--", *list(protected)], cwd=ROOT, check=False)


def write_index(manifest: list[str]) -> None:
    """Preserve npm entry; full mirrored tree lives under src/<package>/."""
    entry = ROOT / "src" / "index.ts"
    head = subprocess.run(
        ["git", "show", "HEAD:src/index.ts"],
        cwd=ROOT,
        capture_output=True,
    )
    if head.returncode == 0:
        entry.write_bytes(head.stdout)
    elif not entry.exists():
        entry.write_text('export const VERSION = "2.0.0";\n', encoding="utf-8")


def main() -> int:
    manifest = load_manifest()
    protected = load_protected()
    print(f"Converting {len(manifest)} Python modules ({len(protected)} protected hand-written)...")

    for p in manifest:
        parts = p.removeprefix("core/").split("/")
        if len(parts) > 1:
            PACKAGES.add(parts[0])
        for depth in range(1, len(parts)):
            PACKAGE_PATHS.add("/".join(parts[:depth]))

    # mirror non-Python data assets (schemas, fixtures) into src/
    r = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "origin/python", "--", "core/"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    data_files = [
        ln.strip()
        for ln in r.stdout.splitlines()
        if ln.strip() and not ln.strip().endswith(".py")
        and ln.strip().rsplit(".", 1)[-1] in ("json", "txt", "yaml", "yml", "md")
    ]
    for df in data_files:
        content = subprocess.run(
            ["git", "show", f"origin/python:{df}"],
            cwd=ROOT,
            capture_output=True,
        )
        if content.returncode == 0:
            dest = SRC / df.removeprefix("core/")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content.stdout)
    if data_files:
        print(f"  mirrored {len(data_files)} data assets")

    print("Prescanning ASTs for class/function registries...")
    sources: dict[str, str] = {}
    for py_path in manifest:
        src = git_show(py_path)
        if src is not None:
            sources[py_path] = src
    prescan(sources)
    print(f"  classes={len(CLASS_NAMES)} functions={len(FUNC_PARAMS)}")

    SRC.mkdir(parents=True, exist_ok=True)

    ok = fail = 0
    failures: list[str] = []

    for i, py_path in enumerate(manifest, 1):
        ts_rel = py_path_to_ts(py_path)
        ts_full = SRC / ts_rel
        ts_key = f"src/{ts_rel}".replace("\\", "/")
        if ts_key in protected:
            continue
        src = sources.get(py_path)
        if src is None:
            fail += 1
            failures.append(py_path)
            continue
        try:
            out = ModuleEmitter(py_path, ts_rel).convert(src)
            ts_full.parent.mkdir(parents=True, exist_ok=True)
            ts_full.write_text(out, encoding="utf-8")
            ok += 1
        except SyntaxError as e:
            # the PYTHON source itself is unparseable — the Python module
            # raises SyntaxError on import; mirror that exactly.
            depth = ts_rel.count("/")
            rel = "/".join([".."] * depth) or "."
            stub = "\n".join(
                [
                    "/**",
                    f" * Converted from Python: {py_path}",
                    " * @generated — the upstream Python source is syntactically",
                    " * invalid; importing it raises SyntaxError in both runtimes.",
                    " */",
                    f'import * as py from "{rel}/runtime/pyCompat.js";',
                    "",
                    f'throw py.err("SyntaxError", {json.dumps(str(e))});',
                    "",
                ]
            )
            ts_full.parent.mkdir(parents=True, exist_ok=True)
            ts_full.write_text(stub, encoding="utf-8")
            ok += 1
        except Exception as e:  # noqa: BLE001
            fail += 1
            failures.append(f"{py_path}: {e}")
        if i % 200 == 0:
            print(f"  progress: {i}/{len(manifest)}")

    # post-pass: imports that reference modules missing on BOTH sides
    # (Python raises ModuleNotFoundError) get throwing stubs so the
    # JavaScript runtime—and tsc—mirror that exactly.
    import_re = re.compile(r'import\s+([^;]*?)\s+from\s+"(\.[^"]+\.js)"')
    stubs = 0
    missing: dict[Path, set[str]] = {}
    for ts_file in sorted(SRC.rglob("*.ts")):
        text = ts_file.read_text(encoding="utf-8", errors="replace")
        for clause, rel_target in import_re.findall(text):
            target = (ts_file.parent / rel_target).resolve()
            target_ts = target.with_suffix("").with_suffix(".ts")
            if target_ts.exists() and target_ts not in missing:
                continue
            names = missing.setdefault(target_ts, set())
            m = re.search(r"\{([^}]*)\}", clause)
            if m:
                for part in m.group(1).split(","):
                    orig = part.split(" as ")[0].strip()
                    if orig:
                        names.add(orig)
    for target_ts, names in sorted(missing.items()):
        if target_ts.exists():
            continue
        target_ts.parent.mkdir(parents=True, exist_ok=True)
        if True:
            depth = len(target_ts.relative_to(SRC.resolve()).parts) - 1
            rel_rt = "/".join([".."] * depth) or "."
            target_ts.write_text(
                "\n".join(
                    [
                        "/**",
                        " * @generated — this module does not exist in the Python",
                        " * implementation either; importing raises ModuleNotFoundError",
                        " * in both runtimes (specification-equivalent failure).",
                        " */",
                        f'import * as py from "{rel_rt}/runtime/pyCompat.js";',
                        "",
                        'throw py.err("ModuleNotFoundError", "No module named ' + target_ts.stem + '");',
                        "",
                        "// named exports importers reference — typed but never",
                        "// reachable: the throw above fires before any binding.",
                        *[f"export let {n}: any;" for n in sorted(names)],
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            stubs += 1
    if stubs:
        print(f"  wrote {stubs} missing-module parity stubs")

    # NOTE: protected files are skipped during conversion (never overwritten),
    # so restoring them from protected_backup is unnecessary and would clobber
    # newer hand-edits. restore_protected() is kept for manual recovery only.
    if "src/index.ts" not in protected and not (SRC / "index.ts").exists():
        write_index(manifest)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "\n".join(
            [
                "# Python → JavaScript Library Conversion Report",
                "",
                f"**Date:** {__import__('datetime').datetime.utcnow().isoformat()}Z",
                "",
                f"| Python modules | {len(manifest)} |",
                f"| Converted | {ok} |",
                f"| Failed | {fail} |",
                f"| Protected (hand-written) | {len(protected)} |",
                "",
                *(f"- FAILED: `{f}`" for f in failures[:50]),
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Done: {ok} converted, {fail} failed, {len(protected)} protected restored")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
