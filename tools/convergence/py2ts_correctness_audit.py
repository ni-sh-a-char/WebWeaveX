#!/usr/bin/env python3
"""Phase A — audit py2ts transforms with live Python→TS→validation."""
from __future__ import annotations

import ast
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs/archive"
sys.path.insert(0, str(ROOT / "tools/py2ts"))
from py2ts import ModuleEmitter, postprocess  # noqa: E402

SAMPLES: list[tuple[str, str, str]] = [
    ("dict_get", "x = d.get('k', {}).get('c', [])", "dict .get chain"),
    ("append", "items = []\nitems.append({'a': 1})", "list .append"),
    ("fstring", "s = f'fallback_{index}'", "f-string"),
    ("comprehension", "xs = [str(x) for x in items]", "list comprehension"),
    ("enumerate", "for i, v in enumerate(items):\n    pass", "enumerate loop"),
    ("len_sorted", "n = len(items)\nxs = sorted(items)", "len and sorted"),
    ("dict_literal", "return {'bounded': True, 'nodes': nodes}", "dict return"),
    ("call_name", "return recover_modal_runtime(page, html)", "snake_case call"),
]


def validate_ts_snippet(ts: str, root: Path) -> tuple[bool, str]:
    bad_patterns = [
        (r"undefined /\* expr \*/", "unresolved expression"),
        (r"\.append\(", "python append"),
        (r"\.get\(", "python dict.get (unconverted)"),
        (r"'[^']*'\$\{", "broken f-string join"),
        (r"\blen\(", "python len()"),
        (r"\bint\(", "python int()"),
        (r"\benumerate\(", "python enumerate in for-header"),
        (r"/\* listcomp \*/", "invalid comprehension"),
        (r"/\* dictcomp \*/", "invalid dict comprehension"),
    ]
    for pat, label in bad_patterns:
        if re.search(pat, ts):
            return False, label
    return True, "ok"


def wrap_sample(body: str) -> str:
    indented = "\n".join("  " + ln if ln.strip() else ln for ln in body.splitlines())
    return f"def probe():\n{indented}\n  return None\n"


def emit_sample(body: str) -> str:
    src = wrap_sample(body)
    tree = ast.parse(src)
    fn = tree.body[0]
    assert isinstance(fn, ast.FunctionDef)
    mod = ModuleEmitter("core/_probe_/probe.py", "probe.ts")
    lines = mod.emit_function(fn, 0)
    return postprocess("\n".join(lines))


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    rows: list[dict] = []
    invalid = 0
    for name, py_snip, desc in SAMPLES:
        try:
            gen = emit_sample(py_snip)
        except Exception as exc:  # noqa: BLE001
            gen = f"/* emit error: {exc} */"
            ok, reason = False, str(exc)
        else:
            ok, reason = validate_ts_snippet(gen, ROOT)
        if not ok:
            invalid += 1
        rows.append({"name": name, "description": desc, "python": py_snip, "typescript": gen, "valid": ok, "reason": reason})

    # scan generated src for invalid patterns
    scan_hits: dict[str, int] = {}
    scan_patterns = {
        "undefined_expr": r"undefined /\* expr \*/",
        "append": r"\.append\(",
        "dict_get": r"\.get\(",
        "broken_fstring": r"'[^']*'\$\{",
        "len()": r"\blen\(",
        "int()": r"\bint\(",
    }
    protected = {
        ln.strip()
        for ln in (ROOT / "tools/convergence/protected_js.txt").read_text(encoding="utf-8").splitlines()
        if ln.strip()
    }
    for p in (ROOT / "src").rglob("*.ts"):
        if "protected_backup" in str(p):
            continue
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if rel in protected:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for label, pat in scan_patterns.items():
            hits = len(re.findall(pat, text))
            if hits:
                scan_hits[label] = scan_hits.get(label, 0) + hits

    body = [
        "# FINAL PY2TS CORRECTNESS REPORT",
        "",
        f"**Measured:** {ts}",
        "",
        f"**Status:** {'PASS' if not scan_hits and invalid == 0 else 'FAIL'}",
        "",
        f"| Sample transforms | {len(rows)} |",
        f"| Invalid samples | {invalid} |",
        "",
        "## Transform audit",
        "",
        "| Transform | Python | Valid | Reason |",
        "|-----------|--------|-------|--------|",
    ]
    for r in rows:
        py_one = r["python"].replace("\n", " ")[:80]
        body.append(f"| {r['name']} | `{py_one}` | {'PASS' if r['valid'] else 'FAIL'} | {r['reason']} |")
    body.extend(["", "## Generated tree scan (non-protected)", ""])
    if scan_hits:
        for k, v in sorted(scan_hits.items(), key=lambda x: -x[1]):
            body.append(f"- {k}: **{v}** occurrences")
    else:
        body.append("- No known invalid patterns detected in generated tree.")
    body.extend(["", "## Sample outputs", ""])
    for r in rows:
        body.extend([f"### {r['name']}", "", "```python", r["python"], "```", "", "```typescript", r["typescript"][:1200], "```", ""])
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    (ARCHIVE / "FINAL_PY2TS_CORRECTNESS_REPORT.md").write_text("\n".join(body), encoding="utf-8")
    print(f"Invalid samples: {invalid}/{len(rows)} scan_hits={scan_hits}")
    return 0 if not scan_hits and invalid == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
