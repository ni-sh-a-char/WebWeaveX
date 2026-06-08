#!/usr/bin/env python3
import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "py2ts"))
from py2ts import ModuleEmitter, postprocess  # noqa: E402


def emit(body: str) -> str:
    src = "def probe():\n" + "\n".join("  " + ln for ln in body.splitlines()) + "\n  return None\n"
    fn = ast.parse(src).body[0]
    mod = ModuleEmitter("core/_probe_/probe.py", "probe.ts")
    return postprocess("\n".join(mod.emit_function(fn, 0)))


samples = [
    "x = d.get('k', {}).get('c', [])",
    "items = []\nitems.append({'a': 1})",
    "s = f'fallback_{index}'",
    "xs = [str(x) for x in items]",
    "for i, v in enumerate(items):\n    pass",
    "return {'bounded': True, 'nodes': nodes}",
    "return recover_modal_runtime(page, html)",
]

for s in samples:
    print("---", s.replace("\n", " / "))
    print(emit(s))
    print()
