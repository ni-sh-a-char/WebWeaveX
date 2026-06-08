#!/usr/bin/env python3
"""
Phase 2: Generated-port behavioral proof registry.
Marks each module PASS | FAIL | UNTESTED | PROTECTED_TESTED.
Certification blocked while any generated module is UNTESTED.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs" / "archive"
SPECS = ROOT / "docs" / "specs"
PROTECTED = ROOT / "tools/convergence/protected_js.txt"

sys.path.insert(0, str(ROOT / "tools/py2ts"))
from py2ts import py_path_to_ts  # noqa: E402


def git_lines(*args: str) -> list[str]:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()] if r.returncode == 0 else []


def export_symbols(ts_path: Path) -> list[str]:
    text = ts_path.read_text(encoding="utf-8", errors="replace")
    out: list[str] = []
    for m in re.finditer(r"^export (?:async )?function (\w+)", text, re.M):
        out.append(f"function:{m.group(1)}")
    for m in re.finditer(r"^export class (\w+)", text, re.M):
        out.append(f"class:{m.group(1)}")
    for m in re.finditer(r"^export const (\w+)", text, re.M):
        out.append(f"const:{m.group(1)}")
    return out


def load_equivalence_passed() -> set[str]:
    path = SPECS / "universal_equivalence.json"
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    passed: set[str] = set()
    for probe in data.get("probes", []):
        if probe.get("pass"):
            passed.add(probe.get("family", ""))
    return passed


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    protected: set[str] = set()
    if PROTECTED.exists():
        protected = {ln.strip() for ln in PROTECTED.read_text(encoding="utf-8").splitlines() if ln.strip()}

    py_mods = [p for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/") if p.endswith(".py")]
    equiv_families = load_equivalence_passed()

    rows: list[dict] = []
    counts = {"PASS": 0, "FAIL": 0, "UNTESTED": 0, "PROTECTED_TESTED": 0}

    for py in py_mods:
        ts_rel = "src/" + py_path_to_ts(py)
        ts_path = ROOT / ts_rel
        is_protected = ts_rel in protected
        row = {
            "python_source": py,
            "ts_target": ts_rel,
            "exists": ts_path.exists(),
            "exported_symbols": [],
            "ts_nocheck": False,
            "status": "UNTESTED",
        }
        if ts_path.exists():
            text = ts_path.read_text(encoding="utf-8", errors="replace")
            row["ts_nocheck"] = "@ts-nocheck" in text
            row["exported_symbols"] = export_symbols(ts_path)

        if is_protected:
            row["status"] = "PROTECTED_TESTED"
        elif not ts_path.exists():
            row["status"] = "FAIL"
        else:
            row["status"] = "UNTESTED"

        counts[row["status"]] = counts.get(row["status"], 0) + 1
        rows.append(row)

    untested = counts["UNTESTED"]
    nocheck = sum(1 for r in rows if r["ts_nocheck"] and r["status"] == "UNTESTED")
    proven = equiv_families  # vector families with passing harness

    body = "\n".join(
        [
            "# FINAL GENERATED PORT BEHAVIOR REPORT",
            "",
            f"**Measured:** {ts}",
            "",
            "## Summary",
            "",
            "| Status | Count |",
            "|--------|-------|",
            f"| PROTECTED_TESTED | {counts['PROTECTED_TESTED']} |",
            f"| PASS | {counts['PASS']} |",
            f"| FAIL | {counts['FAIL']} |",
            f"| UNTESTED | {counts['UNTESTED']} |",
            f"| `@ts-nocheck` (generated) | {nocheck} |",
            "",
            "## Verdict",
            "",
            "**Generated-port behavioral equivalence: NOT PROVEN**",
            "",
            f"- UNTESTED generated modules: **{untested}** (certification blocked while > 0)",
            f"- Equivalence harness families passing: {len(proven)}",
            "",
            "Protected operational modules are validated via differential vectors and hand-written parity.",
            "AST-generated modules require per-engine probe expansion — topology alone is insufficient.",
            "",
            "## Sample (first 50 UNTESTED)",
            "",
            "| Python | TypeScript | @ts-nocheck | Exports |",
            "|--------|------------|-------------|---------|",
        ]
    )
    sample = [r for r in rows if r["status"] == "UNTESTED"][:50]
    for r in sample:
        exp = ", ".join(r["exported_symbols"][:4]) or "—"
        body += f"| `{r['python_source']}` | `{r['ts_target']}` | {'yes' if r['ts_nocheck'] else 'no'} | {exp} |\n"

    body += "\n```json\n" + json.dumps(
        {
            "measured_at": ts,
            "counts": counts,
            "untested_generated": untested,
            "nocheck_generated": nocheck,
            "execution_equivalence_proven": False,
            "certification_blocked": untested > 0 or nocheck > 0,
        },
        indent=2,
    ) + "\n```\n"

    ARCHIVE.mkdir(parents=True, exist_ok=True)
    (ARCHIVE / "FINAL_GENERATED_PORT_BEHAVIOR_REPORT.md").write_text(body, encoding="utf-8")
    (SPECS / "generated_port_behavior.json").write_text(
        json.dumps({"measured_at": ts, "rows": rows, "counts": counts}, indent=2),
        encoding="utf-8",
    )
    print(body[:2000])
    return 1 if untested > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
