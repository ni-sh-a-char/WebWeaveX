#!/usr/bin/env python3
"""
Sample generated TypeScript ports vs Python modules (honest structural verification).
Full 1724-module execution parity requires validate:differential vectors + per-module probes.
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
PROTECTED = ROOT / "tools" / "convergence" / "protected_js.txt"
sys.path.insert(0, str(ROOT / "tools" / "py2ts"))
from py2ts import py_path_to_ts  # noqa: E402


def git_lines(*args: str) -> list[str]:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()] if r.returncode == 0 else []


def main() -> None:
    ts = datetime.now(timezone.utc).isoformat()
    py_mods = [p for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/") if p.endswith(".py")]
    protected = set()
    if PROTECTED.exists():
        protected = {ln.strip() for ln in PROTECTED.read_text(encoding="utf-8").splitlines() if ln.strip()}

    ts_paths = [p for p in (ROOT / "src").rglob("*.ts") if p.is_file()]
    generated = [str(p.relative_to(ROOT)).replace("\\", "/") for p in ts_paths if str(p.relative_to(ROOT)).replace("\\", "/") not in protected]

    missing_ts: list[str] = []
    present = 0
    for py in py_mods:
        ts_rel = "src/" + py_path_to_ts(py)
        if (ROOT / ts_rel).exists():
            present += 1
        else:
            missing_ts.append(py)

    # Spot-check: @ts-nocheck density in generated files
    nocheck = 0
    for rel in generated[:200]:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        if "@ts-nocheck" in text:
            nocheck += 1

    report = {
        "measured_at": ts,
        "python_modules": len(py_mods),
        "typescript_modules": len(ts_paths),
        "generated_modules": len(generated),
        "protected_modules": len(protected),
        "topology_present": present,
        "topology_missing": len(missing_ts),
        "sample_nocheck_in_first_200_generated": nocheck,
        "execution_equivalence_proven": False,
        "execution_samples_passed": 0,
        "execution_samples_failed": 0,
        "behavioral_equivalence": "NOT PROVEN — topology only; per-module execution compare not complete",
    }

    body = "\n".join(
        [
            "# FINAL GENERATED PORT VERIFICATION",
            "",
            f"**Measured:** {ts}",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Python `core/*.py` | {report['python_modules']} |",
            f"| TypeScript `src/*.ts` | {report['typescript_modules']} |",
            f"| Generated (non-protected) | {report['generated_modules']} |",
            f"| Protected operational | {report['protected_modules']} |",
            f"| Topology files present | {report['topology_present']} |",
            f"| Topology files missing | {report['topology_missing']} |",
            f"| `@ts-nocheck` in sample (200) | {report['sample_nocheck_in_first_200_generated']} |",
            "",
            "## Verdict",
            "",
            "**Generated port behavioral equivalence: NOT PROVEN**",
            "",
            "Run `npm run validate:differential` for executable cross-language probes.",
            "",
            "```json",
            json.dumps(report, indent=2),
            "```",
            "",
        ]
    )
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    (ARCHIVE / "FINAL_GENERATED_PORT_VERIFICATION.md").write_text(body, encoding="utf-8")
    print(body)


if __name__ == "__main__":
    main()
