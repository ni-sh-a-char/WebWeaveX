#!/usr/bin/env python3
"""Phase E — engine execution matrix from live module probes."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs/archive"
MATRIX = ARCHIVE / "generated_module_matrix.json"


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    if not MATRIX.exists():
        print("Run module certification first.")
        return 1
    modules = json.loads(MATRIX.read_text(encoding="utf-8")).get("modules", [])
    engines = sorted(
        {
            (m.get("module") or m.get("python_module") or "").split("/")[1]
            for m in modules
            if (m.get("module") or m.get("python_module") or "").startswith("core/")
            and "/" in (m.get("module") or m.get("python_module") or "").removeprefix("core/")
        }
    )
    rows: list[dict] = []
    for eng in engines:
        mod_rows = [m for m in modules if f"core/{eng}/" in (m.get("module") or m.get("python_module") or "")]
        if not mod_rows:
            continue
        py_ok = all(m.get("python_executed") for m in mod_rows)
        js_ok = all(m.get("javascript_executed") for m in mod_rows)
        out_ok = all(m.get("output_match") for m in mod_rows if m.get("status") == "PASS")
        passed = all(m.get("status") == "PASS" for m in mod_rows)
        rows.append(
            {
                "engine": eng,
                "modules": len(mod_rows),
                "python_executed": py_ok,
                "javascript_executed": js_ok,
                "output_match": out_ok,
                "status": "PASS" if passed else "FAIL",
            }
        )
    executed = sum(1 for r in rows if r["status"] == "PASS")
    total = len(rows)
    pct = round(100.0 * executed / total, 2) if total else 0.0
    body = [
        "# FINAL ENGINE EXECUTION MATRIX",
        "",
        f"**Measured:** {ts}",
        "",
        f"**Status:** {'PASS' if pct >= 100 else 'FAIL'}",
        "",
        f"| Executed engines | {executed} |",
        f"| Total engines | {total} |",
        f"| Coverage | {pct}% |",
        "",
        "| Engine | Modules | Python | JavaScript | Output match | Status |",
        "|--------|---------|--------|------------|--------------|--------|",
    ]
    for r in rows[:80]:
        body.append(
            f"| {r['engine']} | {r['modules']} | {'PASS' if r['python_executed'] else 'FAIL'} | "
            f"{'PASS' if r['javascript_executed'] else 'FAIL'} | {'PASS' if r['output_match'] else 'FAIL'} | {r['status']} |"
        )
    if len(rows) > 80:
        body.append(f"| … | … | … | … | … | … |")
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    (ARCHIVE / "FINAL_ENGINE_EXECUTION_MATRIX.md").write_text("\n".join(body), encoding="utf-8")
    print(f"Engine execution: {executed}/{total} ({pct}%)")
    return 0 if pct >= 100 else 1


if __name__ == "__main__":
    raise SystemExit(main())
