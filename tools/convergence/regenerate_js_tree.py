#!/usr/bin/env python3
"""Phase B — regenerate non-protected JS tree and emit FINAL_REGENERATION_REPORT.md."""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs/archive"


def count_patterns() -> dict[str, int]:
    protected = {
        ln.strip()
        for ln in (ROOT / "tools/convergence/protected_js.txt").read_text(encoding="utf-8").splitlines()
        if ln.strip()
    }
    patterns = {
        "nocheck": r"@ts-nocheck",
        "undefined_expr": r"undefined /\* expr \*/",
        "append": r"\.append\(",
        "dict_get": r"\.get\(",
        "broken_fstring": r"'[^']*'\$\{",
    }
    hits = {k: 0 for k in patterns}
    generated = 0
    for p in (ROOT / "src").rglob("*.ts"):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if rel in protected:
            continue
        generated += 1
        text = p.read_text(encoding="utf-8", errors="replace")
        for label, pat in patterns.items():
            hits[label] += len(re.findall(pat, text))
    hits["generated_modules"] = generated
    return hits


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/py2ts/py2ts.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=7200,
    )
    hits = count_patterns()
    py_count = len(
        [
            ln
            for ln in subprocess.run(
                ["git", "ls-tree", "-r", "--name-only", "origin/python", "--", "core/"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
            if ln.endswith(".py")
        ]
    )
    protected_n = len(
        [ln for ln in (ROOT / "tools/convergence/protected_js.txt").read_text().splitlines() if ln.strip()]
    )
    ok = (
        hits.get("nocheck", 0) == 0
        and hits.get("undefined_expr", 0) == 0
        and hits.get("append", 0) == 0
        and hits.get("dict_get", 0) == 0
        and hits.get("broken_fstring", 0) == 0
    )
    body = [
        "# FINAL REGENERATION REPORT",
        "",
        f"**Measured:** {ts}",
        "",
        f"**Status:** {'PASS' if ok else 'FAIL'}",
        "",
        f"| Python modules (origin/python) | {py_count} |",
        f"| Protected hand-written | {protected_n} |",
        f"| Generated TS files | {hits.get('generated_modules', 0)} |",
        f"| py2ts exit code | {proc.returncode} |",
        "",
        "## Invalid pattern scan (generated only)",
        "",
        f"| @ts-nocheck | {hits.get('nocheck', 0)} |",
        f"| undefined_expr | {hits.get('undefined_expr', 0)} |",
        f"| .append( | {hits.get('append', 0)} |",
        f"| .get( | {hits.get('dict_get', 0)} |",
        f"| broken_fstring | {hits.get('broken_fstring', 0)} |",
        "",
        "## py2ts stdout (tail)",
        "",
        "```",
        (proc.stdout or "")[-2000:],
        "```",
        "",
    ]
    if proc.stderr:
        body.extend(["## py2ts stderr (tail)", "", "```", proc.stderr[-1000:], "```", ""])
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    (ARCHIVE / "FINAL_REGENERATION_REPORT.md").write_text("\n".join(body), encoding="utf-8")
    print(f"Regeneration: ok={ok} hits={hits}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
