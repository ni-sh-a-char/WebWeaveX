#!/usr/bin/env python3
"""Diff Python vs JavaScript probe outputs for behavioral-mismatch rows.

Usage:
  python tools/convergence/diff_mismatches.py [--matrix docs/specs/generated_module_matrix.json] [--limit N]

Writes docs/specs/behavioral_diffs.json with the first divergent path per module.
"""
from __future__ import annotations

import argparse
import importlib
import inspect
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/convergence"))
sys.path.insert(0, str(ROOT / "tools/py2ts"))

from module_certifier import run_js_probe, run_python_probe  # noqa: E402
from probe_discovery import (  # noqa: E402
    STAGING,
    build_probe_args,
    discover_python_functions,
    py_path_to_module,
    resolve_python_callable,
)
from py2ts import py_path_to_ts, snake_to_camel  # noqa: E402


def first_diff(a, b, path="$"):
    """Return (path, py_value, js_value) of first divergence, else None."""
    if isinstance(a, float) and a == int(a):
        a = int(a)
    if isinstance(b, float) and b == int(b):
        b = int(b)
    if type(a) is not type(b):
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and a == b:
            return None
        return (path, repr(a)[:120], repr(b)[:120])
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                return (f"{path}.{k}", "<missing>", repr(b[k])[:120])
            if k not in b:
                return (f"{path}.{k}", repr(a[k])[:120], "<missing>")
            d = first_diff(a[k], b[k], f"{path}.{k}")
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return (f"{path}.length", len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, f"{path}[{i}]")
            if d:
                return d
        return None
    if a != b:
        return (path, repr(a)[:120], repr(b)[:120])
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", default="docs/specs/generated_module_matrix.json")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    matrix = json.loads((ROOT / args.matrix).read_text(encoding="utf-8"))
    rows = [
        m for m in matrix["modules"]
        if m.get("status") == "FAIL" and (m.get("error") or "") == "output_or_state_mismatch"
    ]
    if args.limit:
        rows = rows[: args.limit]

    if str(STAGING) not in sys.path:
        sys.path.insert(0, str(STAGING))

    out = []
    for m in rows:
        py_path = m["python_module"]
        ts_rel = "src/" + py_path_to_ts(py_path)
        try:
            fns = discover_python_functions(STAGING / py_path)
            if not fns:
                continue
            fn_name = fns[0]
            mod = py_path_to_module(py_path)
            pymod = importlib.import_module(mod)
            fn = resolve_python_callable(pymod, fn_name)
            arg_sets = build_probe_args(fn)
            order = [
                p for p, prm in inspect.signature(fn).parameters.items()
                if prm.kind not in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL)
            ]
            ts_fn = snake_to_camel(fn_name) if "." not in fn_name else fn_name.split(".")[0]
            method = None if "." not in fn_name else fn_name.split(".", 1)[1]
            pyr = run_python_probe(mod, fn_name, arg_sets[0])
            jsr = run_js_probe(ts_rel, ts_fn, arg_sets[0], param_order=order, method=method)
            if not pyr.get("ok") or not jsr.get("ok"):
                out.append({
                    "module": py_path,
                    "probe": fn_name,
                    "kind": "probe_error",
                    "py_error": pyr.get("error"),
                    "js_error": jsr.get("error"),
                })
                continue
            d = first_diff(pyr.get("output"), jsr.get("output"))
            out.append({
                "module": py_path,
                "probe": fn_name,
                "kind": "diff" if d else "match_now",
                "path": d[0] if d else None,
                "py": d[1] if d else None,
                "js": d[2] if d else None,
            })
            print(f"{'MATCH' if not d else 'DIFF ':6} {py_path}  {d[0] + ' py=' + str(d[1]) + ' js=' + str(d[2]) if d else ''}"[:200], flush=True)
        except Exception as exc:  # noqa: BLE001
            out.append({"module": py_path, "kind": "tool_error", "error": str(exc)[:200]})

    (ROOT / "docs/specs/behavioral_diffs.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )
    kinds = {}
    for o in out:
        kinds[o["kind"]] = kinds.get(o["kind"], 0) + 1
    print("SUMMARY:", kinds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
