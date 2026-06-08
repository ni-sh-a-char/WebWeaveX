#!/usr/bin/env python3
"""Execute a single Python module function probe; stdout JSON result."""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import traceback
from pathlib import Path

STAGING = Path(__file__).resolve().parents[1] / "runtime_vectors" / ".py_staging"
if str(STAGING) not in sys.path:
    sys.path.insert(0, str(STAGING))
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Block optional third-party libs so probes exercise the spec-defined
# "dependency missing" branches — matching the JavaScript runtime's
# capability envelope. (The Python modules guard these imports.)
_BLOCKED_OPTIONAL = {
    "pytesseract", "PIL", "pypdf", "docx", "tree_sitter", "yaml",
    "comtypes", "pyatspi", "groq", "openai", "anthropic", "mistralai",
    "ollama", "google", "zipfile_unused",
}


class _OptionalBlocker:
    def find_module(self, fullname, path=None):  # noqa: ARG002
        root = fullname.split(".")[0]
        return self if root in _BLOCKED_OPTIONAL else None

    def load_module(self, fullname):
        # message matches the JS runtime's unavailable-import binding
        raise ImportError("module not available")

    # PEP 451 interface
    def find_spec(self, fullname, path=None, target=None):  # noqa: ARG002
        root = fullname.split(".")[0]
        if root in _BLOCKED_OPTIONAL:
            raise ImportError("module not available")
        return None


sys.meta_path.insert(0, _OptionalBlocker())

from probe_discovery import resolve_python_callable  # noqa: E402


def serialize(value: object, depth: int = 0) -> object:
    import inspect as _inspect

    if depth > 8:
        return str(value)
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if _inspect.isgenerator(value):
        out = []
        for i, v in enumerate(value):
            if i >= 200:
                break
            out.append(serialize(v, depth + 1))
        return out
    if isinstance(value, (list, tuple)):
        return [serialize(v, depth + 1) for v in list(value)[:200]]
    if isinstance(value, dict):
        return {str(k): serialize(v, depth + 1) for k, v in list(value.items())[:200]}
    if hasattr(value, "__dict__"):
        return serialize(vars(value), depth + 1)
    return str(value)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--module", required=True)
    p.add_argument("--function", required=True)
    p.add_argument("--args-json", default="{}")
    args = p.parse_args()
    payload: dict = {"ok": False, "error": None, "output": None}
    try:
        mod = importlib.import_module(args.module)
        if args.function == "__constants__":
            from probe_discovery import discover_module_constants, py_name_to_ts_export

            def map_name(n: str) -> str:
                body = n.lstrip("_")
                if body and body.upper() == body:
                    return n
                return py_name_to_ts_export(n)

            declared = set(discover_module_constants(Path(mod.__file__)))
            consts = {}
            for name in sorted(declared):
                if not hasattr(mod, name):
                    continue
                val = getattr(mod, name)
                if callable(val) or type(val).__name__ == "module":
                    continue
                consts[map_name(name)] = val
            print(json.dumps({"ok": True, "output": serialize(consts), "error": None}, default=str))
            return 0
        fn = resolve_python_callable(mod, args.function)
        call_args = json.loads(args.args_json)
        if isinstance(call_args, dict):
            out = fn(**call_args) if call_args else fn()
        elif isinstance(call_args, list):
            out = fn(*call_args)
        else:
            out = fn(call_args)
        payload = {"ok": True, "output": serialize(out), "error": None}
    except Exception as exc:  # noqa: BLE001
        payload = {"ok": False, "error": f"{type(exc).__name__}: {exc}", "trace": traceback.format_exc()[-500:]}
    print(json.dumps(payload, default=str))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
