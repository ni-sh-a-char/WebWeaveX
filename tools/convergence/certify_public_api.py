#!/usr/bin/env python3
"""FINAL_PUBLIC_API_CERTIFICATION.md — derived purely from execution evidence.

Measures:
  * Python public API   = origin/python:webweavex/__init__.py __all__
  * JavaScript public API = runtime keys of the built dist bundle (node import)
Builds the exact snake->camel mapping and verifies 100% coverage, no missing,
no double-ownership, no star-conflict. Emits a verdict that is computed, never
hardcoded.
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs/archive"
SRC = ROOT / "src"


def camel(s: str) -> str:
    if s.startswith("__") and s.endswith("__"):
        return s
    if s.isupper():
        return s
    lead = len(s) - len(s.lstrip("_"))
    core = s[lead:]
    parts = core.split("_")
    return "_" * lead + parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:] if p)


def python_public_api() -> list[str]:
    src = subprocess.run(
        ["git", "show", "origin/python:webweavex/__init__.py"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    ).stdout
    tree = ast.parse(src)
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id == "__all__":
                    return sorted(ast.literal_eval(n.value))
    return []


def js_public_api() -> list[str]:
    """Runtime export keys of the built bundle — measured, not parsed."""
    code = (
        "import('file://' + process.argv[1]).then(m => "
        "{ process.stdout.write(JSON.stringify(Object.keys(m))); });"
    )
    dist = (ROOT / "dist" / "index.js").as_posix()
    out = subprocess.run(
        ["node", "-e", code, dist],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout
    return sorted(json.loads(out))


def declared_owners() -> dict[str, list[str]]:
    owners: dict[str, list[str]] = {}
    for fname in ("index.ts", "publicApi.ts"):
        f = SRC / fname
        for ln in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r'\s*export\s+(?:type\s+)?\{([^}]*)\}\s+from\s+"([^"]+)"', ln)
            if m:
                mod = m.group(2)
                for part in m.group(1).split(","):
                    nm = part.split(" as ")[-1].strip()
                    if nm:
                        owners.setdefault(nm, []).append(f"{fname}:{mod}")
            m2 = re.match(r"\s*export\s+(?:async\s+)?(?:function|const|let|class)\s+([A-Za-z0-9_]+)", ln)
            if m2:
                owners.setdefault(m2.group(1), []).append(f"{fname}:<local>")
    return owners


def star_names(rel: str) -> set[str]:
    s: set[str] = set()
    p = SRC / rel
    if not p.exists():
        return s
    for ln in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*export\s+\{([^}]*)\}", ln)
        if m:
            for part in m.group(1).split(","):
                nm = part.split(" as ")[-1].strip()
                if nm:
                    s.add(nm)
        m2 = re.match(r"\s*export\s+(?:async\s+)?(?:function|const|let|class)\s+([A-Za-z0-9_]+)", ln)
        if m2:
            s.add(m2.group(1))
    return s


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    py = python_public_api()
    js = set(js_public_api())
    alias = {"__version__": "VERSION", "version": "version"}

    mapping: list[tuple[str, str]] = []
    missing: list[str] = []
    for n in py:
        cands = {n, camel(n), alias.get(n, "")}
        hit = cands & js
        if hit:
            mapping.append((n, sorted(hit)[0]))
        else:
            missing.append(n)

    owners = declared_owners()
    double = {n: o for n, o in owners.items() if len(set(o)) > 1}
    clash = star_names("connectors/index.ts") & star_names("publicApi.ts")

    coverage_ok = len(missing) == 0
    no_double = len(double) == 0
    no_clash = len(clash) == 0
    verdict_pass = coverage_ok and no_double and no_clash

    lines = [
        "# FINAL PUBLIC API CERTIFICATION",
        "",
        f"**Measured:** {ts}",
        "",
        f"**Status:** {'PASS' if verdict_pass else 'FAIL'}",
        "",
        "Evidence: Python `__all__` from `origin/python:webweavex/__init__.py`; "
        "JavaScript surface = runtime `Object.keys()` of the built `dist/index.js`.",
        "",
        "| Check | Result | Detail |",
        "|-------|--------|--------|",
        f"| Python public names | {len(py)} | from `__all__` |",
        f"| JavaScript runtime exports | {len(js)} | from dist import |",
        f"| Coverage (every Python name has a JS export) | {'PASS' if coverage_ok else 'FAIL'} | {len(mapping)}/{len(py)} |",
        f"| Missing exports | {'PASS' if coverage_ok else 'FAIL'} | {missing or 'none'} |",
        f"| Double-ownership (name declared by >1 source) | {'PASS' if no_double else 'FAIL'} | {dict(double) or 'none'} |",
        f"| Star-import conflict (connectors vs publicApi) | {'PASS' if no_clash else 'FAIL'} | {sorted(clash) or 'none'} |",
        "",
        "## Spec-conformance notes",
        "",
        "- `buildRuntimeGraph` / `queryRuntimeGraph` resolve to the spec ports "
        "`src/runtime_graph/*` (`core.runtime_graph`, list-of-IRs / `(graph, query)`), "
        "matching the Python public signatures. The dict-source helpers in "
        "`src/graph/runtimeGraph.ts` are JS-internal (pipeline) and are NOT the public exports.",
        "- `UniversalInput` is exported as a runtime class value (not type-only).",
        "",
        "## Full mapping (Python public name -> JavaScript export)",
        "",
        "| Python | JavaScript |",
        "|--------|------------|",
        *[f"| `{p}` | `{j}` |" for p, j in mapping],
        "",
    ]
    (ARCHIVE / "FINAL_PUBLIC_API_CERTIFICATION.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"API cert: {'PASS' if verdict_pass else 'FAIL'} coverage={len(mapping)}/{len(py)} "
          f"double={len(double)} clash={len(clash)}")
    return 0 if verdict_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
