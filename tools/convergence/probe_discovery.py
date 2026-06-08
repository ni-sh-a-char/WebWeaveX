#!/usr/bin/env python3
"""Discover symbols and generate probe argument sets for Python/TS modules."""
from __future__ import annotations

import ast
import inspect
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STAGING = ROOT / "tools" / "runtime_vectors" / ".py_staging"


def read_python_source(py_path: Path) -> str:
    """UTF-8 with BOM strip — materialized origin/python archives often include BOM."""
    return py_path.read_text(encoding="utf-8-sig", errors="replace").replace("\x00", "")


def py_path_to_module(py_path: str) -> str:
    rel = py_path.removeprefix("core/").removesuffix(".py").replace("/", ".")
    if rel.endswith(".__init__"):
        rel = rel[: -len(".__init__")]
    return f"core.{rel}" if rel else "core"


def discover_init_exports(py_path: Path) -> list[str]:
    """Public symbols re-exported from a package __init__.py."""
    try:
        tree = ast.parse(read_python_source(py_path))
    except SyntaxError:
        return []
    stdlib_skip = {"__future__", "typing", "dataclasses", "abc", "enum", "collections", "pathlib"}
    out: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            if node.module in stdlib_skip and not node.level:
                continue
            for alias in node.names:
                if alias.name != "*":
                    out.append(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            continue  # plain stdlib imports are not re-exported surface
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and not t.id.startswith("_"):
                    out.append(t.id)
    return out


def discover_python_functions(py_path: Path) -> list[str]:
    try:
        tree = ast.parse(read_python_source(py_path))
    except SyntaxError:
        return []
    out: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
            out.append(node.name)
    if not out:
        preferred = ("to_dict", "build", "run", "execute", "create", "from_dict")
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                base_names = {
                    b.id if isinstance(b, ast.Name) else (b.attr if isinstance(b, ast.Attribute) else "")
                    for b in node.bases
                }
                if base_names & {"Protocol", "ABC", "Enum", "IntEnum", "StrEnum"}:
                    continue
                publics = [
                    item.name
                    for item in node.body
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and not item.name.startswith("_")
                ]
                for name in preferred:
                    if name in publics:
                        out.append(f"{node.name}.{name}")
                        break
                else:
                    if publics:
                        out.append(f"{node.name}.{publics[0]}")
                    else:
                        # attribute-only class — instantiate and compare state
                        out.append(f"{node.name}.__instance__")
    return out


def discover_module_constants(py_path: Path) -> list[str]:
    """Public module-level constants for constants-only modules."""
    try:
        tree = ast.parse(read_python_source(py_path))
    except SyntaxError:
        return []
    out: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if not name.startswith("_") and name != "__all__":
                out.append(name)
    return out


def discover_ts_exports(ts_path: Path) -> list[str]:
    import re

    text = ts_path.read_text(encoding="utf-8", errors="replace")
    out: list[str] = []
    for m in re.finditer(r"^export (?:async )?function\*? (\w+)", text, re.M):
        out.append(m.group(1))
    for m in re.finditer(r"^export (?:abstract )?class (\w+)", text, re.M):
        out.append(m.group(1))
    for m in re.finditer(r"^export (?:const|let|var) (\w+)", text, re.M):
        out.append(m.group(1))
    for m in re.finditer(r"^export \{([^}]+)\}", text, re.M):
        for part in m.group(1).split(","):
            part = part.strip()
            if not part:
                continue
            name = part.split(" as ")[-1].strip()
            out.append(name)
    return out


def py_name_to_ts_export(py_name: str) -> str:
    if "." in py_name:
        _, meth = py_name.split(".", 1)
        parts = meth.split("_")
        return parts[0] + "".join(p.capitalize() for p in parts[1:])
    parts = py_name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def resolve_python_callable(mod: Any, symbol: str) -> Any:
    if "." not in symbol:
        return getattr(mod, symbol)
    class_name, method_name = symbol.split(".", 1)
    cls = getattr(mod, class_name)
    if method_name == "__instance__":
        return cls
    raw = inspect.getattr_static(cls, method_name, None)
    if isinstance(raw, (staticmethod, classmethod)):
        return getattr(cls, method_name)
    # instance method — instantiate with guessed ctor args and bind
    kwargs: dict[str, Any] = {}
    try:
        for pname, param in inspect.signature(cls).parameters.items():
            if param.kind in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL):
                continue
            kwargs[pname] = guess_arg(pname, param.annotation)
    except (ValueError, TypeError):
        kwargs = {}
    instance = cls(**kwargs)
    return getattr(instance, method_name)


def guess_arg(name: str, annotation: Any = inspect.Parameter.empty) -> Any:
    ann = ""
    if annotation is not inspect.Parameter.empty:
        ann = str(annotation).lower().replace("typing.", "")
    if "list[" in ann or ann.startswith("list") or "sequence[" in ann:
        return []
    if "dict" in ann or "mapping" in ann:
        return {}
    if "int" in ann and "hint" not in ann:
        return 0
    if "float" in ann:
        return 0.0
    if "bool" in ann:
        return False
    n = name.lower()
    if n in ("budget", "parser_budget"):
        return None
    if n in ("url", "seed", "href", "link"):
        return "http://127.0.0.1:8787/probe"
    if n in ("path", "filepath", "file_path", "src_path", "dest_path", "output_path", "input_path"):
        return str(ROOT / "tools" / "runtime_vectors" / "probe_fixture.txt")
    if n in ("html", "dom", "content", "text", "payload", "data"):
        return "<div id='probe'>x</div>"
    if n in ("key", "token", "secret", "name", "id", "worker_id", "task_id"):
        return "probe_id"
    if "selector" in n:
        return ".next"
    if "hash" in n or n.endswith("_id"):
        return "probe_hash"
    if n in ("tick", "index", "order", "priority", "retries", "cooldown", "max_steps", "limit"):
        return 0
    if n in ("count", "depth", "size"):
        return 1
    if n.startswith("is_") or n in ("bounded", "enabled", "active", "valid"):
        return False
    if n in ("states", "tasks", "workers", "nodes", "edges", "events", "steps", "entities", "history"):
        return []
    if n.endswith("_nodes") or n.endswith("_fields"):
        return []
    if n in ("state", "memory", "graph", "plan", "envelope", "session", "identity", "schema", "sources", "process", "proc", "bundle", "record", "event", "task", "node", "frame"):
        return {}
    if n == "snapshot":
        # deterministic connector snapshots — avoids live-filesystem walks
        return {"filesystem": {"root": "probe", "files": []}}
    if n in (
        "adaptation",
        "config",
        "options",
        "metadata",
        "context",
        "runtime",
        "page",
        "sources",
        "ir",
        "runtime_ir",
        "runtime_graph",
        "unified_runtime_graph",
    ):
        return {}
    if n in ("entities", "instructions", "adaptive_states", "runtime_graphs"):
        return []
    return "probe"


def build_probe_args(func: Any) -> list[dict[str, Any]]:
    """Return probe variants: minimal, normal, edge."""
    try:
        sig = inspect.signature(func)
    except (ValueError, TypeError):
        return [{}]

    def build_one(extra: dict[str, Any] | None = None) -> dict[str, Any]:
        args: dict[str, Any] = {}
        for pname, param in sig.parameters.items():
            if param.kind in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL):
                continue
            if param.default is not inspect.Parameter.empty and extra is None:
                continue
            args[pname] = guess_arg(pname, param.annotation)
        if extra:
            args.update(extra)
        return args

    extra: dict[str, Any] = {}
    for pname in sig.parameters:
        if pname == "tick":
            extra["tick"] = 1
            break
    variants = [build_one(), build_one(extra) if extra else build_one(), build_one({})]
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for v in variants:
        key = json.dumps(v, sort_keys=True, default=str)
        if key not in seen:
            seen.add(key)
            unique.append(v)
    return unique[:5]


def _normalize_compare(value: Any) -> Any:
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, dict):
        return {str(k): _normalize_compare(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize_compare(v) for v in value]
    return value


def stable_hash(value: Any) -> str:
    import hashlib

    body = json.dumps(
        _normalize_compare(value),
        sort_keys=True,
        default=str,
        separators=(",", ":"),
    )
    return hashlib.sha256(body.encode("utf-8")).hexdigest()
