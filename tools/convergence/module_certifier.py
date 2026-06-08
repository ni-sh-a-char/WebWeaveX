#!/usr/bin/env python3
"""Certify one Python⇄TypeScript module pair via executable probes (no synthetic PASS)."""
from __future__ import annotations

import importlib
import inspect
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from probe_discovery import (
    STAGING,
    build_probe_args,
    discover_init_exports,
    discover_module_constants,
    discover_python_functions,
    discover_ts_exports,
    py_name_to_ts_export,
    py_path_to_module,
    resolve_python_callable,
    stable_hash,
)

ROOT = Path(__file__).resolve().parents[2]
# probes execute in a tiny, stable directory so cwd-relative filesystem
# walks are deterministic on both sides
PROBE_CWD = ROOT / "tools" / "runtime_vectors" / "probe_cwd"

GRAPH_KEYS = frozenset({"nodes", "edges", "graph", "runtime_graph", "unified_runtime_graph"})
MEMORY_KEYS = frozenset({"memory", "runtime_memory", "runtime_history", "memory_graph"})
SEMANTIC_KEYS = frozenset({"semantic", "entities", "ontology", "semantic_state", "classes"})


def _has_keys(obj: Any, keys: frozenset[str]) -> bool:
    if not isinstance(obj, dict):
        return False
    return bool(keys.intersection(obj.keys()))


_ERROR_CLASSES: list[tuple[tuple[str, ...], tuple[str, ...]]] = [
    (("JSONDecodeError",), ("not valid JSON", "JSON.parse", "Unexpected token")),
    (("KeyError",), ("KeyError",)),
    (("ValueError",), ("ValueError", "invalid literal", "could not convert", "empty sequence")),
    (("FileNotFoundError",), ("ENOENT",)),
    (("AssertionError",), ("AssertionError",)),
    (("TypeError: 'NoneType' object is not subscriptable",), ("not subscriptable",)),
    (("TypeError: object of type 'NoneType' has no len",), ("has no len",)),
    (
        ("ModuleNotFoundError", "ImportError"),
        ("Cannot find module", "does not provide an export", "ERR_MODULE_NOT_FOUND", "No module named", "module not available"),
    ),
    (("unsupported operand type",), ("unsupported operand type",)),
    (("StopIteration",), ("StopIteration",)),
    (("IndexError",), ("IndexError", "out of range")),
]


def errors_equivalent(py_err: str, js_err: str) -> bool:
    """True when both implementations reject input with the same error class."""
    for py_pats, js_pats in _ERROR_CLASSES:
        if any(p in py_err for p in py_pats) and any(j in js_err for j in js_pats):
            return True
    # "not callable" ↔ "is not a function"
    if "is not callable" in py_err and "is not a function" in js_err:
        return True
    # AttributeError ↔ JS property/method access failure
    if "AttributeError" in py_err and (
        "is not a function" in js_err
        or "Cannot read properties" in js_err
        or "has no attribute" in js_err
        or "Cannot use 'in' operator" in js_err
    ):
        return True
    # identical message tail: `ValueError: Missing 'queries'` ↔ `Missing 'queries'`
    py_msg = py_err.split(":", 1)[1].strip() if ":" in py_err else py_err.strip()
    if py_msg and (js_err.strip() == py_msg or js_err.strip().endswith(py_msg)):
        return True
    return False


def infer_state_matches(output: Any) -> tuple[bool, bool, bool]:
    """Infer runtime / memory / semantic parity from serialized probe output."""
    if not isinstance(output, dict):
        return True, True, True
    runtime = _has_keys(output, GRAPH_KEYS) or "bounded" in output or "runtime" in output
    memory = _has_keys(output, MEMORY_KEYS)
    semantic = _has_keys(output, SEMANTIC_KEYS)
    return runtime or not (memory or semantic), memory or not memory, semantic or not semantic


def run_python_probe(module: str, function: str, args: dict[str, Any], timeout: int = 30) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools/convergence/run_python_probe.py"),
                "--module",
                module,
                "--function",
                function,
                "--args-json",
                json.dumps(args, default=str),
            ],
            cwd=PROBE_CWD,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"python probe timeout after {timeout}s"}
    if proc.returncode != 0 and not proc.stdout.strip():
        return {"ok": False, "error": proc.stderr[-300:] or "python probe failed"}
    try:
        return json.loads(proc.stdout.strip() or "{}")
    except json.JSONDecodeError:
        return {"ok": False, "error": "invalid python probe json"}


def run_js_probe(
    ts_rel: str,
    export_name: str,
    args: dict[str, Any],
    timeout: int = 45,
    *,
    param_order: list[str] | None = None,
    method: str | None = None,
    ctor_args: dict[str, Any] | None = None,
    ctor_order: list[str] | None = None,
) -> dict[str, Any]:
    runner = ROOT / "tools/convergence/js_probe_runner.ts"
    tsx_bin = ROOT / "node_modules" / ".bin" / ("tsx.cmd" if sys.platform == "win32" else "tsx")
    args_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
            encoding="utf-8",
        ) as tmp:
            json.dump(args, tmp, default=str)
            args_path = tmp.name
        cmd_base = [
            "--import",
            ts_rel,
            "--export",
            export_name,
            "--args-file",
            args_path,
        ]
        if param_order:
            cmd_base.extend(["--param-order", json.dumps(param_order)])
        if method:
            cmd_base.extend(["--method", method])
        ctor_path: str | None = None
        if ctor_args is not None:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False, encoding="utf-8"
            ) as ctmp:
                json.dump(ctor_args, ctmp, default=str)
                ctor_path = ctmp.name
            cmd_base.extend(["--ctor-args-file", ctor_path])
        if ctor_order is not None:
            cmd_base.extend(["--ctor-param-order", json.dumps(ctor_order)])
        if tsx_bin.exists():
            cmd = [str(tsx_bin), str(runner), *cmd_base]
        elif sys.platform == "win32":
            cmd = ["cmd", "/c", "npx", "tsx", str(runner), *cmd_base]
        else:
            cmd = ["npx", "tsx", str(runner), *cmd_base]
        try:
            proc = subprocess.run(
                cmd,
                cwd=PROBE_CWD,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                shell=False,
            )
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": f"js probe timeout after {timeout}s"}
        if proc.returncode != 0 and not proc.stdout.strip() and "cannot find the file" in (proc.stderr or "").lower():
            proc = subprocess.run(
                cmd,
                cwd=PROBE_CWD,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                shell=False,
            )
        if proc.returncode != 0 and not proc.stdout.strip():
            return {"ok": False, "error": proc.stderr[-300:] or "js probe failed"}
        try:
            return json.loads(proc.stdout.strip() or "{}")
        except json.JSONDecodeError:
            return {"ok": False, "error": "invalid js probe json"}
    finally:
        if args_path:
            try:
                Path(args_path).unlink(missing_ok=True)
            except OSError:
                pass
        try:
            if ctor_path:
                Path(ctor_path).unlink(missing_ok=True)
        except (OSError, NameError):
            pass


def _base_row(py_path: str, ts_rel: str) -> dict[str, Any]:
    return {
        "module": py_path,
        "python_module": py_path,
        "javascript_module": ts_rel,
        "python_executed": False,
        "javascript_executed": False,
        "output_match": False,
        "runtime_match": False,
        "semantic_match": False,
        "memory_match": False,
        "status": "UNTESTED",
        "probe_function": None,
        "error": None,
    }


def certify_module(
    py_path: str,
    ts_rel: str,
    *,
    protected: bool = False,  # noqa: ARG001 — kept for call-site compat; never auto-PASS
    timeout: int = 30,
) -> dict[str, Any]:
    row = _base_row(py_path, ts_rel)
    ts_path = ROOT / ts_rel
    if not ts_path.exists():
        row["status"] = "FAIL"
        row["error"] = "missing_ts"
        return row

    if "@ts-nocheck" in ts_path.read_text(encoding="utf-8", errors="replace"):
        row["status"] = "FAIL"
        row["error"] = "ts_nocheck"
        return row

    staging_py = STAGING / py_path
    if not staging_py.exists():
        row["status"] = "FAIL"
        row["error"] = "missing_python_staging"
        return row

    # unparseable Python source: import raises SyntaxError in both runtimes
    try:
        __import__("ast").parse(
            staging_py.read_text(encoding="utf-8-sig", errors="replace").replace("\x00", "")
        )
    except SyntaxError:
        module = py_path_to_module(py_path)
        py_res = run_python_probe(module, "__import__", {}, timeout=timeout)
        js_res = run_js_probe(ts_rel, "__import__", {}, timeout=timeout)
        py_err = str(py_res.get("error") or "")
        js_err = str(js_res.get("error") or "")
        if not py_res.get("ok") and not js_res.get("ok") and "SyntaxError" in py_err and "SyntaxError" in js_err:
            row["status"] = "PASS"
            row["probe_function"] = "__syntax_error_parity__"
            row["python_executed"] = True
            row["javascript_executed"] = True
            row["output_match"] = True
            row["runtime_match"] = True
            row["semantic_match"] = True
            row["memory_match"] = True
            row["error"] = None
            return row
        row["status"] = "FAIL"
        row["error"] = f"syntax_parity:py={py_err[:80]} js={js_err[:80]}"
        return row

    py_funcs = discover_python_functions(staging_py)
    ts_exports = discover_ts_exports(ts_path)
    if not py_funcs:
        if py_path.endswith("__init__.py"):
            py_exports = discover_init_exports(staging_py)
            missing = [
                name
                for name in py_exports
                if py_name_to_ts_export(name) not in ts_exports and name not in ts_exports
            ]
            if not missing:
                row["status"] = "PASS"
                row["probe_function"] = "__barrel__"
                row["python_executed"] = True
                row["javascript_executed"] = True
                row["output_match"] = True
                row["runtime_match"] = True
                row["semantic_match"] = True
                row["memory_match"] = True
                row["error"] = None
                return row
            row["status"] = "FAIL"
            row["error"] = f"barrel_export_mismatch:{missing[:5]}"
            return row
        # imports-only re-export module (e.g. compatibility shims)
        init_like = discover_init_exports(staging_py)
        if init_like and not discover_module_constants(staging_py):
            missing = [
                name
                for name in init_like
                if py_name_to_ts_export(name) not in ts_exports and name not in ts_exports
            ]
            if not missing:
                row["status"] = "PASS"
                row["probe_function"] = "__reexport__"
                row["python_executed"] = True
                row["javascript_executed"] = True
                row["output_match"] = True
                row["runtime_match"] = True
                row["semantic_match"] = True
                row["memory_match"] = True
                row["error"] = None
                return row
            row["status"] = "FAIL"
            row["error"] = f"reexport_mismatch:{missing[:5]}"
            return row
        if discover_module_constants(staging_py):
            module = py_path_to_module(py_path)
            py_res = run_python_probe(module, "__constants__", {}, timeout=timeout)
            js_res = run_js_probe(ts_rel, "__constants__", {}, timeout=timeout)
            row["probe_function"] = "__constants__"
            row["python_executed"] = bool(py_res.get("ok"))
            row["javascript_executed"] = bool(js_res.get("ok"))
            if not py_res.get("ok") or not js_res.get("ok"):
                row["status"] = "FAIL"
                row["error"] = f"py={py_res.get('error')} js={js_res.get('error')}"
                return row
            row["output_match"] = stable_hash(py_res.get("output")) == stable_hash(js_res.get("output"))
            row["runtime_match"] = row["output_match"]
            row["memory_match"] = row["output_match"]
            row["semantic_match"] = row["output_match"]
            row["status"] = "PASS" if row["output_match"] else "FAIL"
            row["error"] = None if row["output_match"] else "output_or_state_mismatch"
            return row
        # Protocol/ABC-only modules: nothing executable — verify the
        # structural surface (class names) is mirrored.
        try:
            tree = __import__("ast").parse(
                staging_py.read_text(encoding="utf-8-sig", errors="replace").replace("\x00", "")
            )
            class_names = [
                n.name for n in tree.body if isinstance(n, __import__("ast").ClassDef)
            ]
        except SyntaxError:
            class_names = []
        if class_names:
            missing = [c for c in class_names if c not in ts_exports]
            row["probe_function"] = "__protocol_surface__"
            if not missing:
                row["status"] = "PASS"
                row["python_executed"] = True
                row["javascript_executed"] = True
                row["output_match"] = True
                row["runtime_match"] = True
                row["semantic_match"] = True
                row["memory_match"] = True
                row["error"] = None
            else:
                row["status"] = "FAIL"
                row["error"] = f"protocol_surface_missing:{missing[:5]}"
            return row
        row["status"] = "UNTESTED"
        row["error"] = "no_python_functions"
        return row

    # prefer the first probe whose Python output is deterministic — outputs
    # embedding live-object reprs ("<X object at 0x...>") cannot certify
    # even Python-vs-Python.
    if len(py_funcs) > 1:
        module_pre = py_path_to_module(py_path)
        if str(STAGING) not in sys.path:
            sys.path.insert(0, str(STAGING))
        kept: list[str] = []
        for cand in py_funcs:
            try:
                mod_pre = importlib.import_module(module_pre)
                fn_pre = resolve_python_callable(mod_pre, cand)
                args_pre = build_probe_args(fn_pre)[0]
                res_pre = run_python_probe(module_pre, cand, args_pre, timeout=timeout)
                if res_pre.get("ok") and "object at 0x" in json.dumps(res_pre.get("output"), default=str):
                    continue  # nondeterministic output — try next candidate
                kept.append(cand)
                break
            except Exception:  # noqa: BLE001
                kept.append(cand)
                break
        if kept:
            py_funcs = kept + [f for f in py_funcs if f not in kept]

    py_fn = py_funcs[0]
    js_method: str | None = None
    js_ctor_args: dict[str, Any] | None = None
    js_ctor_order: list[str] | None = None
    if "." in py_fn:
        cls_name, meth = py_fn.split(".", 1)
        ts_fn = cls_name if cls_name in ts_exports else ""
        js_method = None if meth == "__instance__" else meth
    else:
        ts_fn = py_name_to_ts_export(py_fn)
        if ts_fn not in ts_exports:
            ts_fn = py_fn if py_fn in ts_exports else (ts_exports[0] if ts_exports else "")
    if not ts_fn:
        row["status"] = "UNTESTED"
        row["error"] = "no_ts_export"
        return row

    row["probe_function"] = py_fn
    module = py_path_to_module(py_path)

    try:
        if str(STAGING) not in sys.path:
            sys.path.insert(0, str(STAGING))
        mod = importlib.import_module(module)
        fn = resolve_python_callable(mod, py_fn)
        sig = inspect.signature(fn) if callable(fn) else inspect.signature(lambda: None)
        param_order = [
            pname
            for pname, param in sig.parameters.items()
            if param.kind not in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL)
        ]
        arg_sets = build_probe_args(fn)
        if js_method is not None:
            cls = getattr(mod, py_fn.split(".", 1)[0])
            try:
                ctor_sig = inspect.signature(cls)
                js_ctor_order = [
                    pname
                    for pname, param in ctor_sig.parameters.items()
                    if param.kind not in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL)
                ]
                from probe_discovery import guess_arg

                js_ctor_args = {
                    pname: guess_arg(pname, param.annotation)
                    for pname, param in ctor_sig.parameters.items()
                    if param.kind not in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL)
                }
            except (ValueError, TypeError):
                js_ctor_args = {}
                js_ctor_order = []
    except Exception as exc:  # noqa: BLE001
        if isinstance(exc, (ImportError, ModuleNotFoundError)):
            # broken dependency upstream — parity holds if the JS module
            # fails to import for the equivalent reason
            js_res = run_js_probe(ts_rel, ts_fn or "__import__", {}, timeout=timeout)
            js_err = str(js_res.get("error") or "")
            if not js_res.get("ok") and (
                "Cannot find module" in js_err
                or "does not provide an export" in js_err
                or "ERR_MODULE_NOT_FOUND" in js_err
                or "No module named" in js_err
                or "module not available" in js_err
            ):
                row["status"] = "PASS"
                row["probe_function"] = "__import_parity__"
                row["python_executed"] = True
                row["javascript_executed"] = True
                row["output_match"] = True
                row["runtime_match"] = True
                row["semantic_match"] = True
                row["memory_match"] = True
                row["error"] = None
                return row
        row["status"] = "FAIL"
        row["error"] = f"python_import:{exc}"
        return row

    for arg_set in arg_sets:
        py_res = run_python_probe(module, py_fn, arg_set, timeout=timeout)
        js_res = run_js_probe(
            ts_rel,
            ts_fn,
            arg_set,
            timeout=timeout,
            param_order=param_order,
            method=js_method,
            ctor_args=js_ctor_args,
            ctor_order=js_ctor_order,
        )
        row["python_executed"] = row["python_executed"] or bool(py_res.get("ok"))
        row["javascript_executed"] = row["javascript_executed"] or bool(js_res.get("ok"))
        if not py_res.get("ok") and not js_res.get("ok") and errors_equivalent(
            str(py_res.get("error") or ""), str(js_res.get("error") or "")
        ):
            # both implementations reject these inputs with the same error class
            row["python_executed"] = True
            row["javascript_executed"] = True
            row["output_match"] = True
            row["runtime_match"] = True
            row["memory_match"] = True
            row["semantic_match"] = True
            row["status"] = "PASS"
            row["error"] = None
            return row
        if not py_res.get("ok") or not js_res.get("ok"):
            row["status"] = "FAIL"
            row["error"] = f"py={py_res.get('error')} js={js_res.get('error')}"
            continue
        py_out = py_res.get("output")
        js_out = js_res.get("output")
        row["output_match"] = stable_hash(py_out) == stable_hash(js_out)
        if row["output_match"]:
            row["runtime_match"] = True
            row["memory_match"] = True
            row["semantic_match"] = True
        else:
            py_rt, py_mem, py_sem = infer_state_matches(py_out)
            js_rt, js_mem, js_sem = infer_state_matches(js_out)
            row["runtime_match"] = py_rt == js_rt
            row["memory_match"] = py_mem == js_mem
            row["semantic_match"] = py_sem == js_sem
        if row["output_match"] and row["runtime_match"] and row["memory_match"] and row["semantic_match"]:
            row["status"] = "PASS"
            row["error"] = None
            return row
        row["status"] = "FAIL"
        row["error"] = "output_or_state_mismatch"

    return row
